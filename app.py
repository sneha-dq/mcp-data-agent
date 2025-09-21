import streamlit as st
from ui.layout import render_sidebar
from services.ollama_service import stream_model_response
from services.agent import query_data_agent

st.set_page_config(page_title="MCP Agent Playground", layout="wide")

model, option = render_sidebar()
user_input = st.text_input("Enter your message:")

if st.button("Submit"):
    st.write("You selected:", option)
    st.write("Your message:", user_input)

    if option == "Chat":
        with st.spinner("Processing..."):
            output = stream_model_response(model, user_input)
        st.success("Done!")

    elif option == "Data Agent":
        with st.spinner("Processing..."):
            df = query_data_agent(user_input, model)
        st.dataframe(df)
        st.success("Done!")

    else:
        st.warning("Invalid option selected.")
