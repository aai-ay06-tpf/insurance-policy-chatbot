import os

import chainlit as cl

from utils.config import QDRANT_LOCAL_PATH

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


@cl.on_chat_start
async def init():
    
    msg = cl.Message(content=f"Processing chat components…")
    await msg.send()
    
    embedding_name = "sbert_embeddings"
    
    files_ = [element for element in os.listdir(QDRANT_LOCAL_PATH) if (element.startswith("all") and element.endswith(embedding_name))]
    articles_ = [element for element in os.listdir(QDRANT_LOCAL_PATH) if (element.startswith("POL") and element.endswith(embedding_name))]
    
    # Retriever
    file_retriever = files_lotr_retriever(collection_names=files_)
    article_retriever = articles_lotr_retriever(collection_names=articles_)
    cl.user_session.set("file_retriever", file_retriever)
    cl.user_session.set("article_retriever", article_retriever)
    
    
    
    # Chain
    chain = obtain_rag_chain(article_retriever)
    cl.user_session.set("chain", chain)
    
    msg.content = f"Chat loaded. You can now ask questions!"
    await msg.update()
    


@cl.on_message
async def main(message: cl.Message):

    # Get the user session
    chain = cl.user_session.get("chain")
    file_retriever = cl.user_session.get("file_retriever")
    article_retriever = cl.user_session.get("article_retriever")
    
    # ejecutar el file retriever con invoke en el message
    
    # ejecutar el article retriever con invoke en el message
    
    # filtrar los articles por el top match del file
    
    # enviar los matches por pantalla al usuario con un hardcoded input
    
    # interpretar la segunda respuesta del user para ejecutar el modelo
    #TODO: la conversión debe poder reiniciarse en este punto.
    
    
    # Make the prediction
    response = await chain.ainvoke(input=message.content)
    answer = response.get("result")
    sources = response.get("source_documents")
    
    #TODO: El historial de conversacion debe actualizarse
    
    
    # Embed the answer in a message with the sources metadata
    sources_found = []
    sources_elements = []
    if sources:#TODO: def obtain_sources_elements(sources)
        for source in sources:
            try:
                source_name = sources.metadata["source"]
            except:
                source_name = "<Unknown>"
            content = source.page_content
            sources_found.append(source_name)
            sources_elements.append(cl.Text(
                content=content,
                name=source_name
            ))
    if sources_found:
        answer += f"\n\nSources: {', '.join(sources_found)}"
    else:
        answer += "\n\nNo sources found."
            
     
    # Send a response back to the user
    await cl.Message(
        content=answer,
        elements=sources_elements
    ).send()
    
    
# `cd frontend`
# `chainlit run chainlit_app.py -w`
# The -w flag tells Chainlit to enable auto-reloading, so you don’t need to restart the server every time you make changes to your application
