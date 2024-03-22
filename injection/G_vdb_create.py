import os
import time
import pickle


from langchain_community.vectorstores.qdrant import Qdrant

from ml_service.tools.embeddings import Embeddings
from utils.config import FEATURES_PATH, QDRANT_URL


start = time.time()


def create_vector_db(
    chunks: list, embedding_label: str, collection_prefix: str
) -> None:
    """
    Create a containerized vector database using the given chunks, embedding label, and collection label.

    Parameters:
    - chunks (list): A list of documents to be indexed in the vector database.
    - embedding_label (str): The label of the embedding to be used for indexing.
    - collection_prefix (str): The prefix of the collection name to be created in the vector database.

    Returns:
    None
    """
    # TODO: verificar que el servicio esté up and running
    # TODO: unit test: verificar que los chunks sean documentos de langchain
    # TODO: unit test: verificar que los chunks tengan longitudes similares

    emb = Embeddings()
    embedding = emb.obtain_embeddings(embedding_label)

    # Create the containerized vector database
    try:
        Qdrant.from_documents(
            documents=chunks,
            embedding=embedding,
            url=QDRANT_URL,
            prefer_grpc=True,
            collection_name=f"{collection_prefix}_{emb.get_current()}",
        )
    except Exception as e:
        print(e)
        print()
        print(f"Error creating vector database for {collection_prefix}")
        return None


def main():

    # DEFINE DE EMBEDDING MODEL
    embedding_label = "openai_embeddings"

    # LOAD ALL THE FEATURES
    final_features_path = os.path.join(FEATURES_PATH, "final_features.pkl")

    with open(final_features_path, "rb") as file:
        final_features = pickle.load(file)

    # CREATE VECTOR DATABASE - FEATURE FILES
    create_vector_db(
        chunks=final_features,
        embedding_label=embedding_label,
        collection_prefix="pdf_final_feature",
    )

    end = time.time()

    print(f"total time taken: {round(end-start, 1)} seconds")
