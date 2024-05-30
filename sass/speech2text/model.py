import logging
from typing import TYPE_CHECKING

from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    import numpy as np


class SpeechToText:
    model: WhisperModel = None

    def __init__(
        self,
        pretrained_model_path: str | None = None,
    ):
        self.model = WhisperModel(pretrained_model_path)

    def generate_transcript(
        self,
        input: "np.ndarray",
        language: str | None = None,
    ):
        return self.model.transcribe(input, language=language)
