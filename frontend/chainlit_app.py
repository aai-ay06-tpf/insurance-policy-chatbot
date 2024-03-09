import chainlit as cl
from ml_service.retrievers import obtain_retrievers
from ml_service.simple_rag import obtain_rag_chain

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
    
    # Values for obtaining the retrievers from the vector database
    collection_name = "sbert_embeddings"
    vdb_name="all_files"
    
    # Retriever
    retriever = obtain_retrievers(vdb_name, collection_name)
    cl.user_session.set("retriever", retriever)
    
    # Chain
    chain = obtain_rag_chain(retriever)
    cl.user_session.set("chain", chain)
    
    msg.content = f"Chat loaded. You can now ask questions!"
    await msg.update()
    


@cl.on_message
async def main(message: cl.Message):
    import sys
    sys.exit(0)
    # Get the user session
    chain = cl.user_session.get("chain")
    
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
