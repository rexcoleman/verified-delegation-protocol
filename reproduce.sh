#!/bin/bash
set -e
echo "=== FP-16 Reproduce Pipeline ==="
echo "Date: $(date)"
echo "Git: $(git rev-parse --short HEAD 2>/dev/null || echo 'n/a')"

# Gate 0.5 check
echo "--- Gate 0.5 Validation ---"
grep -qi "lock_commit.*TO BE SET\|lock_commit.*PENDING" EXPERIMENTAL_DESIGN.md && echo "FAIL: lock_commit not set" && exit 1 || echo "PASS: lock_commit set"

# R35: Ensure compute_logs exists
mkdir -p ~/compute_logs

# Install
pip install numpy pyyaml pytest 2>&1 | tail -3

# Tests
echo "--- Tests ---"
python -m pytest tests/ -v

# Experiments (R35: nohup for long compute)
MODE="${1:-mock}"
echo "--- Experiments (mode=$MODE, nohup + ~/compute_logs/) ---"
nohup python3 scripts/run_experiments.py --mode "$MODE" > ~/compute_logs/fp16_experiments.log 2>&1 &
EXPID=$!
echo "PID: $EXPID — Log: ~/compute_logs/fp16_experiments.log"
echo "Waiting for experiments to complete..."
wait $EXPID
echo "Experiments done. Results in outputs/experiments/"

echo "=== DONE: $(date) ==="
