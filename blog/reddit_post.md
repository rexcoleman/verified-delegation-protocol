# I built a 3-layer multi-agent defense protocol and it made things worse — the LLM judge increased poison rate by 3pp

I designed a verified delegation protocol (LLM-as-judge verification + cryptographic signing + adaptive rate limiting) and pre-registered 7 hypotheses predicting 70% cascade poison reduction. Tested on real Claude agents: 5 of 7 hypotheses refuted. The full protocol is actually worse than no defense at all (+2pp poison rate). The simulation I based the design on was wrong by 48 percentage points.

The protocol was designed to close the gap that zero-trust leaves open in multi-agent cascade. Instead, the LLM judge actively hurts — it blocks legitimate outputs more than poisoned ones because the attack (a financial recommendation in business analysis) looks like legitimate content. A judge-aware adversary achieves 100% compromise across all seeds. The dumbest component (rate limiting, no semantic understanding, just slowing down delegation) provided the most benefit at -6pp.

Ablation results tell the full story:

- **Full protocol: +2pp worse than no defense** — the components don't compose well, judge false positives negate rate limiting gains
- **LLM-as-judge alone: +3pp worse** — false positives dominate, the judge blocks legitimate content more than attacks
- **Rate limiting alone: -6pp (best single component)** — doesn't try to understand content, just reduces attack surface
- **Judge-aware adversary: 100% poison** — if the attacker knows the defense exists, it's already defeated
- **Simulation-to-real gap: 48pp** — simulation predicted 97% no-defense poison, real agents showed 49% due to inherent semantic resistance

These are honest negative results. Every refutation narrows the solution space — LLM-as-judge is not viable for delegation verification, semantic verification fails against semantically plausible attacks, and simulations don't predict real agent behavior.

Methodology: 3 seeds, 5 tasks, 3 agents per system, real Claude Haiku agents, pre-registered hypotheses with Gate 0.5 governance. ~$10 API cost.

Repo: [github.com/rexcoleman/verified-delegation-protocol](https://github.com/rexcoleman/verified-delegation-protocol)

Code is open source. Happy to answer questions — especially about why negative results matter more than confirmations in this space.
