# Experimental Design Review — FP-16: Verified Delegation Protocol for Multi-Agent Systems

> **Gate:** 0.5 (must pass before Phase 1 compute)
> **Date:** 2026-03-19
> **Target venue:** AISec Workshop (ACM CCS 2026) — Tier 2
> **lock_commit:** TO BE SET after review, before Phase 1
> **Profile:** simulation-track (real agent validation via API)
> **Designed for:** 8/10 from day 1 (Gate 0.5 + R34 depth escalation)
> **Budget:** ~$10-15 Claude Haiku API

---

## 1) Project Identity

**Project:** FP-16 — Verified Delegation Protocol for Multi-Agent Systems
**Target venue:** AISec Workshop (ACM CCS 2026), Tier 2
**Compute:** CPU only + Claude Haiku API (~$10-15)
**Predecessor:** FP-15 (Multi-Agent Security Testing Framework — measured the problem)
**This project:** Proposes and validates a SOLUTION

---

## 2) Novelty Claim (one sentence)

> We propose a verified delegation protocol combining LLM-as-judge output verification, cryptographic task signing, and adaptive rate limiting that reduces multi-agent cascade poison rate by ≥70% against adaptive adversaries — closing the 54% recovery gap FP-15 identified in static zero-trust.

**Self-test (≤25 words):** Verified delegation protocol with LLM-as-judge verification defeats adaptive adversaries that bypass static zero-trust in multi-agent systems. ✓

---

## 3) Comparison Baselines

| # | Method | Citation | How We Compare | Why This Baseline |
|---|--------|----------|---------------|-------------------|
| 1 | No defense (implicit trust) | FP-15 Coleman 2026 | Our protocol vs undefended system. Delta = total defense value. | Lower bound — any defense must beat this. |
| 2 | Static zero-trust (verification_prob=0.8) | FP-15 Coleman 2026 | Our protocol vs FP-15's best defense. Delta = improvement over current best. | FP-15 showed zero-trust cuts 40% but adaptive recovers 54%. We need to beat that. |
| 3 | Input filtering (prompt-level defense) | Rebuff / LLM Guard (open-source) | Our protocol vs off-the-shelf prompt injection defenses applied per-agent. Shows architectural defense > per-agent defense. | Industry standard. Reviewer expects comparison to existing tools. |
| 4 | Human-in-the-loop (oracle verification) | Simulated perfect verifier | Our protocol vs theoretical upper bound. Shows how close to optimal we get. | Establishes ceiling — no automated defense can exceed oracle. |

---

## 4) Pre-Registered Reviewer Kill Shots

| # | Criticism | Planned Mitigation | Design Decision |
|---|----------|-------------------|-----------------|
| 1 | "LLM-as-judge is just another LLM that can be fooled — you're defending LLMs with LLMs." | Experiment E3 explicitly tests whether the judge LLM can be fooled by the same attacks that fool agent LLMs. Use a DIFFERENT model as judge (e.g., Claude Sonnet judging Haiku agents). Show that model asymmetry creates a defense advantage. | Judge model ≠ agent model. Cross-model verification is the architectural insight. |
| 2 | "The protocol adds latency — is it practical for real-time agent systems?" | Measure and report latency overhead per delegation. Show that verification adds <500ms per hop (acceptable for most workflows). Report the security-latency tradeoff curve. | Latency measurement is a required metric, not optional. |
| 3 | "This is just zero-trust with extra steps. What's actually new?" | The novelty is the COMBINATION: (a) LLM-as-judge for semantic verification (not just pattern matching), (b) cryptographic signing for delegation chain integrity, (c) adaptive rate limiting that increases verification frequency when anomalies detected. No published work combines all three for multi-agent systems. | Each component alone is not novel. The combination and its validation against adaptive adversaries is. |
| 4 | "5 agents is toy-scale. Does this work at 50?" | Run scaling experiment (5, 10, 20, 50 agents) and show protocol overhead scales sub-linearly because verification is per-hop, not per-agent. | Scaling experiment is required, not optional. |

---

## 5) Ablation Plan

