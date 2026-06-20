# Systems Thinking — Skills

Reusable [Claude Code](https://claude.ai/claude-code) skills for systems thinking, drawn from the **AI + Systems Thinking** course (Empatika, Season 2026) by [Bayram Annakov](https://github.com/BayramAnnakov). Installable as a Claude Code plugin marketplace, also runnable as copy-paste mega-prompts in Codex / ChatGPT / Cursor.

The course is hands-on: participants draw stock-flow diagrams by hand, run live multiplayer simulations, and use these AI skills as a *critic, builder, and amplifier* — never as a designer. The skills enforce that pedagogy: they refuse to draw the diagram for you.

## Available skills

### `/ai-systems-coach` — Stock-flow diagram critic & archetype identifier *(ships with W2)*

**You draw the diagram. The skill grades it.**

Critiques a hand-drawn stock-flow / causal-loop diagram, identifies the system archetype (Limits to Growth, Shifting the Burden, Fixes that Fail), and surfaces Meadows leverage points. Outputs a Mermaid diagram, validates stocks, flags missing delays, prepares a clean stock-flow specification for Workshop 3 simulation.

Refuses to design a diagram from scratch, invent variables you didn't name, or force-fit an archetype.

**Example:**
```
/ai-systems-coach

Stock: Active Customers
Inflow: New signups (driven by referrals from Active Customers)
Outflow: Churn (driven by Service Quality, which drops past Capacity)
R: Active Customers → Referrals → New signups → Active Customers
B: Active Customers → Service Quality (delay 2 weeks) → Churn → Active Customers
```

### `/leverage-finder` — Map your model to Meadows' 12 leverage points *(ships with W4)*

**You bring a model and a goal. The skill returns 3 candidate interventions, ranked.**

Takes a stock-flow model you have already built and a measurable goal you have already stated, then maps elements of your model to Donella Meadows' 12 leverage points and returns the 3 highest-leverage candidate interventions for your goal.

The skill enforces the asymmetry lesson structurally: at least one of the 3 candidates must be at knob ≤5 (rules, info flow, goals, paradigm). Most teams reach for parameters (knob 12) first because they have numbers to tune; the skill forces you to consider stronger leverage you can't see as easily.

**Three structural rules:**
1. **Phase 0 gate** — no measurable goal, no output. The skill refuses to rank leverage without a stated purpose. "Improve the system" gets pushed back with three sharpening questions.
2. **No inventing structure** — only maps stocks, flows, and parameters the model already contains. Won't add elements the user didn't draw.
3. **Forced choice** — returns exactly 3 candidates, not a long list. Forcing the choice is part of the discipline.

Each candidate is formatted as: Meadows knob (number + name), what to change in the user's model, why it has leverage for the stated goal, one concrete experiment testable in 2 weeks, one caveat. Closes with an asymmetry paragraph noting which candidate is strongest and which feels most natural — those usually don't match.

**Refuses:** to invent stocks/flows/parameters not in the model, to write code, to march through all 12 leverage points as a checklist, to return more than 3 candidates.

### `/ai-stockflow-builder` — Commission a runnable simulation app *(ships with W3)*

**The skill emits a brief. Your AI agent (Claude Code or Codex) builds the app. You own the equations.**

Walks you from a stock-flow diagram (or `/ai-systems-coach` output) to an interactive single-HTML-file simulation web app with sliders, chart, and equation chips — via three phases:

1. **Readback** — skill reads your model back in plain English, surfaces ambiguity, forces ≥1 disagreement before any code
2. **Brief** — skill emits a copy-paste commissioning brief; you paste it into Claude Code or Codex; your agent builds `model.html` with React via CDN, Recharts, Euler integration with dt=1
3. **Extraction test** — you hand-compute t=1 from defaults and compare to the agent's app at t=1; mismatch = AI broke equations = stop and find where

If you don't have a diagram, **Phase 0 — Interview mode** asks Socratic questions and your answers become the model. The skill never proposes a stock or flow you didn't name.

**Two-pass discipline:**

| Pass | Caps |
|---|---|
| **Pass 1 (Simplified)** | exactly 1 stock, 2 flows, 2 parameters, ≤30 time steps, linear equations only — no `min()`, ternaries, or delays |
| **Pass 2 (Full)** | no caps; extends Pass 1 |

When your model violates a Pass 1 cap, the skill runs a **trim conversation** — it proposes which entities to drop, demote to constants, or defer to Pass 2. Pass 1 forces "minimum viable model" discipline; Pass 2 layers complexity. Most workshops use Pass 1 first, then Pass 2 as a follow-up.

**Refuses:** to write the app itself (your agent does), invent missing parameters, deploy, stylize, or run the simulation.

### `/constraint-finder` — Find the binding constraint (Theory of Constraints) *(ships with W6)*

**You bring a flow and a goal. The skill finds the ONE wall — and whether it's a resource or a rule.**

Takes a flow/process system and its goal, finds the single binding constraint, classifies it as a **resource** or (usually) a **policy**, and returns Goldratt's 5 Focusing Steps as concrete actions — Exploit and Subordinate *before* Elevate. This is the **"find the wall"** move.

The error it exists to kill: "find the slow thing and speed it up" — that's profiling, not ToC. The real constraint is almost never a machine; it's a rule, a metric, or an assumption.

**Structural rules:** a goal gate (no throughput unit, no output); a guard that refuses to force a single constraint on a demand-constrained or exploratory system; resource→policy promotion (default suspicion is a policy — far higher leverage than capacity); Exploit/Subordinate before Elevate (spending money first is the classic, costly ToC error); and Subordinate kept as the climax (fast resources must be *willing to sit idle*).

**Refuses:** to optimize a non-constraint, to Elevate before Exploit/Subordinate, to proceed without a goal, to call a policy constraint a resource, or to invent steps.

### `/triz-dissolve` — Dissolve a trade-off (TRIZ) *(ships with W6)*

**You bring a trade-off. The skill eliminates the contradiction — it doesn't balance it.**

Takes a trade-off ("improving X worsens Y") and dissolves it with TRIZ: reframe as a physical contradiction, state the Ideal Final Result, then scan the full 40 inventive principles + the 4 separation principles + resource analysis to generate genuinely different structural resolutions — each run through a dissolve-vs-relocate test. This is the **"move the wall"** move.

The LLM already knows TRIZ, so the skill doesn't re-teach it. It does two things: **enforces the discipline the LLM skips** (left alone it defaults to *compromise* and lets cost-relocations pass as solutions), and **directs it to use the full toolkit** ("you ARE the contradiction matrix" — reason over all 40 principles, don't cite hallucination-prone matrix cells).

