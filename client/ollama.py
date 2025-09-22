import requests
from typing import Optional, Iterator
import json
from core.primitives import ModelContext

OLLAMA_URL = "http://localhost:11434"

def get_ollama_models():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        response.raise_for_status()
        models = [m["name"] for m in response.json()["models"]]
        return models
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return ["No models available"]

def call_model(model: str, prompt: str, ctx: Optional[ModelContext] = None) -> Iterator[str]:
    url = f"{OLLAMA_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,  # This tells Ollama to stream the response
        "mcp": ctx.to_mcp_payload() if ctx else {},
    }
    
    # Use 'stream=True' with requests.post to handle the response content in chunks
    r = requests.post(url, json=payload, stream=True)
    r.raise_for_status()

    # Iterate through each line of the streamed response
    for line in r.iter_lines():
        if line:
            try:
                # Decode the line, which is a single JSON object
                json_data = json.loads(line.decode('utf-8'))
                # Extract and yield the 'response' field
                response_text = json_data.get("response", "")
                yield response_text
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue