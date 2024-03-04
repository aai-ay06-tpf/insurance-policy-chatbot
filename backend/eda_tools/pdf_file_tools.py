import os, re
from itertools import chain
from pypdf import PdfReader
from langchain_community.document_loaders.pdf import PyPDFLoader

def extract_uppercase_lines(file_path: str) -> dict:
    # PDF files data extraction
    reader = PdfReader(file_path)
    result = []
    for page in reader.pages:
        text = page.extract_text()

        # Obtain the uppercase lines in the text
        uppercase_lines = [line.strip() for line in text.split("\n") if line.isupper()]
        result.append(uppercase_lines)

        
    return result


# def extract_patterns(file_path: str, pattern: str, normalize: bool=False) -> list:
#     reader = PdfReader(file_path)
#     text = ''.join([page.extract_text() for page in reader.pages])
#     if normalize:
#         return re.findall(r''+pattern, text, flags=re.IGNORECASE)
#     else:
#         return re.findall(r''+pattern, text)





def extract_patterns(file_path: str, pattern: str, normalize: bool = False) -> list:
    reader = PdfReader(file_path)
    text = ''.join(chain.from_iterable(page.extract_text() for page in reader.pages))
    lines = text.split('\n')
    flags = re.IGNORECASE if normalize else 0
    matches = [line for line in lines if re.search(pattern, line, flags=flags)]
    return matches


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
                            if page[ix+i].strip() != '':
                                matches.append(page[ix+i])
                        except:
                            break
        # result.append(" ".join(matches)) # es mas procesable
        result.append(matches)# es mas comprensible
    
    return result


# Please remove from here.
pattern = "ART.CULO\s\d+.+:"
# Important for EnsambleRetriever

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