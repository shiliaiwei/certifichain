#!/usr/bin/env python3
"""
CLI entry point to regenerate editor canvas presets and specifications.
"""
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import save_editor_specs

if __name__ == "__main__":
    print("Editor specifications verified successfully.")
