import os

SERVICE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = os.path.basename(SERVICE_PATH)
SERVICE_2_NAME = "backend"
SERVICE_2_PATH = os.path.join(os.path.dirname(SERVICE_PATH), SERVICE_2_NAME)
RETRIEVER_PATH = os.path.join(SERVICE_2_PATH, "main_retriever.pkl")
