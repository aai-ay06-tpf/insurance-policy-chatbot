from langchain_community.vectorstores.qdrant import Qdrant
from ml_service.tools.embeddings import Embeddings

emb = Embeddings()
embeddings = emb.obtain_embeddings("openai_embeddings")


def obtain_vectorstore_from_docs(documents: list) -> Qdrant:

    qdrant = Qdrant.from_documents(
        documents,
        embeddings,
        location=":memory:",
        collection_name="webscrapper_codigo_chile",
    )

    return qdrant
