# MCP Data Agent

This project is a modularized Streamlit application that demonstrates a **Model Context Protocol (MCP)**-based chat and data agent. It refactors a monolithic script into a clean, maintainable, and extensible folder structure, while preserving the original functionality.

## Project Overview

The application provides a simple UI to interact with an AI model via two distinct agents:

* **Chat Agent:** A basic conversational agent that streams responses from a language model.
* **Data Agent:** An agent that translates natural language queries into SQL, executes them against a PostgreSQL database, and displays the results as a Pandas DataFrame.

---

## 📂 Project Structure

```
mcp-data-agent/
├── README.md
├── mcp_chat_data_agent.py      # Main Streamlit application
├── agents/                     # Agent implementations
│   ├── chat_agent.py
│   └── data_agent.py
├── client/                     # External API clients (e.g., Ollama)
│   └── ollama.py
├── core/                       # Core MCP framework components
│   ├── primitives.py           # ModelContext data class
│   └── server.py               # MCPServer for tool registration
├── tools/                      # Reusable tool functions
│   ├── postgres_tool.py
│   └── sql_cleaner.py
└── utils/                      # Utility functions
└── resources.py
├── snapshots/              # Demo images for README
│   ├── DataAgent.png
│   ├── modelSelection.png
│   ├── optionSelection.png
│   └── streamingOutput.png
└── venv/                   # Virtual environment
```

---

## Key Functionalities

* **User Interface:** A Streamlit UI allows users to select a model (from a running Ollama server), choose between a "Chat" and "Data Agent" mode, and submit a query.
* **Conversational AI:** The **Chat Agent** uses the selected model to generate real-time, streaming responses.
* **Natural Language to SQL:** The **Data Agent** takes a user's query about a database and generates a corresponding SQL statement.
* **Database Interaction:** It executes the generated SQL against a PostgreSQL database and presents the output in a tabular format.

***

## MCP Implementation Details

This project provides a true, albeit simplified, implementation of the Model Context Protocol. It captures the essential elements of MCP without relying on external libraries or complex architectural patterns.

* **The `ModelContext` Object:** The core of the protocol is the `ModelContext` class (`core/primitives.py`). This dataclass is the sole source of truth for each interaction. It encapsulates the conversation history, metadata, and (optionally) documents, and is passed with every request to the language model.
* **The `MCPServer`:** The `MCPServer` (`core/server.py`) acts as a central **tool registry**. It doesn't handle the conversation state itself. Instead, its purpose is to register and manage **tools** and **resources** that agents can access. This design cleanly separates the agent's logic from the specific implementations of its capabilities.
* **Tool Registration:** Functions like `query_postgres` and `load_table_schemas` are explicitly registered with the `MCPServer` in `mcp_chat_data_agent.py`. This manual registration makes the dependencies of the agents clear and easy to manage.
* **Agent-Tool Separation:** The `DataAgent` knows it needs to perform a database query, but it doesn't know the specifics of how. It simply calls `server.run_tool("query_postgres", ...)` to delegate the task to the registered tool. This abstraction is a cornerstone of the MCP design, promoting modularity and reusability.

---

## 🛠️ Extensibility

The modular design of this project makes it straightforward to add new functionalities without altering the core framework. This separation of concerns is a direct benefit of the MCP-based architecture.

### **Adding a New Tool**

To add a new tool, like a function to get real-time weather data, follow these steps:

1.  **Create the Tool File:** Create a new Python file in the `tools/` directory (e.g., `weather_tool.py`).
    
2.  **Define the Function:** Inside the file, define your function (e.g., `get_weather_data`). It should take parameters and perform a specific, single task.
    
    Python
    
    ```
    # tools/weather_tool.py
    import requests
    def get_weather_data(city: str):
        # ... logic to call a weather API ...
        # return data
    ```
    
3.  **Register the Tool:** In `mcp_chat_data_agent.py`, import the new tool and register it with the **`MCPServer`**.
    
    Python
    
    ```
    # mcp_chat_data_agent.py
    from tools.weather_tool import get_weather_data
    # ...
    server.register_tool("get_weather", get_weather_data)
    ```
    
    This makes the tool available to any agent.
    

* * *

### **Adding a New Agent**

To add a new agent, such as a "Code Agent" that writes Python code, follow these steps:

1.  **Create the Agent File:** Create a new Python file in the `agents/` directory (e.g., `code_agent.py`).
    
2.  **Define the Agent Class:** Inside the file, define a new class (e.g., `CodeAgent`) that takes the `model` and `server` as inputs.
    
3.  **Implement the `handle` Method:** Implement the `handle` method to define the agent's behavior. It will use the `server.run_tool()` method to access any necessary tools.
    
    Python
    
    ```
    # agents/code_agent.py
    from core.primitives import ModelContext
    from core.server import MCPServer
    class CodeAgent:
        def __init__(self, model, server, call_model_func):
            # ...
        def handle(self, user_input):
            # Formulate the prompt
            # Call the model for a response
            # Use self.server.run_tool('run_python_code', code) if needed
    ```
    
4.  **Integrate with UI:** In `mcp_chat_data_agent.py`, add the new agent as an option in the UI and create the logic to instantiate and run it.
    

* * *

### **Adding a New Server (or Protocol)**

While the current project uses an in-process `MCPServer`, the design allows for easy integration with a separate server if the project were to scale.

- You would replace the `MCPServer` instantiation with a client that connects to an external server's API (e.g., `MCPApiClient('http://localhost:8000')`).
    
- This client would expose the same `register_tool` and `run_tool` methods, but they would internally make API calls to the remote server.
    
This flexibility demonstrates how the MCP provides a robust, future-proof framework for building scalable and maintainable agent-based applications.
---

## 🖼️ Screenshots

### Data Agent UI
![Data Agent](snapshots/DataAgent.png)

### Model Selection
![Model Selection](snapshots/modelSelection.png)

### Option Selection
![Option Selection](snapshots/optionSelection.png)

### Streaming SQL Output
![Streaming Output](snapshots/streamingOutput.png)

---

## ▶️ Getting Started

### 1. Clone Repo
```bash
git clone https://github.com/yourusername/mcp-data-agent.git
cd mcp-data-agent
```

### 2. Create Virtual Env
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
streamlit run mcp_chat_data_agent.py
```

---

## 📌 Roadmap

- [ ] Add authentication & user roles.  
- [ ] Support multiple DB backends simultaneously.  
- [ ] Add natural language **data validation checks** (integration with Great Expectations).  
- [ ] Enable export of generated SQL queries.  
- [ ] Enhance streaming UX (syntax highlighting, query diff).  

---

## 📜 License

This project is licensed under the MIT License.  
See [LICENSE](LICENSE) for details.
