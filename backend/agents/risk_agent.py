import json
from typing import List, Dict
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None

RISK_DEMAND_PROMPT = """
You are a financial risk analyst for small businesses.
Input:
1. Recent transactions (time window).
2. Derived metrics (avg ticket size, frequency, customer behavior).

Output: STRICT JSON schema:
{
  "late_payment_risk": [
    {"invoice_id": int, "reason": "string", "score": float} // score 0.0-1.0
  ],
  "high_demand_signals": [
    {"item": "string", "reason": "string", "score": float} // score 0.0-1.0
  ]
}

Responsibilities:
- Identify customers with repeated late payments.
- Identify products/services with sudden demand spikes.
- Tag potentially risky or high-importance entities.
- Return ONLY JSON.
"""

def _call_gemini(prompt: str, content: str) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        return {}
    
    full_prompt = f"{prompt}\n\nINPUT_DATA:\n{content}"
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

def analyze_risk_and_demand(recent_transactions: List[Dict], metrics: Dict) -> Dict:
    """
    Analyzes transactions and metrics to flag risks and demand signals.
    """
    content = json.dumps({
        "recent_transactions": recent_transactions,
        "metrics": metrics
    }, indent=2)
    return _call_gemini(RISK_DEMAND_PROMPT, content)
