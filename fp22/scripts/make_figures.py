#!/usr/bin/env python3
"""
FP-22: Generate report figures.

Produces:
1. Heatmap of task x governance quality scores
2. Bar chart of failure points by pipeline stage
3. Box plot of quality scores by governance level
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

# Try matplotlib; fall back to text-based figures
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

FIGURES_DIR = str(Path(__file__).parent.parent / "figures")
BLOG_IMAGES_DIR = str(Path(__file__).parent.parent / "blog" / "images")
EXPERIMENTS_DIR = str(Path(__file__).parent.parent / "outputs" / "experiments")


def load_data():
    """Load experiment results."""
    with open(os.path.join(EXPERIMENTS_DIR, "e1_evaluations.json")) as f:
        evals = json.load(f)
    with open(os.path.join(EXPERIMENTS_DIR, "e3_statistics.json")) as f:
        stats = json.load(f)
    with open(os.path.join(EXPERIMENTS_DIR, "e2_failure_analysis.json")) as f:
        failures = json.load(f)
    return evals, stats, failures


def make_heatmap(stats):
    """Figure 1: Heatmap of mean quality scores (task x governance)."""
    tasks = ["task_a", "task_b", "task_c"]
    govs = ["none", "partial", "full"]
    task_labels = ["Task A\n(Easy)", "Task B\n(Medium)", "Task C\n(Hard)"]
    gov_labels = ["No Governance", "Partial", "Full govML"]

    data = []
    for task in tasks:
        row = []
        for gov in govs:
            key = f"{task}_{gov}"
            row.append(stats["cell_stats"][key]["mean"])
        data.append(row)

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(8, 5))

        # Custom colormap: red (low) -> yellow (mid) -> green (high)
        cmap = plt.cm.RdYlGn
        im = ax.imshow(data, cmap=cmap, vmin=0, vmax=10, aspect='auto')

        ax.set_xticks(range(len(gov_labels)))
        ax.set_xticklabels(gov_labels, fontsize=12)
        ax.set_yticks(range(len(task_labels)))
        ax.set_yticklabels(task_labels, fontsize=12)

        # Add value annotations
        for i in range(len(tasks)):
            for j in range(len(govs)):
                val = data[i][j]
                color = "white" if val < 5 else "black"
                ax.text(j, i, f"{val:.1f}", ha="center", va="center",
                       fontsize=16, fontweight="bold", color=color)

        ax.set_title("FP-22: Quality Score by Task Complexity and Governance Level",
                     fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Governance Level", fontsize=12, labelpad=10)
        ax.set_ylabel("Task Complexity", fontsize=12, labelpad=10)

        cbar = plt.colorbar(im, ax=ax, label="Quality Score (0-10)")
        cbar.ax.tick_params(labelsize=10)

        plt.tight_layout()
        for d in [FIGURES_DIR, BLOG_IMAGES_DIR]:
            os.makedirs(d, exist_ok=True)
            plt.savefig(os.path.join(d, "heatmap_task_governance.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("Figure 1: heatmap_task_governance.png generated")
    else:
        # Text fallback
        print("Figure 1 (text): Heatmap of Task x Governance Quality Scores")
        print(f"{'':15} {'No Gov':>10} {'Partial':>10} {'Full':>10}")
        for i, task in enumerate(task_labels):
            row = " ".join(f"{data[i][j]:10.1f}" for j in range(3))
            print(f"{task:15} {row}")


def make_failure_chart(failures):
    """Figure 2: Bar chart of failure points by pipeline stage."""
    counts = failures["failure_counts"]

    # Order stages logically
    stage_order = [
        "Gate 0: Problem Definition",
        "Gate 1: Structural Completeness",
        "Gate 2: Statistical Rigor",
        "Gate 3: Honest Reporting",
        "Gate 4: Content Quality",
        "Gate 5: Governance Compliance",
        "COMPLETE (all gates passed)",
    ]

    labels = []
    values = []
    colors = []
    for stage in stage_order:
        if stage in counts:
            short = stage.replace("Gate ", "G").replace(": ", "\n").replace("COMPLETE (all gates passed)", "COMPLETE\n(All Pass)")
            labels.append(short)
            values.append(counts[stage])
            colors.append("#2ecc71" if "COMPLETE" in stage else "#e74c3c" if counts[stage] > 10 else "#f39c12")

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(range(len(labels)), values, color=colors, edgecolor="black", linewidth=0.5)

        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=10, ha="center")
        ax.set_ylabel("Number of Conditions (out of 45)", fontsize=12)
        ax.set_title("FP-22: Where Does the Agent Fail in the Research Pipeline?",
                     fontsize=14, fontweight="bold", pad=15)

        # Add value labels on bars
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                   str(val), ha='center', va='bottom', fontsize=12, fontweight='bold')

        ax.set_ylim(0, max(values) + 3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.tight_layout()
        for d in [FIGURES_DIR, BLOG_IMAGES_DIR]:
            plt.savefig(os.path.join(d, "failure_points_bar.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("Figure 2: failure_points_bar.png generated")
    else:
        print("\nFigure 2 (text): Failure Points")
        for label, val in zip(labels, values):
            bar = "#" * val
            print(f"  {label:30} | {bar} ({val})")


def make_boxplot(evals):
    """Figure 3: Box plot of quality scores by governance level."""
    by_gov = defaultdict(list)
    for e in evals:
        by_gov[e["governance_level"]].append(e["total_score"])

    gov_order = ["none", "partial", "full"]
    gov_labels = ["No Governance", "Partial Governance", "Full govML"]
    data = [by_gov[g] for g in gov_order]

    if HAS_MPL:
        fig, ax = plt.subplots(figsize=(8, 5))

        bp = ax.boxplot(data, labels=gov_labels, patch_artist=True, widths=0.5)
        colors_bp = ["#e74c3c", "#f39c12", "#2ecc71"]
        for patch, color in zip(bp['boxes'], colors_bp):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        # Overlay individual points
        for i, (scores, color) in enumerate(zip(data, colors_bp)):
            import random
            random.seed(42)
            jitter = [random.gauss(0, 0.04) for _ in scores]
            ax.scatter([i+1+j for j in jitter], scores, color=color,
                      edgecolor='black', s=50, zorder=5, alpha=0.8)

        ax.set_ylabel("Quality Score (0-10)", fontsize=12)
        ax.set_title("FP-22: Quality Score Distribution by Governance Level",
                     fontsize=14, fontweight="bold", pad=15)
        ax.set_ylim(-0.5, 11)
        ax.axhline(y=8, color='gray', linestyle='--', alpha=0.5, label='Target (8.0)')
        ax.legend(fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add mean annotations
        for i, scores in enumerate(data):
            mean = sum(scores) / len(scores)
            ax.annotate(f"mean={mean:.1f}", xy=(i+1, mean), xytext=(i+1.3, mean+0.3),
                       fontsize=10, fontweight='bold',
                       arrowprops=dict(arrowstyle='->', color='black'))

        plt.tight_layout()
        for d in [FIGURES_DIR, BLOG_IMAGES_DIR]:
            plt.savefig(os.path.join(d, "boxplot_governance.png"), dpi=150, bbox_inches='tight')
        plt.close()
        print("Figure 3: boxplot_governance.png generated")
    else:
        print("\nFigure 3 (text): Quality Score Distribution")
        for label, scores in zip(gov_labels, data):
            mean = sum(scores) / len(scores)
            print(f"  {label:25} mean={mean:.1f}  scores={scores}")


def main():
    evals, stats, failures = load_data()
    os.makedirs(FIGURES_DIR, exist_ok=True)
    os.makedirs(BLOG_IMAGES_DIR, exist_ok=True)

    make_heatmap(stats)
    make_failure_chart(failures)
    make_boxplot(evals)

    print(f"\nAll figures saved to {FIGURES_DIR}/ and {BLOG_IMAGES_DIR}/")


if __name__ == "__main__":
    main()
