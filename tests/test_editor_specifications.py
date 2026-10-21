import json
import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestEditorSpecifications(unittest.TestCase):
    def setUp(self):
        self.specs_dir = os.path.join(BASE_DIR, "editor_specifications")

    def test_specs_files_exist(self):
        required = [
            "blank_canvas_presets.json",
            "dynamic_attributes.json",
            "typography_and_fonts.json",
            "qr_code_specs.json",
        ]
        for fname in required:
            path = os.path.join(self.specs_dir, fname)
            self.assertTrue(os.path.exists(path), f"Missing spec: {fname}")

    def test_blank_canvas_presets(self):
        path = os.path.join(self.specs_dir, "blank_canvas_presets.json")
        with open(path, "r", encoding="utf-8") as f:
            presets = json.load(f)
        self.assertIn("certificate_a4_landscape", presets)
        self.assertIn("certificate_a4_portrait", presets)
        self.assertIn("badge_square", presets)
        self.assertIn("transcript_a4", presets)
        self.assertIn("training_record_a4", presets)
        self.assertIn("assessment_a4", presets)
        self.assertIn("letter_a4_portrait", presets)
        for preset_name, preset_data in presets.items():
            self.assertEqual(preset_data.get("background", {}).get("value"), "#ffffff", f"Preset {preset_name} does not have white background")

    def test_dynamic_attributes(self):
        path = os.path.join(self.specs_dir, "dynamic_attributes.json")
        with open(path, "r", encoding="utf-8") as f:
            attrs = json.load(f)
        all_tags = []
        for group, items in attrs.items():
            for it in items:
                all_tags.append(it["tag"])
        self.assertIn("[recipient.name]", all_tags)
        self.assertIn("[certificate.uuid]", all_tags)

    def test_typography_and_fonts(self):
        path = os.path.join(self.specs_dir, "typography_and_fonts.json")
        with open(path, "r", encoding="utf-8") as f:
            typo = json.load(f)
        fonts = typo.get("googleFonts", {})
        total_fonts = sum(len(v) for v in fonts.values())
        self.assertEqual(total_fonts, 58)

if __name__ == "__main__":
    unittest.main()
