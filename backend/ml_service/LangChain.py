import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils.config import APIKEY_J


#  1. Set env var OPENAI_API_KEY
load_dotenv()
os.environ["OPENAI_API_KEY"] = APIKEY_J


chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)


# DOCS: https://python.langchain.com/docs/use_cases/chatbots/quickstart
chat.invoke(
    [
        HumanMessage(
            content="Translate this sentence from English to French: I love programming."
        )
    ]
)