| Component | Hypothesis When Removed | Expected Effect | Priority |
|-----------|------------------------|-----------------|----------|
| LLM-as-judge verification | Without semantic verification, adaptive adversary crafts outputs that pass syntactic checks | Poison rate increases to near-implicit levels (~90%+) | HIGH — core novelty |
| Cryptographic task signing | Without signing, attacker can inject tasks from any source | Delegation abuse attacks succeed; cascade via forged tasks | HIGH |
| Adaptive rate limiting | Without rate limiting, attacker can flood system before detection | Faster cascade, shorter time-to-compromise | MEDIUM |
| Cross-model judge (Sonnet judging Haiku) | Same-model judge: attacker knows exactly what to evade | Poison rate increases because attacker can optimize against known judge | HIGH — tests kill shot #1 |
| Full protocol (all three) | Baseline: no defense | Maximum cascade, ~97% poison rate (FP-15 E1 result) | CONTROL |

---

## 6) Ground Truth Audit

| Source | Type | Count | Known Lag | Positive Rate | Limitations |
|--------|------|-------|-----------|---------------|-------------|
| Real Claude Haiku agent outputs | Empirical (API) | ~2000 delegations per experiment | None | Controlled injection rate | Model behavior may change with API updates |
| FP-15 simulation baseline | Simulation transfer | ~150 runs | None | Controlled | Simulation may not match real agent behavior — this project validates |
| FP-02 attack taxonomy | Empirical transfer | 7 attack classes | Claude Sonnet only | 25-100% by class | Single model, may not transfer to Haiku |

### Alternative Sources Considered

| Source | Included? | Rationale |
|--------|-----------|-----------|
| OWASP LLM Top 10 attacks | YES (qualitative) | Attack taxonomy reference |
| Real multi-agent incident reports | NO | <10 documented cases |
| AgentDojo benchmark | NO | Single-agent only, not multi-agent cascade |

---

## 7) Statistical Plan

| Parameter | Value | Justification |
|-----------|-------|---------------|
| Seeds | 5 (42, 123, 456, 789, 1024) | govML standard. For real agents, "seed" = different task sets per run. |
| Significance test | Bootstrap CI (95%), 10K resamples | Non-parametric; no distributional assumptions on LLM output |
| Effect size threshold | ≥20pp poison rate reduction vs static zero-trust | Practitioner-meaningful: must beat FP-15's best defense by a meaningful margin |
| CI method | Percentile bootstrap | Standard for small-N with unknown distributions |
| Multiple comparisons | Bonferroni for 4 pairwise defense comparisons | 4 defenses × pairwise = 6 comparisons |
| Latency reporting | Mean, P50, P95, P99 per delegation | Standard for system performance |

---

## 8) Related Work Checklist (≥5 for Tier 2)

| # | Paper | Year | Relevance | How We Differ |
|---|-------|------|-----------|---------------|
| 1 | Coleman FP-15 — Multi-Agent Cascade | 2026 | Direct predecessor: measured cascade problem | We propose the SOLUTION, not just measure the problem |
| 2 | Cohen et al. — "AI Worm" propagation | 2024 | Demonstrated agent-to-agent attack propagation | They showed the attack; we build the defense |
| 3 | Gu et al. — "Agent Smith" mass jailbreak | 2024 | Single input compromises many agents | We defend against delegation-based cascade (different vector) |
| 4 | Zheng et al. — "Judging LLM-as-a-Judge" | 2024 | Evaluated LLM judge reliability | We apply LLM-as-judge for SECURITY verification, not quality evaluation |
| 5 | Inan et al. — Llama Guard | 2023 | LLM-based safety classifier | We use judge for delegation verification, not content moderation |
| 6 | CyberArk — Agent IAM proposals | 2026 | Identity-based agent trust | We add semantic verification on top of identity (identity alone fails per FP-15 E4) |
| 7 | Coleman FP-02 — Single-Agent Red-Team | 2026 | 7 attack classes for single agents | We defend against these attacks in multi-agent context |

---

## 9) Design Review Checklist (Gate 0.5)

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 1 | Novelty claim stated in ≤25 words | [x] | §2 |
| 2 | ≥2 comparison baselines identified | [x] | §3: 4 baselines (implicit, static ZT, input filter, oracle) |
| 3 | ≥2 reviewer kill shots with mitigations | [x] | §4: 4 kill shots |
| 4 | Ablation plan with hypothesized effects | [x] | §5: 5 components |
| 5 | Ground truth audit: sources, lag, positive rate | [x] | §6: real agents + FP-15 + FP-02 |
| 6 | Alternative label sources considered | [x] | §6: OWASP, incidents, AgentDojo |
| 7 | Statistical plan: seeds, tests, CIs | [x] | §7: 5 seeds, bootstrap, Bonferroni |
| 8 | Related work: ≥5 papers | [x] | §8: 7 papers |
| 9 | Hypotheses pre-registered in HYPOTHESIS_REGISTRY | [ ] | To create before Phase 1 |
| 10 | lock_commit set in HYPOTHESIS_REGISTRY | [ ] | To set before Phase 1 |
| 11 | Target venue identified | [x] | AISec Workshop (ACM CCS 2026) |
| 12 | This document committed before any training script | [x] | This commit |

