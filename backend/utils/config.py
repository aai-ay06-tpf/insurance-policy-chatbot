import os
from configparser import ConfigParser


def read_config(parser: ConfigParser, location: str) -> None:
    assert parser.read(location), f"Could not read config {location}"


def get_config(parser: ConfigParser, section: str, key: str) -> str:
    return parser.get(section, key)

env_config = ConfigParser()
CONFIG_FILE = os.path.join(os.getcwd(), '.env')
read_config(env_config, CONFIG_FILE)

# Main directory paths
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVICE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = os.path.basename(SERVICE_PATH)

# AWS S3 Configuration
ACCESS_KEY = get_config(env_config, 'aws-s3', 'ACCESS_KEY')
SECRET_KEY = get_config(env_config, 'aws-s3', 'SECRET_KEY')
DATASET_PATH = get_config(env_config, 'aws-s3', 'DATASET_PATH')
BUCKET_NAME = get_config(env_config, 'aws-s3', 'BUCKET_NAME')
prefix = get_config(env_config, 'aws-s3', 'prefix')

# AWS S3 PDF download path
DOWNLOAD_PATH = os.path.join(SERVICE_PATH, 'database_s3', 'queplan_insurance')
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Qdrant Vector Database Path 
QVDB_BASE_PATH = os.path.join(ROOT_PATH, "vdb_qdrant", "{filename}")
os.makedirs(os.path.split(QVDB_BASE_PATH)[0], exist_ok=True)

