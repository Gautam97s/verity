import json
from typing import Dict
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None

REPORT_GENERATION_PROMPT = """
You are a credit analyst preparing a report for a lender.
Input: Aggregated metrics (revenue, expenses, overdue, customer concentration, etc.).
Output: STRICT JSON schema:
{
  "sections": [
    {
      "title": "string",
      "body": "string"
    }
  ]
}

Responsibilities:
- Create structured sections: "Business Overview", "Cashflow & Risk", "Creditworthiness".
- Summarize key health indicators.
- Be professional and objective.
- Return ONLY JSON.
"""

def _call_gemini(prompt: str, content: str) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        return {"sections": []}
    
    full_prompt = f"{prompt}\n\nINPUT_METRICS:\n{content}"
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
        return {"sections": [], "error": str(e)}

def generate_financial_report(metrics: Dict) -> Dict:
    """
    Generates a financial health report.
    """
    content = json.dumps(metrics, indent=2)
    return _call_gemini(REPORT_GENERATION_PROMPT, content)
