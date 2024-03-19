from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents.base import Document

# Dictionary for mapping each type of document to its base URL and bookmarks
DOCUMENTS_INFO = {
    "codigo_de_comercio": "https://leyes-cl.com/codigo_de_comercio/{article_number}.htm",
    "companias_de_seguros": "https://leyes-cl.com/companias_de_seguros_sociedades_anonimas_y_bolsas_de_comercio/{article_number}.htm",
    "protocolo_seguridad_sanitaria": "https://leyes-cl.com/establece_protocolo_de_seguridad_sanitaria_laboral_para_el_retorno_gradual_y_seguro_al_trabajo/{article_number}.htm",
    "codigo_sanitario": "https://leyes-cl.com/codigo_sanitario/{article_number}.htm",
    "codigo_penal": "https://leyes-cl.com/codigo_penal/{article_number}.htm",
}


def obtain_scrapped_documents(web_id: str, articles: list) -> list:
    """Para un código en particular obtiene multiples artículos, los devuelve en formato Langchain.Document."""

    assert web_id in DOCUMENTS_INFO, f"Document type {web_id} not found."

    web_feature = []
    for article_number in articles:

        # Current stop lines
        start_marker = "Imprimir"
        end_marker = f"Chile Art. {article_number}"

        # Load the data
        loader = WebBaseLoader(
            DOCUMENTS_INFO[web_id].format(article_number=article_number)
        )
        data = loader.load()

        # Preprocessing results
        cleaned_lines = [
            line.replace("\xa0", " ").strip()
            for line in data[0].page_content.splitlines()
            if line.strip()
        ]

        # Splitting results and getting the Langchain.Documents
        if cleaned_lines:
            start_index = next(
                (
                    i
                    for i, line in enumerate(cleaned_lines)
                    if line.endswith(start_marker)
                ),
                None,
            )
            end_index = next(
                (
                    i
                    for i, line in enumerate(cleaned_lines)
                    if line.startswith(end_marker)
                ),
                None,
            )

            if start_index is not None and end_index is not None:
                relevant_content = cleaned_lines[start_index + 1 : end_index]

            else:
                raise ValueError(
                    f"Start or end marker not found for article {article_number}."
                )

            web_feature.append(
                Document(
                    page_content=" ".join(relevant_content),
                    metadata={
                        "url": DOCUMENTS_INFO[web_id].format(
                            article_number=article_number
                        ),
                        "article_number": article_number,
                    },
                )
            )
        else:
            raise ValueError(f"Content not found for article {article_number}.")

    return web_feature
