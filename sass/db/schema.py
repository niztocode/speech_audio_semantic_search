import argparse
import logging

from sass.db.weaviate_db import w_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)
logger = logging.getLogger(__name__)

audioclip_class_obj = {
    "class": "AudioClip",
    "description": "The audio clip's information and meta data.",
    "vectorizer": "text2vec-transformers",
    "moduleConfig": {"text2vec-transformers": {"vectorizeClassName": "false"}},
    "properties": [
        {
            "name": "title",
            "dataType": ["text"],
            "description": "Title of audio clip file.",
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": "false",
                    "vectorizePropertyName": "true",
                }
            },
        },
        {
            "name": "sample_ratio",
            "dataType": ["int"],
            "description": "Sample ratio of audio clip. Number of samples per second.",
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": "true",
                    "vectorizePropertyName": "false",
                }
            },
        },
        {
            "name": "frame_overlap",
            "dataType": ["int"],
            "description": "Percentage of overlap between audio frames.",
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": "true",
                    "vectorizePropertyName": "false",
                }
            },
        },
        {
            "name": "hasAudioFrame",
            "dataType": ["AudioFrame"],
            "description": "An audio clip is composed by a number of audio frames.",
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": "true",
                    "vectorizePropertyName": "false",
                }
            },
        },
    ],
    "vectorIndexType": "hnsw",
    "vectorIndexConfig": {
        "distance": "cosine",
    },
}

audioframe_class_obj = {
    "class": "AudioFrame",
    "description": "An audio frame is a part of audio clip containing audio and transcript information.",
    "vectorizer": "text2vec-transformers",
    "moduleConfig": {"text2vec-transformers": {"vectorizeClassName": "false"}},
    "properties": [
        # {
        #    "name": "audio",
        #    "description": "String containing frame's audio data in a 'json' form.",
        #    "dataType": ["text"],
        #    "moduleConfig": {
        #        "text2vec-transformers": {
        #            "skip": "true",
        #            "vectorizePropertyName": "false",
        #        }
        #    },
        # },
        {
            "name": "transcript",
            "description": "String containing frame's transcript.",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": "true",
                    "vectorizePropertyName": "false",
                }
            },
        },
        {
            "name": "start",
            "description": "Start timestamp of frame.",
            "dataType": ["number"],
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": "true",
                    "vectorizePropertyName": "false",
                }
            },
        },
        {
            "name": "end",
            "description": "End timestamp of frame.",
            "dataType": ["number"],
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": "true",
                    "vectorizePropertyName": "false",
                }
            },
        },
    ],
}

schema = {"classes": [audioframe_class_obj, audioclip_class_obj]}


def delete_schema():
    db_classes = w_client.schema.get().get("classes", [])
    for cls in db_classes:
        logger.info("deleting %s class...", cls["class"])
        w_client.schema.delete_class(cls["class"])
    return


def validate_db_schema():
    db_classes = w_client.schema.get().get("classes", [])
    db_classnames = [c["class"] for c in db_classes]

    return bool(
        sum(
            [
                True if cls["class"] not in db_classnames else False
                for cls in schema["classes"]
            ]
        )
    )


def create_schema():
    w_client.schema.create(schema)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create/delete db schema and valitate"
    )
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

    if not validate_db_schema():
        logger.info("Schema validated")
    else:
        logger.warning("Invalid db schema")
