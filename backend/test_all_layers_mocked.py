import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure we can import backend modules
sys.path.append(".")

# Import all agents
from agents import parser_agent, enrichment_agent, risk_agent, insight_agent, reminder_agent, forecast_agent, pitchdeck_agent

class TestAllLayersMocked(unittest.TestCase):

    def setUp(self):
        # Mock settings.GEMINI_API_KEY to be truthy so agents try to use the client
        self.settings_patcher = patch("config.settings.GEMINI_API_KEY", "mock_key")
        self.settings_patcher.start()

    def tearDown(self):
        self.settings_patcher.stop()

    def test_all_layers(self):
        
        # Patch the generate_content function in each agent
        with patch("agents.parser_agent.generate_content") as mock_parser, \
             patch("agents.enrichment_agent.generate_content") as mock_enrich, \
             patch("agents.risk_agent.generate_content") as mock_risk, \
             patch("agents.insight_agent.generate_content") as mock_insight, \
             patch("agents.reminder_agent.generate_content") as mock_reminder, \
             patch("agents.forecast_agent.generate_content") as mock_forecast, \
             patch("agents.pitchdeck_agent.generate_content") as mock_pitchdeck:

            print("\n========== LAYER 1: DATA INGESTION ==========")
            
            # 1. Transaction Parser
            mock_parser.return_value = {
                "direction": "inflow", "amount": 1500.0, "method": "upi", 
                "counterparty_name": "Raju", "category": "sales", 
                "invoice": {"has_invoice": False}
            }
            
            res = parser_agent.parse_transaction_with_ai("Received 1500 from Raju via UPI")
            print(f"[Transaction Parser] Output: {res}")
            self.assertEqual(res.get("amount"), 1500.0)

            # 2. Invoice Parser
            mock_parser.return_value = {
                "invoice_number": "INV-101", "total_amount": 10000.0, 
                "items": [{"name": "Rice", "amount": 10000}]
            }
            res = parser_agent.parse_invoice_with_ai("OCR Text of Invoice INV-101...")
            print(f"[Invoice Parser] Output: {res}")
            self.assertEqual(res.get("invoice_number"), "INV-101")

            print("\n========== LAYER 2: ENRICHMENT & RISK ==========")

            # 3. Ledger Mapping
            mock_enrich.return_value = {
                "contact_match": {"match_type": "exact", "contact_name": "Raju"},
                "invoice_match": {"matched": False}
            }
            res = enrichment_agent.match_ledger_entry({"name": "Raju"}, {})
            print(f"[Ledger Mapping] Output: {res}")
            self.assertEqual(res["contact_match"]["contact_name"], "Raju")

            # 4. Risk Analysis
            mock_risk.return_value = {
                "late_payment_risk": [{"invoice_id": 1, "score": 0.8}],
                "high_demand_signals": []
            }
            res = risk_agent.analyze_risk_and_demand([], {})
            print(f"[Risk Analysis] Output: {res}")
            self.assertEqual(res["late_payment_risk"][0]["score"], 0.8)

            print("\n========== LAYER 3: INSIGHTS ==========")

            # 5. Insights
            mock_insight.return_value = {
                "insights": [{
                    "type": "OVERDUE_RISK", "severity": "high", 
                    "title": "High Overdue Risk", "description": "Details..."
                }]
            }
            res = insight_agent.generate_insights({})
            print(f"[Insights] Output: {res}")
            self.assertEqual(res["insights"][0]["type"], "OVERDUE_RISK")

            print("\n========== LAYER 4: AUTONOMOUS ACTIONS ==========")

            # 6. Payment Reminder
            mock_reminder.return_value = {
                "message": "Hi Raju, please pay 10k."
            }
            res = reminder_agent.generate_payment_reminder({})
            print(f"[Payment Reminder] Output: {res}")
            self.assertIn("Raju", res["message"])

            # 7. Forecast Explanation
            mock_forecast.return_value = {
                "summary": "Cashflow dipping.", "recommendations": ["Delay purchases"]
            }
            res = forecast_agent.explain_forecast({})
            print(f"[Forecast] Output: {res}")
            self.assertIn("Cashflow", res["summary"])

            # 8. Pitchdeck
            mock_pitchdeck.return_value = {
                "title": "My Business Deck", "slides": []
            }
            res = pitchdeck_agent.generate_pitchdeck_outline({})
            print(f"[Pitchdeck] Output: {res}")
            self.assertEqual(res["title"], "My Business Deck")

if __name__ == "__main__":
    unittest.main()
