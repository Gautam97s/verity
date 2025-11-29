import json
from typing import Dict
from utils.llm import generate_content

REPORT_GENERATION_PROMPT = """
You are a credit analyst preparing a report for a lender.
Input: Consolidated financial metrics (P&L, Balance Sheet items, Ratios).
Output: STRICT JSON:
{
  "executive_summary": "string",
  "credit_score_rationale": "string",
  "sections": [
    {"title": "string", "content": "string"}
  ]
}
Assess creditworthiness. Highlight strengths and weaknesses.
Return ONLY JSON.
"""

def generate_financial_report(metrics: Dict) -> Dict:
    """
    Generates a financial health report.
    """
    content = json.dumps(metrics, indent=2)
    return generate_content(REPORT_GENERATION_PROMPT, content)
