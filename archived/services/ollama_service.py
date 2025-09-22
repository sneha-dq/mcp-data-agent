import requests, json
import streamlit as st
from config import OLLAMA_URL

def get_ollama_models():
    response = requests.get(f"{OLLAMA_URL}/api/tags")
    return [m["name"] for m in response.json()["models"]]

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
