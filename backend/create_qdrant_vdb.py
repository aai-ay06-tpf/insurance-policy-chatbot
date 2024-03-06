import os
from langchain_community.vectorstores.qdrant import Qdrant
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# https://python.langchain.com/docs/integrations/vectorstores/qdrant#on-disk-storage

from ml_service.embeddings import Embeddings
from utils.config import DOWNLOAD_PATH, QVDB_BASE_PATH

import time

start = time.time()




def create_vector_db():
    loader = PyPDFDirectoryLoader(DOWNLOAD_PATH)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    texts = text_splitter.split_documents(documents)
    metadatas = [{"source": f"{i}-lt"} for i in range(len(texts))]
    
    
    emb = Embeddings()
    embeddings = emb.obtain_embeddings("sbert_embeddings")
    
    # Create the local vector database
    Qdrant.from_documents(
        documents = texts,
        embedding=embeddings,
        path=QVDB_BASE_PATH.format(filename="all_files"),
        collection_name=emb.get_current()
    )
    


if __name__ == "__main__":
    create_vector_db()
    end = time.time()
    
    print(f"total time taken: {round(end-start, 1)} seconds")
    
    
    