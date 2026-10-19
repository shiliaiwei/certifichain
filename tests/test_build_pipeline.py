import os
import unittest
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from build_catalog_html import main

class TestBuildPipeline(unittest.TestCase):
    def test_build_execution_and_tokens(self):
        # Run main build
        main()

        index_html = os.path.join(BASE_DIR, "index.html")
        public_html = os.path.join(BASE_DIR, "public", "index.html")

        self.assertTrue(os.path.exists(index_html), "index.html missing after build")
        self.assertTrue(os.path.exists(public_html), "public/index.html missing after build")

        # Size check (> 1MB due to embedded JSON catalog)
        self.assertGreater(os.path.getsize(index_html), 1000000)
        self.assertGreater(os.path.getsize(public_html), 1000000)

        with open(index_html, "r", encoding="utf-8") as f:
            content = f.read()

        # 3D Skeuomorphic Leather tokens
        self.assertIn("leather-sleeve", content)
        self.assertIn("leather-pebble-grain", content)
        self.assertIn("leather-stitch-svg", content)
        self.assertIn("inserted-card-slot", content)
        self.assertIn("guilloche-watermark", content)
        self.assertIn("front-leather-flap", content)
        self.assertIn("SHILIAI", content)
        self.assertIn("WEI", content)

        # .TECH Domains Cyber-Grid tokens
        self.assertIn("cyber-canvas", content)
        self.assertIn("chamfer-18-wrapper", content)
        self.assertIn("chamfer-14-wrapper", content)
        self.assertIn("cyber-search-group", content)
        self.assertIn("stepper-tabs", content)
        self.assertIn("Space Grotesk", content)
        self.assertIn("DM Sans", content)
        self.assertIn("#08090b", content)

        # Keyline SVG icons
        self.assertIn("icon-search", content)
        self.assertIn("icon-certificate", content)
        self.assertIn("icon-badge", content)
        self.assertIn("icon-transcript", content)
        self.assertIn("icon-download", content)
        self.assertIn("icon-eye", content)

if __name__ == "__main__":
    unittest.main()
