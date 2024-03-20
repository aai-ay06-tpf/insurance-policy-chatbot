import os
from configparser import ConfigParser


def read_config(parser: ConfigParser, location: str) -> None:
    assert parser.read(location), f"Could not read config {location}"


env_config = ConfigParser()
CONFIG_FILE = os.path.join(os.getcwd(), ".env")
read_config(env_config, CONFIG_FILE)

# Main directory paths
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = os.path.basename(SERVICE_PATH)

# AWS S3 Configuration
ACCESS_KEY = env_config.get("aws-s3", "ACCESS_KEY")
SECRET_KEY = env_config.get("aws-s3", "SECRET_KEY")
DATASET_PATH = env_config.get("aws-s3", "DATASET_PATH")
BUCKET_NAME = env_config.get("aws-s3", "BUCKET_NAME")
prefix = env_config.get("aws-s3", "prefix")

# AWS S3 PDF download path
DOWNLOAD_PATH = os.path.join(SERVICE_PATH, "database_s3", "queplan_insurance")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Pickle serialized features path
FEATURES_PATH = os.path.join(SERVICE_PATH, ".serialized_features")
os.makedirs(FEATURES_PATH, exist_ok=True)

QDRANT_HOST = env_config.get("qdrant", "QDRANT_HOST")
QDRANT_PORT = env_config.get("qdrant", "QDRANT_PORT")

# Qdrant Vector Database Path
QDRANT_URL = env_config.get("qdrant", "QDRANT_URL")
QDRANT_LOCAL_PATH = os.path.join(ROOT_PATH, "qdrant_collections")
