import unittest
from unittest.mock import MagicMock, patch
import json
import os
import sys

# Ensure we can import backend modules
sys.path.append(".")

# Import all agents
from agents import parser_agent, csv_agent, enrichment_agent, risk_agent, insight_agent, reminder_agent, forecast_agent, report_agent, pitchdeck_agent

class TestAllLayersMocked(unittest.TestCase):

    def setUp(self):
        # Mock settings.GEMINI_API_KEY to be truthy so agents try to use the client
        self.settings_patcher = patch("config.settings.GEMINI_API_KEY", "mock_key")
        self.settings_patcher.start()

    def tearDown(self):
        self.settings_patcher.stop()

    def test_all_layers(self):
        # Create a shared mock client
        mock_client = MagicMock()
        mock_model = mock_client.models
        
        # Patch the 'client' variable in each agent module
        # We need to do this because the modules have already imported/initialized 'client'
        with patch("agents.parser_agent.client", mock_client), \
             patch("agents.csv_agent.client", mock_client), \
             patch("agents.enrichment_agent.client", mock_client), \
             patch("agents.risk_agent.client", mock_client), \
             patch("agents.insight_agent.client", mock_client), \
             patch("agents.reminder_agent.client", mock_client), \
             patch("agents.forecast_agent.client", mock_client), \
             patch("agents.report_agent.client", mock_client), \
             patch("agents.pitchdeck_agent.client", mock_client):

            print("\n========== LAYER 1: DATA INGESTION ==========")
            
            # 1. Transaction Parser
            mock_model.generate_content.return_value.text = json.dumps({
                "direction": "inflow", "amount": 1500.0, "method": "upi", 
                "counterparty_name": "Raju", "category": "sales", 
                "invoice": {"has_invoice": False}
            })
            
            res = parser_agent.parse_transaction_with_ai("Received 1500 from Raju via UPI")
            print(f"[Transaction Parser] Output: {res}")
            self.assertEqual(res.get("amount"), 1500.0)

            # 2. Invoice Parser
            mock_model.generate_content.return_value.text = json.dumps({
                "invoice_number": "INV-101", "total_amount": 10000.0, 
                "items": [{"name": "Rice", "amount": 10000}]
            })
            res = parser_agent.parse_invoice_with_ai("OCR Text of Invoice INV-101...")
            print(f"[Invoice Parser] Output: {res}")
            self.assertEqual(res.get("invoice_number"), "INV-101")

            print("\n========== LAYER 2: ENRICHMENT & RISK ==========")

            # 3. Ledger Mapping
            mock_model.generate_content.return_value.text = json.dumps({
                "contact_match": {"match_type": "exact", "contact_name": "Raju"},
                "invoice_match": {"matched": False}
            })
            res = enrichment_agent.match_ledger_entry({"name": "Raju"}, {})
            print(f"[Ledger Mapping] Output: {res}")
            self.assertEqual(res["contact_match"]["contact_name"], "Raju")

            # 4. Risk Analysis
            mock_model.generate_content.return_value.text = json.dumps({
                "late_payment_risk": [{"invoice_id": 1, "score": 0.8}],
                "high_demand_signals": []
            })
            res = risk_agent.analyze_risk_and_demand([], {})
            print(f"[Risk Analysis] Output: {res}")
            self.assertEqual(res["late_payment_risk"][0]["score"], 0.8)

            print("\n========== LAYER 3: INSIGHTS ==========")

            # 5. Insights
            mock_model.generate_content.return_value.text = json.dumps({
                "insights": [{
                    "type": "OVERDUE_RISK", "severity": "high", 
                    "title": "High Overdue Risk", "description": "Details..."
                }]
            })
            res = insight_agent.generate_insights({})
            print(f"[Insights] Output: {res}")
            self.assertEqual(res["insights"][0]["type"], "OVERDUE_RISK")

            print("\n========== LAYER 4: AUTONOMOUS ACTIONS ==========")

            # 6. Payment Reminder
            mock_model.generate_content.return_value.text = json.dumps({
                "message": "Hi Raju, please pay 10k."
            })
            res = reminder_agent.generate_payment_reminder({})
            print(f"[Payment Reminder] Output: {res}")
            self.assertIn("Raju", res["message"])

            # 7. Forecast Explanation
            mock_model.generate_content.return_value.text = json.dumps({
                "summary": "Cashflow dipping.", "recommendations": ["Delay purchases"]
            })
            res = forecast_agent.explain_forecast({})
            print(f"[Forecast] Output: {res}")
            self.assertIn("Cashflow", res["summary"])

            # 8. Pitchdeck
            mock_model.generate_content.return_value.text = json.dumps({
                "title": "My Business Deck", "slides": []
            })
            res = pitchdeck_agent.generate_pitchdeck_outline({})
            print(f"[Pitchdeck] Output: {res}")
            self.assertEqual(res["title"], "My Business Deck")

if __name__ == "__main__":
    unittest.main()

