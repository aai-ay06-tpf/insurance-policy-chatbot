import os, time, pickle

from langchain_community.vectorstores.qdrant import Qdrant

from ml_service.embeddings import Embeddings
from utils.config import QDRANT_URL, FEATURES_PATH


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
        collection_name=f"{collection_prefix}_{emb.get_current()}"
    )


if __name__ == "__main__":

    # DEFINE DE EMBEDDING MODEL
    embedding_label = "sbert_embeddings"
    
    # LOAD THE FEATURES
    feature_files_path = os.path.join(FEATURES_PATH, "feature_files.pkl")
    feature_articles_path = os.path.join(FEATURES_PATH, "feature_articles.pkl")
    
    with open(feature_files_path, "rb") as file:
        feature_files = pickle.load(file)
    
    with open(feature_articles_path, "rb") as file:
        feature_articles = pickle.load(file)
        
    # CREATE VECTOR DATABASE - FEATURE FILES
    create_vector_db(
        chunks=feature_files,
        embedding_label=embedding_label,
        collection_prefix="all_files"
    )
    
    # CREATE VECTOR DATABASE - FEATURE ARTICLES
    for feature in feature_articles:
        file = feature[0].metadata["file"]
        create_vector_db(
            chunks=feature,
            embedding_label=embedding_label,
            collection_prefix=file
        )
        time.sleep(0.2)
    
    
    
    end = time.time()

    print(f"total time taken: {round(end-start, 1)} seconds")