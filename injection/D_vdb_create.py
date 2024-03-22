import os
import time
import pickle

from langchain_community.vectorstores.qdrant import Qdrant

from ml_service.tools.embeddings import Embeddings
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
    # TODO: verificar que el contenedor con el servicio de Qdrant esté activo (ping)
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
    feature_files_path = os.path.join(FEATURES_PATH, "feature_files.pkl")
    feature_articles_path = os.path.join(FEATURES_PATH, "feature_articles.pkl")

    with open(feature_files_path, "rb") as file:
        feature_files = pickle.load(file)

    with open(feature_articles_path, "rb") as file:
        feature_articles = pickle.load(file)

    feature_files_path = os.path.join(FEATURES_PATH, "grouped_feature_files.pkl")
    feature_articles_path = os.path.join(FEATURES_PATH, "grouped_feature_articles.pkl")

    with open(feature_files_path, "rb") as file:
        grouped_feature_files = pickle.load(file)

    with open(feature_articles_path, "rb") as file:
        grouped_feature_articles = pickle.load(file)


    final_feature_file = feature_files + grouped_feature_files
    final_feature_article = feature_articles + grouped_feature_articles
    final_feature_article = [element for lista in final_feature_article for element in lista]
    

    # CREATE VECTOR DATABASE - POLICY FEATURE
    create_vector_db(
        chunks=final_feature_file,
        embedding_label=embedding_label,
        collection_prefix="pdf_pol_feature",
    )

    time.sleep(0.05)

    # CREATE VECTOR DATABASE - ARTICLE FEATURE
    create_vector_db(
        chunks=final_feature_article,
        embedding_label=embedding_label,
        collection_prefix="pdf_art_feature",
    )

    end = time.time()

    print(f"total time taken: {round(end-start, 1)} seconds")
