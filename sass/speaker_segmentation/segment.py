import logging
from pathlib import Path

import torchaudio
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook

from sass.config import get_app_config

logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyannote.core.annotation import Annotation
    from torch import Tensor


def load_pipeline() -> Pipeline:
    return Pipeline.from_pretrained(
        Path(get_app_config().diarization_pipeline_path),
    )


def process(waveform: "Tensor", sample_rate: int) -> list["Annotation"]:
    pipeline = load_pipeline()
    with ProgressHook() as hook:
        diarization = pipeline(
            {"waveform": waveform, "sample_rate": sample_rate}, hook=hook
        )
    return diarization


if __name__ == "__main__":
    import sys

    logging.basicConfig(
        level=logging.INFO,
        handlers=[logging.StreamHandler(sys.stdout)],
        format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
    )

    audio_path = "./audio/The Expert Progress Meeting (Short Comedy Sketch).mp3"

    waveform, sr = torchaudio.load(audio_path)
    diarization = process(waveform, sr)

    with open("audio.rttm", "w") as f:
        diarization.write_rttm(f)
