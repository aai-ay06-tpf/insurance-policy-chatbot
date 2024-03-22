from concurrent.futures import ThreadPoolExecutor
from copy import copy

from ml_service.webscrapper_codigos_chile import web_documents, web_vectorstore
from ml_service.webscrapper_codigos_chile.web_parent_document_retriever import (
    obtain_parentdocument_retriever,
)

from ml_service.tools.retrievers_validation import validate_search_kwargs


# For running the function in parallel
def run_func(args):
    return web_documents.obtain_scrapped_documents(*args)


# For creating a global variable with all the documents
def obtain_docs(searchs):
    global all_docs
    with ThreadPoolExecutor() as executor:
        docs = list(executor.map(run_func, searchs))

    all_docs = [doc for sublist in docs for doc in sublist]
    return all_docs


# For executing 'obtain_docs' only once
def obtain_docs_executed():
    # check the global variables and see if 'all_docs' exists:
    if "all_docs" in globals().keys():
        return True
    return False


def qdrant_retriever(searchs, search_type="similarity", kwargs=None):
    global all_docs
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

    if not obtain_docs_executed():
        all_docs = obtain_docs(searchs)
    else:
        all_docs = copy(all_docs)

    vectorstore = web_vectorstore.obtain_vectorstore_from_docs(all_docs)

    if kwargs:
        kwargs = validate_search_kwargs(kwargs)
        return vectorstore.as_retriever(search_type=search_type, search_kwargs=kwargs)

    return vectorstore.as_retriever(search_type=search_type)


def parent_document_retriever(searchs):
    global all_docs

    if not obtain_docs_executed():
        all_docs = obtain_docs(searchs)
    else:
        all_docs = copy(all_docs)

    return obtain_parentdocument_retriever(all_docs)
