# LinkedIn Post — Verified Delegation Results

> Blog link as FIRST COMMENT.

---

I built a 3-layer defense for multi-agent AI systems and pre-registered 7 hypotheses predicting 70% poison reduction.

Real agent experiments refuted 5 of 7. The defense doesn't work.

Here's what actually happened:

Our simulation predicted 97% poison rate. Real Claude agents: 49%. The simulation was wrong by 48 percentage points.

The LLM-as-judge component makes things WORSE — false positives blocking legitimate outputs outweigh true positives catching attacks.

A judge-aware adversary achieves 100% poison. If the attacker knows your defense exists, it's already defeated.

The dumbest component — rate limiting, no semantic understanding — worked best (-6pp).

What the refutations narrow down:

1. LLM-as-judge is not viable for delegation verification
2. Cascade simulations don't predict real agent behavior
3. Real LLMs have inherent resistance that simulations miss
4. Rate limiting > semantic verification for cascade defense

7 pre-registered hypotheses, 5 honestly refuted. That's what designing for rigor from day 1 looks like.

Framework is open source.

What multi-agent defense approach is your team exploring?

#AISecurity #NegativeResults #MultiAgent #HonestResearch #BuildInPublic
