import os, re
from itertools import chain
from pypdf import PdfReader
from langchain_community.document_loaders.pdf import PyPDFLoader


def extract_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ''.join(chain.from_iterable(page.extract_text() for page in reader.pages))
    return text

def remove_pattern_from_lines(lines: list, pattern: str) -> list:
    """
    Remove the specified pattern from each line in the list of strings,
    removing double whitespaces and trimming whitespace at the beginning
    and end of each line.

    Args:
        lines (list): A list of strings.
        pattern (str): The pattern to remove from each line.

    Returns:
        list: A list of strings with the specified pattern removed from each line,
        with double whitespaces removed, and with whitespace trimmed from the
        beginning and end of each line.
    """
        
    cleaned_lines = []
    for line in lines:
        cleaned_line = re.sub(pattern, '', line).strip()
        cleaned_line = re.sub(r'\s+', ' ', cleaned_line)
        cleaned_lines.append(cleaned_line)
    return cleaned_lines

def extract_patterns(file_path: str, pattern: str, normalize: bool = False) -> list:
    reader = PdfReader(file_path)
    text = ''.join(chain.from_iterable(page.extract_text() for page in reader.pages))
    lines = text.split('\n')
    flags = re.IGNORECASE if normalize else 0
    matches = [line for line in lines if re.search(pattern, line, flags=flags)]
    return matches


# TODO: REMOVER LAS FUNCIONES QUE NO SE IMPLEMENTAN (CREAR cementerio: cra.py)
# def ignore_patterns(file_path: str, pattern: str) -> list:
#     reader = PdfReader(file_path)
#     text = ''.join(chain.from_iterable(page.extract_text() for page in reader.pages))
#     lines = text.split('\n')
#     matches = [line for line in lines if not re.search(pattern, line)]
#     return matches
def extract_extended_pattern():
    pass
def extract_patterns_per_page(file_path: str, pattern: str, extend: bool = True) -> list:
    reader = PyPDFLoader(file_path)
    documents = reader.load()
    result = []
    for doc in documents:
        matches = []
        page = doc.page_content.split('\n')
        for ix, line in enumerate(page):
            if re.search(pattern, line):
                matches.append(line)
                if extend:
                    for i in range(1, 5):
                        try:
                            if re.search(pattern, page[ix+i]):
                                break
                            if page[ix+i].strip() != '':
                                matches.append(page[ix+i])
                        except IndexError:
                        
                            break
        # result.append(" ".join(matches)) # es mas procesable
        result.append(matches)# es mas comprensible
    
    return result


def obtain_header_paragraphs(text: list, extraction: list) -> list:
    """
    Obtain the paragraphs that are under the header of the extraction
    
    Parameters:
    - text (list): A list of strings containing the text of the policy.
    - extraction (list): A list of strings containing the headers of the articles.
    
    Returns:
    list: A list of lists of strings, each list containing the paragraphs of the policy
    """
    paragraph = []
    for i, line in enumerate(text):
        cache = []
        if line in extraction:
            while True:
                i += 1
                if text[i].strip() == "":
                    continue
                if text[i] in extraction:
                    paragraph.append(" ".join(cache))
                    cache = []
                    break
                if len(cache) > 15:
                    while True:
                        if not cache[-1].strip().endswith("."):
                            cache.pop()
                        else:
                            break
                    paragraph.append(" ".join(cache))
                    cache = []
                    break
                if len(paragraph) == len(extraction) -1:
                    #TODO: ver una manera de obtener el ultimo articulo sin repetir el codigo de arriba
                    # articles.append(cache)
                    # print(text[i])
                    print(f"function: {__name__}.obtain_header_paragraphs - pending work")
                    
                    
                    
                    break

                cache.append(text[i].strip())
        # HINT: usar un segundo cache? 
        # encontrar otra condicion de exit? -> if (len(paragraph) == len(extraction) -1) and (...):
                
    return paragraph

def distribute_weights(string_list):
    """Distribute the weights of a list of strings based on their length."""
    # Calculate the total length of all strings
    total_length = sum(len(string) for string in string_list)
    
    # Calculate the weights of each string
    weights = [len(string) / total_length for string in string_list]
    
    # Normalize the weights so that the sum is 1
    sum_weights = sum(weights)
    normalized_weights = [weight / sum_weights for weight in weights]
    
    return normalized_weights

