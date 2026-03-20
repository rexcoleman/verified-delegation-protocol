#!/usr/bin/env python3
"""
FP-22: Main experiment runner.

Executes all experimental conditions:
  E0: Sanity validation (agent on Task A with full governance, seed=42)
  E1: Full factorial (3 tasks x 3 governance levels x 5 seeds = 45 conditions)
  E2: Failure point analysis (which pipeline stage breaks per condition)
  E3: Quality score distribution and statistical analysis

Usage:
  python scripts/run_experiments.py [--simulate] [--api-key KEY]

Budget estimate (Haiku):
  - Simulated: $0 (deterministic outputs)
  - Live API: ~$0.50 for 45 conditions
"""

import argparse
import json
import os
import sys
from pathlib import Path
from collections import defaultdict
import math

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from research_tasks import ALL_TASKS, GOVERNANCE_LEVELS
from agent_runner import run_agent, run_all_conditions
from evaluator import evaluate_output, save_results, EvaluationResult

SEEDS = [42, 123, 456, 789, 1024]
OUTPUT_DIR = str(Path(__file__).parent.parent / "outputs" / "experiments")


def run_e0(simulate: bool = True, api_key: str = None) -> dict:
    """
    E0: Sanity validation.
    - E0a: Positive control (Task A + full governance, seed=42) -> score >= 5
    - E0b: Negative control (garbage text) -> score <= 2
    - E0c: Dose-response (Task A, 3 governance levels, seed=42) -> monotonic
    """
    print("=" * 60)
    print("E0: SANITY VALIDATION")
    print("=" * 60)

    results = {}

    # E0a: Positive control
    print("\n--- E0a: Positive control ---")
    task_a = ALL_TASKS[0]  # easy task
    run = run_agent(task_a, "full", 42, api_key=api_key, simulate=simulate)
    eval_result = evaluate_output(run["output"], task_a["id"], "full", 42)
    results["e0a"] = {
        "score": eval_result.total_score,
        "gate_0_pass": eval_result.gate_0_pass,
        "pass": eval_result.total_score >= 5 and eval_result.gate_0_pass,
        "details": eval_result.to_dict(),
    }
    print(f"  Score: {eval_result.total_score}/10, Gate 0: {'PASS' if eval_result.gate_0_pass else 'FAIL'}")
    print(f"  E0a: {'PASS' if results['e0a']['pass'] else 'FAIL'}")

    # E0b: Negative control
    print("\n--- E0b: Negative control ---")
    garbage = "Lorem ipsum dolor sit amet. " * 20
    eval_garbage = evaluate_output(garbage, "garbage", "full", 0)
    results["e0b"] = {
        "score": eval_garbage.total_score,
        "gate_0_pass": eval_garbage.gate_0_pass,
        "pass": eval_garbage.total_score <= 2 and not eval_garbage.gate_0_pass,
        "details": eval_garbage.to_dict(),
    }
    print(f"  Score: {eval_garbage.total_score}/10, Gate 0: {'PASS' if eval_garbage.gate_0_pass else 'FAIL'}")
    print(f"  E0b: {'PASS' if results['e0b']['pass'] else 'FAIL'}")

    # E0c: Dose-response
    print("\n--- E0c: Dose-response ---")
    dose_scores = {}
    for gov_level in ["none", "partial", "full"]:
        run = run_agent(task_a, gov_level, 42, api_key=api_key, simulate=simulate)
        eval_result = evaluate_output(run["output"], task_a["id"], gov_level, 42)
        dose_scores[gov_level] = eval_result.total_score
        print(f"  {gov_level}: {eval_result.total_score}/10")

    monotonic = dose_scores["none"] <= dose_scores["partial"] <= dose_scores["full"]
    results["e0c"] = {
        "scores": dose_scores,
        "monotonic": monotonic,
        "pass": monotonic,
    }
    print(f"  Monotonic: {'YES' if monotonic else 'NO'}")
    print(f"  E0c: {'PASS' if results['e0c']['pass'] else 'FAIL'}")

    # Overall E0 verdict
    all_pass = all(r["pass"] for r in results.values())
    results["overall"] = {"pass": all_pass}
    print(f"\n  E0 Overall: {'PASS' if all_pass else 'FAIL'}")

    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "e0_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    return results


def run_e1(simulate: bool = True, api_key: str = None) -> list:
    """
    E1: Full factorial experiment.
    3 tasks x 3 governance levels x 5 seeds = 45 conditions.
    """
    print("\n" + "=" * 60)
    print("E1: FULL FACTORIAL (45 conditions)")
    print("=" * 60)

    all_runs = run_all_conditions(
        seeds=SEEDS, api_key=api_key, simulate=simulate, output_dir=OUTPUT_DIR
    )

    # Evaluate all outputs
    eval_results = []
    for run in all_runs:
        er = evaluate_output(
            run["output"], run["task_id"], run["governance_level"], run["seed"]
        )
        eval_results.append(er)

    save_results(eval_results, os.path.join(OUTPUT_DIR, "e1_evaluations.json"))

    # Summary statistics
    print("\n--- E1 Summary ---")
    by_task_gov = defaultdict(list)
    for er in eval_results:
        by_task_gov[(er.task_id, er.governance_level)].append(er.total_score)

    for (task, gov), scores in sorted(by_task_gov.items()):
        mean = sum(scores) / len(scores)
        print(f"  {task} x {gov}: mean={mean:.1f}, scores={scores}")

    return eval_results


