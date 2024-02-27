import os
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, "database_s3", "queplan_insurance")
DB_PATH = os.path.join(PROJECT_ROOT, "database_chromadb", "db")


def create_vector_db():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents = texts,
        embedding=GPT4AllEmbeddings(),
        persist_directory=DB_PATH
    )
    vectorstore.persist()


if __name__ == "__main__":
    create_vector_db()