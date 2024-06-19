import logging

import librosa
import numpy as np
import torch
from faster_whisper import WhisperModel
from transformers import WhisperForConditionalGeneration, WhisperProcessor

logger = logging.getLogger(__name__)


class FasterSpeechToText:
    model: WhisperModel = None
    sample_rate: int = 16000

    def __init__(
        self,
        pretrained_model_path: str | None = None,
    ):
        self.model = WhisperModel(pretrained_model_path)

    @classmethod
    def resample(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        return librosa.resample(audio, orig_sr=sample_rate, target_sr=self.sample_rate)

    def generate_transcript(
        self,
        audio: str | np.ndarray,
        sample_rate: int | None = None,
        language: str | None = "en",
    ):
        if isinstance(audio, np.ndarray) and sample_rate != self.sample_rate:
            audio = self.resample(audio, sample_rate)
            if audio.shape[0] > 1:
                audio = audio[0]
                return self.model.transcribe(np.float32(audio), language=language)
        return self.model.transcribe(audio, language=language)


class SpeechToText:
    processor: WhisperProcessor = None
    model: WhisperForConditionalGeneration = None
    sample_rate: int = 16000

    def __init__(
        self,
        pretrained_model_path: str | None = None,
    ):
        self.processor = WhisperProcessor.from_pretrained(pretrained_model_path)
        self.model = WhisperForConditionalGeneration.from_pretrained(
            pretrained_model_path
        )
        self.model.config.forced_decoder_ids = None

    def featurize_audio(
        self,
        sample: np.array,
        sampling_rate: int | float,
    ) -> np.array:
        return self.processor(
            sample,
            sampling_rate=sampling_rate,
        ).input_features

    def featurize_audio_batch(
        self,
        samples: np.ndarray,
        sampling_rate: int | float,
    ) -> torch.Tensor:
        return torch.from_numpy(
            np.concatenate(
                [self.featurize_audio(sample, sampling_rate) for sample in samples],
                axis=0,
            )
        )

    def generate_transcript(
        self,
        input_features: torch.Tensor,
    ):
        predicted_ids = self.model.generate(input_features)
        return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)