**Gate 0.5 verdict:** [x] PASS (pending items 9-10 before Phase 1 start)

---

## 10) Tier 2 Depth Escalation (R34)

### Depth Commitment

**Primary finding (one sentence):** Verified delegation with cross-model LLM-as-judge reduces adaptive adversary cascade poison rate by ≥70%, compared to 40% for static zero-trust.

**Evaluation settings (minimum 2):**

| # | Setting | How It Differs | What It Tests |
|---|---------|---------------|---------------|
| 1 | Real Claude Haiku agents (5-agent hierarchical) | Primary: real LLM behavior | Core protocol effectiveness |
| 2 | Real agents at scale (10, 20, 50 agents) | Scaling | Protocol overhead and effectiveness at scale |
| 3 | Cross-model (Haiku agents, Sonnet judge) vs same-model (Haiku judge) | Model asymmetry | Whether cross-model verification is necessary (kill shot #1) |

### Mechanism Analysis Plan

| Finding | Proposed Mechanism | Experiment to Verify |
|---------|-------------------|---------------------|
| Cross-model judge beats same-model | Attacker optimizes for agent model's blind spots; different judge has different blind spots | Compare same-model vs cross-model judge poison detection rate |
| Adaptive rate limiting helps | Early anomaly detection triggers increased scrutiny before full cascade | Measure time-to-detection with vs without rate limiting; compare cascade curves |
| Protocol works at scale | Per-hop verification, not per-agent — overhead is O(edges) not O(nodes²) | Measure latency and poison rate at 5, 10, 20, 50 agents |
| Null: cryptographic signing alone doesn't help | Signing prevents impersonation but not output poisoning (identity ≠ content quality) | Ablation: signing-only vs full protocol |

### Adaptive Adversary Plan

| Robustness Claim | Weak Test | Adaptive Test |
|-----------------|-----------|---------------|
| Protocol reduces cascade | Naive attacker (same as FP-15) | Defense-aware: knows protocol exists, crafts outputs to pass judge verification |
| Cross-model judge resists evasion | Attacker targets agent model only | Attacker has black-box access to judge model, optimizes outputs to pass both |
| Rate limiting detects anomalies | Static attack rate | Attacker varies rate to stay below detection threshold |

### Formal Contribution Statement (draft)

We contribute:
1. **A verified delegation protocol** combining LLM-as-judge semantic verification, cryptographic task signing, and adaptive rate limiting — the first defense-in-depth architecture for multi-agent delegation security.
2. **Empirical evidence on real LLM agents** that cross-model verification (judge ≠ agent model) provides a structural defense advantage that same-model verification does not, because model-specific blind spots differ.
3. **Scaling analysis from 5 to 50 agents** showing the protocol maintains ≥70% poison reduction with sub-linear latency overhead, making it practical for production multi-agent systems.

### Published Baseline Reproduction Plan

| Published Method | Their Benchmark | Our Reproduction Plan |
|-----------------|----------------|----------------------|
| FP-15 static zero-trust | 5-agent simulation, 5 seeds | Reproduce E2 (trust model) and E4 (adaptive) with REAL agents. Direct comparison: simulation vs empirical. |
| Rebuff/LLM Guard input filtering | Prompt injection detection | Apply their defense to each agent's input. Measure: does per-agent filtering prevent cascade? |

### Parameter Sensitivity Plan (G-5)

| Parameter | Sweep Values | Expected: Finding Robust? |
|-----------|-------------|--------------------------|
| Judge verification threshold | 0.3, 0.5, 0.7, 0.9 | Yes — higher threshold = less poison but more latency |
| Rate limiting sensitivity | 1σ, 2σ, 3σ anomaly threshold | Yes — tighter threshold = faster detection but more false positives |
| Agent count | 5, 10, 20, 50 | Yes — protocol should scale |

### Simulation-to-Real Validation Plan (G-4)

| Simulation Finding (FP-15) | Real-System Validation (FP-16) |
|---------------------------|-------------------------------|
| Zero-trust reduces cascade to 84% | Reproduce with real agents — does it hold? |
| Adaptive adversary recovers 54% | Reproduce with real agents — is recovery similar? |
| Topology doesn't matter | Test hierarchical vs flat with real agents |

### Depth Escalation Checklist

| # | Requirement | Status |
|---|------------|--------|
| 1 | ONE primary finding identified | [x] | Verified delegation beats static ZT by ≥30pp |
| 2 | ≥2 evaluation settings designed | [x] | 3 settings (base, scale, cross-model) |
| 3 | Mechanism analysis planned (including nulls) | [x] | 4 mechanisms (cross-model, rate limiting, scaling, signing-null) |
| 4 | Adaptive adversary test planned | [x] | 3 adversary scenarios |
| 5 | Formal contribution statement drafted | [x] | 3 contributions |
| 6 | ≥1 published baseline reproduction planned | [x] | FP-15 reproduction + Rebuff/LLM Guard |
| 7 | Parameter sensitivity sweep planned | [x] | 3 parameters |
| 8 | Simulation-to-real validation planned | [x] | 3 FP-15 findings to validate |

---

## 11) Phase 1 Exit Checkpoint (Mid-Execution Verification)

| # | Check | Status | Deviation? |
|---|-------|--------|------------|
| 1 | All 4 comparison baselines implemented and run | [ ] | |
| 2 | 5 seeds per experiment completed | [ ] | |
| 3 | All 5 ablation components tested | [ ] | |
| 4 | Real agent experiments (not just simulation) | [ ] | |
| 5 | Any deviations logged in DECISION_LOG | [ ] | |
| 6 | Experiment outputs exist for all conditions | [ ] | |

---

## 12) Experiment Matrix

| ID | Question | IV | Levels | DV | Seeds | Real Agents? |
|----|----------|-----|--------|-----|-------|-------------|
| E1 | Does verified delegation beat static zero-trust? | Defense type | implicit, static-ZT, verified-delegation, oracle | Poison rate, cascade rate | 5 | YES |
| E2 | Does cross-model judge outperform same-model? | Judge model | same (Haiku→Haiku), cross (Haiku→Sonnet) | Judge detection rate, poison rate | 5 | YES |
| E3 | Can adaptive adversary defeat the judge? | Attacker sophistication | naive, defense-aware, judge-aware | Poison rate, judge evasion rate | 5 | YES |
| E4 | How does protocol scale? | Agent count | 5, 10, 20, 50 | Poison rate, latency overhead | 5 | YES |
| E5 | Ablation: which components matter? | Component removed | judge-only, signing-only, rate-limit-only, full | Poison rate | 5 | YES |
| E6 | FP-15 simulation validation | Defense type | implicit, static-ZT (real vs simulated) | Poison rate delta | 5 | YES |

**Total: 6 experiments. Estimated ~900 API calls, ~$10-15 Haiku.**

---

## 13) Phase Plan

| Phase | Activities | Gate | Compute |
|-------|-----------|------|---------|
| 0 | Contracts, HYPOTHESIS_REGISTRY, protocol design, lock_commit | Gate 0.5 | 0 |
| 1 | Build real-agent testbed, implement protocol, run E1-E3 | Phase 1 checkpoint | ~$8 API |
| 2 | Run E4-E6 (scaling, ablation, FP-15 validation) | — | ~$5 API |
| 3 | FINDINGS.md, figures, statistical tests | Gate 8.5 | CPU only |
| 4 | Blog, conference abstract, content pipeline, Gate 9 | Gate 9 | 0 |

---

## Venue Tier Reference

| Requirement | This Project (Tier 2) |
|-------------|----------------------|
| Comparison baselines | 4 (implicit, static-ZT, input filter, oracle) |
| Seeds | 5 |
| Ablation depth | All 5 components |
| Related work | 7 papers |
| Ground truth sources | 3 (real agents, FP-15 sim, FP-02 taxonomy) |
| Kill shots | 4 with formal responses |
| Evaluation settings | 3 (base, scale, cross-model) |
| Mechanism analysis | 4 mechanisms (including 1 expected null) |
| Adaptive adversary | 3 scenarios |
| Published baseline repro | 2 (FP-15, Rebuff) |
| Parameter sensitivity | 3 parameters |
| Simulation-to-real | 3 findings validated |
