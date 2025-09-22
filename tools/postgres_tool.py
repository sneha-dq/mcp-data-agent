from sqlalchemy import create_engine, text
import pandas as pd

# DB Connection Config
PG_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/others"
engine = create_engine(PG_URI)

def query_postgres(sql: str) -> pd.DataFrame:
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return pd.DataFrame(result.fetchall(), columns=result.keys())