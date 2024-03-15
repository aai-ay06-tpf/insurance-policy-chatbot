import os
import ast


import chainlit as cl
from ml_service.conversational_rag import main_chain


# @cl.password_auth_callback
# def auth_callback(username: str, password: str):
#     # Fetch the user matching username from your database
#     # and compare the hashed password with the value stored in the database
#     if (username, password) == ("admin", "admin"):
#         return cl.User(
#             identifier="admin", metadata={"role": "admin", "provider": "credentials"}
#         )
#     else:
#         return None


@cl.on_chat_start
async def init():

    msg = cl.Message(content=f"Processing chat components…")
    await msg.send()

    # Chain
    chain = main_chain()
    cl.user_session.set("chain", chain)

    msg.content = f"Chat loaded. You can now ask questions!"
    await msg.update()


@cl.on_message
async def main(message: cl.Message):

    # Get the user session
    chain = cl.user_session.get("chain")

    # Make the prediction
    response = chain.invoke({"question": message.content})
    result = ast.literal_eval(response["answer"])
    answer = result.get("answer")
    sources = result.get("sources")

    # # Embed the answer in a message with the sources metadata
    # sources_found = []
    # sources_elements = []
    # if sources:#TODO: def obtain_sources_elements(sources)
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
