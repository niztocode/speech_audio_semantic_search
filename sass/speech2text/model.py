import logging
from typing import List, Optional, Union

import numpy as np
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

logger = logging.getLogger(__name__)


class SpeechToText:
    processor: WhisperProcessor = None
    model: WhisperForConditionalGeneration = None

    def __init__(
        self,
        pretrained_model_path: Optional[str] = None,
    ):
        self.processor = WhisperProcessor.from_pretrained(
            pretrained_model_path
        )
        self.model = WhisperForConditionalGeneration.from_pretrained(
            pretrained_model_path
        )
        self.model.config.forced_decoder_ids = None

    def featurize_audio(
        self,
        sample: np.array,
        sampling_rate: Union[int, float],
    ) -> np.array:
        return self.processor(
            sample,
            sampling_rate=sampling_rate,
        ).input_features

    def featurize_audio_batch(
        self,
        samples: np.ndarray,
        sampling_rate: Union[int, float],
    ) -> torch.Tensor:
        return torch.from_numpy(
            np.concatenate(
                [
                    self.featurize_audio(sample, sampling_rate)
                    for sample in samples
                ],
                axis=0,
            )
        )

    def generate_transcript(
        self,
        input_features: torch.Tensor,
    ):
        predicted_ids = self.model.generate(input_features)
        return self.processor.batch_decode(
            predicted_ids, skip_special_tokens=True
        )
