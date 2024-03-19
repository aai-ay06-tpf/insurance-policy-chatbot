import os
from configparser import ConfigParser


def read_config(parser: ConfigParser, location: str) -> None:
    assert parser.read(location), f"Could not read config {location}"


env_config = ConfigParser()
CONFIG_FILE = os.path.join(os.getcwd(), ".env")
read_config(env_config, CONFIG_FILE)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = os.path.basename(SERVICE_PATH)


QDRANT_HOST = env_config.get("qdrant", "QDRANT_HOST")
QDRANT_PORT = env_config.get("qdrant", "QDRANT_PORT")

QDRANT_URL = env_config.get("qdrant", "QDRANT_URL")
QDRANT_LOCAL_PATH = os.path.join(ROOT_PATH, "qdrant_collections")

