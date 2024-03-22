# https://python.langchain.com/docs/modules/data_connection/retrievers/parent_document_retriever
from langchain_community.vectorstores.chroma import Chroma
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters.character import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_text_splitters.base import TextSplitter

from ml_service.tools.embeddings import Embeddings
from utils.config import QDRANT_URL


def obtain_parentdocument_retriever(docs):

    # It should create documents smaller than the parent
    child_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=20
    )

    parrent_splitter = []

    emb = Embeddings()
    embeddings = emb.obtain_embeddings("openai_embeddings")

    # The vectorstore to use to index the child chunks
    vectorstore = Chroma(collection_name="all_documents", embedding_function=embeddings)

    # The storage layer for the parent documents
    store = InMemoryStore()

    pd_retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
    )

    pd_retriever.add_documents(docs, ids=None)

    return pd_retriever
