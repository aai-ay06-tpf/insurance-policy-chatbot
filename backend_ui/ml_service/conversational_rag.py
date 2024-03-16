import os
from dotenv import load_dotenv
import ast

from langchain.chains.openai_functions.qa_with_structure import create_qa_with_sources_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory

from ml_service.pdf_vdb import qdrant_retriever

load_dotenv()

def main_chain():
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125", api_key=os.getenv("OPENAI_API_KEY"))

    qa_chain = create_qa_with_sources_chain(llm)

    doc_prompt = PromptTemplate(
        template="Content: {page_content}\nSource: {policy_header}",
        input_variables=["page_content", "policy_header"],
    )

    final_qa_chain = StuffDocumentsChain(
        llm_chain=qa_chain,
        document_variable_name="context",
        document_prompt=doc_prompt,
    )

    # Retriever params
    search_type = "mmr"
    search_kwargs = {"k": 3, "lambda_mult": 0.25}

    # Obtain the retrievers
    pdf_retriever = qdrant_retriever(search_type, search_kwargs)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.\
    Make sure to avoid using any unclear pronouns.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
    condense_question_chain = LLMChain(
        llm=llm,
        prompt=CONDENSE_QUESTION_PROMPT,
    )

    qa = ConversationalRetrievalChain(
        question_generator=condense_question_chain,
        retriever=pdf_retriever,
        memory=memory,
        combine_docs_chain=final_qa_chain,
    )
    
    return qa