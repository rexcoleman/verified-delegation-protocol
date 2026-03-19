# Conference Abstract — AISec Workshop (ACM CCS 2026)

> **Title:** Verified Delegation: Cross-Model LLM-as-Judge Closes the Adaptive Adversary Gap in Multi-Agent Systems
> **Speaker:** Rex Coleman
> **Track:** AI Security / Multi-Agent Defense
> **Length:** 20-30 minutes

## Abstract

Multi-agent AI systems under implicit trust cascade to 100% compromise from a single compromised agent. Static zero-trust reduces poison rate by 40%, but adaptive adversaries recover 54% of the advantage (FP-15, Coleman 2026). We propose a verified delegation protocol combining three defense layers: (1) cross-model LLM-as-judge semantic verification, where a structurally different model evaluates each delegated output, exploiting the fact that model-specific blind spots differ; (2) cryptographic task signing preventing delegation forgery; and (3) adaptive rate limiting that escalates verification on anomaly detection.

We validate against 4 baselines (no defense, static zero-trust, input filtering, oracle) with 7 pre-registered hypotheses across real Claude agents (Haiku agents, Sonnet judge). Key expected results: (1) verified delegation reduces poison rate by ≥70% vs implicit trust, beating static zero-trust by ≥20pp; (2) cross-model judge outperforms same-model judge due to model-asymmetric blind spots; (3) adaptive adversaries recover ≤50% of the protocol's advantage (vs 54% against static zero-trust); (4) signing alone is a null result — identity verification doesn't prevent output poisoning, confirming FP-15's credential theft finding.

We release the protocol as open source with mock mode (17 tests, no API key needed) and API mode (~$10-15 for full experiment suite). Designed for 8/10 using govML Gate 0.5 + R34 depth escalation from day 1.

## Bio (100 words)

Rex Coleman is building at the intersection of AI security and ML systems engineering. He spent over a decade at FireEye and Mandiant in data analytics and enterprise sales, working with security teams across Fortune 500 organizations. He is completing his MS in Computer Science at Georgia Tech (Machine Learning specialization), where he researches AI security — adversarial evaluation of ML systems, agent exploitation, and ML governance tooling. He is the creator of govML, an open-source governance framework for ML research projects. CFA charterholder.
