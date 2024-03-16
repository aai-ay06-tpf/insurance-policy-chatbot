from ml_service.pdf_final_feature.pdf_vectorstore import obtain_vectorstore_from_client
from ml_service.tools.retrievers_validation import validate_search_kwargs


vectorstore = obtain_vectorstore_from_client()


search_type = "similarity"
kwargs = {"k":1}
kwargs = validate_search_kwargs(kwargs)



retriever = vectorstore.as_retriever(search_type=search_type, search_kwargs=kwargs)


def invoke_retriever(msg:str) -> list:
    """
    Invoke the retriever to search for the most similar documents to the given message.

    Parameters:
    - msg (str): The message to search for in the vector database.

    Returns:
    list: A list of the most similar documents to the given message.
    """
    return retriever.invoke(msg)