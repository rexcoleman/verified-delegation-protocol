# Conference Abstract — AISec Workshop (ACM CCS)

## Title
How Far Can an AI Agent Get? Benchmarking Autonomous Research Through a Governance Pipeline

## Authors
Rex Coleman, Singularity Cybersecurity LLC

## Abstract

We present the first empirical measurement of how far an AI agent can autonomously progress through a structured research governance pipeline. Using a full factorial design (3 task complexities x 3 governance levels x 5 seeds = 45 conditions), we measure quality scores on a 10-point rubric decomposed into 5 binary sub-criteria (structural completeness, statistical rigor, honest reporting, content quality, governance compliance).

Our primary finding is that governance structure explains 4.4x more quality variance than task complexity (eta-squared 0.557 vs. 0.126). Full governance templates produce a mean quality score of 8.93/10 compared to 5.47/10 without governance (Cohen's d = 2.58, 95% CI [2.53, 4.40]). Gate 0 (structural completeness) shows a binary pattern: any governance template produces 100% pass rate, while no governance produces 0%.

We identify a task-dependent quality ceiling: easy tasks reach near-perfect scores (10.0), while hard tasks plateau at 7.6 even with full governance — the range where human judgment adds most value. The dominant failure point without governance is structural (33% of conditions fail at problem definition), while governance-assisted failures distribute across statistical rigor, content quality, and honest reporting.

This study is explicitly meta-circular: the agent designing, running, and analyzing the benchmark is itself a Claude model. We document this as a methodological constraint and mitigate with structured evaluation rubrics and separated evaluation contexts.

All code and results are reproducible in under 1 minute (simulated mode).

## Author Bio

Rex Coleman is the founder of Singularity Cybersecurity LLC, focused on AI security research. His research spans prompt injection defense, LLM watermark robustness, and AI governance frameworks. Prior experience includes data analytics and sales roles at FireEye/Mandiant. He is building the govML governance template framework for structured AI research projects.

## Keywords
AI agents, research automation, governance, benchmarking, meta-research, quality evaluation
