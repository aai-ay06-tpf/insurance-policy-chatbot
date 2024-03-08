import os
from typing import Callable

from langchain_core.documents.base import Document
from langchain_community.vectorstores.qdrant import Qdrant
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# https://python.langchain.com/docs/integrations/vectorstores/qdrant#on-disk-storage

from ml_service.embeddings import Embeddings
from eda_tools.doc_fragmentation import extract_documents_from_text
from eda_tools.pdf_file_tools import (
    extract_patterns, extract_text,
    remove_pattern_from_lines
)
from utils.config import DOWNLOAD_PATH
from utils.config import QDRANT_URL

import time

start = time.time()



def create_file_batch(files:list, func: Callable, *args: tuple) -> list:
    """
    Create a file batch by inspecting the output of a given function with many differnte arguments.
    The function will be asking the user if the output is correct, and if not, the user can remove the file from the batch.

    Parameters:
    - files (list): A list of the files to be inspected.
    - funcs (function): The function to be used to inspect each of the files.
    - *args: The arguments to be used for the function.

    Returns:
    List: A list of the files that were selected by the user.
    
    """

    batch_files = [(None, None)]
    
    for arg in args:
        print(f"\n{arg}\n")
        for file in files:
            selected_file = os.path.join(DOWNLOAD_PATH, file)
            # Once the file was added there is no need to check with other arguments
            if selected_file in (batch[0] for batch in batch_files):
                continue
            # Function Execution
            print(func(selected_file, arg))
            # UI Context
            filename = selected_file.split("\\")[-1].replace(".pdf", "")
            print(f"File: {filename}")
            ui = input("Want to add this file to the batch? (y/n): ")
            print()
            # Output Management
            if not ui.isalpha():
                raise ValueError("Invalid input")
            if ui.lower() == "y":
                batch_files.append((selected_file, arg))
    
    return batch_files[1:]



def create_doc_batch(batch_files: list) -> list:
    """
    Create list of langchain Documents in which each document is a representation of all the articles in the policy.
    
    Parameters:
    - batch_files (list): A list of tuples containing the file path and the pattern to be used to extract the articles.
    
    Returns:
    List: A list of langchain Documents.
    """
    
    filenames = [filename.split("\\")[-1].replace(".pdf", "") for filename, _ in batch_files]
    
    extractions = [extract_patterns(file, pattern) for file, pattern in batch_files]
    
    # articles = [" ".join(element) for element in extractions]
    # Esperar que este lista la función remove pattern from lines
    articles = [" ".join(element) for element in [remove_pattern_from_lines(extraction, pattern) for extraction, (_, pattern) in zip(extractions, batch_files)]]
    policy_headers = [extract_text(file).split("\n")[0] for file, _ in batch_files]
    
    features = [f"{header} {article}" for article, header in zip(articles, policy_headers)]
    
    documents = []
    for i, feature in enumerate(features):
        documents.append(Document(page_content=feature, metadata={
            "file": filenames[i], "policy_header": policy_headers[i]
            }
        ))
    
    return documents
    

def create_article_batch(selected_file: str, patterns: list) -> list:
    pass


def create_documents():
    pass


def create_chunks(collection_label: str, embedding_label: str) -> None:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    chunks = text_splitter.split_documents(documents)
    metadatas = [{"source": f"{i}-lt"} for i in range(len(chunks))]


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
    
    pdf_files = os.listdir(DOWNLOAD_PATH)
    patterns = ["^ART.CULO\s\d+.:?", "^Art.culo\s(N|Nº|N°)?\s\d+[°º]?[.:]+"]
    
    file_batch = create_file_batch(pdf_files, extract_patterns, *patterns)
    
    # First Feature: Extracting the articles and header from the policies
    feature_files = create_doc_batch(file_batch)
    
    # First Staging: obtaining the documents of each article for each policy
    articles = [(selected_file, extract_patterns(selected_file, pattern)) for selected_file, pattern in file_batch]
    documents_by_file = [extract_documents_from_text(selected_file, article) for selected_file, article in articles]
    
    create_vector_db(
        chunks=feature_files,
        embedding_label="sbert_embeddings",
        collection_label="all_files"
    )
    
    end = time.time()

    print(f"total time taken: {round(end-start, 1)} seconds")