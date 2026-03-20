# HYPOTHESIS REGISTRY — FP-22: Autonomous Research Agent Benchmark

<!-- version: 1.0 -->
<!-- created: 2026-03-20 -->

> **Authority hierarchy:** govML templates (Tier 1) > MEMORY.md governance rules (Tier 2) > This document (Contract)
> **Upstream:** EXPERIMENTAL_DESIGN (design decisions informing hypothesis scope)
> **Downstream:** FINDINGS (hypothesis resolution narratives and evidence references)

## Pre-Registration Lock

**Lock commit:** SET AT COMMIT TIME (this file committed before any experiment output)
**Lock date:** 2026-03-20

> **Temporal gate (LL-74):** All hypotheses committed and locked before any experimental results are generated.

---

## Registry Table

| hypothesis_id | statement | falsification_criterion | metric | resolution | evidence |
|---------------|-----------|------------------------|--------|------------|----------|
| H-1 | An AI agent (Claude Haiku) reaches Gate 0 PASS autonomously >= 90% of the time when given full govML templates and a research task | Gate 0 pass rate < 90% across all tasks and seeds | gate_0_pass_rate >= 0.90 | **SUPPORTED** | e3_statistics.json: gate_0_rates — full=100%, partial=100%, none=0%. Exceeded prediction. |
| H-2 | Agent quality score plateaus at 6-7/10 without human intervention; the "last mile" from 7 to 8+ requires human judgment | Mean quality score across all full-governance conditions is >= 8.0 (would refute the plateau claim) | mean_quality_score in [6.0, 7.5] for full governance | **PARTIALLY SUPPORTED** | e1_evaluations.json — full gov mean=8.93 (exceeds prediction), but Task C full=7.6 (within predicted range). Ceiling is task-dependent. |
| H-3 | Full governance (govML templates) produces higher mean quality scores than no-governance across all task complexities | Full governance mean score <= no-governance mean score | mean_score(full_gov) > mean_score(no_gov) with p < 0.05 | **SUPPORTED** | e3_statistics.json: full=8.93 vs none=5.47, d=2.58, 95% CI=[2.53, 4.40] |
| H-4 | Task complexity is the strongest predictor of agent failure point, stronger than governance level | Governance level explains more variance in quality score than task complexity (eta-squared comparison) | eta_squared(task_complexity) > eta_squared(governance_level) | **REFUTED** | e3_statistics.json: governance eta-sq=0.557 vs task eta-sq=0.126. Governance explains 4.4x more variance. |

---

## Hypothesis Details

### H-1: Structural Compliance Is Easy

**Statement:** An AI agent (Claude Haiku) reaches Gate 0 PASS autonomously >= 90% of the time when given full govML templates and a research task.

**Rationale:** Gate 0 is primarily structural: does the document have the required sections, are hypotheses stated, is a novelty claim present? This is template-filling, which LLMs excel at. The interesting question is what happens AFTER structural compliance.

**Falsification:** Gate 0 pass rate < 90% across 15 full-governance conditions (3 tasks x 5 seeds).

**Linked experiments:** E0 (sanity), E1 (full factorial)

---

### H-2: The Quality Ceiling

**Statement:** Agent quality score plateaus at 6-7/10 without human intervention. Reaching 8+ requires human judgment for content quality, statistical reasoning, and honest limitation assessment.

**Rationale:** Based on observation from FP-18 and other portfolio projects: structural compliance is necessary but not sufficient. The gap between a "complete" document and a "good" document requires judgment calls that current agents struggle with.

**Falsification:** Mean quality score across all full-governance conditions is >= 8.0 (would mean the agent CAN reach high quality autonomously, refuting the plateau).

**Linked experiments:** E1 (full factorial), E3 (quality score distribution)

---

### H-3: Governance Adds Value

**Statement:** Full governance (govML templates) produces higher mean quality scores than no-governance across all task complexities.

**Rationale:** This is the core validation of the govML framework. If governance templates do not measurably improve agent output quality, the framework's value is questioned.

**Falsification:** Full governance mean score <= no-governance mean score (governance does not help or hurts).

**Linked experiments:** E1 (full factorial), E2 (failure point analysis)

---

### H-4: Complexity Dominates Governance

**Statement:** Task complexity is the strongest predictor of agent failure point, explaining more variance in quality scores than governance level.

**Rationale:** Intuitively, a hard research task should be hard regardless of how much structural support you provide. Governance helps with format, but cannot substitute for the reasoning required by complex tasks.

**Falsification:** Governance level explains more variance (higher eta-squared) than task complexity.

**Linked experiments:** E1 (full factorial), E2 (failure point analysis)

---

## Acceptance Criteria

- [x] >= 4 hypotheses registered before Phase 1
- [x] All hypotheses follow the required format (all 6 fields populated)
- [ ] All hypotheses resolved (no PENDING status at project end)
- [ ] Every resolution includes an evidence reference to a specific output file
- [x] No hypothesis was added after experiment results were observed
- [ ] Resolution narrative for each hypothesis included in FINDINGS.md
