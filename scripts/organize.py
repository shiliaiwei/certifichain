#!/usr/bin/env python3
"""
CLI entry point to organize template files into categorized folder structure.
"""
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from organize_templates_as_is import organize

if __name__ == "__main__":
    organize()
