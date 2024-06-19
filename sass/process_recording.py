import argparse
import logging
import os
import shutil
import sys
from math import ceil, floor
from typing import TYPE_CHECKING

import librosa as la
import playsound as ps
import torchaudio

from sass.load.weaviate import load_audio_data
from sass.speaker_segmentation import segment
from sass.speech2text.config import get_config
from sass.speech2text.model import SpeechToText
from sass.speech2text.transcript import audio_transcript

if TYPE_CHECKING:
    import numpy as np
    import torch as t
    from pyannote.core.annotation import Annotation

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)

logger = logging.getLogger(__name__)

SOUND_FILE_EXTENSIONS = ["mp3", "wav"]


def enter_recording_name() -> str:
    entered_name = True
    while entered_name:
        recording_name = input("\nEnter the name of the recording: ")
        if recording_name.strip() == "":
            print("Recording name cannot be empty!")
            continue
        entered_name = False

    return recording_name.strip()


def interactive_speaker_labelling(
    speaker_segs: dict[str, "Annotation"], waveform: "t.Tensor", sr: int
) -> dict[str, str]:
    temp_dir = "_temp"
    os.makedirs(temp_dir, exist_ok=True)
    for speaker, seg in speaker_segs.items():
        torchaudio.save(
            os.path.join(temp_dir, f"{speaker}.wav"),
            waveform[:, floor(seg.start) * sr : ceil(seg.end) * sr],
            sr,
        )

    print("\n\n======== Interactive Speaker Labelling initiated ========\n\n")
    print("Instructions:")
    print("A sample of the audio will be played for each speaker.")
    print("You will be asked to provide a name for each speaker.")
    start = True
    while start:
        start = input("\nPress Enter to start...")
        if start.strip() != "":
            continue
        start = False

    speaker_names = {}
    for speaker, seg in speaker_segs.items():
        print(f"\nSpeaker: {speaker}")
        print("Enter 'r' to replay the audio if you wish to listen again.")
        entered_name = True
        while entered_name:
            ps.playsound(os.path.join(temp_dir, f"{speaker}.wav"))
            speaker_name = input("Enter the name of the speaker: ")
            if speaker_name == "r":
                continue
            entered_name = False

        speaker_names[speaker] = speaker_name.strip()

    shutil.rmtree(temp_dir)

    return speaker_names


def get_segments_transcripts(
    speaker_segments: dict[str, "Annotation"], waveform: "np.ndarray", sr: int
) -> dict[str, dict["Annotation", list[dict[str, int | str]]]]:
    asr_model = SpeechToText(get_config().whisper_path)

    logger.info(
        "Resampling the audio to the model's sample rate: %sHz -> %sHz",
        sr,
        asr_model.sample_rate,
    )
    sr_resampled = asr_model.sample_rate
    waveform_resampled = la.resample(waveform, orig_sr=sr, target_sr=sr_resampled)

    transcripts = {speaker: {} for speaker in speaker_segments}

    for speaker, segments in speaker_segments.items():
        for segment in segments:
            speaker_waveform = waveform_resampled[
                :,
                floor(segment.start) * sr_resampled : ceil(segment.end) * sr_resampled,
            ]

            logger.debug("Transcribing segment: %s", segment)
            transcripts[speaker][segment] = audio_transcript(
                speaker_waveform[0, :], asr_model
            )

    return transcripts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a recording file path.")
    parser.add_argument(
        "--recording", type=str, help="Path to a file with extension mp3 or wav"
    )

    args = parser.parse_args()
    recording_filepath = args.recording

    # Check if the file exists
    if not os.path.exists(recording_filepath):
        logger.exception("Error: The file '%s' does not exist.", recording_filepath)
        sys.exit(1)

    if recording_filepath.split(".")[-1] not in SOUND_FILE_EXTENSIONS:
        logger.exception("Error: The input file must be either '.mp3' or '.wav'!")
        sys.exit(1)

    logger.debug("Processing recording file: '%s'", recording_filepath)
    waveform, sr = torchaudio.load(recording_filepath)

    logger.debug(
        "Loaded recording with sample_rate=%d & length=%ss", sr, waveform.shape[1] / sr
    )

    logger.debug("Segmenting the recording...")
    diarization = segment.process(waveform, sr)

    labels_segs = {}
    for label in diarization.labels():
        labels_segs[label] = [
            seg
            for seg, track_label in diarization._tracks.items()
            if list(track_label.values())[0] == label and seg.duration >= 1
        ]

    speakers_names = interactive_speaker_labelling(
        {label: labels_segs[label][0] for label in labels_segs}, waveform, sr
    )

    recording_name = enter_recording_name()

    logger.debug("Generating transcripts for the recording...")

    transcripts = get_segments_transcripts(
        labels_segs,
        waveform.numpy(),
        sr,
    )

    data = {
        "audioclip": {"title": recording_name},
        "segments": [
            {
                "transcript": transripction,
                "start": seg.start,
                "end": seg.end,
                "speaker": speakers_names[speakerid],
            }
            for speakerid, segments in transcripts.items()
            for seg, transripction in segments.items()
        ],
    }

    load_audio_data(data)
