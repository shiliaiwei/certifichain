import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestDirectoryStructure(unittest.TestCase):
    def test_standard_directories_exist(self):
        standard_dirs = [
            "src",
            "src/components",
            "src/styles",
            "src/utils",
            "public",
            "scripts",
            "tests",
            "catalogs",
            "editor_specifications",
            "elements",
            "certificates",
            "badges",
            "transcripts",
            "training_records",
            "assessments",
            "letters",
            "Templates",
        ]
        for d in standard_dirs:
            full_path = os.path.join(BASE_DIR, d)
            self.assertTrue(os.path.isdir(full_path), f"Standard directory missing: {d}")

    def test_clean_root_no_orphaned_binaries(self):
        root_files = os.listdir(BASE_DIR)
        for f in root_files:
            # Root should not have heavy media or random loose pngs
            self.assertFalse(f.endswith(".png"), f"Found loose png file in root: {f}")
            self.assertFalse(f.endswith(".mp4"), f"Found loose mp4 file in root: {f}")
            self.assertFalse(f.endswith(".zip"), f"Found loose zip file in root: {f}")

    def test_gitignore_covers_heavy_files(self):
        gitignore_path = os.path.join(BASE_DIR, ".gitignore")
        self.assertTrue(os.path.exists(gitignore_path), ".gitignore is missing")
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("*.mp4", content)
        self.assertIn("*.mov", content)
        self.assertIn("*.zip", content)
        self.assertIn(".DS_Store", content)

    def test_styles_exist(self):
        leather_css = os.path.join(BASE_DIR, "src", "styles", "skeuomorphic_leather.css")
        cyber_css = os.path.join(BASE_DIR, "src", "styles", "cyber_grid.css")
        self.assertTrue(os.path.exists(leather_css), "skeuomorphic_leather.css missing")
        self.assertTrue(os.path.exists(cyber_css), "cyber_grid.css missing")

if __name__ == "__main__":
    unittest.main()
