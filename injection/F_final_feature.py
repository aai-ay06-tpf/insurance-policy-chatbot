import pickle, os, re
from utils.config import FEATURES_PATH
from langchain_core.documents.base import Document
from eda_tools.preprocess_stopwords import (
    remove_stopwords,
    preprocess_non_printable_characters,
)


def main():
    # Build the paths for the articles bin files
    simple_results = os.path.join(FEATURES_PATH, "simple_files_extractions.pkl")
    grouped_results = os.path.join(FEATURES_PATH, "grouped_files_extractions.pkl")

    # Load the articles
    with open(simple_results, "rb") as f:
        simple_data = pickle.load(f)
    with open(grouped_results, "rb") as f:
        grouped_data = pickle.load(f)

    # Gather all the information on a single list
    all_data = simple_data + grouped_data

    # Get the content for each article
    all_contents = [article[3] for policy in all_data for article in policy]

    # Remove '\n' and '\t' characters
    all_contents = [re.sub(r"[\n\t]", " ", content) for content in all_contents]

    # Remove extra spaces
    all_contents = [re.sub(r"\s+", " ", content) for content in all_contents]

    # clean non printable chars
    preprocessing = [
        preprocess_non_printable_characters(content) for content in all_contents
    ]

    # clean stopwords
    features = remove_stopwords(preprocessing)

    # build again the
    feature_contents = []
    ci = 0

    for policy in all_data:
        for article in policy:
            if "_" in article[1]:
                policy_file = article[1].split("_")[0]
                policy_name = article[1].split("_")[1]
            else:
                policy_file = article[1]
                policy_name = article[1]

            policy_header = article[0]
            article_title = article[2]
            page_content = policy_name + " \n " + policy_header + " \n " +\
                            article_title + " \n " + features[ci]
            
            ci += 1

            feature_contents.append(
                Document(
                    page_content=page_content,
                    metadata={
                        "policy_file": policy_file + ".pdf",
                        "policy_name": policy_name,
                        "policy_header": policy_header,
                        "article_title": article_title,
                    },
                )
            )

    # Save the features
    with open(os.path.join(FEATURES_PATH, f"final_features.pkl"), "wb") as f:
        pickle.dump(feature_contents, f)
