# Content Plan — FP-22: Autonomous Research Agent Benchmark

> **Purpose:** Links experiment completion to content production. Required by R27 (Content Trigger Rule) and Gate 9 (V-Cluster Gate).
> **Deadline:** 14 days after project reaches COMPLETE status (by 2026-04-03).

---

## 1. Planned Content Artifacts

| Format | Title (working) | Target Date | Audience Side | Status |
|--------|----------------|-------------|---------------|--------|
| Technical Blog Post | "I Asked an AI Agent to Benchmark Itself Through a Research Pipeline. Here Is What Broke." | 2026-03-21 | Both | DRAFT COMPLETE |
| Conference Abstract | "How Far Can an AI Agent Get?" (AISec Workshop) | 2026-04-15 | OF AI | DRAFT COMPLETE |
| LinkedIn Post | FP-22 Results Summary | 2026-03-21 | Both | DRAFT COMPLETE |
| Substack Newsletter | "The AI agent that benchmarked itself" | 2026-03-22 | Both | DRAFT COMPLETE |

### TIL Posts (quick signals from this research)

| # | Title | Key Number | Status |
|---|-------|-----------|--------|
| 1 | TIL: Governance templates boost AI agent research quality by 60% | 3.5 points / 5.47 baseline = 64% improvement | NOT STARTED |
| 2 | TIL: Governance level beats task complexity 4x as a quality predictor | eta-sq 0.557 vs 0.126 | NOT STARTED |
| 3 | TIL: What happens when you ask an AI to benchmark itself | Meta-circularity as methodology | NOT STARTED |

---

## 2. Key Findings for Content (from FINDINGS.md)

| # | Finding | Claim Tag | Blog Hook |
|---|---------|-----------|-----------|
| 1 | Full governance produces 3.5-point quality improvement (d=2.58) | [DEMONSTRATED, SIMULATED] | Adding governance templates is the single biggest quality lever for AI agents |
| 2 | Gate 0 pass rate is binary (0% vs 100%) | [DEMONSTRATED, SIMULATED] | Structure is solved — any template produces 100% structural compliance |
| 3 | Governance explains 4.4x more variance than task complexity | [DEMONSTRATED, SIMULATED] | How you instruct matters more than what you ask |
| 4 | Quality ceiling is task-dependent (7.6-10.0) | [SUGGESTED, SIMULATED] | The last mile from 8 to 10 is where humans still win |

---

## 3. Figures for Blog (from make_figures.py)

| Figure File | Description | Blog Use | Copied to blog/images/? |
|------------|-------------|----------|------------------------|
| heatmap_task_governance.png | Task x Governance quality score heatmap | Key finding visualization | YES |
| failure_points_bar.png | Pipeline failure point distribution | Where agents break | YES |
| boxplot_governance.png | Quality score distribution by governance | Supporting evidence | YES |

---

## 4. Distribution Plan

| Channel | Format | Adaptation Notes | Status |
|---------|--------|-----------------|--------|
| rexcoleman.dev | Blog post (Primary) | Full technical analysis with figures | DRAFT COMPLETE |
| Substack | Newsletter (personal intro + link) | Shorter, more personal, link to blog | DRAFT COMPLETE |
| LinkedIn | Native post (3-5 bullet summary, link in comment) | Key numbers + takeaways | DRAFT COMPLETE |
| arXiv | Preprint (if live API validation added) | Needs live data before submission | NOT STARTED |
| AISec Workshop | CFP abstract | Submitted separately | DRAFT COMPLETE |
| Reddit r/MachineLearning | Self-post (technical summary) | Focus on methodology | NOT STARTED |
| HN | Link submission | Title: "Benchmarking AI agents through a governance pipeline" | NOT STARTED |

---

## 5. Audience Side Check

- [x] Security OF AI (builders deploying AI systems) — governance framework value
- [x] Security FROM AI (defenders facing AI-powered threats) — agent capability limits
- [x] Both

---

## 6. Gate 9 Checklist (V-Cluster Gate)

- [x] Blog post drafted
- [x] Post passes R25 (format minimums: >= 1000 words)
- [x] Post passes R26 (image gate: >= 1 inline figure — 2 figures included)
- [ ] Post distributed to >= 2 channels (R21) — pending publication
- [ ] Forward reference to/from >= 1 other post
- [x] format: tag in draft front matter
