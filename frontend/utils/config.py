import os

SERVICE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = os.path.basename(SERVICE_PATH)
SERVICE_1_NAME = "backend"
SERVICE_1_PATH = os.path.join(os.path.dirname(SERVICE_PATH), SERVICE_1_NAME)
RETRIEVERS_PATH = os.path.join(SERVICE_1_PATH, "pdf_dict.pkl")
