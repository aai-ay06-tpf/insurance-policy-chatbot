from qdrant_client import QdrantClient
from langchain_community.vectorstores.qdrant import Qdrant
from langchain.retrievers.merger_retriever import MergerRetriever
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from langchain_community.document_transformers.embeddings_redundant_filter import EmbeddingsRedundantFilter
from langchain.retrievers.document_compressors.base import DocumentCompressorPipeline
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_transformers.long_context_reorder import LongContextReorder


from backend.ml_service.tools.embeddings import Embeddings
from utils.config import QDRANT_LOCAL_PATH, QDRANT_URL


def obtain_embeddings(collection_name):
    """
    Obtain the embeddings for the given collection name.
    :param collection_name: The name of the collection
    :return: The embeddings
    """
    emb = Embeddings()
    embeddings = emb.get_embeddings()
    
    for name in embeddings:
        if collection_name.endswith(name):
            return name
    raise ValueError(f"Embeddings for collection {collection_name} not found.")

def obtain_feature_file_retrievers(collection_names: list) -> list:
    global qdrants_files
    """
    Obtain the retriever for the given collection name.
    :param vdb_name: The name of the vector database
    :param collection_name: The name of the collection
    :return: The retriever
    """
    
    emb_name = obtain_embeddings(collection_names[0])
    emb = Embeddings()
    embeddings = emb.obtain_embeddings(emb_name)

    client = QdrantClient(url=QDRANT_URL)
    qdrants_files = []
    for collection_name in collection_names:
        qdrants_files.append(Qdrant(client, collection_name, embeddings))
    
    return [qdrant.as_retriever(search_type="mmr") for qdrant in qdrants_files]


def obtain_feature_article_retrievers(collection_names: list) -> list:
    global qdrants_articles
    """
    Obtain the retriever for the given collection name.
    :param vdb_name: The name of the vector database
    :param collection_name: The name of the collection
    :return: The retriever
    """
    emb_name = obtain_embeddings(collection_names[0])
    
    emb = Embeddings()
    embeddings = emb.obtain_embeddings(emb_name)

    client = QdrantClient(url=QDRANT_URL)
    qdrants_files = []
    for collection_name in collection_names:
        qdrants_files.append(Qdrant(client, collection_name, embeddings))
    
    return [qdrant.as_retriever(search_type="mmr") for qdrant in qdrants_files]


def files_lotr_retriever(collection_names: list) -> ContextualCompressionRetriever:
    """
    Feature engineering instance for merging retrievers and compressing documents.
    :param collection_names: The names of the collections to be merged
    :return: The retriever for files feature
    """
    
    retrievers = obtain_feature_file_retrievers(collection_names)

    # Create a MergerRetriever
    lotr = MergerRetriever(retrievers=retrievers)

    # Create embedding model for redundant compressor
    emb_name = obtain_embeddings(collection_names[0])
    emb = Embeddings()
    embeddings = emb.obtain_embeddings(emb_name)

    # Create the redundant compressor filter
    filter = EmbeddingsRedundantFilter(embeddings=embeddings)

    # Create a context reorder transformer
    reorder = LongContextReorder()

    # Create a Document compressor pipeline 
    pipeline = DocumentCompressorPipeline(transformers=[filter, reorder])

    # Create a Contextual Compressor Retriever
    compression_reorder_retriever = ContextualCompressionRetriever(
        base_compressor=pipeline,
        base_retriever=lotr
    )

    return compression_reorder_retriever

def articles_lotr_retriever(collection_names: list) -> ContextualCompressionRetriever:
    """
    Feature engineering instance for merging retrievers and compressing documents.
    :param collection_names: The names of the collections to be merged
    :return: The retriever for articles feature
    """
    retrievers = obtain_feature_article_retrievers(collection_names)

    # Create a MergerRetriever
    lotr = MergerRetriever(retrievers=retrievers)

    # Create embedding model for redundant compressor
    emb_name = obtain_embeddings(collection_names[0])
    emb = Embeddings()
    embeddings = emb.obtain_embeddings(emb_name)

    # Create the redundant compressor filter
    filter = EmbeddingsRedundantFilter(embeddings=embeddings)

    # Create a context reorder transformer
    reorder = LongContextReorder()

    # Create a Document compressor pipeline 
    pipeline = DocumentCompressorPipeline(transformers=[filter, reorder])

    # Create a Contextual Compressor Retriever
    compression_reorder_retriever = ContextualCompressionRetriever(
        base_compressor=pipeline,
        base_retriever=lotr
    )

    return compression_reorder_retriever