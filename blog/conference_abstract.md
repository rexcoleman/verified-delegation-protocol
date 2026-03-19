# Conference Abstract — AISec Workshop (ACM CCS 2026)

> **Title:** Verified Delegation Fails: Real LLM Agents Resist Cascade Differently Than Simulations Predict
> **Speaker:** Rex Coleman
> **Track:** AI Security / Multi-Agent Defense

## Abstract

We propose a verified delegation protocol combining LLM-as-judge semantic verification, cryptographic task signing, and adaptive rate limiting for multi-agent systems, and pre-register 7 hypotheses predicting ≥70% cascade poison reduction. Real Claude Haiku agent experiments refute 5 of 7 hypotheses.

Key findings: (1) The protocol provides no meaningful defense — verified delegation achieves 0.500 poison rate vs 0.494 baseline (no improvement). (2) The LLM-as-judge component actively HURTS performance (+3pp poison) due to false positives outweighing true positives. (3) A judge-aware adversary achieves 100% poison, defeating every defense. (4) Cascade simulations overestimate poison by 48pp (97% simulated vs 49% real) because real agents have inherent semantic resistance. (5) Rate limiting — the simplest component — provides the most benefit (-6pp).

These negative results narrow the solution space: LLM-as-judge is not viable for delegation verification against semantically plausible attacks; cascade simulations require LLM-specific resistance modeling; and behavioral defenses (rate limiting) outperform semantic defenses (content verification) for multi-agent cascade.

## Bio (100 words)

Rex Coleman is building at the intersection of AI security and ML systems engineering. He spent over a decade at FireEye and Mandiant in data analytics and enterprise sales, working with security teams across Fortune 500 organizations. He is completing his MS in Computer Science at Georgia Tech (Machine Learning specialization), where he researches AI security — adversarial evaluation of ML systems, agent exploitation, and ML governance tooling. He is the creator of govML, an open-source governance framework for ML research projects. CFA charterholder.
