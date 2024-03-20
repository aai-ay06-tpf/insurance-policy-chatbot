import os
import time
import pickle
import re
from typing import Callable
from copy import copy

from langchain_core.documents.base import Document
from eda_tools.pdf_file_tools import (
    extract_text,
    remove_pattern_from_lines,
    obtain_header_paragraphs,
)
from utils.config import DOWNLOAD_PATH, FEATURES_PATH
from eda_tools.preprocess_stopwords import (
    preprocess_non_printable_characters,
    remove_stopwords,
)


def check_sequence(lst):
    for i in range(1, len(lst)):
        if not (lst[i] == lst[i - 1] + 1):
            return False
    return True


def isolate_sequences(lst):
    result = []
    sublist = [lst[0]]
    for i in range(1, len(lst)):
        if lst[i] == lst[i - 1] + 1:
            sublist.append(lst[i])
        else:
            result.append(sublist)
            sublist = [lst[i]]
    result.append(sublist)
    return result


# [[1, 2, 3, 4, 5, ...],[ 1, 2, 3, ...],[ 1, 2]]


def extract_grouped_patterns(file_path: str, pattern: str) -> list:
    """Extract the whole lines from a PDF file in which the specified pattern is found."""
    text = extract_text(file_path)
    lines = text.split("\n")
    matches = [line for line in lines if re.search(pattern, line)]
    # obtain the groups of the pattern
    groups = [int(re.search(pattern, line).groups()[0]) for line in matches]
    if check_sequence(groups):
        return ["no patterns to be grouped."]

    # Group the matches
    sequences = isolate_sequences(groups)
    iter_match = iter(matches)
    grouped_matches = []
    for lst in sequences:
        group = []
        for i in lst:
            group.append(next(iter_match))
        grouped_matches.append(group)

    return grouped_matches


# [[Art_1, Art_2, 3, 4, 5, ...],[ 1, 2, 3, ...],[ 1, 2]]


# TODO: Mejorar el print del output de la func
def create_file_batch(files: list, func: Callable, *args: tuple) -> list:
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
            res = func(selected_file, arg)
            for r in res:
                print(r)
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


