import os
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from langchain_community.vectorstores.qdrant import Qdrant
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.chat_models.openai import ChatOpenAI

from ml_service.tools.embeddings import Embeddings
from utils.config import QDRANT_HOST, QDRANT_PORT

load_dotenv()


def obtain_vectorstore_from_client(
    embedding_name: str = "openai_embeddings",
    collection_name: str = "init_pdf_feature_1710520826_openai_embeddings"
) -> Qdrant:

    emb = Embeddings()
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    embeddings = emb.obtain_embeddings(embedding_name)
    qdrant = Qdrant(client, collection_name, embeddings)

    return qdrant


def obtain_multiquery_retriever_init():

    # load it into Qdrant
    db = obtain_vectorstore_from_client()

    # set the LLM for multiquery
    llm = ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

    # Multiquery retrieval using OpenAI
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=db.as_retriever(), llm=llm)

    return retriever_from_llm
