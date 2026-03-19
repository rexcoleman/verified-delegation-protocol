#!/bin/bash
set -e
echo "=== FP-16 Reproduce Pipeline ==="
echo "Date: $(date)"
echo "Git: $(git rev-parse --short HEAD 2>/dev/null || echo 'n/a')"

# Gate 0.5 check
echo "--- Gate 0.5 Validation ---"
grep -qi "lock_commit.*TO BE SET\|lock_commit.*PENDING" EXPERIMENTAL_DESIGN.md && echo "FAIL: lock_commit not set" && exit 1 || echo "PASS: lock_commit set"

# Install
pip install -e ".[dev]" 2>&1 | tail -3

# Tests
echo "--- Tests ---"
python -m pytest tests/ -v

# Experiments (mock mode — no API key needed)
echo "--- Experiments (mock mode) ---"
python scripts/run_experiments.py --mode mock

echo "=== DONE ==="
