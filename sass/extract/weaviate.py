import logging
from typing import Any, Dict, List, Union

from sass.db.weaviate_db import w_client

logger = logging.getLogger(__name__)


def get_similar_frames(text: str, limit: int) -> List[Dict[str, Any]]:
    return (
        w_client.query.get("AudioFrame", ["transcript", "start", "end"])
        .with_near_text({"concepts": [text]})
        .with_limit(limit)
        .with_additional(["id", "certainty", "distance"])
        .do()
    )["data"]["Get"]["AudioFrame"]


def get_frame_clip(frame_id: str) -> Dict[str, Union[str, float]]:
    where_filter = {
        "path": [
            "hasAudioFrame",
            "AudioFrame",
            "id",
        ],
        "operator": "Equal",
        "valueString": frame_id,
    }
    return (
        w_client.query.get(
            "AudioClip",
            [
                "title",
                "sample_ratio",
                "frame_overlap",
            ],
        )
        .with_where(where_filter)
        .do()
    )["data"]["Get"]["AudioClip"][0]
