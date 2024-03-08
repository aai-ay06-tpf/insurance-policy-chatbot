import os, time, pickle

from langchain_community.vectorstores.qdrant import Qdrant

from ml_service.embeddings import Embeddings
from utils.config import QDRANT_URL, FEATURES_PATH


start = time.time()


def create_vector_db(
    chunks: list, embedding_label: str, collection_label: str
    ) -> None:
    """
    Create a containerized vector database using the given chunks, embedding label, and collection label.

    Parameters:
    - chunks (list): A list of documents to be indexed in the vector database.
    - embedding_label (str): The label of the embedding to be used for indexing.
    - collection_label (str): The label of the collection to be created in the vector database.

    Returns:
    None
    """
    
    # TODO: unit test: verificar que los chunks sean documentos de langchain
    # TODO: unit test: verificar que los chunks tengan longitudes similares
    
    emb = Embeddings()
    embedding = emb.obtain_embeddings(embedding_label)

    # Create the containerized vector database
    Qdrant.from_documents(
        documents=chunks,
        embedding=embedding,
        url=QDRANT_URL,
        prefer_grpc=True,
        collection_name=f"{collection_label}_{emb.get_current()}"
    )


if __name__ == "__main__":

    embedding_label = "sbert_embeddings"
    
    feature_name = "feature_files"
    
    feature_path = os.path.join(FEATURES_PATH, f"{feature_name}.pkl")
    
    with open(feature_path, "rb") as file:
        feature_files = pickle.load(file)
    
    create_vector_db(
        chunks=feature_files,
        embedding_label=embedding_label,
        collection_label=feature_name
    )
    
    end = time.time()

    print(f"total time taken: {round(end-start, 1)} seconds")