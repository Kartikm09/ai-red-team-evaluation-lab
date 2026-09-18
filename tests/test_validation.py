import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def cli(script, rows, *, options=(), extra_json=None):
    with tempfile.TemporaryDirectory() as temp:
        source = Path(temp) / "input.csv"
        if isinstance(rows, list) and (not rows or isinstance(rows[0], dict)):
            fields = list(rows[0]) if rows else ["score", "language"]
            with source.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
        args = [sys.executable, str(ROOT / "scripts" / script), str(source)]
        if extra_json is not None:
            output = Path(temp) / "outputs.json"
            output.write_text(json.dumps(extra_json), encoding="utf-8")
            args.append(str(output))
        return subprocess.run([*args, *options], text=True, capture_output=True, cwd=ROOT, timeout=10)

class ScoreTests(unittest.TestCase):
    def test_hand_computed_category_and_failure_counts(self):
        rows = [{"test_id": "one", "category": "a", "score": "5"},
                {"test_id": "two", "category": "a", "score": "1"},
                {"test_id": "three", "category": "b", "score": "3"}]
        result = cli("score_responses.py", rows, options=["--json"])
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual((data["case_count"], data["average_score"], data["failure_count"]), (3, 3, 1))
        self.assertEqual(data["categories"]["a"], {"count": 2, "average_score": 3, "lowest_score": 1})
        self.assertEqual(data["failures"][0]["test_id"], "two")

    def test_invalid_scores_are_data_errors(self):
        for score in ["", "0", "6", "100", "1.5", "bad"]:
            with self.subTest(score=score):
                result = cli("score_responses.py", [{"test_id": "bad", "category": "a", "score": score}], options=["--json"])
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("score", result.stderr.lower())
                self.assertNotIn("Traceback", result.stderr)

    def test_missing_score_is_not_a_model_failure(self):
        result = cli("score_responses.py", [{"test_id": "bad", "category": "a"}], options=["--json"])
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('"failure_count"', result.stdout)

if __name__ == "__main__":
    unittest.main()
