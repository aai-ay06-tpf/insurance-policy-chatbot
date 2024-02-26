import os


# Get the current file path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Configure the download path
DOWNLOAD_PATH = os.path.join(BASE_PATH, 'queplan_insurance')
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Configure the AWS credentials
ACCESS_KEY = 'AKIA2JHUK4EGBAMYAYFY'
SECRET_KEY = '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'
DATASET_PATH = 's3://anyoneai-datasets/queplan_insurance/'
BUCKET_NAME = "anyoneai-datasets"
prefix = "queplan_insurance/"



