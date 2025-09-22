import json
import pandas as pd
import time
import streamlit as st  # Import streamlit
from core.primitives import ModelContext
from core.server import MCPServer

class DataAgent:
    def __init__(self, model: str, server: MCPServer, call_model_func, clean_sql_func):
        self.model = model
        self.server = server
        self.call_model_func = call_model_func
        self.clean_sql_func = clean_sql_func

    def handle(self, user_input: str) -> pd.DataFrame:
        ctx = ModelContext(id=f"data-{int(time.time())}")
        ctx.add_history("user", user_input)

        schema_info = json.dumps(self.server.resources["table_schemas"])
        instruction = f"""
        You are a Data Agent with access to a PostgreSQL database.
        Table schemas: {schema_info}
        Translate the user request into a valid SQL query for PostgreSQL.
        Only return the SQL, no explanations.
        Add prefix 'public.' to all table names.

        User request: {user_input}
        """

        sql_parts = self.call_model_func(self.model, instruction, ctx)
        sql_raw = "".join(list(sql_parts)).strip()
        sql_query = self.clean_sql_func(sql_raw)
        
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language='sql')
        
        try:
            return self.server.run_tool("query_postgres", sql_query)
        except Exception as e:
            return pd.DataFrame({"Error": [f"Failed to execute SQL:\n{sql_query}\n\n{e}"]})