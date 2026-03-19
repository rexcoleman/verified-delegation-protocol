# Substack Email Intro

> Paste BEFORE the full blog post in Substack editor.

---

Last week I showed that multi-agent AI systems have a 97% poison rate under default trust — and that zero-trust only cuts it by 40%.

This week: the defense.

A verified delegation protocol combining cross-model LLM-as-judge verification, cryptographic signing, and adaptive rate limiting. The key insight: defending with a DIFFERENT model than the agents creates a structural advantage that same-model defense doesn't have.

7 hypotheses pre-registered before any experiments. 1 expected null result. This is what it looks like when you design research for rigor from day 1.

Read on for the protocol design, the ablation plan, and why identity matters less than output quality for agent trust.
