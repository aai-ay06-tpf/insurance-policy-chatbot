import re
from pypdf import PdfReader


def extract_text(file_path: str) -> str:
    """Return the text of a PDF file as a single string."""
    reader = PdfReader(file_path)
    text = "".join("\n".join(page.extract_text() for page in reader.pages))
    return text


def extract_patterns(file_path: str, pattern: str) -> list:
    """Extract the whole lines from a PDF file in which the specified pattern is found."""
    text = extract_text(file_path)
    lines = text.split("\n")
    matches = [line.replace(".", "") for line in lines if re.search(pattern, line)]
    return matches


def remove_pattern_from_lines(lines: list, pattern: str) -> list:
    """
    Remove the specified pattern from each line in the list of strings,
    removing double whitespaces and trimming whitespace at the beginning
    and end of each line.

    Args:
        lines (list): A list of strings.
        pattern (str): The pattern to remove from each line.

    Returns:
        list: A list of preprocessed strings with the specified pattern removed from each line.
    """

    cleaned_lines = []
    for line in lines:
        cleaned_line = re.sub(pattern, "", line).strip()
        cleaned_line = re.sub(r"\s+", " ", cleaned_line)
        cleaned_lines.append(cleaned_line)
    return cleaned_lines


def obtain_header_paragraphs(text: list, extraction: list) -> list:
    """
    Obtain the paragraphs that are under the header of the extraction

    Parameters:
    - text (list): A list of strings containing the text of the policy.
    - extraction (list): A list of strings containing the article titles.

    Returns:
    list: A list of lists of strings, each list containing the header paragraphs of the policy
    """
    paragraph = []
    for i, line in enumerate(text):
        cache = []
        if line in extraction:
            while True:
                try:
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

                    cache.append(text[i].strip())

                except IndexError:
                    paragraph.append(" ".join(cache))
                    break

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
