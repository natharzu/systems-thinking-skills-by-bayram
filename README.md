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

## Installation

The skills follow the [agentskills.io](https://agentskills.io) open standard — installable in both Claude Code and OpenAI Codex with the same `SKILL.md` files.

### Option 1: Claude Code plugin install

```
/plugin marketplace add BayramAnnakov/systems-thinking-skills
/plugin install ai-systems-coach@systems-thinking-skills
/plugin install ai-stockflow-builder@systems-thinking-skills
/reload-plugins
```

### Option 2: Codex CLI

```bash
git clone https://github.com/BayramAnnakov/systems-thinking-skills.git ~/.agents/systems-thinking-skills
mkdir -p ~/.agents/skills
ln -s ~/.agents/systems-thinking-skills/skills/ai-systems-coach ~/.agents/skills/ai-systems-coach
ln -s ~/.agents/systems-thinking-skills/skills/ai-stockflow-builder ~/.agents/skills/ai-stockflow-builder
```

Codex auto-discovers skills under `~/.agents/skills/`. See [Codex skills docs](https://developers.openai.com/codex/skills).

### Option 3: Clone + copy (any runtime)

```bash
git clone https://github.com/BayramAnnakov/systems-thinking-skills.git
# Claude Code:
cp -r systems-thinking-skills/skills/ai-systems-coach ~/.claude/skills/
cp -r systems-thinking-skills/skills/ai-stockflow-builder ~/.claude/skills/
# Or Codex:
cp -r systems-thinking-skills/skills/ai-systems-coach ~/.agents/skills/
cp -r systems-thinking-skills/skills/ai-stockflow-builder ~/.agents/skills/
```

### Option 4: Mega-prompt (no skills runtime — plain ChatGPT, Cursor, Claude.ai)

If your runtime doesn't support skills, copy the `PROMPT.md` from each skill's directory. Paste the block between `===PROMPT START===` and `===PROMPT END===` into your tool, then paste your model.

## Usage

```
/ai-systems-coach          # paste your hand-drawn diagram in structured form
/ai-stockflow-builder      # paste your model, or say "interview me" for Phase 0
```

The W2 → W3 progression: run `/ai-systems-coach` after Workshop 2 to grade your archetype homework. Take its "Simulation prep" output and paste it into `/ai-stockflow-builder` after Workshop 3 to build the runnable app.

Both skills respond bilingually — they auto-detect English / Russian and use whichever you typed in.

## Course context

Part of the **AI + Systems Thinking** course (6 biweekly online sessions, 2026):

1. How Systems Work — stocks, flows, feedback, delays
2. **System Archetypes** — Limits to Growth, Shifting the Burden, Fixes that Fail *(ships `/ai-systems-coach`)*
3. **From Diagram to Simulation** — turning your diagram into runnable code *(ships `/ai-stockflow-builder`)*
4. Theory of Constraints — finding your bottleneck
5. FishBanks — live competitive market simulation
6. From Understanding to Transformation — meta-framework

More skills will land in this repo as later workshops ship.

## Pedagogical philosophy

These skills enforce a strict separation: **humans draw and own equations; AI critiques and builds infrastructure.** We don't ship AI tools for skills participants haven't first practiced manually. That's why:

- `/ai-systems-coach` ships with W2 (after archetypes are taught by hand) and refuses to design a diagram from scratch
- `/ai-stockflow-builder` ships with W3 (after stock-flow notation is taught) and refuses to invent equations the human didn't name

The skills also encode the workshop's force-disagreement mechanic. Both refuse to proceed if the user says "looks perfect" — they push back with units, polarity, periodicity, or threshold-vs-linear questions until the user has corrected something. Drawing and disagreeing *are* the act of thinking.

If you want to design from scratch, draw it on paper first. The friction *is* the lesson.

## License

MIT — see [LICENSE](LICENSE).
