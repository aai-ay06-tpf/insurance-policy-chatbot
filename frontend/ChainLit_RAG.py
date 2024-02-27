# REVISAR: https://medium.aiplanet.com/implementing-rag-using-langchain-ollama-and-chainlit-on-windows-using-wsl-92d14472f15d
# langchain.llms.Ollama
# langchain.chains RetrievalQA, RetrievalQAWithSourcesChain


import chainlit as cl


# The main function will be called every time a user inputs
# a message in the chatbot UI. 
@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()
    
    
# `cd frontend`
# `chainlit run ChainLit_RAG.py -w`
# The -w flag tells Chainlit to enable auto-reloading, so you don’t need to restart the server every time you make changes to your application
