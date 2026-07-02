import json
import unittest
from pathlib import Path

from engine.diagnosis import final_view, run_rules
from engine.metrics import annualization_factor, compute_all, compute_year


class AnnualizationTests(unittest.TestCase):
    def test_backward_compatibility_demo_data(self):
        demo_path = Path(__file__).resolve().parents[1] / "examples" / "demo_company_5y.json"
        payload = json.loads(demo_path.read_text(encoding="utf-8"))
        metrics = compute_all(payload["data"], payload["years"])
        y2023 = metrics["2023"]

        self.assertEqual(y2023["period"], "annual")
        self.assertEqual(y2023["annualization_factor"], 1.0)
        self.assertAlmostEqual(y2023["ar_to_rev"], 360 / 1400)
        self.assertAlmostEqual(y2023["inv_to_cogs"], 320 / 920)
        self.assertAlmostEqual(y2023["cash_ratio"], 400 / 2400)
        self.assertEqual(final_view(run_rules(metrics)), "回避")

    def test_q1_annualizes_only_class3_metrics(self):
        base = {
            "revenue": 1000,
            "cogs": 600,
            "taxes_surcharges": 10,
            "selling_exp": 80,
            "admin_exp": 60,
            "rd_exp": 40,
            "operating_interest_exp": 5,
            "other_income": 3,
            "cfo": 190,
            "net_profit": 180,
            "ar": 150,
            "inventory": 120,
            "cash": 300,
            "total_assets": 1500,
            "short_debt": 100,
            "long_debt": 150,
            "goodwill": 50,
            "total_equity": 800,
            "capex": 100,
        }
        annual_metrics = compute_year({**base, "period": "annual"})
        q1_metrics = compute_year({**base, "period": "q1"})

        self.assertEqual(q1_metrics["annualization_factor"], 4.0)
        self.assertAlmostEqual(q1_metrics["ar_to_rev"], annual_metrics["ar_to_rev"] / 4)
        self.assertAlmostEqual(q1_metrics["inv_to_cogs"], annual_metrics["inv_to_cogs"] / 4)
        self.assertAlmostEqual(q1_metrics["capex_intensity"], annual_metrics["capex_intensity"] / 4)
        self.assertAlmostEqual(q1_metrics["goodwill_to_core_profit"], annual_metrics["goodwill_to_core_profit"] / 4)
        self.assertAlmostEqual(q1_metrics["cash_ratio"], annual_metrics["cash_ratio"])
        self.assertAlmostEqual(q1_metrics["debt_ratio"], annual_metrics["debt_ratio"])
        self.assertAlmostEqual(q1_metrics["core_profit_margin"], annual_metrics["core_profit_margin"])
        self.assertAlmostEqual(q1_metrics["cash_conversion"], annual_metrics["cash_conversion"])
        self.assertAlmostEqual(q1_metrics["core_profit"], annual_metrics["core_profit"])

    def test_real_case_values(self):
        ar_case = compute_year({"period": "q1", "ar": 37.78e8, "revenue": 292.65e8, "cogs": 1})
        inv_case = compute_year({"period": "q1", "inventory": 127.04e8, "cogs": 275.61e8, "revenue": 1})

        self.assertAlmostEqual(ar_case["ar_to_rev"], 0.0323, places=4)
        self.assertAlmostEqual(inv_case["inv_to_cogs"], 0.1152, places=4)

    def test_h1_q2_q3_factors(self):
        self.assertEqual(annualization_factor("h1"), 2.0)
        self.assertEqual(annualization_factor("q2"), 2.0)
        self.assertAlmostEqual(annualization_factor("q3"), 4.0 / 3.0)
        self.assertEqual(annualization_factor("annual"), 1.0)
        self.assertEqual(annualization_factor("UNKNOWN"), 1.0)

    def test_na_semantics_with_missing_flow_denominator(self):
        m = compute_year({"period": "q1", "ar": 100, "inventory": 200, "goodwill": 300})

        self.assertIsNone(m["ar_to_rev"])
        self.assertIsNone(m["inv_to_cogs"])
        self.assertIsNone(m["capex_intensity"])
        self.assertIsNone(m["goodwill_to_core_profit"])


if __name__ == "__main__":
    unittest.main()
