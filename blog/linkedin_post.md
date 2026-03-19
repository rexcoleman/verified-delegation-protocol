# LinkedIn Post — Verified Delegation Protocol

> Paste as native LinkedIn text. Blog link as FIRST COMMENT.

---

My last project (FP-15) found that zero-trust cuts multi-agent cascade poison by 40% — but adaptive adversaries recover 54% of that advantage.

So I built the defense.

Verified Delegation Protocol — three layers:

1. LLM-as-judge: a DIFFERENT model verifies every delegated output. Model-specific blind spots differ, so an attacker who fools the agent model doesn't automatically fool the judge.

2. Cryptographic signing: HMAC prevents delegation forgery. (Though FP-15 showed identity matters less than output quality — signing is the weakest layer.)

3. Adaptive rate limiting: when anomalies are detected, verification frequency escalates automatically.

The key insight: defending LLMs with a DIFFERENT LLM creates a structural advantage that same-model defense doesn't have. Cross-model verification is the architectural defense.

7 pre-registered hypotheses. 1 expected null result (signing alone doesn't help). 4 comparison baselines. 5-component ablation.

Built with govML Gate 0.5 — every hypothesis, baseline, and kill shot was designed before writing a single line of experiment code.

Framework is open source. Mock mode runs without API key. Real agent experiments coming soon (~$10 in Claude Haiku API).

#AISecurity #MultiAgent #ZeroTrust #DefenseInDepth #BuildInPublic

---

> First comment: "Full write-up: [blog URL]"
> Second comment: "Code: github.com/rexcoleman/verified-delegation-protocol"
> Third comment: "Attack model: github.com/rexcoleman/multi-agent-security"
