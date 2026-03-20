#!/usr/bin/env python3
"""
FP-22: Tests for the evaluation rubric.

Verifies that:
1. Evaluator produces consistent scores for known inputs
2. Score decomposition (5 binary sub-criteria) sums correctly
3. Positive control gets high score, negative control gets low score
4. Gate 0 check correctly identifies structural completeness
5. Failure point identification works correctly
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from evaluator import (
    evaluate_output,
    evaluate_structural_completeness,
    evaluate_statistical_rigor,
    evaluate_honest_reporting,
    evaluate_content_quality,
    evaluate_governance_compliance,
    check_gate_0,
    identify_failure_point,
    EvaluationResult,
)


# --- Test fixtures ---

GOOD_FULL_GOVERNANCE_OUTPUT = """
# Research Report: Test Task

## Novelty Claim
First measurement of test metric using controlled methodology.

## Research Question
What is the effect of X on Y?

## Hypothesis Registry

| hypothesis_id | statement | falsification_criterion | metric | resolution | evidence |
|---------------|-----------|------------------------|--------|------------|----------|
| H-1 | X increases Y by >= 10% | Effect < 10% | effect >= 0.10 | SUPPORTED | outputs/results.json |

## Experimental Design
We conducted a controlled experiment with n=100 samples.
Statistical analysis used two-sided t-test with Bonferroni correction.
The experimental protocol followed standard methodology for measuring the target effect.
Power analysis indicated 80% power to detect d=0.5 at alpha=0.05 with this sample size.

## Findings

### Finding 1: Primary Result
**Claim tag:** [DEMONSTRATED]
**Evidence:** outputs/results.json
**Metric:** Effect size = 15.3% (95% CI: [10.2%, 20.4%])