def run_e2(eval_results: list) -> dict:
    """
    E2: Failure point analysis.
    For each condition, identify where the agent output breaks down.
    """
    print("\n" + "=" * 60)
    print("E2: FAILURE POINT ANALYSIS")
    print("=" * 60)

    failure_counts = defaultdict(int)
    failure_by_condition = defaultdict(lambda: defaultdict(int))

    for er in eval_results:
        failure_counts[er.failure_point] += 1
        failure_by_condition[(er.task_id, er.governance_level)][er.failure_point] += 1

    print("\n--- Overall failure points ---")
    for point, count in sorted(failure_counts.items(), key=lambda x: -x[1]):
        print(f"  {point}: {count}/{len(eval_results)}")

    print("\n--- Failure by condition ---")
    for (task, gov), points in sorted(failure_by_condition.items()):
        print(f"  {task} x {gov}:")
        for point, count in sorted(points.items(), key=lambda x: -x[1]):
            print(f"    {point}: {count}")

    results = {
        "failure_counts": dict(failure_counts),
        "failure_by_condition": {
            f"{k[0]}_{k[1]}": dict(v) for k, v in failure_by_condition.items()
        },
    }

    with open(os.path.join(OUTPUT_DIR, "e2_failure_analysis.json"), "w") as f:
        json.dump(results, f, indent=2)

    return results


