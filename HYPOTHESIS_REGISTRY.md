# HYPOTHESIS REGISTRY — FP-16 Verified Delegation Protocol

> **Project:** FP-16 (Verified Delegation Protocol for Multi-Agent Systems)
> **Created:** 2026-03-19
> **Status:** Pre-registered (7/7 hypotheses locked before Phase 1)
> **Lock commit:** TO BE SET
> **Lock date:** 2026-03-19

> **Temporal gate (LL-74):** All hypotheses committed and locked before any experimental results are generated.

---

## H-1: Verified delegation reduces poison rate ≥70% vs implicit trust

| Field | Value |
|-------|-------|
| **Statement** | The full verified delegation protocol (LLM-as-judge + signing + rate limiting) reduces cascade poison rate by at least 70% compared to implicit trust on real Claude Haiku agents. |
| **Prediction** | poison_rate(verified) ≤ 0.3 * poison_rate(implicit) |
| **Falsification** | If poison_rate(verified) > 0.3 * poison_rate(implicit), H-1 is refuted. |
| **Status** | PENDING |
| **Linked Experiment** | E1 |
| **lock_commit** | `PENDING` |

---

## H-2: Verified delegation beats static zero-trust by ≥20pp

| Field | Value |
|-------|-------|
| **Statement** | Verified delegation achieves at least 20 percentage points lower poison rate than static zero-trust (FP-15's best defense), on real agents. |
| **Prediction** | poison_rate(static_ZT) - poison_rate(verified) ≥ 0.20 |
| **Falsification** | If delta < 0.20, the protocol doesn't sufficiently improve over FP-15. |
| **Status** | PENDING |
| **Linked Experiment** | E1 |
| **lock_commit** | `PENDING` |

---

## H-3: Cross-model judge outperforms same-model judge

| Field | Value |
|-------|-------|
| **Statement** | Using a different model as judge (Sonnet judging Haiku agents) achieves lower poison rate than same-model judge (Haiku judging Haiku), because model-specific blind spots differ. |
| **Prediction** | poison_rate(cross_model) < poison_rate(same_model) |
| **Falsification** | If cross-model ≥ same-model, the architectural insight about model asymmetry is wrong. |
| **Status** | PENDING |
| **Linked Experiment** | E2 |
| **lock_commit** | `PENDING` |

---

## H-4: Adaptive adversary cannot fully defeat verified delegation

| Field | Value |
|-------|-------|
| **Statement** | Even a judge-aware adversary (who has black-box access to the judge model) cannot recover more than 50% of the poison rate gap that verified delegation creates vs implicit trust. |
| **Prediction** | recovery_rate(judge_aware) ≤ 0.50 |
| **Falsification** | If recovery > 50%, the protocol is brittle against adaptive adversaries. |
| **Status** | PENDING |
| **Linked Experiment** | E3 |
| **lock_commit** | `PENDING` |

---

## H-5: Protocol scales sub-linearly with agent count

| Field | Value |
|-------|-------|
| **Statement** | Protocol latency overhead scales sub-linearly with agent count (per-hop verification, not per-agent²). At 50 agents, poison rate remains within 10pp of the 5-agent result. |
| **Prediction** | |poison_rate(50) - poison_rate(5)| ≤ 0.10 AND latency(50)/latency(5) < 10 |
| **Falsification** | If poison rate degrades by >10pp OR latency scales ≥ linearly, protocol doesn't scale. |
| **Status** | PENDING |
| **Linked Experiment** | E4 |
| **lock_commit** | `PENDING` |

---

## H-6: Cryptographic signing alone does NOT reduce poison rate (expected null)

| Field | Value |
|-------|-------|
| **Statement** | Signing-only (without LLM-as-judge or rate limiting) does not meaningfully reduce poison rate because signing validates identity, not output quality. FP-15 E4 showed credential theft is less effective than defense-awareness — identity is not the primary attack vector. |
| **Prediction** | poison_rate(signing_only) ≈ poison_rate(implicit) (within 5pp) |
| **Falsification** | If signing alone reduces poison by >5pp, identity verification has more value than FP-15 suggested. |
| **Status** | PENDING |
| **Linked Experiment** | E5 (ablation) |
| **lock_commit** | `PENDING` |

---

## H-7: Real agent results validate FP-15 simulation

| Field | Value |
|-------|-------|
| **Statement** | Real Claude Haiku agents under implicit trust and static zero-trust produce cascade/poison rates within 15pp of FP-15 simulation predictions. |
| **Prediction** | |real - simulated| ≤ 0.15 for both implicit and zero-trust conditions |
| **Falsification** | If delta > 15pp, the FP-15 simulation model is not predictive of real agent behavior. |
| **Status** | PENDING |
| **Linked Experiment** | E6 |
| **lock_commit** | `PENDING` |

---

## Summary

| ID | Statement (short) | Prediction | Status |
|----|-------------------|-----------|--------|
| H-1 | Verified delegation ≥70% poison reduction | poison ≤ 0.3 × implicit | PENDING |
| H-2 | Beats static ZT by ≥20pp | delta ≥ 0.20 | PENDING |
| H-3 | Cross-model judge > same-model | cross < same | PENDING |
| H-4 | Adaptive adversary ≤50% recovery | recovery ≤ 0.50 | PENDING |
| H-5 | Sub-linear scaling to 50 agents | ≤10pp degradation, <10x latency | PENDING |
| H-6 | Signing alone = null (expected) | within 5pp of implicit | PENDING |
| H-7 | Real agents validate FP-15 simulation | within 15pp | PENDING |
