# CONTENT PLAN — FP-16 Verified Delegation Protocol

> **Project:** FP-16 (Verified Delegation Protocol)
> **Created:** 2026-03-19
> **Status:** Blog drafted, conference abstract drafted, experiments pending API key

---

## Content Assets

| ID | Type | Title | Status | Target | Path |
|----|------|-------|--------|--------|------|
| C-01 | Blog post | Closing the 54% Gap | DRAFTED | rexcoleman.dev | `blog/draft.md` |
| C-02 | LinkedIn post | Verified Delegation Protocol | DRAFTED | LinkedIn | `blog/linkedin_post.md` |
| C-03 | Substack intro | Defense for multi-agent cascade | DRAFTED | Substack | `blog/substack_intro.md` |
| C-04 | Conference abstract | AISec Workshop (ACM CCS 2026) | DRAFTED | AISec | `blog/conference_abstract.md` |
| C-05 | TIL | "Defend LLMs with a DIFFERENT LLM" — cross-model advantage | PLANNED | dev.to | — |
| C-06 | TIL | "Signing alone doesn't help" — identity ≠ quality | PLANNED | dev.to | — |
| C-07 | TIL | "Adaptive rate limiting: the security feedback loop" | PLANNED | dev.to | — |
| C-08 | TIL | "7 hypotheses, 1 expected null: designing for honesty" | PLANNED | dev.to | — |
| C-09 | Thread | Twitter/X: FP-15 found the problem, FP-16 builds the defense | PLANNED | Twitter/X | — |

---

## Key Messages

1. **Static zero-trust is necessary but not sufficient.** Adaptive adversaries recover 54%.
2. **Cross-model verification is the architectural insight.** Different model = different blind spots.
3. **Identity matters less than output quality.** Signing alone is a null result (H-6).
4. **Defense-in-depth works.** Three layers, each independently ablatable.
5. **Design for rigor from day 1.** Gate 0.5 forced the right decisions before any code.
