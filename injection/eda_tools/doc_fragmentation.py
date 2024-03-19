import re
from itertools import chain
from pypdf import PdfReader
from langchain_core.documents.base import Document


def extract_documents_from_text(file, articles):

    reader = PdfReader(file)
    text = "".join(chain.from_iterable(page.extract_text() for page in reader.pages))
    file = file.split("\\")[-1]
    policy_header = text.split("\n")[0]
    metadata = {
        "file": file,
        "policy_header": policy_header,
    }

    documents = []
    for i in range(len(articles)):

        metadata.update(article_title=articles[i])

        if i == len(articles) - 1:
            documents.append(
                Document(
                    page_content=text[text.find(articles[i]) :].replace("\n", " "),
                    metadata=metadata,
                )
            )
            break

        start_index, end_index = text.find(articles[i]), text.find(articles[i + 1])
        documents.append(
            Document(
                page_content=text[start_index:end_index].replace("\n", " "),
                metadata=metadata,
            )
        )

    return documents


# #TODO:
# def extract_documents_from_pattern(text: str, pattern: str) -> list:
#     matches = re.findall(pattern, text)

#     documents = []

#     for i in range(len(matches)):

#         metadata = {
#             "file": file,
#             "policy_header": policy_header,
#             "article_title": articles[i],
#         }

#         if i == len(articles) - 1:
#             documents.append(
#                 Document(
#                     page_content=text[text.find(articles[i]):].replace("\n", " "),
#                     metadata=metadata
#                 )
#             )
#             break

#         start_index, end_index = text.find(articles[i]), text.find(articles[i+1])
#         documents.append(
#             Document(
#                 page_content=text[start_index:end_index].replace("\n", " "),
#                 metadata=metadata
#             )
#         )

#     return documents
