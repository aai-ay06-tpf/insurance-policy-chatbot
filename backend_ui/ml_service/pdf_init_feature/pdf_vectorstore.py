from qdrant_client import QdrantClient
from langchain_community.vectorstores.qdrant import Qdrant

from ml_service.tools.embeddings import Embeddings
from utils.config import QDRANT_HOST, QDRANT_PORT


def obtain_vectorstore_from_client(
    embedding_name: str = "openai_embeddings",
    collection_name: str = "init_pdf_feature_1710520826_openai_embeddings"
) -> Qdrant:

    emb = Embeddings()
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    embeddings = emb.obtain_embeddings(embedding_name)
    qdrant = Qdrant(client, collection_name, embeddings)

    return qdrant
