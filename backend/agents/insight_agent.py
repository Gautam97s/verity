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
    if "error" in result:
        return {"insights": [], "error": result["error"]}
    return result
