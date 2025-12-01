import json
from typing import Dict
from utils.llm import generate_content

FORECAST_EXPLANATION_PROMPT = """
You are a financial analyst explaining a cashflow forecast to a small business owner.
Input: Forecasted cashflow data (next 30-90 days).
Output: STRICT JSON:
{
  "summary": "string",
  "key_drivers": ["string"],
  "recommendations": ["string"]
}
Explain why cashflow is trending up/down. Suggest actions.
Return ONLY JSON.
"""

def explain_forecast(forecast_data: Dict) -> Dict:
    """
    Explains a cashflow forecast.
    """
    content = json.dumps(forecast_data, indent=2)
    result = generate_content(FORECAST_EXPLANATION_PROMPT, content)
    if not result or "error" in result:
        error_msg = result.get('error', 'No result returned') if result else 'No result returned'
        print(f"Forecast Agent Error: {error_msg}.")
        return None
    return result
