import re

def clean_sql(sql_text: str) -> str:
    sql_text = re.sub(r"```(?:sql)?", "", sql_text, flags=re.IGNORECASE)
    sql_text = "\n".join(line for line in sql_text.splitlines() if not line.strip().startswith("--"))
    return sql_text.strip()