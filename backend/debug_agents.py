from sqlmodel import Session
from db import engine
from services.pitchdeck_service import compute_business_metrics
from agents.insight_agent import generate_insights
from agents.forecast_agent import explain_forecast
import json

def debug():
    with Session(engine) as session:
        print("--- Fetching Metrics ---")
        try:
            metrics = compute_business_metrics(session, 1)
            print(json.dumps(metrics, indent=2, default=str))
        except Exception as e:
            print(f"Error fetching metrics: {e}")
            return

        print("\n--- Generating Insights ---")
        try:
            insights = generate_insights(metrics)
            print(json.dumps(insights, indent=2))
        except Exception as e:
            print(f"Error generating insights: {e}")

        print("\n--- Generating Forecast ---")
        try:
            forecast_data = {
                "cashflow_summary": metrics.get("monthly_revenue", {}),
                "total_inflow": metrics.get("total_inflow_last_3m", 0),
                "growth": metrics.get("revenue_growth_percent", 0)
            }
            forecast = explain_forecast(forecast_data)
            print(json.dumps(forecast, indent=2))
        except Exception as e:
            print(f"Error generating forecast: {e}")

        print("\n--- Generating Pitch Deck ---")
        try:
            from agents.pitchdeck_agent import generate_pitchdeck_outline
            deck = generate_pitchdeck_outline(metrics)
            print(json.dumps(deck, indent=2))
        except Exception as e:
            print(f"Error generating pitch deck: {e}")

if __name__ == "__main__":
    debug()
