# Answer-kinds & grading - the core of the rigor

This is what separates a Why Tree from a confident-sounding guess. **Every node gets three tags: an answer-kind, a confidence grade, and a citation.** The answer-kind tells the reader *what kind of thing they're trusting* before they decide how much to trust it.

## The seven answer-kinds

| Kind | Chip | Means | Test before you assign it |
|------|------|-------|---------------------------|
| **MEASURED** | green | A hard number from real data, with an n. "64% of new workspaces add a 2nd member (n=820)." | Is there an actual count/rate behind it? What's the n and the window? |
| **INSTANCE** | amber | A specific observed example, n=1-few. "One new workspace was created with no teammate invited." | Is this one case (or a handful), not a rate? Don't generalize it. |
| **EXTERNAL** | blue | A third-party / industry fact not about this system. "Gmail's complaint ceiling is 0.3%." | Is it from outside the system, and is the source named? |
| **CLAIM** | red | A stakeholder assertion, unverified. "~20 signups/day." | Did a person say it without data? Flag contradictions (e.g. another source implies ~2/day = 10x gap). |
| **INFERENCE** | purple | Logic built on measured premises. "92% never invite a teammate, so the surface is mis-positioned." | Are the premises MEASURED? Is the logical step valid, or is there a hidden third factor? |
| **HYPOTHESIS** | gold-dashed | A testable proposition not yet tested. "Users finish the invite step in the UI by preference." | Can you name the exact test that would settle it? If not, it's not even a hypothesis. |
| **FRAMING** | grey | A restatement of the problem itself, a lens. The apex is always FRAMING. | Is this a way of *seeing* the problem rather than a cause? |

**The decisive insight:** the nodes that *locate the constraint* are often the HYPOTHESIS ones - exactly the part that's unmeasured. A tree that's "~45% MEASURED" can still be shallow at the decision point if the 20% that would pin the constraint is all HYPOTHESIS. The census (below) exists to catch this.

## Confidence grade (orthogonal to kind)

Independent of *what kind* of evidence it is, how strong is it?

- **Strong** - robust within its kind (large n, clean source, tight logic).
- **Mod** - real but limited (small n, single window, one source).
- **Weak** - thin, suggestive only.

A node can be `MEASURED / Weak` (real number, tiny n) or `EXTERNAL / Strong` (well-established third-party fact). State both. A common honest tag is `CLAIM / Strong-that-it's-unverified` - we're sure someone said it, unsure it's true.

## Role badges (assigned during convergence, Phase 2 step 5-6)

| Role | Means |
|------|-------|
| **ROOT** | A point where branches converge - a root cause (label R0/R1...). |
| **CONSTRAINT?** | A candidate for THE system constraint. Exactly one should end up as THE constraint. |
| **LEVER** | A fixable point with good leverage. |
| **NEGATIVE** | A fix that would backfire - kept in the tree as a warning. |
| **REFUTED** | Killed by the adversarial pass - kept visible with the killing evidence. |
| **DOWNGRADED** | Survived but demoted (e.g. "blocker -> friction reducer") with the evidence that demoted it. |
| **critic-added** | Surfaced by the refute/critic pass, not the original fan-out. |

## Citation rules

- Every non-FRAMING node names its source: a file+section (`What_We_Learned §5`), a query result (`n=6 sends, 7-day window`), a URL, or a named stakeholder.
- MEASURED nodes must state the **n and the window** - "45% (n=820, Mar 3-9)", never a bare percentage.
- If a node's only source is one person, it's a CLAIM, not MEASURED - no matter how confident they sounded.
- A HYPOTHESIS with no nameable test is not allowed - either find the test or drop the node.
- **Measurable-in-hand rule (decisive):** a node is NOT a HYPOTHESIS or CLAIM if one query/read over evidence you have ALREADY pulled would settle it. Run the check and grade it MEASURED. Distinguish two flavors of "unmeasured": *measurable-in-hand* (you just didn't look — go look, now) vs *genuinely-external* (needs new data you don't have). Only the latter may stay HYPOTHESIS and become a cheapest-test; the former is a research gap, not a real unknown. (Real example: "why activators stop before the 50-seat wall" was left HYPOTHESIS when the items-per-account *distribution* — which answers it — was one `GROUP BY` away in a table already queried.)
- **Threshold needs its distribution:** a node that makes a causal claim about why people don't cross a threshold (≥N, hit-the-wall) needs the **distribution** of the underlying quantity, not just the threshold count. Without it, the claim is at best INFERENCE/Weak — "83% never reached 50" cannot tell "satisfied at 48" from "bounced at 5."

## The evidence census (Phase 4)

Tally the answer-kind mix and write the honest bottom line. Template:

> ~X% MEASURED (but note the window/n caveat) · ~Y% INFERENCE · ~Z% HYPOTHESIS - **and the constraint-locating nodes are in the HYPOTHESIS bucket.** So: broad but shallow at the decision point. Headline = "where to look," not "here's the verdict." The #1 cheapest-test targets exactly those HYPOTHESIS nodes.

If instead the decisive nodes are MEASURED/Strong, say so - then the tree *is* a verdict, and the recommendation can be "act," not "test first."
