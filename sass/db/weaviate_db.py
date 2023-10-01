import logging

import weaviate

from sass.db.config import get_weaviate_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(module)s | %(message)s",
)
logger = logging.getLogger(__name__)
config = get_weaviate_config()

w_client = weaviate.Client(url=config.db_url)
logger.info("Created client to Weaviate DB @ %s", config.db_url)
