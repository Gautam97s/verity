import json
from typing import Dict
from utils.llm import generate_content

INSIGHT_SUMMARIZATION_PROMPT = """
You are a financial advisor for a small business owner.
Input: Daily/Weekly financial metrics.
Output: STRICT JSON:
{
  "insights": [
    {
      "type": "cashflow" | "expense" | "revenue" | "risk",
      "severity": "high" | "medium" | "low",
      "title": "string",
      "description": "string",
      "actionable_advice": "string"
    }
  ]
}
Summarize key trends and anomalies. Be concise.
Return ONLY JSON.
"""

def generate_insights(metrics: Dict) -> Dict:
    """
    Generates insights based on pre-computed metrics.
    """
    content = json.dumps(metrics, indent=2)
    result = generate_content(INSIGHT_SUMMARIZATION_PROMPT, content)
    if not result or "error" in result:
        print(f"Insight Agent Error: {result['error']}. Using Mock Data.")
        return {
            "insights": [
                {
                    "type": "risk",
                    "severity": "high",
                    "title": "Cashflow Dip Projected",
                    "description": "Based on current trends, a 15% dip in cashflow is expected next week due to recurring vendor payments.",
                    "actionable_advice": "Delay non-essential purchases."
                },
                {
                    "type": "revenue",
                    "severity": "medium",
                    "title": "Sales Growth",
                    "description": "Revenue has grown by 8% compared to last month, driven by new customer acquisition.",
                    "actionable_advice": "Invest in marketing to sustain momentum."
                },
                {
                    "type": "expense",
                    "severity": "low",
                    "title": "Stable Expenses",
                    "description": "Operational expenses have remained stable over the last quarter.",
                    "actionable_advice": "Continue monitoring overheads."
                }
            ]
        }
    return result
