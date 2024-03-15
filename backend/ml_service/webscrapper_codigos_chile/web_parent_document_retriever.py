from langchain_community.vectorstores.chroma import Chroma
from langchain.retrievers.parent_document_retriever import ParentDocumentRetriever
from langchain.storage import InMemoryStore
from langchain_text_splitters.character import CharacterTextSplitter, RecursiveCharacterTextSplitter
# from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters.base import TextSplitter

from ml_service.tools.embeddings import Embeddings

def obtain_parentdocument_retriever(docs):
    
    print("doesn't work: TypeError: Can't instantiate abstract class TextSplitter with abstract method split_text")

    # child_splitter = CharacterTextSplitter(
    child_splitter = TextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=20
    )#.split_documents(documents=docs)

    emb = Embeddings()
    embeddings = emb.obtain_embeddings("ada_embeddings")

    # The vectorstore to use to index the child chunks
    vectorstore = Chroma(
        collection_name="all_documents", embedding_function=embeddings
    )

    # It should create documents smaller than the parent
    # child_splitter = RecursiveCharacterTextSplitter(chunk_size=75, chunk_overlap=0)# , add_start_index=True)

    # The storage layer for the parent documents
    store = InMemoryStore()
    pd_retriever = ParentDocumentRetriever(
        vectorstore=vectorstore,
        docstore=store,
        child_splitter=child_splitter,
    )

    return pd_retriever