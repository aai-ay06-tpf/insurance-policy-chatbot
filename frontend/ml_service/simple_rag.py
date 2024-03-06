import os
from dotenv import load_dotenv

from langchain.chains.llm import LLMChain
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.cohere import Cohere

from ml_service.retrievers import obtain_retrievers


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


def obtain_rag_chain(retriever):
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
    )
    
    llm = Cohere(
        model="command",
        cohere_api_key=os.getenv("COHERE_API_KEY"),
        temperature=0.33
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | llm_chain
    )

    return rag_chain
