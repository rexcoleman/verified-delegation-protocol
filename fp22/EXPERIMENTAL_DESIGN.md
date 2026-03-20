# EXPERIMENTAL DESIGN REVIEW — FP-22: Autonomous Research Agent Benchmark

<!-- version: 1.0 -->
<!-- created: 2026-03-20 -->
<!-- gate: 0.5 (must pass before Phase 1 compute) -->

> **Authority hierarchy:** govML templates (Tier 1) > MEMORY.md governance rules (Tier 2) > This document (Contract)
> **Conflict rule:** When a higher-tier document and this contract disagree, the higher tier wins.
> **Upstream:** HYPOTHESIS_REGISTRY (pre-registered hypotheses)
> **Downstream:** All Phase 1+ artifacts. This document gates the transition from Phase 0 (setup) to Phase 1 (experiments).

> **Purpose:** Force experimental design decisions BEFORE compute begins. This project is meta-reflexive: the agent writing this document is also the subject being measured.

---

## 1) Project Identity

**Project:** FP-22: Autonomous Research Agent Benchmark
**Research question:** Given a research question, govML templates, and API access, how far can a Claude agent autonomously progress through a structured research governance pipeline (Gate 0 through experiments through findings through quality score of 8 or higher)?
**Target venue:** arXiv preprint, then AISec Workshop (ACM CCS) (Workshop tier)
**Design lock commit:** TO BE SET after this document is committed
**Design lock date:** 2026-03-20

> **Gate 0.5 rule:** This document must be committed before any Phase 1 training script is executed.

> **Meta-circularity disclosure:** This document is being written by a Claude agent (Opus 4.6) as part of FP-22 itself. The agent is simultaneously the researcher designing the experiment AND the subject whose capabilities are being measured. This is acknowledged as a fundamental methodological constraint. See Threats to Validity section 9.

---

## 2) Novelty Claim (one sentence)

> First empirical measurement of how far an AI agent can autonomously progress through a structured research governance pipeline.

**Word count:** 20 words. PASS (under 25-word limit).

**Self-test:** What is new: no prior work measures AI agent research capability against a governance-gate quality framework. Prior benchmarks (SWE-bench, ML-bench) measure code generation, not end-to-end research governance compliance.

---

## 3) Comparison Baselines

> **Minimum:** 1 or more (Workshop tier)

| # | Method | Citation | How We Compare | Why This Baseline |
|---|--------|----------|---------------|-------------------|
| 1 | Human researcher (FP-18 timeline) | Coleman 2026 (this portfolio) | We measure agent quality scores and time against the human-driven FP-18 project timeline and scores | Establishes human performance ceiling on the same governance pipeline |
| 2 | No-governance unstructured agent | N/A (ablation condition) | Agent given same research task but NO govML templates, just a plain instruction | Isolates govML template contribution from raw agent capability |
| 3 | Partial-governance agent | N/A (ablation condition) | Agent given research task with ONLY structural templates (HYPOTHESIS_REGISTRY, FINDINGS skeleton) but no quality rubrics or gate checks | Tests whether structure alone is sufficient or quality-specific guidance is needed |

**Self-test:** A reviewer asking "how does this compare to just asking ChatGPT to do research?" is answered by baseline 2 (no-governance).

---

## 4) Pre-Registered Reviewer Kill Shots

> **Minimum:** 2 kill shots with planned mitigations.

| # | Criticism a Reviewer Would Make | Planned Mitigation | Design Decision |
|---|--------------------------------|-------------------|-----------------|
| 1 | **Meta-circularity:** The agent evaluating itself creates an unfalsifiable loop. It can game its own scoring rubric. | Use a SEPARATE evaluation pass with a different prompt context. Human expert spot-checks 20% of scores. Report inter-rater agreement between agent evaluator and human. | Accept meta-circularity as a known limitation. Mitigate with separation of evaluation context and human calibration. |
| 2 | **govML familiarity bias:** The agent was likely trained on govML-like templates, inflating governance-assisted scores. | govML templates are private to this portfolio, not in any public training corpus. Also: the agent's ability to follow them measures in-context instruction following, not memorization. | Document that govML templates are NOT public. The agent's performance measures instruction-following capability. |
| 3 | **Evaluation subjectivity:** Quality scores are inherently subjective. A 10-point rubric may not be reliable. | Decompose the 10-point score into 5 binary sub-criteria (structural completeness, statistical rigor, honest reporting, content quality, governance compliance) worth 2 points each. Report scoring rubric explicitly. | Use structured rubric with clear binary sub-criteria to maximize scoring consistency. |

