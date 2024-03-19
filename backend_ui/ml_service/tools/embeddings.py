"""Doc summary:

The Embedding class presented it conglomerates the different embeddings models that are available.
The class EmbeddingsLabels and EmbeddingsModels are connected to the Embedding class, and they are used to
define the choices of embeddings models that are available.

For adding a new model: 
    - add a new alias and the corresponding model name for the embedding model
    - add the new model to the `create_embeddings` method (add a new return)
    - create the method that invokes the new model at the bottom of the class

Warning: some models require an API key, and also, libraries installed in the environment.

"""

import os
from enum import Enum
from dotenv import load_dotenv


from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from langchain_community.embeddings.cohere import CohereEmbeddings
from langchain_community.embeddings.huggingface import (
    HuggingFaceEmbeddings,
    HuggingFaceBgeEmbeddings,
)


load_dotenv()


# new model: https://platform.openai.com/docs/guides/embeddings/
# text-embedding-3-small and text-embedding-3-large,
class EmbeddingsLabels(Enum):
    ADA = "ada_embeddings"
    GPT4ALL = "gpt4all_embeddings"
    SBERT = "sbert_embeddings"
    COHERE = "cohere_embeddings"
    OPENAI = "openai_embeddings"


class EmbeddingsModels(Enum):
    ADA = "text-embedding-ada-002"
    GPT4ALL = ""
    SBERT = "sentence-transformers/all-MiniLM-L6-v2"
    COHERE = "Cohere/Cohere-embed-multilingual-light-v3.0"
    OPENAI = "text-embedding-3-large"


class Embeddings:

    def __init__(self):
        self._embeddings = [emb_label.value for emb_label in EmbeddingsLabels]
        self._default = self._embeddings[1]
        self._current = self._default

    def get_embeddings(self):
        return self._embeddings

    def get_current(self):
        return self._current

    def set_current(self, emb_label):
        assert (
            emb_label in self._embeddings
        ), f"Invalid embeddings label: {emb_label}, use `get_embeddings()`"
        self._current = emb_label

    def obtain_embeddings(self, emb_label=None):
        try:
            result = self.create_embeddings(emb_label)
            return result
        except Exception as e:
            print(f"Error creating the embedding model: {e}")
            return None

    def create_embeddings(self, emb_label=None):
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
        elif self._current == EmbeddingsLabels.OPENAI.value:
            return self.openai_embeddings()
        else:
            raise ValueError(
                f"Invalid embeddings label: {emb_label}, use `set_current`"
            )

    def ada_embeddings(self):
        return OpenAIEmbeddings(
            model=EmbeddingsModels.ADA.value, api_key=os.getenv("OPENAI_API_KEY")
        )

    def gpt4all_embeddings(self):
        return GPT4AllEmbeddings()

    def sbert_embeddings(self):
        return HuggingFaceEmbeddings(
            model_name=EmbeddingsModels.SBERT.value, model_kwargs={"device": "cpu"}
        )

    def cohere_embeddings(self):
        return CohereEmbeddings(
            model=EmbeddingsModels.COHERE.value,
            cohere_api_key=os.getenv("COHERE_API_KEY"),
        )

    def openai_embeddings(self):
        return OpenAIEmbeddings(
            model=EmbeddingsModels.OPENAI.value, api_key=os.getenv("OPENAI_API_KEY")
        )
