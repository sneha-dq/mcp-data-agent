from .ollama_service import stream_model_response
from .db_service import run_sql
from utils.helpers import clean_sql
import pandas as pd
import streamlit as st

def query_data_agent(prompt, model):
    instruction = f"""
    You are a Data Agent with access to a PostgreSQL database.
    Translate the following user request into a valid SQL query for PostgreSQL.
    Only return the SQL, no explanations.
    Add prefix 'public.' to all table names.
    Clean the query so that it can be directly executed.

    User request: {prompt}
    """

    sql_query_raw = stream_model_response(model, instruction).strip()
    sql_query = clean_sql(sql_query_raw)

    try:
        return run_sql(sql_query)
    except Exception as e:
        return pd.DataFrame({"Error": [f"Failed SQL:\n{sql_query}\n\n{e}"]})
