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



APIKEY_1 = "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"
APIKEY_2 = "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"
APIKEY_3 = "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"
APIKEY_4 = "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"

APIKEY_J = "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"

