import pandas as pd
from sqlalchemy import create_engine, text
from config import PG_URI

engine = create_engine(PG_URI)

def run_sql(sql_query: str):
    with engine.connect() as conn:
        result = conn.execute(text(sql_query))
        return pd.DataFrame(result.fetchall(), columns=result.keys())
