import os
import ast


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

    # Chain
    agent = create_agent()
    cl.user_session.set("agent", agent)

    msg.content = f"Chat loaded. You can now ask questions!"
    await msg.update()


@cl.on_message
async def main(message: cl.Message):
    global chat_history
    
    # Get the user session
    agent = cl.user_session.get("agent")

    if len(chat_history) != 0:
        optmizar_el_prompt_del_user_con_el_chat_history = None
    
    # Make the prediction
    result = agent.invoke({"input": message.content, "chat_history": chat_history})
    chat_history = _chat_history(result)
    answer = result.get("output")
    tool = result["intermediate_steps"][0][0].tool
    source = result["intermediate_steps"][0][1]

    # # Embed the answer in a message with the sources metadata
    # sources_found = []
    # sources_elements = []
    # if sources:
    #     for source in sources:
    #         try:
    #             source_name = sources.metadata["source"]
    #         except:
    #             source_name = "<Unknown>"
    #         content = source.page_content
    #         sources_found.append(source_name)
    #         sources_elements.append(cl.Text(
    #             content=content,
    #             name=source_name
    #         ))
    # if sources_found:
    #     answer += f"\n\nSources: {', '.join(sources_found)}"
    # else:
    #     answer += "\n\nNo sources found."

    # Send a response back to the user
    msg = cl.Message(content=answer)#, elements=sources)
    await msg.send()


# `cd frontend`
# `chainlit run chainlit_app.py -w`
# The -w flag tells Chainlit to enable auto-reloading, so you don’t need to restart the server every time you make changes to your application
