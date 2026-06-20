# Why Tree

A heavyweight, **agentic** Goldratt Current-Reality Tree. Point it at a hard, contested problem and it fans **20-55 AI agents** across the problem's branch-space, **grades every node by the kind of evidence behind it** (MEASURED / INFERENCE / CLAIM / HYPOTHESIS …), **tries to refute its own load-bearing branches**, and **converges on the ONE system constraint** — plus the negative branches (fixes that backfire) and the single cheapest test that would fork-decide. Output: a self-contained **interactive HTML tree** + a one-page **decision doc**.

This is the **"build the evidence and find the wall"** move. Its siblings: `/constraint-finder` is the lightweight coach that returns Goldratt's **5 Focusing Steps** once you already know the constraint; `/triz-dissolve` is the **"move the wall"** move. The natural chain is **why-tree → constraint-finder**: this skill *locates and evidences* the constraint on a messy problem; constraint-finder tells you what to *do* about it.

> **5-Whys grown up.** Naive root-causing follows a single thread, stops at the first plausible cause, and cites nothing. A Why Tree searches the *whole* branch-space in parallel, grades every node, refutes before it trusts, and forces convergence to one constraint. If you ship five co-equal "root causes," a tidy single-thread chain, or a confident verdict built on unmeasured nodes — you did it wrong.

## ⚠️ This is not a copy-paste prompt skill

Unlike the other skills in this repo, why-tree's **engine is multi-agent** — it requires **Claude Code's `Workflow` tool** (parallel fan-out + independent refutation) and broad tool access (it reads the files/DBs you point it at, and the web). `PROMPT.md` is a **degraded single-context** version for runtimes without a multi-agent harness: it keeps the discipline (grade every node, refute, converge to one, honest census) but loses the parallel branch-space and the *independent* adversarial refutation that are the whole point. For the real thing, run it in Claude Code.

## Files

- `SKILL.md` — the skill (phased workflow). Place the **whole folder** in `~/.claude/skills/why-tree/` — it needs `references/` and `assets/`, not just `SKILL.md`.
- `references/methodology.md` — Goldratt CRT, the WHY-branch logic, CLR audit, constraint location, Evaporating Cloud.
- `references/answer-kinds.md` — the evidence taxonomy + grading rubric + citation rules (the core of the rigor).
- `references/workflow-template.md` — the copy-paste `Workflow` blueprint + the strict tree-JSON schema.
- `assets/tree-template.html` — the reusable interactive visualization ("The Diagnostician's Bench").
- `assets/sample-tree.html` — a non-confidential worked example (synthetic SaaS).
- `council-viz-design.md` — the 5-voice design rationale for the visualization (Goldratt / Feynman / Tufte / Victor / Minto).
- `tests/` — a zero-token plumbing harness + fixtures.
- `PROMPT.md` — the degraded single-context version for ChatGPT / Claude.ai / Cursor.

## Install (Claude Code)

```bash
# copy the whole folder — references/ and assets/ are required
cp -R skills/why-tree ~/.claude/skills/why-tree
```

Then invoke `/why-tree` (or just describe a hard "why are we falling short of X" problem). It will **gate on a depth choice and state the token cost before launching** — don't skip the gate.

## Use (ChatGPT / Claude.ai / Cursor)

Open `PROMPT.md`, copy the block between `===PROMPT START===` and `===PROMPT END===`, paste your problem + any evidence you can give it. You get a single-context CRT with the grading/refute/converge discipline — but not the parallel multi-agent rigor.

## Token honesty (read before launching)

Multi-agent and token-heavy by design. **Standard ≈ 20-36 agents (~1-1.8M tokens); Deep ≈ 30-55 agents (~1.5-2.7M).** The skill states this and asks for a depth before it launches. **When NOT to use it:** a clear-cut problem a single careful pass would nail — just ask one agent. The machinery only earns its cost when **one mind could confidently pick the wrong cause** (cohort/measurement traps, several plausible roots, a mechanism hidden under a symptom, more branches than one context holds).

## Design constraints (do not modify)

- **Depth + token-cost gate.** Never launch the expensive tier without stating the cost and getting a depth choice. The gate is the skill's conscience.
- **Branch-space first, depth second.** Map *all* the candidate "why"s from many independent lenses before deepening any one.
- **Grade every node.** Answer-kind + confidence + citation on every node. Ungraded assertions are banned. A HYPOTHESIS must name the test that would settle it.
- **Refute before trust.** Load-bearing branches face an independent adversarial pass; killed branches stay visible *with the evidence that killed them*. (A degraded/skipped refute pass is the most dangerous failure — the engine warns loudly if it runs on zero branches.)
- **Converge to ONE.** 3-5 roots, one located system constraint — often a **policy/ownership** problem wearing a tooling costume.
- **The apex is a STATEMENT, not a question**, and never a smuggled solution ("why don't we have feature Y" biases the whole tree).
- **Honest census.** If the decisive nodes are still HYPOTHESIS, the headline is "a map of where to look, not a verdict," and the cheapest test targets exactly those nodes.
- **The tree must be a multi-LEVEL tree** — the constraint branch drills to bedrock as a visible chain, not a one-line root.

## Anti-patterns this skill prevents

- A single-thread 5-Whys chain with a tidy bottom (no branching, no refutation = not a tree).
- "Five key root causes" with no convergence to one constraint.
- A confident verdict resting on HYPOTHESIS-graded nodes, with no census disclosing it.
- Deleting refuted branches instead of keeping them with their killing evidence.
- Running the full multi-agent workflow on a clear-cut problem a single agent would nail.
- Smuggling the answer into the apex (a problem framed as a missing solution).
