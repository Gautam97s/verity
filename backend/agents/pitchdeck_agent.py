# backend/agents/pitchdeck_agent.py
import json
from typing import Dict
from config import settings

try:
    from google import genai
    client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
except ImportError:
    client = None


PITCHDECK_SYSTEM_PROMPT = """
You are an expert in MSME and startup finance.
You create concise, investor-ready pitchdeck outlines for very small businesses.

You will receive STRICT JSON with business financial metrics and context.
You must respond with STRICT JSON in the following schema:

{
  "title": string,           // main deck title
  "subtitle": string,        // optional, can be empty
  "slides": [
    {
      "title": string,
      "bullets": [string, ...]   // 3-6 bullet points, short and concrete
    },
    ...
  ]
}

Guidelines:
- Keep language simple, suited for Indian micro-entrepreneurs applying for loans / small investors.
- Focus on: business overview, revenue trends, cashflow health, key customers, risks and opportunities.
- DO NOT invent crazy metrics: only use or derive from provided numbers.
- If some data is missing, be honest ("Data not available") instead of guessing.
- Return ONLY JSON, no commentary.
"""


def generate_pitchdeck_outline(metrics: Dict) -> Dict:
    """
    metrics: dict with fields like:
    {
      "business_name": "...",
      "industry": "...",
      "location": "...",
      "monthly_revenue": {...},
      "revenue_growth_percent": 12.5,
      "total_inflow_last_3m": 123456,
      "overdue_amount": 12000,
      "top_customers": [...],
      ...
    }
    """
    # Fallback for dev if Gemini not configured
    if client is None or not settings.GEMINI_API_KEY:
        return {
            "title": f"{metrics.get('business_name', 'Business')} – Financial Overview",
            "subtitle": "Demo pitchdeck (offline mode)",
            "slides": [
                {
                    "title": "Business Overview",
                    "bullets": [
                        f"Industry: {metrics.get('industry', 'N/A')}",
                        f"Location: {metrics.get('location', 'N/A')}",
                    ],
                },
                {
                    "title": "Financial Snapshot",
                    "bullets": [
                        f"Overdue receivables: ₹{metrics.get('overdue_amount', 0):,.0f}",
                    ],
                },
            ],
        }

    prompt_content = (
        PITCHDECK_SYSTEM_PROMPT
        + "\n\nINPUT_METRICS_JSON:\n"
        + json.dumps(metrics, ensure_ascii=False, indent=2)
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_content,
    )

    text = response.text.strip()
    # Sometimes model may wrap JSON in markdown fences, clean if needed:
    if text.startswith("```"):
        text = text.strip("`")
        # might be like json\n{...}
        if "{" in text:
            text = text[text.index("{"):]
    data = json.loads(text)
    return data
