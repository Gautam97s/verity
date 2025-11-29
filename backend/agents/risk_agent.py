import json
from typing import List, Dict
from utils.llm import generate_content

RISK_DEMAND_PROMPT = """
You are a financial risk analyst for small businesses.
Input: Recent transactions & risk metrics.
Output: STRICT JSON:
{
  "late_payment_risk": [{"invoice_id": int, "risk_score": float, "reason": "string"}],
  "high_demand_signals": [{"product_category": "string", "trend": "up/down", "confidence": float}]
}
Analyze payment delays and sales spikes.
Return ONLY JSON.
"""

def analyze_risk_and_demand(recent_transactions: List[Dict], metrics: Dict) -> Dict:
    """
    Analyzes transactions and metrics to flag risks and demand signals.
    """
    content = json.dumps({
        "recent_transactions": recent_transactions,
        "metrics": metrics
    }, indent=2)
    return generate_content(RISK_DEMAND_PROMPT, content)
