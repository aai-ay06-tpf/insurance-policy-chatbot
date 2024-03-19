"""
Examples of retriever search_kwargs:

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

from pydantic import BaseModel
from typing import Optional, Dict, Any


class Filter(BaseModel):
    fields: Optional[Dict[str, Any]] = {"fields": {"field1": "value1"}}


class SearchKwargs(BaseModel):
    k: Optional[int] = 4
    score_threshold: Optional[float] = 0.8
    fetch_k: Optional[int] = 20
    lambda_mult: Optional[float] = 0.5
    filter: Optional[Filter]


def validate_search_kwargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:

    # check if kwargs has the attribute filter
    if not kwargs.get("filter"):
        kwargs["filter"] = Filter().model_dump()

    try:
        search_kwargs = SearchKwargs(**kwargs)
        copy_dict = search_kwargs.model_dump()
    except Exception as e:
        print("Validation error in retriever search_kwargs")
        raise e

    param_dict = {}
    for k in kwargs.keys():
        if k in copy_dict.keys():
            param_dict |= {k: copy_dict[k]}
        else:
            print(f"{k} missmatch key")

    # check if the param filter is the same as default
    if param_dict["filter"] == Filter().model_dump():
        param_dict.pop("filter")

    return param_dict


if __name__ == "__main__":

    empty_filter = Filter()
    print(empty_filter.model_dump())
    # ejemplo de uso

    # Crear un diccionario que cumpla con los requisitos
    kwargs = {
        "k": 10,
        # "score_threshold": 0.8,
        "fetch_k": 30,
        "lambda_mssut": 0.7,
        "filter": {"fields": {"field1": "value1", "field2": "value1"}},
    }

    # Crear una instancia del esquema SearchKwargs
    try:
        search_kwargs = SearchKwargs(**kwargs)
        copy_dict = search_kwargs.model_dump()
    except Exception as e:
        print("Validation error in retriever search_kwargs")
        raise e

    param_dict = {}
    for k in kwargs.keys():
        if k in copy_dict.keys():
            param_dict |= {k: copy_dict[k]}
        else:
            print(f"{k} missmatch key")

    # param_dict = {k: copy_dict[k] for k in kwargs.keys() if k in copy_dict.keys()}

    # param_dict = {k: copy_dict[k] if k in copy_dict.keys() else print(f'{k} missmatch key') for k in kwargs.keys()}

    print(param_dict)