**Structural rules:** refuse compromise ("find the optimal balance" is never an answer); a structure-vs-physics guard (don't fake a dissolution for a real law — optimize the honest compromise instead); and a dissolve-vs-relocate test on every resolution (did the cost leave the system, or just move to another team / a later time / tech debt?).

**Refuses:** to return a compromise, to present a relocation as a dissolution, to fake-dissolve a real physical law, or to name a principle without showing how it separates the demands.

The W6 pair is designed to compose: `/constraint-finder` locates the wall, `/triz-dissolve` moves it.

## Installation

The skills follow the [agentskills.io](https://agentskills.io) open standard — installable in both Claude Code and OpenAI Codex with the same `SKILL.md` files.

### Option 1: Claude Code plugin install

```
/plugin marketplace add BayramAnnakov/systems-thinking-skills
/plugin install ai-systems-coach@systems-thinking-skills
/plugin install ai-stockflow-builder@systems-thinking-skills
/plugin install leverage-finder@systems-thinking-skills
/plugin install constraint-finder@systems-thinking-skills
/plugin install triz-dissolve@systems-thinking-skills
/reload-plugins
```

### Option 2: Codex CLI

```bash
git clone https://github.com/BayramAnnakov/systems-thinking-skills.git ~/.agents/systems-thinking-skills
mkdir -p ~/.agents/skills
ln -s ~/.agents/systems-thinking-skills/skills/ai-systems-coach ~/.agents/skills/ai-systems-coach
ln -s ~/.agents/systems-thinking-skills/skills/ai-stockflow-builder ~/.agents/skills/ai-stockflow-builder
ln -s ~/.agents/systems-thinking-skills/skills/leverage-finder ~/.agents/skills/leverage-finder
ln -s ~/.agents/systems-thinking-skills/skills/constraint-finder ~/.agents/skills/constraint-finder
ln -s ~/.agents/systems-thinking-skills/skills/triz-dissolve ~/.agents/skills/triz-dissolve
```

Codex auto-discovers skills under `~/.agents/skills/`. See [Codex skills docs](https://developers.openai.com/codex/skills).

### Option 3: Clone + copy (any runtime)

```bash
git clone https://github.com/BayramAnnakov/systems-thinking-skills.git
# Claude Code:
cp -r systems-thinking-skills/skills/ai-systems-coach ~/.claude/skills/
cp -r systems-thinking-skills/skills/ai-stockflow-builder ~/.claude/skills/
cp -r systems-thinking-skills/skills/leverage-finder ~/.claude/skills/
cp -r systems-thinking-skills/skills/constraint-finder ~/.claude/skills/
cp -r systems-thinking-skills/skills/triz-dissolve ~/.claude/skills/
# Or Codex:
cp -r systems-thinking-skills/skills/ai-systems-coach ~/.agents/skills/
cp -r systems-thinking-skills/skills/ai-stockflow-builder ~/.agents/skills/
cp -r systems-thinking-skills/skills/leverage-finder ~/.agents/skills/
cp -r systems-thinking-skills/skills/constraint-finder ~/.agents/skills/
cp -r systems-thinking-skills/skills/triz-dissolve ~/.agents/skills/
```

### Option 4: Mega-prompt (no skills runtime — plain ChatGPT, Cursor, Claude.ai)

If your runtime doesn't support skills, copy the `PROMPT.md` from each skill's directory. Paste the block between `===PROMPT START===` and `===PROMPT END===` into your tool, then paste your model.

## Usage

```
/ai-systems-coach          # paste your hand-drawn diagram in structured form
/ai-stockflow-builder      # paste your model, or say "interview me" for Phase 0
/leverage-finder           # paste your model + measurable goal; get 3 ranked leverage candidates
/constraint-finder         # paste your flow + goal; find the binding constraint + the 5 focusing steps
/triz-dissolve             # paste a trade-off ("improving X worsens Y"); dissolve the contradiction
```

The W2 → W3 progression: run `/ai-systems-coach` after Workshop 2 to grade your archetype homework. Take its "Simulation prep" output and paste it into `/ai-stockflow-builder` after Workshop 3 to build the runnable app.

Both skills respond bilingually — they auto-detect English / Russian and use whichever you typed in.

## Course context

Part of the **AI + Systems Thinking** course (6 biweekly online sessions, 2026):

1. How Systems Work — stocks, flows, feedback, delays
2. **System Archetypes** — Limits to Growth, Shifting the Burden, Fixes that Fail *(ships `/ai-systems-coach`)*
3. **From Diagram to Simulation** — turning your diagram into runnable code *(ships `/ai-stockflow-builder`)*
4. **Goal of the Model + Meadows Leverage** — from "I have a model" to "I know which knobs matter" *(ships `/leverage-finder`)*
5. Optimization + MCP — connecting models to real data
6. **Theory of Constraints + TRIZ** — find the binding constraint, then dissolve the contradiction *(ships `/constraint-finder` + `/triz-dissolve`)*

More skills will land in this repo as later workshops ship.

## Pedagogical philosophy

These skills enforce a strict separation: **humans draw and own equations; AI critiques and builds infrastructure.** We don't ship AI tools for skills participants haven't first practiced manually. That's why:

- `/ai-systems-coach` ships with W2 (after archetypes are taught by hand) and refuses to design a diagram from scratch
- `/ai-stockflow-builder` ships with W3 (after stock-flow notation is taught) and refuses to invent equations the human didn't name
- `/leverage-finder` ships with W4 (after the goal-of-the-model and Meadows asymmetry are taught on cohort cases) and refuses to rank leverage without an explicit, measurable goal
- `/constraint-finder` and `/triz-dissolve` ship with W6 (after ToC and TRIZ are taught and practiced on a live commons game) and refuse, respectively, to optimize a non-constraint and to return a compromise

The skills also encode the workshop's force-disagreement mechanic. Both refuse to proceed if the user says "looks perfect" — they push back with units, polarity, periodicity, or threshold-vs-linear questions until the user has corrected something. Drawing and disagreeing *are* the act of thinking.

If you want to design from scratch, draw it on paper first. The friction *is* the lesson.

## License

MIT — see [LICENSE](LICENSE).
