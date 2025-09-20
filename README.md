# My AI Playground (Streamlit + Ollama)

This project creates a **Streamlit-based web interface** to interact with locally hosted **Ollama models**.  
It allows you to enter a prompt, select a model, and stream the response in real time.  

---

## 🚀 Features
- **Input box** for user messages  
- **Dropdown menu** (currently only `Chat`) for future extensibility  
- **Model selection** from all Ollama models installed locally  
- **Streaming responses** displayed dynamically in an output box  
- **Sidebar configuration panel** with collapsible sections  

---

## 📦 Requirements

- Python 3.9+  
- [Streamlit](https://streamlit.io)  
- [Ollama](https://ollama.ai) running locally  
- Dependencies:  

```bash
pip install streamlit requests
```

---

## ▶️ How to Run

1. **Start the Ollama server** (default port `11434`):  
   ```bash
   ollama serve
   ```

2. **Run the Streamlit app**:  
   ```bash
   streamlit run app.py
   ```
   (Replace `app.py` with your script filename.)

3. Open your browser at [http://localhost:8501](http://localhost:8501).

---

## 🛠️ Code Overview

- **`get_ollama_models()`** → Fetches all available Ollama models via `/api/tags`.  
- **`stream_model_response()`** → Streams model responses token by token using `/api/generate`.  
- **Sidebar** → Lets you select:
  - Installed Ollama model  
  - Option (`Chat` only for now, extensible in future)  
- **Main panel** → Input text box + streaming output display.  

---

## 📷 UI Layout

- **Sidebar**
  - Project title (`My AI Playground`)
  - Model selection dropdown
  - Option selection dropdown
  - Current selection summary
- **Main Area**
  - Input text box (`Enter your message:`)
  - Submit button
  - Streaming output box showing model response

---

## 📝 Example Usage

1. Select a model from **Change Model** (e.g., `llama2`).  
2. Type a prompt like:  

   ```
   Explain quantum computing in simple terms.
   ```

3. Click **Submit**.  
4. Watch the response stream live in the output box.  

---
## 📷  Snapshots
Snapshots are placed in the Snapshots folder
![Streaming Output](snapshots/streamingOutput.png)  
*Streaming Response from Model*

![Model Selection](snapshots/modelSelection.png)  
*Ability to change Model*

---
## 🔮 Future Enhancements
- Add more options beyond "Chat" (e.g., "Summarize", "Translate" or Agents).  
- Support multi-turn conversations with memory.  
- Save/export chat history.  
- Theme customization for better UX.  

---

## 📄 License
MIT License. Free to use and modify.  