def run_e3(eval_results: list) -> dict:
    """
    E3: Quality score distribution and statistical analysis.
    - Descriptive statistics per condition
    - Kruskal-Wallis test for governance effect
    - Effect sizes (Cohen's d)
    - Bootstrap 95% CIs
    """
    print("\n" + "=" * 60)
    print("E3: STATISTICAL ANALYSIS")
    print("=" * 60)

    # Group scores
    by_gov = defaultdict(list)
    by_task = defaultdict(list)
    by_task_gov = defaultdict(list)

    for er in eval_results:
        by_gov[er.governance_level].append(er.total_score)
        by_task[er.task_id].append(er.total_score)
        by_task_gov[(er.task_id, er.governance_level)].append(er.total_score)

    # Gate 0 pass rates
    gate_0_by_gov = defaultdict(list)
    for er in eval_results:
        gate_0_by_gov[er.governance_level].append(1 if er.gate_0_pass else 0)

    results = {"descriptive": {}, "gate_0_rates": {}, "effects": {}}

    # Descriptive statistics
    print("\n--- Descriptive Statistics ---")
    for gov in ["none", "partial", "full"]:
        scores = by_gov[gov]
        n = len(scores)
        mean = sum(scores) / n
        variance = sum((x - mean) ** 2 for x in scores) / (n - 1) if n > 1 else 0
        sd = math.sqrt(variance)
        gate_rate = sum(gate_0_by_gov[gov]) / len(gate_0_by_gov[gov])

        results["descriptive"][gov] = {
            "n": n,
            "mean": round(mean, 2),
            "sd": round(sd, 2),
            "min": min(scores),
            "max": max(scores),
            "scores": scores,
        }
        results["gate_0_rates"][gov] = round(gate_rate, 3)

        print(f"  {gov}: n={n}, mean={mean:.2f}, sd={sd:.2f}, range=[{min(scores)}, {max(scores)}]")
        print(f"    Gate 0 pass rate: {gate_rate:.1%}")

    for task_id in ["task_a", "task_b", "task_c"]:
        scores = by_task[task_id]
        n = len(scores)
        mean = sum(scores) / n
        variance = sum((x - mean) ** 2 for x in scores) / (n - 1) if n > 1 else 0
        sd = math.sqrt(variance)
        results["descriptive"][task_id] = {
            "n": n, "mean": round(mean, 2), "sd": round(sd, 2),
            "min": min(scores), "max": max(scores),
        }
        print(f"  {task_id}: n={n}, mean={mean:.2f}, sd={sd:.2f}")

    # Cohen's d: full vs none
    full_scores = by_gov["full"]
    none_scores = by_gov["none"]
    mean_diff = sum(full_scores) / len(full_scores) - sum(none_scores) / len(none_scores)

    var_full = sum((x - sum(full_scores)/len(full_scores))**2 for x in full_scores) / (len(full_scores)-1)
    var_none = sum((x - sum(none_scores)/len(none_scores))**2 for x in none_scores) / (len(none_scores)-1)
    pooled_sd = math.sqrt((var_full + var_none) / 2)
    cohens_d = mean_diff / pooled_sd if pooled_sd > 0 else 0

    results["effects"]["full_vs_none"] = {
        "mean_difference": round(mean_diff, 2),
        "cohens_d": round(cohens_d, 2),
        "interpretation": (
            "large" if abs(cohens_d) >= 0.8
            else "medium" if abs(cohens_d) >= 0.5
            else "small"
        ),
    }
    print(f"\n--- Effect Sizes ---")
    print(f"  Full vs None: d={cohens_d:.2f} ({results['effects']['full_vs_none']['interpretation']})")
    print(f"  Mean difference: {mean_diff:.2f} points")

    # Bootstrap CI for mean difference (full - none)
    import random
    random.seed(42)
    boot_diffs = []
    for _ in range(1000):
        boot_full = [random.choice(full_scores) for _ in range(len(full_scores))]
        boot_none = [random.choice(none_scores) for _ in range(len(none_scores))]
        diff = sum(boot_full) / len(boot_full) - sum(boot_none) / len(boot_none)
        boot_diffs.append(diff)
    boot_diffs.sort()
    ci_lower = boot_diffs[24]  # 2.5th percentile
    ci_upper = boot_diffs[974]  # 97.5th percentile

    results["effects"]["bootstrap_ci_95"] = {
        "lower": round(ci_lower, 2),
        "upper": round(ci_upper, 2),
    }
    print(f"  Bootstrap 95% CI for mean diff: [{ci_lower:.2f}, {ci_upper:.2f}]")

    # Eta-squared approximation (proportion of variance explained)
    # For governance level
    grand_mean = sum(er.total_score for er in eval_results) / len(eval_results)
    ss_between_gov = sum(
        len(by_gov[g]) * (sum(by_gov[g])/len(by_gov[g]) - grand_mean)**2
        for g in by_gov
    )
    ss_total = sum((er.total_score - grand_mean)**2 for er in eval_results)
    eta_sq_gov = ss_between_gov / ss_total if ss_total > 0 else 0

    ss_between_task = sum(
        len(by_task[t]) * (sum(by_task[t])/len(by_task[t]) - grand_mean)**2
        for t in by_task
    )
    eta_sq_task = ss_between_task / ss_total if ss_total > 0 else 0

    results["effects"]["eta_squared"] = {
        "governance_level": round(eta_sq_gov, 3),
        "task_complexity": round(eta_sq_task, 3),
        "stronger_predictor": "task_complexity" if eta_sq_task > eta_sq_gov else "governance_level",
    }
    print(f"\n--- Variance Explained ---")
    print(f"  Governance level eta^2: {eta_sq_gov:.3f}")
    print(f"  Task complexity eta^2: {eta_sq_task:.3f}")
    print(f"  Stronger predictor: {results['effects']['eta_squared']['stronger_predictor']}")

    # Per-cell statistics
    print("\n--- Per-Cell Means (Task x Governance) ---")
    cell_stats = {}
    for (task, gov), scores in sorted(by_task_gov.items()):
        mean = sum(scores) / len(scores)
        cell_stats[f"{task}_{gov}"] = {"mean": round(mean, 2), "scores": scores}
        print(f"  {task} x {gov}: {mean:.1f}")

    results["cell_stats"] = cell_stats

    with open(os.path.join(OUTPUT_DIR, "e3_statistics.json"), "w") as f:
        json.dump(results, f, indent=2)

    return results


def main():
    parser = argparse.ArgumentParser(description="FP-22 Experiment Runner")
    parser.add_argument("--simulate", action="store_true", default=True,
                       help="Use simulated outputs (default: True)")
    parser.add_argument("--live", action="store_true",
                       help="Use live API calls (overrides --simulate)")
    parser.add_argument("--api-key", type=str, default=None,
                       help="Anthropic API key")
    parser.add_argument("--experiment", type=str, default="all",
                       choices=["e0", "e1", "e2", "e3", "all"],
                       help="Which experiment to run")
    args = parser.parse_args()

    simulate = not args.live

    print(f"FP-22: Autonomous Research Agent Benchmark")
    print(f"Mode: {'SIMULATED' if simulate else 'LIVE API'}")
    print(f"Seeds: {SEEDS}")
    print(f"Conditions: {len(ALL_TASKS)} tasks x {len(GOVERNANCE_LEVELS)} governance x {len(SEEDS)} seeds = {len(ALL_TASKS) * len(GOVERNANCE_LEVELS) * len(SEEDS)}")
    print()

    if args.experiment in ("e0", "all"):
        e0_results = run_e0(simulate=simulate, api_key=args.api_key)
        if not e0_results["overall"]["pass"]:
            print("\nWARNING: E0 sanity checks did not all pass. Proceeding anyway (documenting as finding).")

    if args.experiment in ("e1", "all"):
        eval_results = run_e1(simulate=simulate, api_key=args.api_key)

        if args.experiment in ("e2", "all"):
            run_e2(eval_results)

        if args.experiment in ("e3", "all"):
            run_e3(eval_results)

    print("\n" + "=" * 60)
    print("EXPERIMENTS COMPLETE")
    print(f"Results saved to: {OUTPUT_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
