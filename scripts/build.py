#!/usr/bin/env python3
"""
CLI entry point to build the Certifier Catalog HTML interface.
"""
import os
import sys

# Ensure root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from build_catalog_html import main

if __name__ == "__main__":
    main()
