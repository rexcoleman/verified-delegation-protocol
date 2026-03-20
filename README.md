# FP-16: Verified Delegation Protocol for Multi-Agent Systems

We proposed a 3-layer defense (LLM-as-judge + cryptographic signing + adaptive rate limiting) and pre-registered 7 hypotheses predicting it would cut cascade poison by 70%. Five hypotheses were refuted. The protocol doesn't work — and that's the finding. Rate limiting (-6pp) was the only effective component. The LLM-as-judge actually made things worse (+3pp).

**Blog post:** [We Built a Multi-Agent Defense and It Failed](https://rexcoleman.dev/posts/verified-delegation-protocol/)

## The Protocol

## The Protocol

```
Agent A → [Sign Task] → [Judge Verifies Output] → [Rate Limiter Checks] → Agent B
                              ↑
                     Different model than agents
                     (cross-model defense advantage)
```

Three layers, each independently ablatable:
1. **LLM-as-judge** — a separate model semantically verifies each delegated output
2. **Cryptographic signing** — HMAC-SHA256 prevents delegation forgery
3. **Adaptive rate limiting** — escalates verification when anomalies detected

## Quick Start

```bash
# Mock mode (no API key needed — deterministic testing)
python -m pytest tests/ -v          # 17 tests
python scripts/run_experiments.py   # All 6 experiments

# Real agent mode (requires ANTHROPIC_API_KEY, ~$10-15)
export ANTHROPIC_API_KEY=sk-...
python scripts/run_experiments.py --mode api
```

## Designed for 8/10

Built with [govML](https://github.com/rexcoleman/govML) Gate 0.5 + R34:
- 7 pre-registered hypotheses (1 expected null: H-6 signing alone)
- 4 comparison baselines (implicit, static ZT, input filter, oracle)
- 4 reviewer kill shots with mitigations
- 5-component ablation plan
- 3 evaluation settings + parameter sensitivity
- Simulation-to-real validation (FP-15 → FP-16)

## Structure

```
├── EXPERIMENTAL_DESIGN.md    # Gate 0.5 design review
├── HYPOTHESIS_REGISTRY.md    # 7 pre-registered hypotheses
├── src/
│   ├── agent.py              # Mock + API agents with signing
│   ├── judge.py              # Mock + API LLM-as-judge
│   ├── protocol.py           # Verified delegation (3-layer defense)
│   └── testbed.py            # Multi-agent delegation testbed
├── scripts/
│   └── run_experiments.py    # E1-E6 experiment runner
├── tests/                    # 17 tests
└── config/base.yaml          # All parameters
```

## Predecessor

[FP-15: Multi-Agent Security Testing Framework](https://github.com/rexcoleman/multi-agent-security) measured the problem. FP-16 proposes the solution.

## License

MIT
