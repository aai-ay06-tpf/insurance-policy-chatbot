# https://python.langchain.com/docs/modules/data_connection/retrievers/MultiQueryRetriever
import os
import logging
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores.qdrant import Qdrant
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.chat_models.openai import ChatOpenAI

from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter


from ml_service.tools.embeddings import Embeddings
from ml_service.tools.retrievers_validation import validate_search_kwargs
from utils.config import QDRANT_HOST, QDRANT_PORT

load_dotenv()


def obtain_vectorstore_from_client(
    collection_name: str,
    embedding_name: str = "openai_embeddings",
) -> Qdrant:

    emb = Embeddings()
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    embeddings = emb.obtain_embeddings(embedding_name)
    qdrant = Qdrant(client, collection_name, embeddings)

    return qdrant


def qdrant_retriever(
    collection_name: str,
    embedding_name: str,
    search_type: str = "mmr",
    search_kwargs: dict = {"k": 3, "lambda_mult": 0.25},
):
    """
    Params:
        - search_type: Can be "similarity" (default), "mmr", or "similarity_score_threshold".
        - kwargs: A dictionary with the parameters for the search_kwargs:
                - k: The number of documents to retrieve (default=4).
                - score_threshold: The minimum relevance threshold for a document to be retrieved.
                - fetch_k: The number of documents to pass to the MMR algorithm (default=20).
                - lambda_mult: The lambda multiplier for the MMR algorithm (default=0.5). 1 for minimun diversity, 0 for maximun diversity.
                - filter: A dictionary with the fields and values to filter the documents metadata.
    """

    vectorstore = obtain_vectorstore_from_client(collection_name, embedding_name)

    if search_kwargs:
        search_kwargs = validate_search_kwargs(search_kwargs)
        return vectorstore.as_retriever(
            search_type=search_type, search_kwargs=search_kwargs
        )

    return vectorstore.as_retriever(search_type=search_type)


def obtain_llm_multiquery_retriever(
    collection_name: str,
    embedding_name: str,
    search_type: str = "mmr",
    search_kwargs: dict = {"k": 3, "lambda_mult": 0.25},
) -> MultiQueryRetriever:

    # load it into Qdrant
    db = obtain_vectorstore_from_client(
        embedding_name=embedding_name, collection_name=collection_name
    )

    # set the LLM for multiquery
    llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Multiquery retrieval using OpenAI
    search_kwargs = validate_search_kwargs(search_kwargs)

    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=db.as_retriever(search_type=search_type, search_kwargs=search_kwargs),
        llm=llm,
    )

    # Set logging for the queries
    logging.basicConfig()
    logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

    return retriever_from_llm


