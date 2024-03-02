import os, re
import time
start = time.time()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceBgeEmbeddings
from langchain_community.retrievers.bm25 import BM25Retriever
from langchain.retrievers.merger_retriever import MergerRetriever
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from langchain_community.document_transformers.embeddings_redundant_filter import EmbeddingsRedundantFilter
from langchain.retrievers.document_compressors.base import DocumentCompressorPipeline
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_transformers.long_context_reorder import LongContextReorder
from utils.config import DOWNLOAD_PATH
from eda_tools.pdf_dir_tools import extract_text
dependencies_end = time.time()


CHUNK_SIZE = 600
CHUNK_OVERLAP = 75
K = 2



# Obtain the list of PDF files in the DOWNLOAD_PATH
pdf_files = [os.path.join(DOWNLOAD_PATH, file) for file in os.listdir(DOWNLOAD_PATH) if file.endswith('.pdf')]


# Extract the text from the PDF files
pdf_dict = extract_text(pdf_files)


# Instance of the RecursiveCharacterTextSplitter class
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)


# Split the text into chunks and obtain bm25 retrievers
for file in pdf_dict.keys():
    texts = text_splitter.split_text(pdf_dict[file]['text'])
    metadatas = [{"source": f"{i}-lt"} for i in range(len(texts))]
    # https://python.langchain.com/docs/integrations/retrievers/bm25
    # https://api.python.langchain.com/en/latest/retrievers/langchain_community.retrievers.bm25.BM25Retriever.html#langchain_community.retrievers.bm25.BM25Retriever
    # https://api.python.langchain.com/en/latest/_modules/langchain_community/retrievers/bm25.html#BM25Retriever
    # https://api.python.langchain.com/en/latest/_modules/langchain_community/retrievers/bm25.html#BM25Retriever.from_texts
    bm25_retriever = BM25Retriever.from_texts(
        texts=texts,
        metadatas=metadatas
    )
    bm25_retriever.k = K
    pdf_dict[file]['chunks'] = texts
    pdf_dict[file]['metadatas'] = metadatas
    pdf_dict[file]['retriever'] = bm25_retriever#TODO: debería serializarlo en pickle y guardar el path
    

retrievers_end = time.time()


# import pickle
# with open("pdf_dict.pkl", "wb") as f:
#     pickle.dump(pdf_dict, f, pickle.HIGHEST_PROTOCOL)

# MergerRetriever
# https://api.python.langchain.com/en/latest/retrievers/langchain.retrievers.merger_retriever.MergerRetriever.html#langchain-retrievers-merger-retriever-mergerretriever

# EmbeddingsRedundantFilter
# https://api.python.langchain.com/en/latest/document_transformers/langchain_community.document_transformers.embeddings_redundant_filter.EmbeddingsRedundantFilter.html#langchain-community-document-transformers-embeddings-redundant-filter-embeddingsredundantfilter

# DocumentCompressorPipeline
# https://api.python.langchain.com/en/latest/retrievers/langchain.retrievers.document_compressors.base.DocumentCompressorPipeline.html#langchain-retrievers-document-compressors-base-documentcompressorpipeline

# ContextualCompressionRetriever
# https://api.python.langchain.com/en/latest/retrievers/langchain.retrievers.contextual_compression.ContextualCompressionRetriever.html#langchain-retrievers-contextual-compression-contextualcompressionretriever

# LongContextReorder
# https://api.python.langchain.com/en/latest/document_transformers/langchain_community.document_transformers.long_context_reorder.LongContextReorder.html#langchain-community-document-transformers-long-context-reorder-longcontextreorder



### part-II

# Create a basic query
query = "Articulos que mencionen siniestros"

# Isolate all the BM25 retrievers
retriever_list = [pdf_dict[key]["retriever"] for key in pdf_dict.keys()]

# Create a MergerRetriever
lotr = MergerRetriever(retrievers=retriever_list)

# Create embedding model for redundant compressor
embedding = GPT4AllEmbeddings()

# Create the redundant compressor filter
filter = EmbeddingsRedundantFilter(embeddings=embedding)

# Create a context reorder transformer
reorder = LongContextReorder()

# Create a Document compressor pipeline 
pipeline = DocumentCompressorPipeline(transformers=[filter, reorder])

# Create a Contextual Compressor Retriever
compression_reorder_retriever = ContextualCompressionRetriever(
    base_compressor=pipeline,
    base_retriever=lotr
)

import pickle
with open("main_retriever.pkl", "wb") as f:
    pickle.dump(compression_reorder_retriever, f, pickle.HIGHEST_PROTOCOL)

main_retriever_end = time.time()

total_time = main_retriever_end - start
dependencies_time = dependencies_end - start
retrievers_time = retrievers_end - dependencies_end
main_retriever_time = main_retriever_end - retrievers_end

# Print the results rounded
print(f"Total time: {round(total_time, 2)} seconds")
print(f"Dependencies time: {round(dependencies_time, 2)} seconds")
print(f"Retrievers time: {round(retrievers_time, 2)} seconds")
print(f"Main retriever time: {round(main_retriever_time, 2)} seconds")


"""
Total time: 6.42 seconds
Dependencies time: 4.6 seconds   
Retrievers time: 0.59 seconds    
Main retriever time: 1.22 seconds
""";