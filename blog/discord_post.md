# For: OpenClaw Discord

I tried building a defense for agent-to-agent delegation — LLM-as-judge + crypto signing + rate limiting. pre-registered 7 hypotheses. tested on real Claude agents. 5 hypotheses refuted. the full protocol actually made things worse.

```
                        poison rate    vs baseline
no defense              0.517          —
full protocol           0.539          +2pp (worse)
judge only              0.550          +3pp (worse)
signing only            0.483          -3pp
rate limit only         0.456          -6pp (best)

judge-aware adversary:  100% compromise
```

the LLM-as-judge actively hurts because false positives dominate — it flags legitimate delegations and passes attacks that look like valid analysis. a judge-aware adversary hits 100% by embedding attacks in properly structured output.

for OpenClaw: if you're thinking about adding verification layers between agent delegations, don't start with the smart stuff. rate limiting (capping how many tasks an agent can delegate per heartbeat cycle) worked best. crypto signing of delegation chains helped slightly. the LLM judge was net-negative.

the dumbest, most mechanical defense won. that's actually good news for tool policies — simple rate limits and structural constraints in your OpenClaw config are more effective than sophisticated AI-based validation.

what this means practically: if agent A delegates to agent B, limit delegation frequency, require signed context, skip the judge layer. keep your tool policies mechanical, not intelligent.

has anyone implemented delegation rate limits in OpenClaw configs? what does the current trust model look like for inter-agent task passing?
