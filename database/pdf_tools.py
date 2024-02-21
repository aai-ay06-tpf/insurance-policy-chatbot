import os, re
from pypdf import PdfReader
from config import DOWNLOAD_PATH

##TODO: remove from here
pdf_files = [os.path.join(DOWNLOAD_PATH, file) for file in os.listdir(DOWNLOAD_PATH) if file.endswith('.pdf')]


def extract_text(pdf_files: list) -> dict:
    # PDF files data extraction
    extractions_dict = {}
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        text = ''.join([page.extract_text() for page in reader.pages])
        extractions_dict[os.path.basename(pdf_file)] = {"text": text}
    
    return extractions_dict


def extract_annotations(pdf_files: list) -> dict:
    # PDF files annotations extraction
    extractions_dict = {}
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        annotations_list = []

        for page in reader.pages:
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    obj = annot.get_object()
                    annotation = {"subtype": obj["/Subtype"], "location": obj["/Rect"]}
                    annotations_list.append(annotation)

        extractions_dict[os.path.basename(pdf_file)] = annotations_list

    return extractions_dict


def extract_unique_characters(pdf_files: list) -> dict:
    # PDF files data extraction
    extractions_dict = {}
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        text = ''.join([page.extract_text() for page in reader.pages])
        characteristics = {"characters": sorted(set(text))}
        extractions_dict[os.path.basename(pdf_file)] = characteristics
        
    return extractions_dict


def extract_uppercase_lines(pdf_files: list) -> dict:
    # PDF files data extraction
    extractions_dict = {}
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        characteristics = {"uppercase_lines": []}

        for page in reader.pages:
            text = page.extract_text()

            # Obtain the uppercase lines in the text
            uppercase_lines = [line.strip() for line in text.split("\n") if line.isupper()]
            characteristics["uppercase_lines"].extend(uppercase_lines)

        # Results storage
        extractions_dict[os.path.basename(pdf_file)] = characteristics
        
    return extractions_dict


def count_patterns(pdf_files: list, pattern: str, normalize: bool=False) -> dict:
    # WARNING: Case Sensitive
    extraction_dict = {}
    for pdf_file in pdf_files:
        characteristics = {}
        reader = PdfReader(pdf_file)
        text = ''.join([page.extract_text() for page in reader.pages])
        if normalize:
            text = text.lower()
            pattern = pattern.lower()
        matches = re.findall(r'\b' + pattern + r'\b', text)
        characteristics[f"count_{pattern}"] = len(matches)
        extraction_dict[os.path.basename(pdf_file)] = characteristics
    
    return extraction_dict
    

def count_pages(pdf_files: list) -> dict:
    # PDF files pages count
    extractions_dict = {}
    for pdf_file in pdf_files:
        characteristics = {}
        reader = PdfReader(pdf_file)
        characteristics["pages"] = len(reader.pages)
        extractions_dict[os.path.basename(pdf_file)] = characteristics
    
    return extractions_dict


def extract_images(pdf_files: list) -> dict:
    # Untested - generated by IA 
    # PDF files images extraction
    extractions_dict = {}
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        images = []

        for page in reader.pages:
            if "/XObject" in page:
                for obj in page["/XObject"]:
                    if page["/XObject"][obj]["/Subtype"] == "/Image":
                        images.append(page["/XObject"][obj])

        # Results storage
        extractions_dict[os.path.basename(pdf_file)] = images
    
    return extractions_dict


if __name__ == "__main__":

    extract_text([pdf_files[0]])