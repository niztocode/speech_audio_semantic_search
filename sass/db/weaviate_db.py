import logging

import weaviate

from sass.db.config import get_weaviate_config

logger = logging.getLogger(__name__)
config = get_weaviate_config()

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
        {
            "name": "audio",
            "description": "String containing frame's audio data in a 'json' form.",
            "dataType": ["text"],
            "moduleConfig": {
                "text2vec-transformers": {
                    "skip": "true",
                    "vectorizePropertyName": "false",
                }
            },
        },
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

schema = {"classes": [audioclip_class_obj, audioframe_class_obj]}

w_client = weaviate.Client(url=config.db_url)
logger.info("Created client to Weaviate DB @ %s", config.db_url)
db_classes = w_client.schema.get().get("classes", [])
db_classnames = [c["class"] for c in db_classes]
for cls in schema["classes"]:
    if cls["class"] not in db_classnames:
        logger.info("creating %s class...", cls["class"])
        w_client.schema.create_class(cls)
    else:
        logger.info("class %s already exists in db schema", cls["class"])
        # print("exiting..")
        # client.schema.delete_class("class_obj['name]") <-- To delete all data of this class
        # return
