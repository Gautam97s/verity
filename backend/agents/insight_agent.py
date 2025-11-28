import json
from typing import Dict
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None

INSIGHT_SUMMARIZATION_PROMPT = """
You are a financial advisor for a small business owner.
Input: Pre-computed financial metrics (cashflow, overdue invoices, large outflows, top customers).
Output: STRICT JSON schema:
{
  "insights": [
    {
      "type": "OVERDUE_RISK" | "LARGE_OUTFLOW" | "CASHFLOW_DIP" | "GROWTH" | "OTHER",
      "severity": "high" | "medium" | "low",
      "title": "string",
      "description": "string"
    }
  ]
}

Responsibilities:
- Analyze the provided metrics.
- Identify what matters most to the entrepreneur.
- Generate human-friendly, prioritised insights.
- "title" should be punchy (e.g., "₹18,000 stuck in overdue invoices").
- "description" should explain the context clearly.
- Return ONLY JSON.
"""

def _call_gemini(prompt: str, content: str) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        return {"insights": []}
    
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
        return {"insights": [], "error": str(e)}

def generate_insights(metrics: Dict) -> Dict:
    """
    Generates insights based on pre-computed metrics.
    metrics example:
    {
      "period": "last_30_days",
      "daily_net_cashflow": { ... },
      "overdue_invoices": [ ... ],
      "large_outflows": [ ... ],
      "top_customers": [ ... ]
    }
    """
    content = json.dumps(metrics, indent=2)
    return _call_gemini(INSIGHT_SUMMARIZATION_PROMPT, content)
