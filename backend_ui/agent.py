import os
from typing import Dict, List, Tuple
from langchain.agents.agent import Agent
from langchain.agents import (
    AgentExecutor,
    Tool,
)
from langchain.agents.format_scratchpad.openai_functions import (
    format_to_openai_function_messages,
)
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

from langchain_community.vectorstores.qdrant import Qdrant
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel
from langchain_core.tools import BaseTool

from ml_service.agent_tools import (
    content_feature_tool,
    policy_feature_tool,
    article_feature_tool,
    web_news_tool,
    retriever_tool_constitucion_chile,
)
from ml_service.tools.embeddings import Embeddings

content_tool = content_feature_tool()
pol_tool = policy_feature_tool()
news_tool = web_news_tool()
cl_constit_tool = retriever_tool_constitucion_chile()


def create_agent():
    # TOOLS AND RETRIEVER TOOLS SET UP
    ALL_TOOLS: List[BaseTool] = [content_tool, pol_tool, news_tool, cl_constit_tool]

    tool_docs = [
        Document(page_content=t.description, metadata={"index": i})
        for i, t in enumerate(ALL_TOOLS)
    ]

    emb = Embeddings()
    embeddings = emb.obtain_embeddings("openai_embeddings")

    vectorstore = Qdrant.from_documents(
        tool_docs,
        embeddings,
        location=":memory:",
        collection_name="agent_tools_documents",
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def get_tools(query: str) -> List[Tool]:
        docs = retriever.get_relevant_documents(query)
        return [ALL_TOOLS[d.metadata["index"]] for d in docs]

    # PROMPT SET UP
    assistant_system_message = """Eres un asistente asesor para una compañia de seguros.\
    Usa la tool 'policy_feature' para adquirir contexto básico de cada poliza.\
    La tool 'content_feature' devuelve el articulo completo para desarrollar respuestas.\
    La tool 'web_news' devuelve noticias, filtrar por 'date' para que sean recientes, sino la respuesta debe ser 'No hay noticias disponibles'."\
    'cl_constit_tool' informacion legal respecto a las leyes de Chile.\
    Desarrollar la respuesta en formato bullet points.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", assistant_system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # AGENT SET UP

    llm = ChatOpenAI(
        temperature=0.0, model="gpt-3.5-turbo-0125", api_key=os.getenv("OPENAI_API_KEY"),
    )

    def llm_with_tools(input: Dict) -> Runnable:
        return RunnableLambda(lambda x: x["input"]) | llm.bind_functions(
            input["functions"]
        )

    def _format_chat_history(chat_history: List[Tuple[str, str]]):
        buffer = []
        for human, ai in chat_history:
            buffer.append(HumanMessage(content=human))
            buffer.append(AIMessage(content=ai))
        return buffer

    # LCEL Agent
    agent = (
        RunnableParallel(
            {
                "input": lambda x: x["input"],
                "chat_history": lambda x: _format_chat_history(x["chat_history"]),
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
                "functions": lambda x: [
                    convert_to_openai_function(tool) for tool in get_tools(x["input"])
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

    agent_executor = AgentExecutor(
        agent=agent, tools=ALL_TOOLS, return_intermediate_steps=True
    )

    return agent_executor
