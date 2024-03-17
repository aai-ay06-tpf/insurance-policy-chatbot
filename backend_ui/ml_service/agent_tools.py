from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain.agents import Tool

from ml_service.pdf_vdb import qdrant_retriever as pdf_qdrant_retriever
from ml_service.web_scrapper import parent_document_retriever, qdrant_retriever



## PDF TOOL RETRIEVER
# Retriever params

search_type = "mmr"
search_kwargs = {"k": 3, "lambda_mult": 0.25}
pdf_retriever = pdf_qdrant_retriever(search_type, search_kwargs)

pdf_tool = create_retriever_tool(
    retriever=pdf_retriever,
    description="Busca y devuelve indices de polizas de seguros o el encabezado de los articulos.",
    name="feature_init_pdf",
)


## CONSTITUCION CHILE TOOL
#TODO: almacenar de forma local
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
web_retriever = qdrant_retriever(searchs, search_type, search_kwargs)

web_tool = create_retriever_tool(
    retriever=web_retriever,
    description="Busca y devuelve extractos de los codigos de ley de la constitucion de Chile.",
    name="webscrapper_codigo_chile",
)


## SERAPI TOOL
params = {
    "engine": "google",
    "gl": "cl",
    "hl": "es",
    "q": "seguros de vida",
    "tbm": "nws"
}
search = SerpAPIWrapper(params=params, serpapi_api_key='e03fb949db7815588cf61f04a2e9a88ba4698abc82d876ac6428c3728978f95e')
repl_tool = Tool(
    name="news_search",
    description="Busca noticias en castellano en Chile sobre seguros de vida. Usa esto para ejecutar búsquedas de noticias. La entrada debe ser un término de búsqueda válido relacionado con seguros de vida.",
    func=search.run,
)
