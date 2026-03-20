# Conference Abstract — AISec Workshop (ACM CCS 2026)

> **Title:** Verified Delegation Fails: Real LLM Agents Resist Cascade Differently Than Simulations Predict
> **Speaker:** Rex Coleman
> **Track:** AI Security / Multi-Agent Defense

## Abstract

Multi-agent AI systems need defense against cascade poisoning, but which defense components actually work? We designed a verified delegation protocol combining LLM-as-judge semantic verification, cryptographic task signing, and adaptive rate limiting — and pre-registered 7 hypotheses predicting at least 70% cascade poison reduction.

Real Claude Haiku agent experiments refute 5 of 7 hypotheses. The protocol provides no meaningful defense (0.500 poison rate vs 0.494 baseline). LLM-as-judge actively hurts performance (+3pp poison). A judge-aware adversary achieves 100% poison. Cascade simulations overestimate poison by 48pp because real agents have inherent semantic resistance. Rate limiting — the simplest component — provides the most benefit (-6pp).

Attendees will leave knowing which multi-agent defense components fail empirically, why LLM-as-judge is not viable for delegation verification, and why behavioral defenses outperform semantic defenses for cascade containment.

## Bio (100 words)

Rex Coleman is building at the intersection of AI security and ML systems engineering. He spent over a decade at FireEye and Mandiant in data analytics and enterprise sales, working with security teams across Fortune 500 organizations. He is completing his MS in Computer Science at Georgia Tech (Machine Learning specialization), where he researches AI security — adversarial evaluation of ML systems, agent exploitation, and ML governance tooling. He is the creator of govML, an open-source governance framework for ML research projects. CFA charterholder.
