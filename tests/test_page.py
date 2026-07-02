import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from scoring.page import page_score, ternary_direction


class PageTests(unittest.TestCase):
    def test_ternary_direction_uses_symmetric_threshold(self):
        self.assertEqual(ternary_direction(2.0, threshold=1.0), 1)
        self.assertEqual(ternary_direction(-2.0, threshold=1.0), -1)
        self.assertEqual(ternary_direction(0.5, threshold=1.0), 0)

    def test_page_score_is_positive_for_reversal(self):
        age = {"A": 1, "B": -1, "C": 1}
        drug = {"A": -1, "B": 1, "C": 1}

        self.assertEqual(page_score(age, drug), 1)


if __name__ == "__main__":
    unittest.main()
