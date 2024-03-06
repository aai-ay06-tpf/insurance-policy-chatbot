import os

SERVICE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = os.path.basename(SERVICE_PATH)
SERVICE_1_NAME = "backend"
SERVICE_1_PATH = os.path.join(os.path.dirname(SERVICE_PATH), SERVICE_1_NAME)
VDB_PATH = os.path.join(SERVICE_1_PATH, "vdb_qdrant")
QVDB_BASE_PATH = os.path.join(SERVICE_PATH, VDB_PATH, "{filename}")


