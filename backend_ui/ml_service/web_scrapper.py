
from concurrent.futures import ThreadPoolExecutor

from ml_service.webscrapper_codigos_chile import web_documents, web_vectorstore
from ml_service.webscrapper_codigos_chile.web_parent_document_retriever import obtain_parentdocument_retriever

from ml_service.tools.retrievers_validation import validate_input


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
    if 'all_docs' in globals().keys():
        return True
    return False


def qdrant_retriever(searchs, search_type="similarity", kwargs=None):
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

    vectorstore = web_vectorstore.obtain_vectorstore_from_docs(all_docs)

    if kwargs:
        kwargs = validate_input(kwargs)
        return vectorstore.as_retriever(search_type=search_type, search_kwargs=kwargs)

    return vectorstore.as_retriever(search_type=search_type)


"""
Examples:

# Retrieve more documents with higher diversity
# Useful if your dataset has many similar documents
docsearch.as_retriever(
    search_type="mmr",
    search_kwargs={'k': 6, 'lambda_mult': 0.25}
)

# Fetch more documents for the MMR algorithm to consider
# But only return the top 5
docsearch.as_retriever(
    search_type="mmr",
    search_kwargs={'k': 5, 'fetch_k': 50}
)

# Only retrieve documents that have a relevance score
# Above a certain threshold
docsearch.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'score_threshold': 0.8}
)

# Only get the single most similar document from the dataset
docsearch.as_retriever(search_kwargs={'k': 1})

# Use a filter to only retrieve documents from a specific paper
docsearch.as_retriever(
    search_kwargs={'filter': {'paper_title':'GPT-4 Technical Report'}}
)

Ref:
* https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.qdrant.Qdrant.html#langchain_community.vectorstores.qdrant.Qdrant.as_retriever
"""


def parent_document_retriever(searchs):
    print("DOESN'T WORK: TypeError: Can't instantiate abstract class TextSplitter with abstract method split_text")
    if not obtain_docs_executed():
        all_docs = obtain_docs(searchs)

    return obtain_parentdocument_retriever(all_docs)
