import os, time, pickle, re
from typing import Callable

from langchain_core.documents.base import Document
from eda_tools.pdf_file_tools import (
    extract_patterns, extract_text,
    remove_pattern_from_lines,
    obtain_header_paragraphs
)
from utils.config import DOWNLOAD_PATH, FEATURES_PATH


start = time.time()



def create_file_batch(files:list, func: Callable, *args: tuple) -> list:
    """
    Create a file batch by inspecting the output of a given function with many differnte arguments.
    The function will be asking the user if the output is correct, and if not, the user can remove the file from the batch.

    Parameters:
    - files (list): A list of the files to be inspected.
    - funcs (function): The function to be used to inspect each of the files.
    - *args: The arguments to be used for the function.

    Returns:
    List: A list of the files that were selected by the user.
    
    """

    batch_files = [(None, None)]
    
    for arg in args:
        print(f"\n{func.__name__} argumments: {arg}\n")
        for file in files:
            selected_file = os.path.join(DOWNLOAD_PATH, file)
            # Once the file was added there is no need to check with other arguments
            if selected_file in (batch[0] for batch in batch_files):
                continue
            # Function Execution
            print(func(selected_file, arg))
            # UI Context
            filename = selected_file.split("\\")[-1].replace(".pdf", "")
            print(f"File: {filename}")
            ui = input("Want to add this file to the batch? (y/n): ")
            print()
            # Output Management
            if not ui.isalpha():
                raise ValueError("Invalid input")
            if ui.lower() == "y":
                batch_files.append((selected_file, arg))
    
    return batch_files[1:]



def create_feature_file(batch_files: list, func: Callable) -> list:
    """
    Create list of langchain Documents in which each document is a representation of all the articles in the policy
    with the corresponding preprocessing and metadata.
    
    Parameters:
    - batch_files (list): A list of tuples containing the file path and the pattern to be used to extract the articles.
    - func (function): The function to be used to extract the articles from the text.
    
    Returns:
    List[Document]: A list of langchain Documents.
    """
    
    filenames = [filename.split("\\")[-1].replace(".pdf", "") for filename, _ in batch_files]
    
    extractions = [func(file, pattern) for file, pattern in batch_files]
    
    articles = [" ".join(element).lower() for element in [remove_pattern_from_lines(extraction, pattern) for extraction, (_, pattern) in zip(extractions, batch_files)]]
    
    texts = [extract_text(file) for file, _ in batch_files]
    policy_headers = [text[:text.find(extractions[i][0])].replace("\n", " ") for i, text in enumerate(texts)]
    cleaned_policy_headers = []
    for header in policy_headers:
        new_header = []
        # use `re` for removing doble spaces
        header = re.sub(r'\s+', ' ', header)
        # Tokenize the header and keep only the uppercase words
        for word in header.split(" "):
            if word.isupper() and word.isalpha():
                new_header.append(word)
        cleaned_policy_headers.append(" ".join(new_header).lower())
        
    features = [f"{header} {article}" for article, header in zip(articles, cleaned_policy_headers)]
    
    return [Document(page_content=feature, metadata={"file": filenames[i]}) for i, feature in enumerate(features)]
    
    
def create_feature_article(batch_files: list, func: Callable) -> list:
    """
    
    TODO: REVIEW THIS DOCS
    
    Create list of langchain Documents in which each document is a representation of all the articles in the policy
    with the corresponding preprocessing and metadata.
    
    Parameters:
    - batch_files (list): A list of tuples containing the file path and the pattern to be used to extract the articles.
    - func (function): The function to be used to extract the articles from the text.
    
    Returns:
    List[ List[Document] ]: A list of lists of langchain Documents.
    """
    
    filenames = [filename.split("\\")[-1].replace(".pdf", "") for filename, _ in batch_files]
    
    extractions = [func(file, pattern) for file, pattern in batch_files]
    
    splitted_text = [extract_text(file).splitlines() for file, _ in batch_files]
    
    contents = [obtain_header_paragraphs(text, extraction) for text, extraction in zip(splitted_text, extractions)]
    
    features = []
    for i, content_list in enumerate(contents):
        batch = []
        for j, content in enumerate(content_list):
            batch.append(Document(page_content=content, metadata={"file": filenames[i], "article": extractions[i][j]}))
        features.append(batch)
        
    return features


if __name__ == "__main__":
    
    pdf_files = os.listdir(DOWNLOAD_PATH)
    patterns = ["^ART.CULO\s(?:N.\s)?\d+.:?"]
    
    # Obtain the features data
    file_batch = create_file_batch(pdf_files, extract_patterns, *patterns)
    
    # First Feature: Extracting the article titles and policy header
    feature_files = create_feature_file(file_batch, extract_patterns)
    
    # Second Feature: Extracting the article headers from policies
    feature_articles = create_feature_article(file_batch, extract_patterns)
    
    # Save the features
    with open(os.path.join(FEATURES_PATH, f"feature_files.pkl"), "wb") as f:
        pickle.dump(feature_files, f)
    
    with open(os.path.join(FEATURES_PATH, f"feature_articles.pkl"), "wb") as f:
        pickle.dump(feature_articles, f)
    
    end = time.time()

    print(f"total time taken: {round(end-start, 1)} seconds")
