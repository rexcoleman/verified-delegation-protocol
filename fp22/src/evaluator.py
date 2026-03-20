"""
FP-22: Evaluation rubric for scoring agent research output.

Scores agent output on a 10-point scale using 5 binary sub-criteria,
each worth 2 points. This decomposition ensures scoring consistency
and reduces subjectivity (per kill shot #3 mitigation).

Rubric Sub-Criteria (2 points each):
  1. Structural Completeness: Are all required sections present?
  2. Statistical Rigor: Are claims backed by appropriate statistics?
  3. Honest Reporting: Are limitations and negative results reported?
  4. Content Quality: Is the analysis substantive (not just template-filling)?
  5. Governance Compliance: Are govML conventions followed (claim tags, etc.)?
"""

import json
import os
import re
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class EvaluationResult:
    """Result of evaluating a single agent research output."""
    task_id: str
    governance_level: str
    seed: int
    structural_completeness: int  # 0 or 2
    statistical_rigor: int  # 0 or 2
    honest_reporting: int  # 0 or 2
    content_quality: int  # 0 or 2
    governance_compliance: int  # 0 or 2
    total_score: int = 0  # computed
    gate_0_pass: bool = False
    failure_point: str = ""  # which stage the agent failed at
    notes: str = ""

    def __post_init__(self):
        self.total_score = (
            self.structural_completeness
            + self.statistical_rigor
            + self.honest_reporting
            + self.content_quality
            + self.governance_compliance
        )

    def to_dict(self):
        return asdict(self)


def evaluate_structural_completeness(text: str, governance_level: str) -> int:
    """
    Check if all required sections are present.
    Returns 2 (pass) or 0 (fail).
    """
    if governance_level == "none":
        # Minimal requirements: has some structure
        required = ["finding", "result", "method", "conclusion"]
        found = sum(1 for r in required if r.lower() in text.lower())
        return 2 if found >= 2 else 0

    elif governance_level == "partial":
        # Must have hypothesis registry and findings sections
        required = ["hypothesis", "finding", "resolution", "limitation"]
        found = sum(1 for r in required if r.lower() in text.lower())
        return 2 if found >= 3 else 0

    else:  # full governance
        # Must have all govML sections
        required = [
            "novelty claim",
            "hypothesis",
            "finding",
            "claim",  # claim tags
            "limitation",
            "statistical",
        ]
        found = sum(1 for r in required if r.lower() in text.lower())
        return 2 if found >= 5 else 0


def evaluate_statistical_rigor(text: str) -> int:
    """
    Check if claims are backed by appropriate statistics.
    Returns 2 (pass) or 0 (fail).
    """
    indicators = [
        r"\b\d+\.?\d*%\b",  # percentages
        r"\bp[- ]?value\b",  # p-values
        r"\bCI\b|\bconfidence interval\b",  # confidence intervals
        r"\bn\s*=\s*\d+",  # sample sizes
        r"\bmean\b|\bmedian\b|\bstandard deviation\b",  # descriptive stats
        r"\beffect size\b|\bCohen",  # effect sizes
    ]
    found = sum(1 for pattern in indicators if re.search(pattern, text, re.IGNORECASE))
    return 2 if found >= 3 else 0


def evaluate_honest_reporting(text: str) -> int:
    """
    Check if limitations and negative results are reported honestly.
    Returns 2 (pass) or 0 (fail).
    """
    honesty_indicators = [
        r"\blimitation\b",
        r"\bnegative result\b|\bdid not\b|\bfailed\b|\bno significant\b",
        r"\bthreat.{0,20}validity\b",
        r"\bcaveat\b|\bhowever\b|\bdespite\b",
        r"\bfuture work\b|\bwould need\b",
    ]
    found = sum(
        1 for pattern in honesty_indicators if re.search(pattern, text, re.IGNORECASE)
    )
    return 2 if found >= 3 else 0


def evaluate_content_quality(text: str) -> int:
    """
    Check if the analysis is substantive (not just template-filling).
    Returns 2 (pass) or 0 (fail).

    Heuristics:
    - Word count >= 500 (substantive content)
    - Has specific numbers/data (not just placeholders)
    - Has analysis paragraphs (not just bullet points)
    """
    word_count = len(text.split())
    has_numbers = len(re.findall(r"\b\d+\.?\d+\b", text)) >= 5
    # Check for paragraphs (lines with > 50 words)
    paragraphs = [
        line
        for line in text.split("\n")
        if len(line.split()) > 30
    ]
    has_analysis = len(paragraphs) >= 3

    score = sum([word_count >= 500, has_numbers, has_analysis])
    return 2 if score >= 2 else 0


