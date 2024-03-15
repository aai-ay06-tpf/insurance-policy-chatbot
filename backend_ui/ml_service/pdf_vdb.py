from ml_service.pdf_init_feature.pdf_vectorstore import obtain_vectorstore_from_client
from ml_service.tools.retrievers_validation import validate_input


def qdrant_retriever(search_type="similarity", kwargs=None):
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

    vectorstore = obtain_vectorstore_from_client()

    if kwargs:
        kwargs = validate_input(kwargs)
        return vectorstore.as_retriever(search_type=search_type, search_kwargs=kwargs)

    return vectorstore.as_retriever(search_type=search_type)
