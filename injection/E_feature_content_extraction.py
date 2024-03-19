import os
import re
import pickle

from eda_tools.pdf_file_tools import extract_text
from utils.config import FEATURES_PATH, DOWNLOAD_PATH


def main():
    # leer los pickles de la carpeta '.serialized_features'
    feature_files_path = os.path.join(FEATURES_PATH, "feature_files.pkl")
    feature_articles_path = os.path.join(FEATURES_PATH, "feature_articles.pkl")
    grouped_feature_files_path = os.path.join(
        FEATURES_PATH, "grouped_feature_files.pkl"
    )
    grouped_feature_articles_path = os.path.join(
        FEATURES_PATH, "grouped_feature_articles.pkl"
    )

    with open(os.path.join(feature_files_path), "rb") as file:
        feature_files = pickle.load(file)

    with open(os.path.join(feature_articles_path), "rb") as file:
        feature_articles = pickle.load(file)

    with open(os.path.join(grouped_feature_files_path), "rb") as file:
        grouped_feature_files = pickle.load(file)

    with open(os.path.join(grouped_feature_articles_path), "rb") as file:
        grouped_feature_articles = pickle.load(file)

    # Obtain the files for each feature
    simple_files = [ff.metadata["file"] + ".pdf" for ff in feature_files]
    grouped_files = [
        gff.metadata["file"].split("_")[0] for gff in grouped_feature_files
    ]
    grouped_files = [f"{gf}.pdf" for gf in grouped_files]

    # Obtain the texts of each of the files
    simple_texts = [
        extract_text(os.path.join(DOWNLOAD_PATH, sf)) for sf in simple_files
    ]
    grouped_texts = [
        extract_text(os.path.join(DOWNLOAD_PATH, gf)) for gf in grouped_files
    ]

    # Obtain the policy headers
    simple_policy_headers = [ff.metadata["policy_header"] for ff in feature_files]
    grouped_policy_headers = [
        gff.metadata["policy_header"] for gff in grouped_feature_files
    ]
    grouped_policy_headers_search = [
        " ".join(gff.metadata["policy_header"].split(" ")[:7])
        for gff in grouped_feature_files
    ]

    # Obtain the articles titles for each feature
    simple_articles = [
        [(doc.metadata["file"], doc.metadata["article"]) for doc in fa]
        for fa in feature_articles
    ]
    grouped_articles = [
        [(doc.metadata["file"], doc.metadata["article"]) for doc in fa]
        for fa in grouped_feature_articles
    ]

    # Update Simple articles
    for i, pdf in enumerate(simple_articles):
        len_sa = len(simple_articles)
        len_pdf = len(pdf)
        for j, articles in enumerate(pdf):
            if j == len_pdf - 1:
                if i == len_sa - 1:
                    simple_articles[i][j] += (None,)
                    break
                simple_articles[i][j] += (None,)
                continue
            simple_articles[i][j] += (simple_articles[i][j + 1][1],)

    # Update grouped articles
    for i, policy in enumerate(grouped_articles):
        len_ga = len(grouped_articles)
        len_policy = len(policy)

        last_policy = grouped_articles[i][0][0].split("_")[0]

        for j, articles in enumerate(policy):

            try:
                next_policy = grouped_articles[i + 1][0][0].split("_")[0]
            except:
                next_policy = None

            if j == len_policy - 1:
                if i == len_ga - 1:
                    grouped_articles[i][j] += (None,)
                    continue

                if last_policy != next_policy:
                    grouped_articles[i][j] += (None,)
                    last_policy = next_policy
                    continue

                grouped_articles[i][j] += (grouped_policy_headers_search[i + 1],)
                continue

            grouped_articles[i][j] += (grouped_articles[i][j + 1][1],)

            last_policy = grouped_articles[i][j][0].split("_")[0]

    # Single files results to be converted into langchain.Documents
    sf_results = []

    for i, file in enumerate(simple_files):
        text = simple_texts[i]

        fragments = []
        li = 0

        for article in simple_articles[i]:

            if file.startswith(article[0]):
                fi = text.find(article[1], li)
                if article[2]:
                    li = text.find(article[2], fi)
                else:
                    li = None
                result = (
                    (simple_policy_headers[i],)
                    + article[:2]
                    + (text[fi:li].split("\n", 1)[1],)
                )
                fragments.append(result)

        sf_results.append(fragments)

    # Grouped files results to be converted into langchain.Documents
    gf_results = []
    for i, file in enumerate(grouped_files):
        text = grouped_texts[i]

        fragments = []
        li = 0
        for article in grouped_articles[i]:
            if file.startswith(article[0].split("_")[0]):
                fi = text.find(article[1], li)
                if article[2]:
                    li = text.find(article[2], fi)
                else:
                    li = None
                result = (
                    (grouped_policy_headers[i],)
                    + article[:2]
                    + (text[fi:li].split("\n", 1)[1],)
                )
                fragments.append(result)

        gf_results.append(fragments)

    # Save the results in a pickle
    with open(
        os.path.join(FEATURES_PATH, "simple_files_extractions.pkl"), "wb"
    ) as file:
        pickle.dump(sf_results, file)

    with open(
        os.path.join(FEATURES_PATH, "grouped_files_extractions.pkl"), "wb"
    ) as file:
        pickle.dump(gf_results, file)

    print("Done!")
