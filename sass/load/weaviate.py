import logging
from typing import Dict, List, Union

import numpy as np
from weaviate.util import generate_uuid5

from sass.db.weaviate_db import w_client

logger = logging.getLogger(__name__)


def load_audio_data(
    data: Dict[str, Union[str, List[str], List["np.array"], int, float]],
    filename: str,
    batch_size: int = 5,
):
    audio_clip_obj = {
        "title": filename,
        "sample_ratio": data["meta"]["sr"],
        "frame_overlap": data["meta"]["overlap"],
    }

    w_client.batch.configure(batch_size=batch_size)

    with w_client.batch as batch:
        # load audio clip
        r = w_client.query.get("AudioClip", ["title"]).do()
        if filename in [c["title"] for c in r["data"]["Get"]["AudioClip"]]:
            logger.warning(
                "'AudioClip' with name %s already exists in db. Skipping...",
                filename,
            )
            return
        uuid_clip = generate_uuid5(audio_clip_obj, "AudioClip")
        batch.add_data_object(
            data_object=audio_clip_obj,
            class_name="AudioClip",
            uuid=uuid_clip,
        )
        for ft, se in zip(data["frame_transcripts"], data["start_end"]):
            audio_frame_obj = {
                # "audio": json.dumps({"data": af}, cls=NumpyArrayEncoder),
                "transcript": ft,
                "start": se[0],
                "end": se[1],
            }
            uuid_frame = generate_uuid5(audio_frame_obj, "AudioFrame")
            batch.add_data_object(
                data_object=audio_frame_obj,
                class_name="AudioFrame",
                uuid=uuid_frame,
            )
            batch.add_reference(
                from_object_uuid=uuid_clip,
                from_object_class_name="AudioClip",
                from_property_name="hasAudioFrame",
                to_object_uuid=uuid_frame,
                to_object_class_name="AudioFrame",
            )
    return
