#Write code to create a streamlit page with a input box on top and below it there is a drop down box with 'Chat' as the only value for now, and there is an output box that results in the output
import streamlit as st
import requests
import time
import json

# Ollama server URL
OLLAMA_URL = "http://localhost:11434"

#import ollama and fetch all models registered with ollama
def get_ollama_models():
    response = requests.get(f"{OLLAMA_URL}/api/tags")
    models = [m["name"] for m in response.json()["models"]]
    return models # Extract model names

#create a function that takes the user input, option, selected model and feeds the input to the model using ollama chat command and returns the output
def stream_model_response(model, user_input):
    url = f"{OLLAMA_URL}/api/generate"
    payload = {"model": model, "prompt": user_input, "stream": True}

    response_text = ""
    placeholder = st.empty()   # placeholder for growing output

    with requests.post(url, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                response_text += token
                # update the placeholder instead of creating new widgets
                placeholder.markdown(f"**Output (streaming):**\n\n{response_text}")

    return response_text

st.sidebar.markdown("<div style='margin-top:-40px;font-size:28px;font-weight:bold;'>My AI Playground</div>",
    unsafe_allow_html=True)

with st.sidebar:
    st.divider()

#Create a left collapsible space with a dropdown box named 'Model' with list all all the models installed with ollama
#By default select the first model in the list
with st.sidebar.expander("Change Model", expanded=False):
    model = st.selectbox("Model", get_ollama_models(), index=0)
    st.write(f"Selected model: {model}")

with st.sidebar.expander("Change Option", expanded=False):
    option = st.selectbox("Option", ["Chat"])
    st.write(f"Selected option: {option}")

with st.sidebar:
    st.divider()
    st.markdown(f"> ### You have selected **{option}** with **{model}**")


user_input = st.text_input("Enter your message:")

# Output box
if st.button("Submit"):
    st.write("You selected:", option)
    st.write("Your message:", user_input)
    with st.spinner("Processing..."):
        output = stream_model_response(model, user_input)
    st.success("Done!")





