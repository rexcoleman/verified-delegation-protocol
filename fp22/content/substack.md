# Substack Newsletter — FP-22

**Subject line:** The AI agent that benchmarked itself (and what broke)

---

This week I ran an experiment that was more recursive than I expected.

I asked a Claude agent to benchmark how far an AI agent can get through a structured research pipeline — and the agent writing the benchmark WAS the subject being measured. Meta-circularity at its finest.

The setup: 3 research tasks (easy, medium, hard), 3 governance levels (none, partial, full govML templates), 5 random seeds = 45 conditions scored on a 10-point rubric.

**The surprise:** I predicted task complexity would be the biggest quality predictor. I was wrong. Governance level explains 55.7% of quality variance vs. 12.6% for task complexity. How you structure agent instructions matters 4x more than what you ask.

**The number:** Full governance produces 8.93/10 average quality vs. 5.47/10 without governance. That is a 3.5-point improvement (d = 2.58). The bootstrap CI excludes zero.

**The honest caveat:** This is simulated data, not live API calls. The evaluator uses structural keyword matching. A follow-up with live Haiku calls and human evaluation would strengthen these claims.

Read the full analysis with figures and methodology on the blog: [link]

Until next time,
Rex

---
*Securing AI from the architecture up.*