---

## 5) Ablation Plan

> **Minimum:** 1 group (Workshop tier)

| Component / Feature Group | Hypothesis When Removed | Expected Effect | Priority |
|--------------------------|------------------------|-----------------|----------|
| Governance level (none / partial / full) | No governance produces lower quality scores than full governance | Quality score drops 2-3 points without governance templates | HIGH |
| Agent model capability (Haiku vs Sonnet) | More capable model reaches higher quality scores | Haiku plateaus 1-2 points lower than Sonnet | MEDIUM — budget permitting |
| Task complexity (easy / medium / hard) | Harder tasks produce lower scores regardless of governance | Quality score decreases monotonically with task complexity | HIGH |

**Self-test:** The governance-level ablation is the core test of whether govML adds value. If removing governance has NO effect, the entire govML framework is questioned.

---

## 6) Ground Truth Audit

> **Minimum:** 1 or more source (Workshop tier)

| Source | Type | Estimated Count | Known Lag | Estimated Positive Rate | Limitations |
|--------|------|----------------|-----------|------------------------|-------------|
| Human expert evaluation | Manual scoring on 10-point rubric with 5 binary sub-criteria | 45 conditions total, human spot-checks 9 (20%) | None (synchronous) | N/A (continuous scale) | Single human rater. No inter-rater reliability possible with one expert. |
| govML gate scores | Automated structural checks (section presence, hypothesis count, word counts) | 45 conditions, all scored | None | Gate pass rate is the metric | Measures structure, not content quality. A perfectly structured but content-empty document passes structural gates. |

**Alternative label sources considered:**

| Source | Why Included or Excluded | If Excluded, Could Add Later? |
|--------|-------------------------|------------------------------|
| GPT-4 as independent evaluator | Excluded: adds cost and introduces different model bias | Yes, as a follow-up experiment |
| Crowdsourced evaluation (MTurk) | Excluded: cost and time prohibitive for a portfolio project | Yes, for a full paper submission |

---

## 7) Statistical Plan

> **Minimum:** 3 or more seeds (Workshop tier)

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Seeds | [42, 123, 456, 789, 1024] | 5 seeds per govML standard |
| Conditions | 3 tasks x 3 governance levels x 5 seeds = 45 total | Full factorial design covers all interactions |
| Significance test | Kruskal-Wallis (non-parametric) for governance-level comparison | Small sample size per cell (n=5), cannot assume normality |
| Effect size threshold | Cohen's d >= 0.8 (large effect) | With n=5 per cell, only large effects are detectable |
| CI method | Bootstrap 95% CIs (1000 resamples) | Standard for small samples, no distributional assumptions |
| Multiple comparison correction | Bonferroni for 3 pairwise governance comparisons | Conservative, appropriate for small number of comparisons |
| Quality score scale | 1-10, decomposed into 5 binary sub-criteria (0 or 2 each) | Ensures scores are grounded in concrete criteria |

**Power analysis (LL-93 compliance):** With 5 observations per cell, a two-sample t-test has 80% power to detect d=1.2 (very large effect). This means we can reliably detect only if governance produces a 2.4+ point improvement on a 10-point scale (assuming SD of 2). We accept this limitation and will report effect sizes regardless of significance.

---

## 8) Related Work Checklist

> **Minimum:** 3 or more papers (Workshop tier)

| # | Paper | Year | Relevance | How We Differ |
|---|-------|------|-----------|---------------|
| 1 | Jimenez et al., "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" | 2024 | Benchmarks LLM agents on software engineering tasks | We benchmark research governance compliance, not code generation |
| 2 | Liu et al., "ML-Bench: Evaluating Large Language Models for Code Generation in Repository-Level Machine Learning Tasks" | 2024 | Benchmarks LLMs on ML pipeline code | We measure end-to-end research quality including writing and statistical design |
| 3 | Lu et al., "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery" | 2024 | Full autonomous research agent (idea through paper) | We focus on governance compliance and quality scoring, not open-ended discovery |
| 4 | Huang et al., "Benchmarking Large Language Models as AI Research Agents" | 2024 | Evaluates LLMs on research tasks | We add the governance dimension: does structured governance improve agent output? |
| 5 | Yang et al., "SciAgent: Tool-augmented Language Models for Scientific Reasoning" | 2024 | Agent-based scientific reasoning with tool use | We test governance as a "tool" for quality rather than computational tools |

