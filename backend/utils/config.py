import os

SERVICE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = os.path.basename(SERVICE_PATH)
SERVICE_2_NAME = "frontend"
SERVICE_2_PATH = os.path.join(os.path.dirname(SERVICE_PATH), SERVICE_2_NAME)

# Configure the PDF download path
DOWNLOAD_PATH = os.path.join(SERVICE_PATH, 'database_s3', 'queplan_insurance')
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Configure the AWS credentials
ACCESS_KEY = 'AKIA2JHUK4EGBAMYAYFY'
SECRET_KEY = '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'
DATASET_PATH = 's3://anyoneai-datasets/queplan_insurance/'
BUCKET_NAME = "anyoneai-datasets"
prefix = "queplan_insurance/"


# Qdrant Vector Database Base Path 
QVDB_BASE_PATH = os.path.join(SERVICE_PATH, "vdb_qdrant", "{filename}")
os.makedirs(os.path.split(QVDB_BASE_PATH)[0], exist_ok=True)

