from typing import Dict, List, Tuple

from langchain.agents import (
    AgentExecutor,
    Tool,
)
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

from langchain_community.vectorstores.qdrant import Qdrant
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.tools.convert_to_openai import format_tool_to_openai_function
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel
from langchain_core.tools import BaseTool
from langchain.tools.retriever import create_retriever_tool



from ml_service.pdf_vdb import qdrant_retriever as pdf_qdrant_retriever
from ml_service.web_scrapper import parent_document_retriever, qdrant_retriever
from ml_service.tools.embeddings import Embeddings


emb = Embeddings()
embeddings = emb.obtain_embeddings('openai_embeddings')


# Retriever params
search_type="mmr"
search_kwargs={'k': 3, 'lambda_mult': 0.25}


# web scrapper params
searchs = [
    ("codigo_de_comercio", [524, 525, 526]),#, 538]),
    ("companias_de_seguros", [3, 10, 36]),
    ("protocolo_seguridad_sanitaria", [18]),
    ("codigo_sanitario", [112]),
    ("codigo_penal", [470])
]

# Obtain the retrievers
pdf_retriever = pdf_qdrant_retriever(search_type, search_kwargs)
web_retriever = qdrant_retriever(searchs, search_type, search_kwargs)



pdf_tool = create_retriever_tool(
    retriever=pdf_retriever,
    name="feature_init_pdf",
    description="Busca y devuelve indices de polizas de seguros o el encabezado de los articulos.",
)


web_tool = create_retriever_tool(
    retriever=web_retriever,
    name="webscrapper_codigo_chile",
    description="Busca y devuelve extractos de los codigos de ley de la constitucion de Chile.",
)



ALL_TOOLS: List[BaseTool] = [pdf_tool, web_tool]

# turn tools into documents for indexing
tool_docs = [
    Document(page_content=t.description, metadata={"index": i})
    for i, t in enumerate(ALL_TOOLS)
]


vectorstore = Qdrant.from_documents(
    tool_docs,
    embeddings,
    location=":memory:",
    collection_name="agent_tools_documents",
)
retriever = vectorstore.as_retriever()


def get_tools(query: str) -> List[Tool]:
    docs = retriever.get_relevant_documents(query)
    return [ALL_TOOLS[d.metadata["index"]] for d in docs]


assistant_system_message = """Eres un asistente asesor para una compañia de seguros. \
Usa la tool 'webscrapper_codigo_chile' solo si se especifica una busqueda relacionada a aspectos legales.
La tool 'feature_init_pdf' es la herramienta principal para identificar polizas o articulos de polizas.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", assistant_system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


def llm_with_tools(input: Dict) -> Runnable:
    return RunnableLambda(lambda x: x["input"]) | ChatOpenAI(temperature=0).bind(
        functions=input["functions"]
    )


def _format_chat_history(chat_history: List[Tuple[str, str]]):
    buffer = []
    for human, ai in chat_history:
        buffer.append(HumanMessage(content=human))
        buffer.append(AIMessage(content=ai))
    return buffer


agent = (
    RunnableParallel(
        {
            "input": lambda x: x["input"],
            "chat_history": lambda x: _format_chat_history(x["chat_history"]),
            "agent_scratchpad": lambda x: format_to_openai_functions(
                x["intermediate_steps"]
            ),
            "functions": lambda x: [
                format_tool_to_openai_function(tool) for tool in get_tools(x["input"])
            ],
        }
    )
    | {
        "input": prompt,
        "functions": lambda x: x["functions"],
    }
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

# LLM chain consisting of the LLM and a prompt


class AgentInput(BaseModel):
    input: str
    chat_history: List[Tuple[str, str]] = Field(
        ..., extra={"widget": {"type": "chat", "input": "input", "output": "output"}}
    )


agent_executor = AgentExecutor(agent=agent, tools=ALL_TOOLS).with_types(
    input_type=AgentInput
)
