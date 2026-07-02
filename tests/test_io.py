import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sharp_baseline.io import load_age_directions, load_hallmark_genes


class IoTests(unittest.TestCase):
    def test_load_hallmark_genes_filters_confidence_and_other(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "hallmarks.csv"
            path.write_text(
                ",GeneId,aging_mechanisms,criteria,confidence,aging_mechanisms_group\n"
                "0,TP53,x,x,5,Genomic instability\n"
                "1,MTOR,x,x,2,Deregulated nutrient sensing\n"
                "2,FOO,x,x,5,other\n"
            )

            grouped = load_hallmark_genes(path, min_confidence=3)

        self.assertEqual(grouped, {"Genomic instability": {"TP53"}})

    def test_load_age_directions_collects_conflicts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "age.tsv"
            path.write_text(
                "HGNC\tchange type\n"
                "TP53\tincreased gene expression\n"
                "TP53\tdecreased gene expression\n"
                "MTOR\tn/a\n"
            )

            directions = load_age_directions(path)

        self.assertEqual(directions, {"TP53": {1, -1}})


if __name__ == "__main__":
    unittest.main()
