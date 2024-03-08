import os
from configparser import ConfigParser


def read_config(parser: ConfigParser, location: str) -> None:
    assert parser.read(location), f"Could not read config {location}"


env_config = ConfigParser()
CONFIG_FILE = os.path.join(os.getcwd(), '.env')
read_config(env_config, CONFIG_FILE)

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = os.path.basename(SERVICE_PATH)

QDRANT_URL = env_config.get('qdrant', 'QDRANT_URL')



