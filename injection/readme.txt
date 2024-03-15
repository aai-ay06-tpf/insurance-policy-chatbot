# To execute the code, please follow the steps below:

1. run `A_download.py` to obtain the PDF files
2. run the `B_....py`: for selecting files that have only one policy in it
3. run the `C_....py`: for selecting files that have grouped policies in it
4. create the docker container for the Qdrant vector database
5. run the `D_....py`: for loading the init feature vectors into the Qdrant vector database



Notas:
1) Además de intalar las dependencias del archivo requirements.txt, instalar el siguiente modelo por consola:
```python -m spacy download es_core_news_sm```