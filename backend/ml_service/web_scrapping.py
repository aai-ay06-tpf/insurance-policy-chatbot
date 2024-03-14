from langchain_community.document_loaders import WebBaseLoader

# Dictionary for mapping each type of document to its base URL and bookmarks
DOCUMENTS_INFO = {
    'codigo_de_comercio': {
        'url': 'https://leyes-cl.com/codigo_de_comercio/{article_number}.htm',
        'start_marker': 'Código de ComercioArtículo {article_number}.',
        'end_marker': 'Chile Art. {article_number} CCom, CDC, C Co'
    },
    'companias_de_seguros': {
        'url': 'https://leyes-cl.com/companias_de_seguros_sociedades_anonimas_y_bolsas_de_comercio/{article_number}.htm',
        'start_marker': 'Compañias de seguros, sociedades anonimas y bolsas de comercioArtículo {article_number}.',
        'end_marker': 'Chile Art. {article_number} Compañias de seguros, sociedades anonimas y bolsas de comercio'
    },
    'protocolo_seguridad_sanitaria': {
        'url': 'https://leyes-cl.com/establece_protocolo_de_seguridad_sanitaria_laboral_para_el_retorno_gradual_y_seguro_al_trabajo/{article_number}.htm',
        'start_marker': 'Establece protocolo de seguridad sanitaria laboral para el retorno gradual y seguro al trabajo en el marco de la alerta sanitaria decretada con ocasión de la enfermedad de covid-19 en el país y otras materias que indicaArtículo {article_number}.',
        'end_marker': 'Chile Art. {article_number} Establece protocolo de seguridad sanitaria laboral para el retorno gradual y seguro al trabajo en el marco de la alerta sanitaria decretada con ocasión de la enfermedad de covid-19 en el país y otras materias que indica'
    },
    'codigo_sanitario': {
        'url': 'https://leyes-cl.com/codigo_sanitario/{article_number}.htm',
        'start_marker': 'Código SanitarioArtículo {article_number}.',
        'end_marker': 'Chile Art. {article_number} Código Sanitario'
    },
    'codigo_penal': {
        'url': 'https://leyes-cl.com/codigo_penal/{article_number}.htm',
        'start_marker': 'Código PenalArtículo {article_number}.',
        'end_marker': 'Chile Art. {article_number} CP'
    },
}

def load_page(article_number, doc_type):
    """Loads the content of the specified article page based on document type."""
    loader = WebBaseLoader(DOCUMENTS_INFO[doc_type]['url'].format(article_number=article_number))
    data = loader.load()
    return data

def clean_and_split_content(data):
    """Cleans and splits the page content into lines."""
    if data and hasattr(data[0], 'page_content'):
        page_content = data[0].page_content
        return [line.replace('\xa0', ' ').strip() for line in page_content.splitlines() if line.strip()]
    else:
        return None

def extract_relevant_content(cleaned_lines, article_number, doc_type):
    """Extracts the relevant content for the specified article based on document type."""
    start_marker = DOCUMENTS_INFO[doc_type]['start_marker'].format(article_number=article_number)
    end_marker = DOCUMENTS_INFO[doc_type]['end_marker'].format(article_number=article_number)

    start_index = end_index = None

    for i, line in enumerate(cleaned_lines):
        if start_marker in line:
            start_index = i
            break

    for i, line in enumerate(cleaned_lines[::-1]):  # Optimisation: reverse the search for the end
        if end_marker in line:
            end_index = len(cleaned_lines) - i - 1
            break

    if start_index is not None and end_index is not None:
        return cleaned_lines[start_index:end_index]
    else:
        return ["The relevant content could not be found."]

def main(doc_type, articles):
    """Main function that processes a list of article numbers based on document type."""
    for article_number in articles:
        data = load_page(article_number, doc_type)
        cleaned_lines = clean_and_split_content(data)
        if cleaned_lines:
            relevant_content = extract_relevant_content(cleaned_lines, article_number, doc_type)
            print(f"Artículo {article_number}:")
            for line in relevant_content:
                print(line)
            print("\n" + "-"*50 + "\n")  # Add visual separation between articles
        else:
            print(f"No content found for article {article_number} or object does not have 'page_content' attribute.")

if __name__ == "__main__":
    print("Código de Comercio")
    main('codigo_de_comercio', [524, 525, 526])

    print("Compañías de Seguros")
    main('companias_de_seguros', [3, 10, 36])

    print("\n\n")

    print("Protocolo de Seguridad Sanitaria")
    main('protocolo_seguridad_sanitaria', [18])
    
    print("\n\n")

    print("Código Sanitario")
    main('codigo_sanitario', [112])

    print("\n\n")

    print("Código Penal")
    main('codigo_penal', [470])
