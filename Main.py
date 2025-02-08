import sqlalchemy
import ollama
import json
import gradio as gr

from Chat import Company_Chatbot

ChatBot = Company_Chatbot()

#Select theme for the interface
Theme = "ocean"

with gr.Blocks(theme = Theme) as ui:
    #Heading on the page
    gr.Markdown("# SQL Data Retriever")
    
    with gr.Row():
        #Select llm model
        LLM = gr.Dropdown(["llama3.2","llama3.1"],value = "llama3.2",label = "Select Model")

    #Main chatbot interface
    chat = gr.ChatInterface(
        ChatBot.chat_func,
        type="messages",
        chatbot=gr.Chatbot(height=500,type="messages"),
        textbox=gr.Textbox(placeholder="Enter Natural Language Query", container=False, scale=7),
        theme=Theme,
        additional_inputs = [LLM]
    )
#launch the website locally. share = True will host the website locally for 72 hours
ui.launch(inbrowser = True,share = False)