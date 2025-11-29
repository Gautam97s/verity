import json
from typing import List, Dict
from utils.llm import generate_content

CSV_MAPPING_PROMPT = """
You are an expert data analyst.
Input: List of CSV headers and sample rows.
Output: STRICT JSON mapping to internal schema:
{
  "date_column": "string",
  "amount_column": "string",
  "description_column": "string",
  "category_column": "string" | null
}
Identify the best matching columns.
Return ONLY JSON.
"""

def map_csv_columns_with_ai(headers: List[str], sample_rows: List[Dict]) -> dict:
    content = f"HEADERS: {headers}\nSAMPLE_ROWS: {sample_rows}"
    return generate_content(CSV_MAPPING_PROMPT, content)
