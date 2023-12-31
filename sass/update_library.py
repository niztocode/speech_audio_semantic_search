import logging
import os

from sass.config import get_app_config
from sass.db.weaviate_db import w_client
from sass.load.weaviate import load_audio_data
from sass.speech2text.transcript import audio_transcript

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)

logger = logging.getLogger(__name__)

SOUND_FILE_EXTENSIONS = ["mp3", "wav"]

if __name__ == "__main__":
    library_dir = get_app_config().library_path

    logger.info("Loading audio files on path: '%s'", library_dir)
    for f in os.listdir(library_dir):
        f_path = os.path.join(library_dir, f)
        if not os.path.isfile(f_path):
            continue

        if f.split(".")[-1] not in SOUND_FILE_EXTENSIONS:
            continue

        r = w_client.query.get("AudioClip", ["title"]).do()
        if f in [c["title"] for c in r["data"]["Get"]["AudioClip"]]:
            logger.warning(
                "'AudioClip' with name %s already exists in db. Skipping...",
                f,
            )
            continue

        logger.info("Getting transcripts for file: '%s'", f)
        trans = audio_transcript(f_path, frame_seconds=20)
        logger.info("Loading data to db")
        load_audio_data(trans, f)
