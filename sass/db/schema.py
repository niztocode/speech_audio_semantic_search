import argparse
import logging

from weaviate.classes.config import (
    Configure,
    DataType,
    Property,
    ReferenceProperty,
    VectorDistances,
)

from sass.db.weaviate_db import w_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)
logger = logging.getLogger(__name__)


def delete_schema():
    logger.info("deleting class %s and objects...", "AudioFrame")
    w_client.collections.delete("AudioFrame")
    logger.info("deleting class %s and objects...", "Segment")
    w_client.collections.delete("Segment")


def create_schema():
    logger.info("Creating class %s...", "Segment")
    w_client.collections.create(
        "Segment",
        description="An audio segment is a part of audio clip containing speech transcripted information.",
        vectorizer_config=Configure.Vectorizer.text2vec_transformers(
            vectorize_collection_name=False
        ),
        properties=[
            Property(
                name="transcript",
                data_type=DataType.TEXT,
                description="String containing segments's transcript.",
            ),
            Property(
                name="start",
                data_type=DataType.NUMBER,
                description="Start timestamp of segment.",
            ),
            Property(
                name="end",
                data_type=DataType.NUMBER,
                description="End timestamp of segment.",
            ),
        ],
        vector_index_config=Configure.VectorIndex.hnsw(
            distance_metric=VectorDistances.COSINE
        ),
    )
    logger.info("Creating class %s...", "AudioClip")
    w_client.collections.create(
        "AudioClip",
        description="The audio clip's information and meta data.",
        vectorizer_config=Configure.Vectorizer.text2vec_transformers(
            vectorize_collection_name=False
        ),
        properties=[
            Property(
                name="title",
                data_type=DataType.TEXT,
                description="Title of audio clip file.",
            ),
        ],
        references=[
            ReferenceProperty(
                name="hasSegment",
                target_collection="Segment",
                description="An audio clip is composed by a number of segments that contain transcripted speech.",
            )
        ],
        vector_index_config=Configure.VectorIndex.hnsw(
            distance_metric=VectorDistances.COSINE
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create/delete db schema.")
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="delete schema from db and recreate",
    )

    args = parser.parse_args()
    if args.delete:
        logger.info("Deleting current schema from db")
        delete_schema()

    logger.info("Creating schema")
    create_schema()