The primary measurement showed a statistically significant effect (p=0.003, Cohen's d=0.72).
This represents a medium-to-large effect size. With n=100 and 5 seeds, this finding meets
the [DEMONSTRATED] threshold. The mean score was 7.5 with standard deviation 1.2 across conditions.
The confidence interval excludes zero, confirming the direction of effect.

### Finding 2: Secondary Pattern
**Claim tag:** [SUGGESTED]
We observed a consistent pattern across 3 of 5 conditions, however the effect
was not statistically significant after Bonferroni correction (p=0.08).

## Negative / Unexpected Results
**What was expected:** Uniform effect across all conditions.
**What happened:** The effect did not reach significance in 2 of 5 conditions.
Despite our initial hypothesis, the negative result on conditions 4 and 5 suggests
boundary conditions exist. This failed prediction is an important caveat.
**Why this matters:** The effect may be context-dependent.
**Implication:** Future work would need to test additional conditions.

## Limitations
1. Sample size (n=100) limits detection of small effects.
2. Results specific to the test domain; generalization requires additional evidence.
3. Single-rater evaluation introduces potential bias.
4. The experimental setup may not capture real-world complexity.

## Threats to Validity
- Internal: Potential confounds from uncontrolled variables.
- External: Domain-specific results may not transfer.
"""

GARBAGE_OUTPUT = "Lorem ipsum dolor sit amet. " * 50

MINIMAL_OUTPUT = """
# Results
We found some things. The method worked okay.
The conclusion is that more research is needed.
"""


# --- Tests ---

def test_score_range():
    """Scores must be in [0, 10] range."""
    result = evaluate_output(GOOD_FULL_GOVERNANCE_OUTPUT, "test", "full", 42)
    assert 0 <= result.total_score <= 10, f"Score {result.total_score} out of range"
    print("PASS: test_score_range")


def test_score_decomposition():
    """Total score must equal sum of 5 sub-criteria."""
    result = evaluate_output(GOOD_FULL_GOVERNANCE_OUTPUT, "test", "full", 42)
    expected = (
        result.structural_completeness
        + result.statistical_rigor
        + result.honest_reporting
        + result.content_quality
        + result.governance_compliance
    )
    assert result.total_score == expected, (
        f"Score {result.total_score} != sum {expected}"
    )
    print("PASS: test_score_decomposition")


def test_sub_criteria_binary():
    """Each sub-criterion must be 0 or 2."""
    result = evaluate_output(GOOD_FULL_GOVERNANCE_OUTPUT, "test", "full", 42)
    for field_name in [
        "structural_completeness",
        "statistical_rigor",
        "honest_reporting",
        "content_quality",
        "governance_compliance",
    ]:
        value = getattr(result, field_name)
        assert value in (0, 2), f"{field_name} = {value}, expected 0 or 2"
    print("PASS: test_sub_criteria_binary")


def test_positive_control():
    """Good output should score >= 6/10."""
    result = evaluate_output(GOOD_FULL_GOVERNANCE_OUTPUT, "test", "full", 42)
    assert result.total_score >= 6, (
        f"Good output scored {result.total_score}/10, expected >= 6"
    )
    assert result.gate_0_pass, "Good output should pass Gate 0"
    print(f"PASS: test_positive_control (score={result.total_score})")


def test_negative_control():
    """Garbage output should score <= 2/10."""
    result = evaluate_output(GARBAGE_OUTPUT, "test", "full", 42)
    assert result.total_score <= 2, (
        f"Garbage scored {result.total_score}/10, expected <= 2"
    )
    assert not result.gate_0_pass, "Garbage should fail Gate 0"
    print(f"PASS: test_negative_control (score={result.total_score})")


def test_gate_0_positive():
    """Good output should pass Gate 0."""
    assert check_gate_0(GOOD_FULL_GOVERNANCE_OUTPUT) is True
    print("PASS: test_gate_0_positive")


def test_gate_0_negative():
    """Garbage should fail Gate 0."""
    assert check_gate_0(GARBAGE_OUTPUT) is False
    print("PASS: test_gate_0_negative")


def test_governance_level_affects_scoring():
    """Same text scored under different governance levels may differ."""
    result_none = evaluate_output(GOOD_FULL_GOVERNANCE_OUTPUT, "test", "none", 42)
    result_full = evaluate_output(GOOD_FULL_GOVERNANCE_OUTPUT, "test", "full", 42)
    # Both should produce valid results (no crashes)
    assert isinstance(result_none.total_score, int)
    assert isinstance(result_full.total_score, int)
    print("PASS: test_governance_level_affects_scoring")


def test_failure_point_identification():
    """Failure point should be a non-empty string."""
    result_good = identify_failure_point(GOOD_FULL_GOVERNANCE_OUTPUT, "full")
    result_bad = identify_failure_point(GARBAGE_OUTPUT, "full")
    assert isinstance(result_good, str) and len(result_good) > 0
    assert isinstance(result_bad, str) and len(result_bad) > 0
    assert result_bad != "COMPLETE (all gates passed)", (
        "Garbage should not pass all gates"
    )
    print("PASS: test_failure_point_identification")


def test_evaluation_result_serialization():
    """EvaluationResult should serialize to dict correctly."""
    result = evaluate_output(GOOD_FULL_GOVERNANCE_OUTPUT, "test", "full", 42)
    d = result.to_dict()
    assert isinstance(d, dict)
    assert "total_score" in d
    assert "task_id" in d
    assert d["task_id"] == "test"
    print("PASS: test_evaluation_result_serialization")


def test_statistical_rigor_detects_stats():
    """Statistical rigor check should find stats in good output."""
    score = evaluate_statistical_rigor(GOOD_FULL_GOVERNANCE_OUTPUT)
    assert score == 2, f"Expected 2 for output with statistics, got {score}"
    print("PASS: test_statistical_rigor_detects_stats")


def test_statistical_rigor_rejects_no_stats():
    """Statistical rigor check should reject output without statistics."""
    score = evaluate_statistical_rigor("This is just a plain paragraph with no numbers.")
    assert score == 0, f"Expected 0 for output without statistics, got {score}"
    print("PASS: test_statistical_rigor_rejects_no_stats")


def test_honest_reporting_detects_honesty():
    """Honest reporting check should find honesty indicators."""
    score = evaluate_honest_reporting(GOOD_FULL_GOVERNANCE_OUTPUT)
    assert score == 2, f"Expected 2, got {score}"
    print("PASS: test_honest_reporting_detects_honesty")


def run_all_tests():
    """Run all tests and report results."""
    tests = [
        test_score_range,
        test_score_decomposition,
        test_sub_criteria_binary,
        test_positive_control,
        test_negative_control,
        test_gate_0_positive,
        test_gate_0_negative,
        test_governance_level_affects_scoring,
        test_failure_point_identification,
        test_evaluation_result_serialization,
        test_statistical_rigor_detects_stats,
        test_statistical_rigor_rejects_no_stats,
        test_honest_reporting_detects_honesty,
    ]

    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test_fn.__name__}: {e}")
            failed += 1

    print(f"\n{'=' * 40}")
    print(f"Results: {passed} passed, {failed} failed, {len(tests)} total")
    print(f"{'=' * 40}")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
