# Leverage Finder

A light skill for Workshop 4 of the AI + Systems Thinking course. Takes a stock-flow model and a measurable goal, returns the 3 highest-leverage candidate interventions mapped to Donella Meadows' 12 leverage points.

## Files

- `SKILL.md` — the skill for Claude Code (place in `.claude/skills/leverage-finder/` or equivalent)
- `PROMPT.md` — copy-paste version for ChatGPT, Claude.ai, Perplexity (any LLM without Claude Code)
- `test-cases.md` — validation cases (Andrey delegation, Marfa 1k-users, negative goal-gate test)

## Install (Claude Code)

```bash
mkdir -p ~/.claude/skills/leverage-finder/
cp SKILL.md ~/.claude/skills/leverage-finder/
```

Then invoke: `/leverage-finder` in any Claude Code session.

## Use (ChatGPT / Claude.ai / Perplexity)

Open `PROMPT.md`. Copy the entire block under "---". Paste into your LLM. Replace `[YOUR GOAL]` and `[YOUR MODEL]` with your content. Send.

## Design constraints (do not modify)

- **Phase 0 gate.** Skill refuses to proceed without a measurable, time-bound goal. This is the foundational structural move from Sterman + Meadows.
- **3 candidates, no more.** Forcing the choice is part of the discipline. If you want a longer list, this is not the right skill.
- **At least one candidate at knob ≤5.** The asymmetry lesson. Without this rule, the skill defaults to safe parameter tweaks (knob 12).
- **No invented structure.** The skill maps and ranks what's there. If the user's model is missing critical elements, the skill flags it, doesn't fill it in.

## Anti-patterns this skill prevents

- Marching through all 12 leverage points as a checklist (Meadows refused to call ready, in council)
- Returning leverage analysis on a goalless model (Sterman refused)
- Returning >3 candidates because "the user might want options" (Marfa refused — she said she needs the choice forced)
