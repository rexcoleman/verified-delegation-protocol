# DECISION LOG — FP-16 Verified Delegation Protocol

## ADR-0001: Mock mode as primary development mode
- **Date:** 2026-03-19 | **Phase:** 0
- **Context:** Real Claude API experiments cost ~$10-15. Need to develop and test framework without API dependency.
- **Decision:** Build mock agent/judge with deterministic behavior. API mode as secondary, activated with --mode api flag and ANTHROPIC_API_KEY.
- **Consequences:** Mock results validate infrastructure, not LLM behavior. Real agent validation is the critical next step. Acknowledged in EXPERIMENTAL_DESIGN.md §10 (simulation-to-real).

## ADR-0002: Cross-model judge as primary defense hypothesis
- **Date:** 2026-03-19 | **Phase:** 0
- **Context:** FP-15 showed static zero-trust fails against adaptive adversaries. Need a defense that exploits structural properties, not just higher detection rate.
- **Decision:** Use Sonnet as judge for Haiku agents. Different model = different blind spots = structural defense advantage.
- **Consequences:** Requires two different API models (higher cost). If cross-model doesn't outperform same-model (H-3 refuted), the protocol's novelty claim weakens.

## ADR-0003: CryptoScamCoin as standardized attack payload
- **Date:** 2026-03-19 | **Phase:** 0
- **Context:** Need a detectable, measurable injection that's clearly off-topic for business analysis tasks but plausible enough to propagate through naive agents.
- **Decision:** Inject financial recommendations for a fictional "CryptoScamCoin" across all attack types (naive, defense-aware, judge-aware).
- **Consequences:** Single attack type limits generalization. Future work: domain-specific attacks (data exfiltration, privilege escalation instructions). R35 nohup pattern applied to all experiments.
