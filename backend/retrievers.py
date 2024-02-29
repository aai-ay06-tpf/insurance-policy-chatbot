import os, re

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.retrievers import BM25Retriever

from utils.config import DOWNLOAD_PATH
from eda_tools.pdf_dir_tools import extract_text

# Obtain the list of PDF files in the DOWNLOAD_PATH
pdf_files = [os.path.join(DOWNLOAD_PATH, file) for file in os.listdir(DOWNLOAD_PATH) if file.endswith('.pdf')]


# Extract the text from the PDF files
pdf_dict = extract_text(pdf_files)


# Instance of the RecursiveCharacterTextSplitter class
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=75
)


# Split the text into chunks and obtain retrieval
# embeddings = HuggingFaceBgeEmbeddings(
#     model_name="BAAI/bge-small-en-v1.5",
#     model_kwargs={"device": "cpu"}
# )
    
for file in pdf_dict.keys():
    texts = text_splitter.split_text(pdf_dict[file]['text'])
    metadatas = [{"source": f"{i}-lt"} for i in range(len(texts))]
    bm25_retriever = BM25Retriever.from_texts(texts, metadatas=metadatas)
    bm25_retriever.k = 5
    pdf_dict[file]['chunks'] = texts
    pdf_dict[file]['metadatas'] = metadatas
    pdf_dict[file]['retriever'] = bm25_retriever#TODO: debería serializarlo en pickle y guardar el path
    
    


import pickle
with open("pdf_dict.pkl", "wb") as f:
    pickle.dump(pdf_dict, f, pickle.HIGHEST_PROTOCOL)

# bm25_retriever = BM25Retriever.from_texts(texts)
# bm25_retriever.k = 5