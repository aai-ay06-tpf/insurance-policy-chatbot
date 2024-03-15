from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import Tool

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

result = repl_tool.func("seguros de vida")

for i, news in enumerate(result, start=1):
    print(f"Noticia {i}:")
    print(f"Título: {news['title']}")
    print(f"Fuente: {news['source']}")
    print(f"Fecha: {news['date']}")
    print(f"Enlace: {news['link']}")
    print(f"Descripción: {news['snippet']}")
    print(f"Imagen: {news['thumbnail']}\n")
