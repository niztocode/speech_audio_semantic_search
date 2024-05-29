import logging

from weaviate.util import generate_uuid5

from sass.db.weaviate_db import w_client

logger = logging.getLogger(__name__)


def load_audio_data(
    data: dict[str, str | int],
):
    audioclip_collection = w_client.collections.get("AudioClip")
    with w_client.collections.get("AudioClip").batch.dynamic() as batch:
        # load audio clip
        titles_db = [
            item.properties.get("title") for item in audioclip_collection.iterator()
        ]
        if data["audioclip"]["title"] in titles_db:
            logger.warning(
                "'AudioClip' with name %s already exists in db. Skipping...",
                data["audioclip"]["title"],
            )
            return
        uuid_clip = generate_uuid5(data["audioclip"], "AudioClip")
        batch.add_object(
            uuid=uuid_clip,
            properties=data["audioclip"],
        )

    segments_collection = w_client.collections.get("Segment")
    with segments_collection.batch.dynamic() as batch:
        for seg in data["segments"]:
            uuid_seg = generate_uuid5(seg, "Segment")
            batch.add_object(
                uuid=uuid_seg,
                properties=seg,
            )

            batch.add_reference(
                from_uuid=uuid_seg,
                from_property="belongsToAudioClip",
                to=uuid_clip,
            )
    return
