import logging
from typing import TYPE_CHECKING

from weaviate.classes.query import MetadataQuery
from weaviate.collections.classes.grpc import QueryReference

from sass.db.weaviate_db import w_client

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from weaviate.collections.classes.internal import QueryReturn


def get_similar_segments(text: str, limit: int) -> "QueryReturn":
    collection = w_client.collections.get(
        "Segment",
    )
    res = collection.query.near_text(
        query=text,
        limit=limit,
        return_metadata=MetadataQuery(
            distance=True,
            certainty=True,
        ),
        return_references=QueryReference(
            link_on="belongsToAudioClip", return_properties=["title"]
        ),
    )
    return res