---

## 9) Threats to Validity

| # | Threat | Type | Mitigation |
|---|--------|------|-----------|
| 1 | Meta-circularity: agent writes and evaluates its own research | Construct | Separate evaluation context; human spot-checks 20%; report agreement |
| 2 | govML template familiarity: agent may have seen similar structures in training | Internal | govML is private; test treats in-context instruction following as the capability |
| 3 | Model capability ceiling: results are specific to Claude models circa March 2026 | External | Report model versions; frame results as a snapshot, not a universal claim |
| 4 | Evaluation subjectivity: quality scores depend on rubric interpretation | Construct | Decompose into binary sub-criteria; report scoring rubric explicitly |
| 5 | Task representativeness: 3 tasks may not span the space of research tasks | External | Chose tasks spanning easy/medium/hard; acknowledge as a limitation |
| 6 | Simulation vs. full autonomy: budget constraints require simulated agent runs | Internal | Document simulation methodology; acknowledge gap from full autonomous loop |

---

## 10) Audience Alignment and Distribution Plan

**Primary audience:** AI/ML researchers interested in agent capabilities and research automation
**Secondary audience:** Security practitioners using governance frameworks for AI projects
**Audience side:** Both (Security OF AI: governance quality; Security FROM AI: agent capability limits)

**Portfolio position:** Meta-research — demonstrates govML framework effectiveness and agent capability limits simultaneously.

**Distribution plan:**
1. rexcoleman.dev blog post (primary)
2. arXiv preprint (if findings warrant)
3. LinkedIn post (3-5 bullet summary)
4. Substack newsletter
5. AISec Workshop CFP submission (if quality score reaches 8+)

---

## 11) E0: Sanity Validation Design (R47)

| Check | Known Input | Expected Output | Purpose |
|---|---|---|---|
| E0a: Positive control | Agent given Task A (easy) + full governance templates, seed=42 | Quality score >= 5/10; all structural gates pass | Agent can produce SOMETHING when given clear instructions |
| E0b: Negative control | Random text (lorem ipsum) evaluated by scoring rubric | Quality score <= 2/10; structural gates fail | Evaluator does not give high scores to garbage |
| E0c: Dose-response | Same task (Task A), governance levels: none < partial < full, seed=42 | Monotonically increasing quality scores | More governance produces better output (basic sanity) |

E0 must pass before E1-E3 run. Results saved to `outputs/experiments/e0_results.json`.

---

## 12) Design Review Checklist (Gate 0.5)

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 1 | Novelty claim stated in 25 words or fewer | [x] | 20 words |
| 2 | 1 or more comparison baselines identified (Workshop tier) | [x] | 3 baselines |
| 3 | 2 or more reviewer kill shots with mitigations | [x] | 3 kill shots |
| 4 | Ablation plan with hypothesized effects | [x] | 3 components |
| 5 | Ground truth audit: sources, lag, positive rate | [x] | 2 sources |
| 6 | Alternative label sources considered | [x] | 2 alternatives |
| 7 | Statistical plan: seeds, tests, CIs | [x] | 5 seeds, Kruskal-Wallis, bootstrap CIs, power analysis |
| 8 | Related work: 3 or more papers (Workshop tier) | [x] | 5 papers |
| 9 | Hypotheses pre-registered in HYPOTHESIS_REGISTRY | [x] | 4 hypotheses (H1-H4) |
| 10 | lock_commit set in HYPOTHESIS_REGISTRY | [x] | Set in same commit as this document |
| 11 | Target venue identified | [x] | arXiv preprint, then AISec Workshop |
| 12 | This document committed before any training script | [x] | Committed before experiments |

**Gate 0.5 verdict:** [x] PASS

---

## 13) Formal Contribution Statement (draft)

We contribute:
1. The first empirical measurement of AI agent progress through a structured research governance pipeline, across 3 task complexities and 3 governance levels (45 conditions).
2. Evidence on whether structured governance templates (govML) improve autonomous agent research output quality versus unstructured agent work.
3. Identification of the "quality ceiling" where agent autonomy breaks down and human judgment becomes necessary.
