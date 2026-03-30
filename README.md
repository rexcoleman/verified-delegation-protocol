# Verified Delegation Fails: Real LLM Agents Resist Cascade Differently Than Simulations Predict

**A judge-aware adversary — one who knows the judge exists and crafts outputs to pass verification — achieves 100% poison rate across all seeds. This is the most dangerous finding: the defense creates a false sense of security while a sophisticated attacker completely defeats it.**

**Blog post:** [LLM-as-Judge Fails: A Judge-Aware Adversary Achieves 100% Poison Rate](https://rexcoleman.dev/posts/verified-delegation-protocol/)

![govML](https://img.shields.io/badge/govML-v3.3-blue) ![Quality](https://img.shields.io/badge/quality-8.0-brightgreen) ![License](https://img.shields.io/badge/license-MIT-green)

![Key Result](docs/images/heatmap_task_governance.png)

## Key Results

| Defense | Poison Rate (mean +/- std) | vs None | Verdict |
|---------|---------------------------|---------|---------|
| None (implicit trust) | 0.494 +/- 0.008 | baseline | |
| Static zero-trust | 0.433 +/- 0.083 | -6pp | Marginal improvement |
| **Verified delegation** | **0.500 +/- 0.047** | **+1pp** | **No improvement** |
| Oracle (perfect judge) | 0.483 +/- 0.089 | -1pp | Even perfect verification barely helps |

**Core insight:** The verified delegation protocol (our proposed defense) performs WORSE than no defense (0.500 vs 0.494). Even a theoretically perfect judge (oracle, 99% detection) only achieves 0.483 — a 1pp improvement that is not statistically significant.

## Quick Start

```bash
git clone https://github.com/rexcoleman/verified-delegation-protocol
cd verified-delegation-protocol
pip install -e .
bash reproduce.sh
```

## Project Structure

```
FINDINGS.md # Research findings with pre-registered hypotheses and full results
EXPERIMENTAL_DESIGN.md # Pre-registered experimental design and methodology
HYPOTHESIS_REGISTRY.md # Hypothesis predictions, results, and verdicts
reproduce.sh # One-command reproduction of all experiments
governance.yaml # govML governance configuration
CITATION.cff # Citation metadata
LICENSE # MIT License
pyproject.toml # Python project configuration
scripts/ # Experiment and analysis scripts
src/ # Source code
tests/ # Test suite
outputs/ # Experiment outputs and results
figures/ # Generated figures and visualizations
config/ # Configuration files
docs/ # Documentation and decision records
```

## Methodology

See [FINDINGS.md](FINDINGS.md) and [EXPERIMENTAL_DESIGN.md](EXPERIMENTAL_DESIGN.md) for detailed methodology, pre-registered hypotheses, and full experimental results with multi-seed validation.

## Limitations

- **3 seeds, 5 tasks per run.** Reduced from 5 seeds / 20 tasks for API cost control (~$10). Statistical power is limited; results should be validated with larger runs.
- **3 agents per system.** Smaller than planned (was 5). Cascade dynamics may differ at larger scale.
- **Single attack payload.** CryptoScamCoin injection tests one attack type. Other payloads (data exfiltration, privilege escalation) may produce different results.
- **Same-model judge only.** Cross-model judge (H-3) was deferred. Sonnet judging Haiku agents may perform differently.
- **Claude Haiku only.** Results may not generalize to GPT-4, Gemini, or open-source models. Haiku's specific resistance characteristics drive the 49% baseline.

## Citation

If you use this work, please cite using the metadata in [CITATION.cff](CITATION.cff).

## License

[MIT](LICENSE) 2026 Rex Coleman

---

Governed by [govML](https://rexcoleman.dev/posts/govml-methodology/) v3.3
