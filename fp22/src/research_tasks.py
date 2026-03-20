"""
FP-22: Research task definitions for the Autonomous Research Agent Benchmark.

Defines 3 research tasks of increasing complexity that an AI agent must complete
through the governance pipeline. Each task specifies the research question,
required outputs, and complexity factors.
"""

TASK_A = {
    "id": "task_a",
    "name": "Keyword Prompt Injection False Positive Rate",
    "complexity": "easy",
    "description": (
        "Measure the false positive rate of a keyword-based prompt injection "
        "detector on 50 benign prompts. The detector flags any prompt containing "
        "keywords like 'ignore', 'override', 'system', 'forget', 'pretend'."
    ),
    "research_question": (
        "What is the false positive rate of a keyword-based prompt injection "
        "detector when applied to benign user prompts?"
    ),
    "required_outputs": [
        "List of 50 benign test prompts",
        "Detector implementation (keyword list + matching logic)",
        "False positive count and rate with 95% CI",
        "Analysis of which keywords cause most false positives",
    ],
    "complexity_factors": [
        "Single metric (FPR)",
        "No model training required",
        "Ground truth is unambiguous (prompts are benign by construction)",
    ],
    "expected_score_range": (7, 9),  # Easy task, agent should do well
}

TASK_B = {
    "id": "task_b",
    "name": "Text Similarity Metrics for Paraphrase Detection",
    "complexity": "medium",
    "description": (
        "Compare 3 text similarity metrics (cosine similarity on TF-IDF, "
        "Jaccard similarity, Levenshtein ratio) for detecting paraphrased "
        "content. Use 20 original-paraphrase pairs and 20 original-unrelated pairs."
    ),
    "research_question": (
        "Which text similarity metric best discriminates between paraphrased "
        "and unrelated text pairs?"
    ),
    "required_outputs": [
        "Dataset of 40 text pairs (20 paraphrase, 20 unrelated)",
        "Implementation of 3 similarity metrics",
        "ROC-AUC for each metric",
        "Statistical comparison (paired bootstrap test)",
        "Analysis of failure cases per metric",
    ],
    "complexity_factors": [
        "Multiple metrics to compare",
        "Requires threshold optimization",
        "Statistical comparison between methods",
        "Failure case analysis requires judgment",
    ],
    "expected_score_range": (5, 7),  # Medium task, some quality gaps expected
}

TASK_C = {
    "id": "task_c",
    "name": "Chain-of-Thought vs Prompt Injection Success Rate",
    "complexity": "hard",
    "description": (
        "Evaluate whether chain-of-thought (CoT) prompting reduces prompt "
        "injection success rate compared to direct prompting. Test 10 injection "
        "attempts against both prompting strategies using a text classification "
        "system prompt."
    ),
    "research_question": (
        "Does chain-of-thought prompting reduce the success rate of prompt "
        "injection attacks compared to direct prompting?"
    ),
    "required_outputs": [
        "10 prompt injection attack strings",
        "System prompt for text classification task",
        "CoT and direct prompting templates",
        "Success/failure for each attack x strategy combination",
        "Statistical test (McNemar's test for paired binary outcomes)",
        "Analysis of WHY CoT helps or doesn't (mechanism analysis)",
        "Threats to validity (model-specific, attack-specific)",
    ],
    "complexity_factors": [
        "Requires API calls to test prompting strategies",
        "Binary outcome with small sample size (low power)",
        "Mechanism analysis requires deep reasoning",
        "Multiple confounds (attack type, model, system prompt)",
        "Requires honest assessment of limitations",
    ],
    "expected_score_range": (4, 6),  # Hard task, significant quality gaps expected
}

ALL_TASKS = [TASK_A, TASK_B, TASK_C]

GOVERNANCE_LEVELS = {
    "none": {
        "id": "none",
        "name": "No Governance",
        "description": "Agent receives only the research question and a generic instruction to produce a research report.",
        "templates_provided": [],
        "instructions": (
            "You are a research assistant. Given the following research question, "
            "produce a complete research report with your findings. Include methodology, "
            "results, and conclusions."
        ),
    },
    "partial": {
        "id": "partial",
        "name": "Partial Governance",
        "description": "Agent receives structural templates (hypothesis registry, findings skeleton) but no quality rubrics or gate checks.",
        "templates_provided": ["HYPOTHESIS_REGISTRY_skeleton", "FINDINGS_skeleton"],
        "instructions": (
            "You are a research assistant. Given the following research question, "
            "produce a complete research report. You MUST use the provided templates "
            "for your hypothesis registry and findings document. Fill in all sections."
        ),
    },
    "full": {
        "id": "full",
        "name": "Full Governance",
        "description": "Agent receives full govML templates including quality rubrics, gate checks, claim strength tags, and statistical requirements.",
        "templates_provided": [
            "EXPERIMENTAL_DESIGN",
            "HYPOTHESIS_REGISTRY",
            "FINDINGS",
            "CLAIM_STRENGTH_SPEC",
            "STATISTICAL_ANALYSIS_SPEC",
        ],
        "instructions": (
            "You are a research assistant following the govML governance framework. "
            "Given the following research question, produce a complete research report. "
            "You MUST: (1) Fill the EXPERIMENTAL_DESIGN template completely, "
            "(2) Pre-register hypotheses in HYPOTHESIS_REGISTRY before analysis, "
            "(3) Report findings in FINDINGS template with claim strength tags "
            "([DEMONSTRATED], [SUGGESTED], [PROJECTED], [HYPOTHESIZED]), "
            "(4) Include statistical tests with effect sizes and confidence intervals, "
            "(5) Report negative results honestly, "
            "(6) List all limitations. "
            "Quality will be scored on a 10-point rubric."
        ),
    },
}

# Templates provided for partial governance
HYPOTHESIS_REGISTRY_SKELETON = """# HYPOTHESIS REGISTRY

## Pre-Registration Lock
**Lock commit:** TO BE SET
**Lock date:** [DATE]

## Registry Table
| hypothesis_id | statement | falsification_criterion | metric | resolution | evidence |
|---------------|-----------|------------------------|--------|------------|----------|
| H-1 | [statement] | [criterion] | [metric] | PENDING | -- |
"""

FINDINGS_SKELETON = """# FINDINGS

## Executive Summary
[2-3 sentence summary]

## Key Findings
### Finding 1: [Title]
[Description]

## Hypothesis Resolutions
| Hypothesis | Result | Verdict |
|-----------|--------|---------|
| H-1 | [result] | SUPPORTED / REFUTED |

## Limitations
[List limitations honestly]
"""

# Full governance templates (abbreviated for API budget)
FULL_GOVERNANCE_ADDITIONS = """
## Claim Strength Tags
- [DEMONSTRATED]: Directly measured, reproducible, >= 3 seeds, CI reported
- [SUGGESTED]: Consistent pattern, limited evidence (1-2 seeds)
- [PROJECTED]: Extrapolated from partial evidence
- [HYPOTHESIZED]: Untested prediction

## Quality Requirements
- All quantitative claims must be tagged with claim strength
- Statistical tests must report effect sizes, not just p-values
- Negative results must be reported with same rigor as positive
- Limitations section must be specific and actionable
- No "preliminary" or "TBD" in final findings
"""
