import os
import time
import pickle
import re
from typing import Callable

from langchain_core.documents.base import Document
from eda_tools.pdf_file_tools import (
    extract_patterns,
    extract_text,
    remove_pattern_from_lines,
    obtain_header_paragraphs,
)
from utils.config import DOWNLOAD_PATH, FEATURES_PATH


start = time.time()


def create_file_batch(files: list, func: Callable, *args: tuple) -> list:
    """
    Create a file batch by inspecting the output of a given function with many different RegEx patterns.
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
            patterns = func(selected_file, arg)
            for pattern in patterns:
                print(pattern)

            # UI Context
            filename = os.path.basename(selected_file).replace(".pdf", "")
            print(f"File: {filename}")
            ui = input("Want to add this file to the batch? (y/n): ")
            print()
            # Output Management
            if not ui.isalpha():
                raise ValueError("Invalid input")
            if ui.lower() == "y":
                batch_files.append((selected_file, arg))

    return batch_files[1:]


def obtain_policy_headers(batch_files: list, extractions: list) -> list:
    texts = [extract_text(file) for file, _ in batch_files]
    policy_headers = [
        text[: text.find(extractions[i][0])].replace("\n", " ")
        for i, text in enumerate(texts)
    ]
    cleaned_policy_headers = []
    for header in policy_headers:
        new_header = []
        # use `re` for removing doble spaces
        header = re.sub(r"\s+", " ", header)
        # Tokenize the header and keep only the uppercase words
        for word in header.split(" "):
            if word.isupper() and word.isalpha():
                new_header.append(word)
        cleaned_policy_headers.append(" ".join(new_header))
    return cleaned_policy_headers


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

    filenames = [
        os.path.basename(filename).replace(".pdf", "") for filename, _ in batch_files
    ]

    extractions = [func(file, pattern) for file, pattern in batch_files]

    articles = [
        ", ".join(element).lower()
        for element in [
            remove_pattern_from_lines(extraction, pattern)
            for extraction, (_, pattern) in zip(extractions, batch_files)
        ]
    ]

    policy_headers = obtain_policy_headers(batch_files, extractions)

    features = [
        "```{'poliza': '"
        + header.lower()
        + "', 'articulos': '"
        + article
        + "', 'filename': '"
        + filenames[i]
        + ".pdf', 'poliza_id': '"
        + filenames[i]
        + "'}```"
        for i, (article, header) in enumerate(zip(articles, policy_headers))
    ]

    return [
        Document(
            page_content=feature,
            metadata={"file": filenames[i], "policy_header": policy_headers[i]},
        )
        for i, feature in enumerate(features)
    ]


def create_feature_article(batch_files: list, func: Callable) -> list:
    """
    Create list of langchain Documents in which each document is a representation of all the articles in the policy
    with the corresponding preprocessing and metadata.

    Parameters:
    - batch_files (list): A list of tuples containing the file path and the pattern to be used to extract the articles.
    - func (function): The function to be used to extract the articles from the text.

    Returns:
    List[ List[Document] ]: A list of lists of langchain Documents.
    """

    filenames = [
        os.path.basename(filename).replace(".pdf", "") for filename, _ in batch_files
    ]

    extractions = [func(file, pattern) for file, pattern in batch_files]

    splitted_text = [extract_text(file).splitlines() for file, _ in batch_files]

    contents = [
        obtain_header_paragraphs(text, extraction)
        for text, extraction in zip(splitted_text, extractions)
    ]

    policy_headers = obtain_policy_headers(batch_files, extractions)

    features = []

    for i, content_list in enumerate(contents):
        batch = []
        for j, content in enumerate(content_list):
            batch.append(
                Document(
                    page_content="```{'poliza': '"
                    + policy_headers[i].lower().strip()
                    + "', 'articulo': '"
                    + re.sub(batch_files[i][1], "", extractions[i][j]).strip().lower()
                    + "', 'introduccion': '"
                    + content
                    + "', 'filename': '"
                    + filenames[i]
                    + ".pdf"
                    + "', 'poliza_id': '"
                    + filenames[i]
                    + "'}```",
                    metadata={
                        "file": filenames[i],
                        "policy_header": policy_headers[i],
                        "article": extractions[i][j],
                    },
                )
            )
        features.append(batch)

    return features


def main():

    pdf_files = os.listdir(DOWNLOAD_PATH)

    patterns = ["^ART.CULO\s(?:N.\s)?\d+.:?"]

    # Obtain the features data
    # For manual creation of the file_batch use this line:
    # file_batch = create_file_batch(pdf_files, extract_patterns, *patterns)
    # else:
    with open("B_default_file_batch.pkl", "rb") as f:
        file_batch = pickle.load(f)

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
