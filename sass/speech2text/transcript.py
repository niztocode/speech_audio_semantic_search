import logging
from typing import TYPE_CHECKING, Any

import librosa as la

from sass.speech2text.model import FasterSpeechToText, SpeechToText
from sass.speech2text.utils import batch_data

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    import numpy as np


def faster_audio_transcript(
    audio: str | list["np.ndarray"],
) -> dict[str, int | str]:
    asr_model = FasterSpeechToText("small")

    transcript_generator, _ = asr_model.generate_transcript(audio)
    segments = [
        {"start": seg.start, "end": seg.end, "transcript": seg.text}
        for seg in transcript_generator
    ]
    return segments


def audio_transcript(
    waveform: str,
    asr_model: SpeechToText,
    frames_batch_size: int = 10,
    frame_seconds: float = 30,
    overlap: float = 0,
) -> dict[str, Any]:
    # Calculate the frame size and frame overlap
    frame_size = int(asr_model.sample_rate * frame_seconds)
    if overlap == 0:
        hop_length = frame_size
    elif overlap < 1:
        hop_length = int(frame_size * (1 - overlap))
    else:
        raise Exception("Overlap must be float ranging in (0, 1)")

    # Break the audio into frames
    if len(waveform) < frame_size:
        logger.info(
            "Waveform is shorter than frame size. Breaking into one frame of %s samples",
            len(waveform),
        )
        audio_frame = la.util.frame(
            waveform,
            frame_length=len(waveform),
            hop_length=len(waveform),
        ).transpose()
        batches = [audio_frame]
    else:
        logger.info(
            "Breaking into frames of %s length & %s samples",
            frame_seconds,
            frame_size,
        )
        audio_frames = la.util.frame(
            waveform, frame_length=frame_size, hop_length=hop_length
        ).transpose()

        logger.info("Batching frames in batches of %s length", frames_batch_size)
        batches = batch_data(audio_frames, frames_batch_size)

    transcript_windows = []
    logger.info("Generating transcripts...")
    for batch in batches:
        transcript_windows.extend(
            asr_model.generate_transcript(
                asr_model.featurize_audio_batch(batch, asr_model.sample_rate)
            )
        )

    return " ".join(transcript_windows)
