import os
from ast import literal_eval
import chainlit as cl
from agent import create_agent




chat_history = []
def _chat_history(result):
    global chat_history
    chat_history.extend([(result["input"], result["output"])])
    return chat_history


@cl.on_chat_start
async def init():

    msg = cl.Message(content=f"Processing chat components…")
    await msg.send()

    # Agent
    agent = create_agent()
    cl.user_session.set("agent", agent)

    msg.content = f"Chat loaded. You can now ask questions!"
    await msg.update()


@cl.on_message
async def main(message: cl.Message):
    global chat_history
    
    # Get the user session
    agent = cl.user_session.get("agent")

    # Make the prediction
    result = agent.invoke({"input": message.content, "chat_history": chat_history})
    chat_history = _chat_history(result)
    answer = result.get("output")

    
    # # Embed the answer in a message with the sources metadata
    source_links = []
    source_elements = []
    try:
        for tool in result["intermediate_steps"]:
            source_link = tool[0].tool + "_link"
            source_links.append(source_link)
            source_elements.append(
                cl.Text(content=tool[1], name=source_link)
            )
    except:
        raise Exception("Error al obtener las fuentes")


    if source_links:
        answer += f"\n\nSources: {', '.join(source_links)}"


    # Send a response back to the user
    msg = cl.Message(content=answer, elements=source_elements)
    await msg.send()


# `cd frontend`
# `chainlit run chainlit_app.py -w`
# The -w flag tells Chainlit to enable auto-reloading, so you don’t need to restart the server every time you make changes to your application
