import logging

from sass.speech2text.model import SpeechToText

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)
logger = logging.getLogger(__name__)


def audio_transcript(
    audio_file_path: str,
) -> dict[str, int | str]:
    asr_model = SpeechToText("small")

    logger.info(f"Generating transcript for {audio_file_path}...")
    transcript_generator, _ = asr_model.generate_transcript(audio_file_path)
    segments = [
        {"start": seg.start, "end": seg.end, "transcript": seg.text}
        for seg in transcript_generator
    ]
    return segments
