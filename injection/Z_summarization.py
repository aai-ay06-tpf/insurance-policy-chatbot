import os
from dotenv import load_dotenv
import pickle, time

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.pdf import PyPDFLoader

from utils.config import DOWNLOAD_PATH

load_dotenv()

pdf_files = os.listdir(DOWNLOAD_PATH)

# for file in pdf_files:
selected_file = os.path.join(DOWNLOAD_PATH, pdf_files[0])

loader = PyPDFLoader(selected_file)
pages = loader.load()


# Define prompt
prompt_template = """Extraer los bullet-points de los articulos\
 contenidos en el TEXTO. La respuesta debe ser de 1000 caracteres como maximo.
TEXTO:
"{text}"
RESUMEN:"""
prompt = PromptTemplate.from_template(prompt_template)

# Define LLM chain
llm = ChatOpenAI(
    temperature=0, model_name="gpt-3.5-turbo-16k", api_key=os.getenv("OPENAI_API_KEY")
)
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Define StuffDocumentsChain
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")


docs = loader.load()

if False:

    response = stuff_chain.invoke([docs[0]])

    with open(f".summarization_backup/response_{int(time.time())}.pkl", "wb") as f:
        pickle.dump(response, f)

    print("\nDone!\n")

else:
    print("\nNot executed\n")
