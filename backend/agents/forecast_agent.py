import json
from typing import Dict
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None

FORECAST_EXPLANATION_PROMPT = """
You are a financial analyst explaining a cashflow forecast to a small business owner.
Input:
{
  "horizon_days": int,
  "projected_daily_balance": [{"date": "...", "balance": float}, ...],
  "risk_flags": ["string", ...],
  "assumptions": ["string", ...]
}

Output: STRICT JSON schema:
{
  "summary": "string",
  "recommendations": ["string", ...]
}

Responsibilities:
- Summarize the trend (e.g., "balance falling from X to Y").
- Explain drivers based on assumptions/flags.
- Provide actionable recommendations.
- Return ONLY JSON.
"""

def _call_gemini(prompt: str, content: str) -> dict:
    if client is None or not settings.GEMINI_API_KEY:
        return {"summary": "Forecast unavailable.", "recommendations": []}
    
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
        return {"summary": "", "recommendations": [], "error": str(e)}

def explain_forecast(forecast_data: Dict) -> Dict:
    """
    Explains a cashflow forecast.
    """
    content = json.dumps(forecast_data, indent=2)
    return _call_gemini(FORECAST_EXPLANATION_PROMPT, content)
