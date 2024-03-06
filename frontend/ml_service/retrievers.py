from qdrant_client import QdrantClient
from langchain_community.vectorstores.qdrant import Qdrant
from ml_service.embeddings import Embeddings
from utils.config import QVDB_BASE_PATH


def obtain_retrievers(vdb_name, collection_name):
    """
    Obtain the retriever for the given collection name.
    :param vdb_name: The name of the vector database
    :param collection_name: The name of the collection
    :return: The retriever
    """
    emb = Embeddings()
    embeddings = emb.obtain_embeddings(collection_name)

    client = QdrantClient(path=QVDB_BASE_PATH.format(filename=vdb_name))
    qdrant = Qdrant(client, collection_name, embeddings)

    return qdrant.as_retriever()



