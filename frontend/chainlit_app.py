import pickle, os
from itertools import count
import chainlit as cl
from langchain.chains import RetrievalQA
from langchain_community.llms.llamacpp import LlamaCpp
from utils.config import RETRIEVER_PATH, SERVICE_PATH


@cl.on_chat_start
async def init():
    
    msg = cl.Message(content=f"Processing chat components…")
    await msg.send()
    
    with open(RETRIEVER_PATH, 'rb') as f:
        retriever = pickle.load(f)
        
    cl.user_session.set("retriever", retriever)
    
    model_path = "chainlit_rag/zephyr-7b-beta.Q4_K_M.gguf"
    llm = LlamaCpp(
        streaming=True,
        model_path=model_path,
        max_tokens=1000,
        temperature=0.2,
        top_p=1,
        gpu_layers=0,
        stream=True,
        verbose=True,
        n_threads=os.cpu_count()//2,
        n_ctx=4096
    )
    
    chain = RetrievalQA.from_chain_type(
        llm = llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        #TODO: callbacks
    )
    
    cl.user_session.set("chain", chain)
    
    msg.content = f"Chat loaded. You can now ask questions!"
    await msg.update()
    


## Please remove this:
# create history directory
if not os.path.exists('history'):
    os.makedirs('history')
HISTORY_PATH = os.path.join(SERVICE_PATH, 'history')
h_count = count(1)


@cl.on_message
async def main(message: cl.Message):
    
    # backup of the message
    idh = f"{next(h_count):02}"
    path = os.path.join(HISTORY_PATH, f"message_{idh}.pkl")
    with open(path, "wb") as f:
        pickle.dump(message, f)
    
    # Get the user session
    chain = cl.user_session.get("chain")
    
    # Make the prediction
    response = await chain.ainvoke(message.content)
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
