import json
from typing import List, Dict
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None

CSV_MAPPING_PROMPT = """
You are an expert data analyst.
Input: A list of column headers and the first few rows of data from a CSV/Excel file.
Output: STRICT JSON mapping from the input column names to canonical fields:
{
  "date_column": "Name of the column containing transaction date",
  "amount_column": "Name of the column containing amount",
  "description_column": "Name of the column containing description/narration",
  "type_column": "Name of the column indicating credit/debit (optional)"
}

Responsibilities:
- Infer which columns correspond to date, amount, description, type.
- If a column is ambiguous, pick the best guess.
- Return ONLY JSON.
"""

def map_csv_columns_with_ai(headers: List[str], sample_rows: List[Dict]) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        return {}

    content = f"HEADERS: {headers}\nSAMPLE_ROWS: {sample_rows}"
    full_prompt = f"{CSV_MAPPING_PROMPT}\n\nINPUT_DATA:\n{content}"

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=full_prompt,
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.strip("`")
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text)
    except Exception as e:
        print(f"Gemini Error: {e}")
        return {}
