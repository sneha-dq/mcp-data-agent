#Write code to create a streamlit page with a input box on top and below it there is a drop down box with 'Chat' as the only value for now, and there is an output box that results in the output
import streamlit as st
import requests
import time
import json
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
import re

# Ollama server URL
OLLAMA_URL = "http://localhost:11434"

# PostgreSQL connection string (update with your creds)
PG_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/others"
engine = create_engine(PG_URI)

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

# Data agent
def query_data_agent(prompt, model):
    # Step 1: Ask Ollama to generate SQL
    instruction = f"""
    You are a Data Agent with access to a PostgreSQL database.
    Translate the following user request into a valid SQL query for PostgreSQL.
    Only return the SQL, no explanations.
    Add prefix 'public.' to all table names.
    Clean the query so that it can be directly fed to the sql execution engine.

    User request: {prompt}
    """
    sql_query_raw = stream_model_response(model, instruction).strip()
    sql_query = clean_sql(sql_query_raw)

    print(sql_query)

    # Step 2: Run SQL on Postgres
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            #print(result)
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            #print(df)
            return df
    except Exception as e:
        return pd.DataFrame({"Error": [f"Failed to execute SQL:\n{sql_query}\n\n{e}"]})

def clean_sql(sql_text):
    # Remove ```sql and ``` code fences
    sql_text = re.sub(r"```(?:sql)?", "", sql_text, flags=re.IGNORECASE)
    # Remove SQL comments starting with --
    sql_text = "\n".join(
        line for line in sql_text.splitlines() if not line.strip().startswith("--")
    )
    # Strip leading/trailing whitespace
    return sql_text.strip()

st.sidebar.markdown("<div style='margin-top:-40px;font-size:28px;font-weight:bold;'>My Agentic-AI Playground</div>",
    unsafe_allow_html=True)

with st.sidebar:
    st.divider()

#Create a left collapsible space with a dropdown box named 'Model' with list all all the models installed with ollama
#By default select the first model in the list
with st.sidebar.expander("Change Model", expanded=False):
    model = st.selectbox("Model", get_ollama_models(), index=0)
    st.write(f"Selected model: {model}")

with st.sidebar.expander("Change Option", expanded=False):
    option = st.selectbox("Option", ["Chat","Data Agent"], index=0)
    st.write(f"Selected option: {option}")

with st.sidebar:
    st.divider()
    st.markdown(f"> ### You have selected **{option}** with **{model}**")


user_input = st.text_input("Enter your message:")

# Output box
if st.button("Submit"):
    st.write("You selected:", option)
    st.write("Your message:", user_input)
    if option == "Chat":
        with st.spinner("Processing..."):
            output = stream_model_response(model, user_input)
        st.success("Done!")
    elif option == "Data Agent":
        with st.spinner("Processing..."):
            output = query_data_agent(user_input, model)
        st.dataframe(output) 
        st.success("Done!")
    else:
        st.warning("Invalid option selected.")
