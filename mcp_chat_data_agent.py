"""
Main entry point for the Streamlit application.
Initializes the MCP server, agents, and runs the UI.
"""

import streamlit as st

from core.server import MCPServer
from core.primitives import ModelContext
from tools.postgres_tool import query_postgres
from tools.sql_cleaner import clean_sql
from agents.chat_agent import ChatAgent
from agents.data_agent import DataAgent
from client.ollama import get_ollama_models, call_model
from utils.resources import load_table_schemas

# ---------------------- Streamlit UI ----------------------

# 1. Initialize Server and Resources
server = MCPServer()
server.register_resource("table_schemas", load_table_schemas())
server.register_tool("query_postgres", query_postgres)

# 2. UI Configuration and Inputs
st.sidebar.markdown(
    "<div style='margin-top:-40px;font-size:28px;font-weight:bold;'>My MCP Playground</div>",
    unsafe_allow_html=True,
)
with st.sidebar:
    st.divider()

with st.sidebar.expander("Change Model", expanded=False):
    model = st.selectbox("Model", get_ollama_models(), index=0)
    st.write(f"Selected model: {model}")

with st.sidebar.expander("Change Option", expanded=False):
    option = st.selectbox("Option", ["Chat", "Data Agent"], index=0)
    st.write(f"Selected option: {option}")

with st.sidebar:
    st.divider()
    st.markdown(f"> ### You have selected **{option}** with **{model}**")

user_input = st.text_input("Enter your message:")

# 3. Main Logic
if st.button("Submit"):
    st.write("You selected:", option)
    st.write("Your message:", user_input)

    if option == "Chat":
        with st.spinner("Processing..."):
            agent = ChatAgent(model, server, call_model_func=call_model)
            response_container = st.empty()
            full_response = ""
            for text_chunk in agent.handle(user_input):
                full_response += text_chunk
                response_container.markdown(full_response + "▌")
            response_container.markdown(full_response)
        #st.write(output)
        st.success("Task Completed!")

    elif option == "Data Agent":
        with st.spinner("Processing..."):
            agent = DataAgent(model, server, call_model_func=call_model, clean_sql_func=clean_sql)
            output = agent.handle(user_input)
        st.dataframe(output)
        st.success("Task Completed!")