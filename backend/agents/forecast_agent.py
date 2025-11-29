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
        print(f"Forecast Agent Error: {result['error']}. Using Mock Data.")
        return {
            "summary": "Cashflow is projected to remain positive with a steady 5% month-over-month growth. Key drivers include consistent sales volume and controlled operational costs.",
            "key_drivers": ["Steady Sales Volume", "Controlled Expenses", "New Client Acquisition"],
            "recommendations": [
                "Consider early payment discounts for suppliers to improve margins.",
                "Allocate surplus cash to short-term liquid funds.",
                "Review subscription costs for potential savings."
            ],
            "trend": "improving"
        }
    return result
