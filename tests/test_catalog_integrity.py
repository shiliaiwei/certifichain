import json
import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestCatalogIntegrity(unittest.TestCase):
    def setUp(self):
        self.catalogs_dir = os.path.join(BASE_DIR, "catalogs")
        self.master_file = os.path.join(self.catalogs_dir, "catalog_all.json")

    def test_master_catalog_exists_and_loads(self):
        self.assertTrue(os.path.exists(self.master_file), "catalog_all.json does not exist")
        with open(self.master_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)
        self.assertIn("certificate", data)
        self.assertIn("badge", data)
        self.assertIn("transcript", data)
        self.assertIn("training_record", data)
        self.assertIn("assessment", data)
        self.assertIn("letter", data)

    def test_catalog_counts(self):
        with open(self.master_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data.get("certificate", [])), 2137)
        self.assertEqual(len(data.get("badge", [])), 86)
        self.assertEqual(len(data.get("transcript", [])), 45)
        self.assertEqual(len(data.get("training_record", [])), 25)
        self.assertEqual(len(data.get("assessment", [])), 25)
        self.assertEqual(len(data.get("letter", [])), 10)
        total = sum(len(v) for v in data.values())
        self.assertEqual(total, 2328)

    def test_template_schema(self):
        with open(self.master_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        for cat, items in data.items():
            for item in items[:10]:
                self.assertIn("id", item)
                self.assertIn("name", item)
                self.assertIn("paperSize", item)
                self.assertIn("orientation", item)

if __name__ == "__main__":
    unittest.main()
