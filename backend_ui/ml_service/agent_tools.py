from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain.agents import Tool

from ml_service.webscrapper_codigos_chile.webscrapper_app import qdrant_retriever as ccr
from ml_service.qdrant_vectorstore.vectorstore_funcs import (
    obtain_vectorstore_from_client,
    obtain_llm_multiquery_retriever,
    qdrant_retriever
)


# PDF TOOL RETRIEVER
# Retriever params
def init_feature_tool():
    search_type = "mmr"
    search_kwargs = {"k": 3, "lambda_mult": 0.25}
    
    embedding_name = "openai_embeddings"
    collection_name = "pdf_init_feature_openai_embeddings"
    
    pdf_retriever = qdrant_retriever(
        embedding_name=embedding_name,
        collection_name=collection_name,
        search_type=search_type,
        search_kwargs=search_kwargs
    )

    init_tool = create_retriever_tool(
        retriever=pdf_retriever,
        description="Diccionario introduccion. Resumen de polizas de seguros. Encabezado de los articulos.",
        name="pdf_init_feature",
    )
    
    return init_tool

 
def final_feature_tool():
    search_type = "mmr"
    search_kwargs = {"k": 2, "lambda_mult": 0.25}# ACA REDUCIMOS EL BIAS
    
    embedding_name = "openai_embeddings"
    collection_name = "pdf_final_feature_openai_embeddings"
    
    pdf_retriever = qdrant_retriever(
        embedding_name=embedding_name,
        collection_name=collection_name,
        search_type=search_type,
        search_kwargs=search_kwargs
    )

    pdf_tool = create_retriever_tool(
        retriever=pdf_retriever,
        description="Informacion completa de los articulos de las polizas de seguros.",
        name="pdf_final_feature",
    )
    
    return pdf_tool

 
# SERAPI TOOL
def news_search_tool():
    params = {
        "engine": "google",
        "gl": "cl",
        "hl": "es",
        "q": "seguros de vida",
        "tbm": "nws"
    }
    search = SerpAPIWrapper(
        params=params, serpapi_api_key='e03fb949db7815588cf61f04a2e9a88ba4698abc82d876ac6428c3728978f95e')

    repl_tool = Tool(
        name="news_search",
        description="Busca noticias web en castellano en Chile sobre polizas de seguro para la salud. La respuesta debe ser una noticia sobre pólizas de seguro en Chile. Si no hay noticias, la respuesta debe ser 'No hay noticias disponibles'.",
        func=search.run,
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
        name="webscrapper_codigo_chile",
    )
    return web_tool
