from functools import wraps

from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain.agents import Tool

from ml_service.webscrapper_codigos_chile.webscrapper_app import qdrant_retriever as ccr
from ml_service.qdrant_vectorstore.vectorstore_funcs import (
    obtain_vectorstore_from_client,
    obtain_llm_multiquery_retriever,
    qdrant_retriever,
)


# PDF TOOL RETRIEVER
# Retriever params
def policy_feature_tool():
    search_type = "mmr"
    search_kwargs = {"k": 3, "lambda_mult": 0.25}

    embedding_name = "openai_embeddings"
    collection_name = "pdf_pol_feature_openai_embeddings"

    pdf_retriever = qdrant_retriever(
        embedding_name=embedding_name,
        collection_name=collection_name,
        search_type=search_type,
        search_kwargs=search_kwargs,
    )

    init_tool = create_retriever_tool(
        retriever=pdf_retriever,
        description="Esquema. Estructura de polizas de seguros. Lista de los articulos.",
        name="policy_feature",
    )

    return init_tool


def article_feature_tool():
    search_type = "mmr"
    search_kwargs = {"k": 2, "lambda_mult": 0.25}

    embedding_name = "openai_embeddings"
    collection_name = "pdf_art_feature_openai_embeddings"

    pdf_retriever = qdrant_retriever(
        embedding_name=embedding_name,
        collection_name=collection_name,
        search_type=search_type,
        search_kwargs=search_kwargs,
    )

    pdf_tool = create_retriever_tool(
        retriever=pdf_retriever,
        description="Resumen. Introduccion de los articulos. Encabezado de los articulos.",
        name="article_feature",
    )

    return pdf_tool

# PDR CONTENT TOOL

def content_feature_tool():
    search_type = "mmr"
    search_kwargs = {"k": 1}

    embedding_name = "openai_embeddings"
    collection_name = "pdf_final_feature_openai_embeddings"

    pdf_retriever = qdrant_retriever(
        embedding_name=embedding_name,
        collection_name=collection_name,
        search_type=search_type,
        search_kwargs=search_kwargs,
    )

    pdf_tool = create_retriever_tool(
        retriever=pdf_retriever,
        description="Desarrollar explicaciones con informacion completa. Contenido de los articulos de las polizas.",
        name="content_feature",
    )

    return pdf_tool


# SERAPI TOOL


def to_string(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return str(func(*args, **kwargs))

    return wrapper


def web_news_tool():
    params = {
        "engine": "google",
        "gl": "cl",
        "hl": "es",
        "q": "seguros de vida",
        "tbm": "nws",
    }
    search = SerpAPIWrapper(
        params=params,
        serpapi_api_key="e03fb949db7815588cf61f04a2e9a88ba4698abc82d876ac6428c3728978f95e",
    )

    # Create the function for the tool
    @to_string
    def dfunc(*args, **kwargs):
        return search.run(*args, **kwargs)

    repl_tool = Tool(
        name="web_news",
        description="Noticias y novedades en internet y la web sobre empresas de seguros.",
        func=dfunc,
    )

    return repl_tool


def retriever_tool_constitucion_chile():
    # CONSTITUCION CHILE TOOL
    # web scrapper params
    searchs = [
        ("codigo_de_comercio", [524, 525, 526]),  # , 538]),
        ("companias_de_seguros", [3, 10, 36]),
        ("protocolo_seguridad_sanitaria", [18]),
        ("codigo_sanitario", [112]),
        ("codigo_penal", [470]),
    ]

    # Obtain the retrievers
    search_type = "mmr"
    search_kwargs = {"k": 3, "lambda_mult": 0.25}
    web_retriever = ccr(searchs, search_type, search_kwargs)

    web_tool = create_retriever_tool(
        retriever=web_retriever,
        description="Constitucion de Chile. Codigo de comercio, Compañias de seguros, Protocolo de seguridad sanitaria, Codigo sanitario, Codigo penal.",
        name="cl_constit_tool",
    )
    return web_tool
