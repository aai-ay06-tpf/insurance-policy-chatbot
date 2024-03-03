import os
from enum import Enum
from dotenv import load_dotenv


from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from langchain_community.embeddings.cohere import CohereEmbeddings
from langchain_community.embeddings.huggingface import (
    HuggingFaceEmbeddings, HuggingFaceBgeEmbeddings
)


load_dotenv()


class EmbeddingsLabels(Enum):
    ADA = "ada_embeddings"
    GPT4ALL = "gpt4all_embeddings"
    SBERT = "sbert_embeddings"
    COHERE = "cohere_embeddings"


class EmbeddingsModels(Enum):
    ADA = "text-embedding-ada-002"
    GPT4ALL = ""
    SBERT = "sentence-transformers/all-MiniLM-L6-v2"
    COHERE = "Cohere/Cohere-embed-multilingual-light-v3.0"


class Embeddings():

    def __init__(self):
        self._embeddings = [emb_label.value for emb_label in EmbeddingsLabels]
        self._default = self._embeddings[1]
        self._current = self._default

    def get_embeddings(self):
        return self._embeddings

    def get_current(self):
        return self._current

    def set_current(self, emb_label):
        assert emb_label in self._embeddings, f"Invalid embeddings label: {emb_label}, use `get_embeddings()`"
        self._current = emb_label

    def obtain_embeddings(self, emb_label=None):

        if emb_label is not None:
            self.set_current(emb_label)

        if self._current == EmbeddingsLabels.ADA.value:
            return self.ada_embeddings()
        elif self._current == EmbeddingsLabels.GPT4ALL.value:
            return self.gpt4all_embeddings()
        elif self._current == EmbeddingsLabels.SBERT.value:
            return self.sbert_embeddings()
        elif self._current == EmbeddingsLabels.COHERE.value:
            return self.cohere_embeddings()
        else:
            raise ValueError(
                f"Invalid embeddings label: {emb_label}, use `set_current`")

    def ada_embeddings(self):
        return OpenAIEmbeddings(
            model=EmbeddingsModels.ADA.value,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def gpt4all_embeddings(self):
        return GPT4AllEmbeddings()

    def sbert_embeddings(self):
        return HuggingFaceEmbeddings(
            model_name=EmbeddingsModels.SBERT.value,
            model_kwargs={"device": "cpu"}
        )

    def cohere_embeddings(self):
        return CohereEmbeddings(
            model=EmbeddingsModels.COHERE.value,
            cohere_api_key=os.getenv("COHERE_API_KEY")
        )
