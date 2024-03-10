import os
from dotenv import load_dotenv

from langchain.chains.llm import LLMChain
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.cohere import Cohere


load_dotenv()


prompt_template = """
[BOS] 
Debes contestar la pregunta al gerente de la empresa de pólizas de seguros.
Utiliza el siguiente contexto para formular la respuesta:

{context}

### PREGUNTA:
{question} 

[EOS]
 """

from langchain_openai import ChatOpenAI

def obtain_rag_chain(retriever):
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )
    
    # llm = Cohere(
    #     model="command",
    #     cohere_api_key=os.getenv("COHERE_API_KEY"),
    #     temperature=0.33
    # )
    
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.1
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | llm_chain
    )

    return rag_chain


if __name__ == "__main__":
    from ml_service.retrievers import obtain_feature_file_retrievers
    
    retriever = obtain_feature_file_retrievers(vdb_name="", collection_name="")
    
    chain_llm = obtain_rag_chain(retriever)
    
    chain_llm.invoke("recomendame un articulo para hacer crecer el pelo")
    
