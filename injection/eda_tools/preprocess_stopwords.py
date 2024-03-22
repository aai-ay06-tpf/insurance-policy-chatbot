import re
import unicodedata
import spacy
from tqdm import tqdm


nlp = spacy.load("es_core_news_sm")


def preprocess_non_printable_characters(
    input_string: str, preserv_symbols: bool = True
) -> str:

    def restore_string(content: str, preserv_symbols: bool) -> str:
        cleaned_content = ""
        for c in content:

            if c in "áéíóúÁÉÍÓÚáéíóúÁÉÍÓÚó":
                cleaned_content += unicodedata.normalize("NFD", c)[0]
            elif c in ["ñ", "Ñ"]:
                cleaned_content += c
            # estos son los valores que eliminamos
            elif not preserv_symbols and (c in "&'()*+‘<=>[]^`{|}~ýª!?¿¡.,/⁉️‼:\""):
                continue
            else:
                cleaned_content += c
        return cleaned_content

    # Normalize the text to lowercase
    input_string = input_string.lower()

    # Remove non-printable characters
    input_string = restore_string(input_string, preserv_symbols=preserv_symbols)

    # remove double spaces
    input_string = re.sub(r"\s+", " ", input_string)

    # remove leading and trailing spaces
    return input_string.strip()


def remove_stopwords(contenido: list) -> list:

    corpus_sample = []
    for parrafo in tqdm(contenido):
        doc = nlp(parrafo)
        corpus_sample.append(
            " ".join([token.text for token in doc if not token.is_stop])
        )
    return corpus_sample