def evaluate_governance_compliance(text: str, governance_level: str) -> int:
    """
    Check if govML conventions are followed.
    Returns 2 (pass) or 0 (fail).

    For 'none' governance: auto-pass (no governance to comply with).
    For 'partial': check hypothesis format.
    For 'full': check claim tags, hypothesis format, all sections.
    """
    if governance_level == "none":
        return 2  # No governance to comply with

    elif governance_level == "partial":
        has_hypothesis_table = bool(
            re.search(r"hypothesis_id.*statement.*resolution", text, re.IGNORECASE)
        )
        has_resolution = bool(
            re.search(r"SUPPORTED|REFUTED|INCONCLUSIVE", text)
        )
        return 2 if (has_hypothesis_table and has_resolution) else 0

    else:  # full
        claim_tags = re.findall(
            r"\[DEMONSTRATED\]|\[SUGGESTED\]|\[PROJECTED\]|\[HYPOTHESIZED\]", text
        )
        has_claim_tags = len(claim_tags) >= 2
        has_hypothesis_table = bool(
            re.search(r"hypothesis_id.*statement.*resolution", text, re.IGNORECASE)
        )
        has_ci = bool(re.search(r"CI|confidence interval", text, re.IGNORECASE))
        score = sum([has_claim_tags, has_hypothesis_table, has_ci])
        return 2 if score >= 2 else 0


def check_gate_0(text: str) -> bool:
    """
    Check if the output passes Gate 0 (structural minimum).
    Gate 0 requires: a novelty claim OR research question,
    at least one hypothesis, and some form of methodology.
    """
    has_question = bool(
        re.search(r"research question|novelty|objective", text, re.IGNORECASE)
    )
    has_hypothesis = bool(re.search(r"hypothesis|H-\d", text, re.IGNORECASE))
    has_method = bool(
        re.search(r"method|approach|experiment|design", text, re.IGNORECASE)
    )
    return has_question and has_hypothesis and has_method


def identify_failure_point(text: str, governance_level: str) -> str:
    """
    Identify where in the pipeline the agent output breaks down.
    Returns the stage name where quality drops below acceptable.
    """
    stages = [
        ("Gate 0: Problem Definition", check_gate_0(text)),
        (
            "Gate 1: Structural Completeness",
            evaluate_structural_completeness(text, governance_level) == 2,
        ),
        ("Gate 2: Statistical Rigor", evaluate_statistical_rigor(text) == 2),
        ("Gate 3: Honest Reporting", evaluate_honest_reporting(text) == 2),
        ("Gate 4: Content Quality", evaluate_content_quality(text) == 2),
        (
            "Gate 5: Governance Compliance",
            evaluate_governance_compliance(text, governance_level) == 2,
        ),
    ]

    for stage_name, passed in stages:
        if not passed:
            return stage_name

    return "COMPLETE (all gates passed)"


def evaluate_output(
    text: str, task_id: str, governance_level: str, seed: int
) -> EvaluationResult:
    """
    Full evaluation of agent research output.
    Returns an EvaluationResult with all sub-scores and metadata.
    """
    structural = evaluate_structural_completeness(text, governance_level)
    statistical = evaluate_statistical_rigor(text)
    honest = evaluate_honest_reporting(text)
    content = evaluate_content_quality(text)
    governance = evaluate_governance_compliance(text, governance_level)
    gate_0 = check_gate_0(text)
    failure = identify_failure_point(text, governance_level)

    return EvaluationResult(
        task_id=task_id,
        governance_level=governance_level,
        seed=seed,
        structural_completeness=structural,
        statistical_rigor=statistical,
        honest_reporting=honest,
        content_quality=content,
        governance_compliance=governance,
        gate_0_pass=gate_0,
        failure_point=failure,
    )


def save_results(results: list, output_path: str):
    """Save evaluation results to JSON."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = [r.to_dict() for r in results]
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


def load_results(output_path: str) -> list:
    """Load evaluation results from JSON."""
    with open(output_path) as f:
        data = json.load(f)
    return [EvaluationResult(**d) for d in data]