def create_grouped_feature(batch_files: list, func: Callable) -> list:
    """
    Create list of langchain Documents in which each document is a representation of all the articles in the policy
    with the corresponding preprocessing and metadata.

    Parameters:
    - batch_files (list): A list of tuples containing the file path and the pattern to be used to extract the articles.

    Returns:
    List[Document]: A list of langchain Documents.
    """

    policy_name_pattern = r"[A-Z]{3}\d+"

    extractions = [func(file, pattern) for file, pattern in batch_files]
    # [ [ pdf ], [ [art_1, art_2, art_f], [art_i, art_2, ..] ], [ ], ...]
    # Intersection between the last article of a policy and the first article of the next policy
    intersections = []
    for pdf in extractions:
        section = []
        for i in range(len(pdf)):
            if i == 0:  # ignore the first policy in the pdf
                continue
            else:
                section.append((pdf[i - 1][-1], pdf[i][0]))
        intersections.append(section)

    # Preparing of the page_content about articles
    articles = []  # page_content -> missing policy header
    for pdf, (_, pattern) in zip(extractions, batch_files):
        section = []
        for extraction in pdf:
            # ", ".join(remove_pattern_from_lines(
            # extraction, pattern))
            art = re.sub(
                r"[-\.]", "", ", ".join(remove_pattern_from_lines(extraction, pattern))
            )
            art = re.sub(r"\s+", " ", art).strip()
            section.append(art)

        articles.append(section)

    # Preparing of the page_content about headers
    texts = [extract_text(file) for file, _ in batch_files]
    first_articles = [pdf[0][0] for pdf in extractions]

    # # Obtain the headers of the first policy in the pdf files and the policy name
    first_policy_paragraph = [
        text[: text.find(article)] for text, article in zip(texts, first_articles)
    ]

    # Obtain the headers of the first policy in the pdf files
    policy_headers = [
        paragraph.replace("\n", " ") for paragraph in first_policy_paragraph
    ]
    first_policy_headers = []  # page_content
    for header in policy_headers:
        new_header = []
        # use `re` for removing doble spaces
        header = re.sub(r"\s+", " ", header)
        # Tokenize the header and keep only the uppercase words
        for word in header.split(" "):
            if word.isupper() and word.isalpha():
                new_header.append(word)
        first_policy_headers.append(" ".join(new_header))

    # Obtain the policy name by pattern
    matches = [
        re.search(policy_name_pattern, string=header)
        for header in first_policy_paragraph
    ]
    first_policy_names = [
        match[0] if match else "Unnamed Policy" for match in matches
    ]  # metadata

    # The middle section between policies | it has len -2 compared with extractions
    middle_section = []
    for ix, text in enumerate(texts):
        text = text.splitlines()
        iter_section = iter(intersections[ix])
        mid_section = next(iter_section)

        section = []
        for i, line in enumerate(text):
            cache = []
            if line == mid_section[0]:
                while True:
                    try:
                        i += 1
                        if text[i].strip() == "":
                            continue
                        if text[i] == mid_section[1]:
                            section.append(cache)
                            cache = []
                            if len(section) < len(intersections[ix]):
                                mid_section = next(iter_section)
                            break
                        cache.append(text[i].strip())
                    except IndexError:
                        section.append(cache)
                        break
        middle_section.append(section)

    # Extract the header of the middle section
    # recorre la lista de lineas y guarda las lineas en mayusculas que encuentra
    middle_policies_header = []
    for pdf in middle_section:
        header_section = []
        for policy in pdf:
            header = []
            for line in policy:
                if line.isupper():
                    header.append(line)

            header_section.append(" ".join(header))

        header_section = [element for element in header_section if element != ""]
        middle_policies_header.append(header_section)

    # Extract the policy name by pattern
    middle_policies_names = []
    for pdf in middle_section:
        policy_name_section = []
        for policy in pdf:
            for line in policy[::-1]:
                match = re.search(policy_name_pattern, string=line)
                if match:
                    policy_name_section.append(match[0])
                    break

        middle_policies_names.append(policy_name_section)

    # FEATURE FILES
    feature_files = []
    for i in range(len(first_policy_headers)):
        headers = [first_policy_headers[i]] + middle_policies_header[i]
        policy_names = [first_policy_names[i]] + middle_policies_names[i]

        # primera parte del page_content
        # file_content_hip = [": ".join(element)
        #                     for element in list(zip(headers, articles[i]))]
        page_content = [
            "```{'poliza': '" + header.lower() + "', 'articulos': '" + article.lower()
            for article, header in zip(articles[i], headers)
        ]

        for j in range(len(policy_names)):
            # agregar la parte que falta del page_content_i
            page_content[j] += (
                "', 'filename': '"
                + policy_names[0]
                + ".pdf', 'poliza_id': '"
                + policy_names[j]
                + "'}```"
            )

            feature_files.append(
                Document(
                    page_content=page_content[j],
                    metadata={
                        "file": f"{policy_names[0]}_{policy_names[j]}",
                        "policy_header": headers[j],
                    },
                )
            )

    # FEATURE ARTICLE
    feature_articles = []
    for i, pdf in enumerate(extractions):
        text = texts[i]
        policy_names = [first_policy_names[i]] + middle_policies_names[i]
        headers = [first_policy_headers[i]] + middle_policies_header[i]
        # Recortar las lineas que tengan mas de 7 palabras
        for ix, head in enumerate(headers):
            if len(head.split(" ")) > 7:
                headers[ix] = " ".join(head.split(" ")[:7])

        fragments = []
        li = 0
        for ix in range(len(headers) - 1):
            fi = text.find(headers[ix], li)
            li = text.find(headers[ix + 1], fi)
            fragments.append(text[fi:li])
        fragments += [text[li:]]

        headers = [first_policy_headers[i]] + middle_policies_header[i]
        article_content = [
            obtain_header_paragraphs(fragments[j].splitlines(), extraction)
            for j, extraction in enumerate(pdf)
        ]

        for j, contents in enumerate(article_content):
            features = []
            for k, content in enumerate(contents):
                # filename/policy_name
                policy_name = f"{policy_names[0]}_{policy_names[j]}"
                # article_name
                article_name = re.sub(batch_files[i][1], "", pdf[j][k])
                article_name = re.sub(r"[-\.]", " ", article_name)
                article_name = re.sub(r"\s+", " ", article_name).strip()
                content = re.sub(r"\\t", " ", content)
                content = re.sub(r"\s+", " ", content)

                article_name = preprocess_non_printable_characters(article_name)
                content = preprocess_non_printable_characters(content)

                page_content = (
                    "```{'poliza': '"
                    + headers[j].lower().strip()
                    + "', 'articulo': '"
                    + article_name
                    + "', 'introduccion': '"
                    + content
                    + "', 'filename': '"
                    + policy_names[0]
                    + ".pdf"
                    + "', 'poliza_id': '"
                    + policy_names[j]
                    + "'}```"
                )

                features.append(
                    Document(
                        page_content=page_content,
                        metadata={
                            "file": policy_name,
                            "policy_header": headers[j],
                            "article": pdf[j][k],
                        },
                    )
                )
            feature_articles.append(features)

    return feature_files, feature_articles


def main():

    pdf_files = os.listdir(DOWNLOAD_PATH)

    # WARNING: This patterns must have 1 grouped element and the group must be only numbers
    # use (?: ) -> for non-capturing groups
    # (\d+) -> for capturing numered groups
    patterns = ["^ART.CULO\s(?:N.\s)?(\d+).:?"]
    # patterns = ["^ART.CULO\s(?:N.\s)?(\d+).:?", "^\s?(?:Art).(?:culo)\s(?:N.\s)?(\d)+(?:.|:)+$"]

    # Obtain the features data
    # For manual creation of the file_batch use this line:
    # file_batch = create_file_batch(
    #     pdf_files, extract_grouped_patterns, *patterns)
    # else:
    with open("C_default_file_batch.pkl", "rb") as f:
        file_batch = pickle.load(f)

    # Features: Both file and articles
    feature_files, feature_articles = create_grouped_feature(
        file_batch, extract_grouped_patterns
    )

    # Save the features
    with open(os.path.join(FEATURES_PATH, f"grouped_feature_files.pkl"), "wb") as f:
        pickle.dump(feature_files, f)

    # Save the features
    with open(os.path.join(FEATURES_PATH, f"grouped_feature_articles.pkl"), "wb") as f:
        pickle.dump(feature_articles, f)

    print("Done!")
