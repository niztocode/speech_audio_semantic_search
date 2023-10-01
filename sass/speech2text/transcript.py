import logging
import os
from typing import Any, Dict

import librosa as la

from sass.speech2text.config import get_config
from sass.speech2text.model import SpeechToText
from sass.speech2text.utils import batch_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)
logger = logging.getLogger(__name__)


def audio_transcript(
    audio_file_path: str,
    frames_batch_size: int = 10,
    frame_seconds: float = 30,
    overlap: float = 0,
) -> Dict[str, Any]:
    asr_model = SpeechToText(get_config().whisper_path)
    audio, sr = la.load(audio_file_path)

    sr_resampled = 16000
    audio_resampled = la.resample(audio, orig_sr=sr, target_sr=sr_resampled)

    # Calculate the frame size and frame overlap
    frame_size = int(sr_resampled * frame_seconds)
    if overlap == 0:
        hop_length = frame_size
    elif overlap < 1:
        hop_length = int(frame_size * (1 - overlap))
    else:
        raise Exception("Overlap must be float ranging in (0, 1)")

    # Break the audio into frames
    logger.info(
        "Breaking into frames of %s length & %s samples",
        frame_seconds,
        frame_size,
    )
    audio_frames = la.util.frame(
        audio_resampled, frame_length=frame_size, hop_length=hop_length
    ).transpose()

    logger.info("Batching frames in batches of %s length", frames_batch_size)
    batches = batch_data(audio_frames, frames_batch_size)

    transcript_windows = []
    audio_windows = []
    start_end = []
    logger.info("Generating transcripts...")
    for i, batch in enumerate(batches):
        for j in range(batch.shape[0]):
            frame_start = (
                (i * frames_batch_size + j)
                * frame_size
                * (1 - overlap)
                / sr_resampled
            )
            frame_end = frame_start + frame_size / sr_resampled
            start_end.append((frame_start, frame_end))
        audio_windows.extend([frame for frame in batch])
        transcript_windows.extend(
            asr_model.generate_transcript(
                asr_model.featurize_audio_batch(batch, sr_resampled)
            )
        )

    return {
        "meta": {
            "frame_size": frame_size,
            "sr": sr_resampled,
            "overlap": overlap,
        },
        "start_end": start_end,
        "audio_frames": audio_windows,
        "frame_transcripts": transcript_windows,
    }


if __name__ == "__main__":
    audio_file_path = "sound_clips/john_oliver_ai_sample.mp3"
    filename = audio_file_path.split("/")[-1].split(".")[0]
    transcript_outpath = f"transcripts/{filename}_transcript.txt"

    transcript_data = audio_transcript(
        audio_file_path, frame_seconds=20, overlap=0
    )

    transcripts = transcript_data["transcript"]
    start_end = transcript_data["start_end"]

    out_dir = "/".join(transcript_outpath.split("/")[:-1])
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(transcript_outpath, "w") as fout:
        for se, trans in zip(start_end, transcripts):
            fout.write(f">> {se[0]}s - {se[1]}s:")
            fout.write("\n" + trans.strip())
            fout.write("\n------------------------------------\n")
