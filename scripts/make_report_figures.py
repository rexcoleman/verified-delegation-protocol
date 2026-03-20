#!/usr/bin/env python3
"""Generate report figures from experiment results.

Reads JSON outputs from outputs/ and generates figures for blog/images/ and outputs/figures/.
Update this script with project-specific figure generation logic.

Usage:
    python scripts/make_report_figures.py
"""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTPUT_DIRS = [Path("blog/images"), Path("outputs/figures")]

def ensure_dirs():
    for d in OUTPUT_DIRS:
        d.mkdir(parents=True, exist_ok=True)

def main():
    ensure_dirs()
    print("TODO: Add figure generation logic for this project")
    # Read experiment outputs from outputs/experiments/
    # Generate project-specific figures

if __name__ == "__main__":
    main()
