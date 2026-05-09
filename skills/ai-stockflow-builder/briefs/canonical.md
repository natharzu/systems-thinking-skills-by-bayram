# Commissioning Brief — Canonical Template

This is the template Phase B of the skill emits. The skill fills in the `<<placeholder>>` blocks with the user's confirmed model from Phase A, then emits the whole thing as a single copy-paste block.

---

## Copy from here ↓

```
You are commissioning your AI coding agent (Claude Code or Codex) to build an interactive stock-flow simulation web app of MY model. Below is the brief. Build exactly what's specified — do not free-style architecture, do not add features I didn't ask for.

# ROLE

You are a frontend/JS engineer. I am the modeler. I own the equations; you own the infrastructure (HTML, React rendering, slider wiring, chart rendering). When in doubt about an equation, STOP and ASK. When in doubt about a layout choice, MAKE IT and we'll iterate.

# MY MODEL

Title: <<short title, e.g., "Support ticket backlog with hire-step">>

Time unit: <<weeks | months | quarters | years>>
Time horizon: <<integer, e.g., 52>>
Integration: Euler, dt = 1

## Stocks (initial values)

- <<StockName1>>: <<initial number>>  // units: <<units>>
- <<StockName2>>: <<initial number>>  // units: <<units>>

## Flows (rate equations)

- <<FlowName1>>: from <<StockName | null>> to <<StockName | null>>
  rate = <<equation in JS expression form, referring to stock and parameter names directly>>
  units: <<units, must be quantity-per-time>>

- <<FlowName2>>: from <<StockName | null>> to <<StockName | null>>
  rate = <<equation>>
  units: <<units>>

## Parameters (sliders)

- <<ParamName1>>: default <<number>>, min <<number>>, max <<number>>, step <<number>>
  label: "<<short human label, ≤20 chars>>"
  units: <<units>>

- <<ParamName2>>: default <<number>>, min <<number>>, max <<number>>, step <<number>>
  label: "<<short human label>>"
  units: <<units>>

## Reference mode

<<one or two lines describing how the primary stock has actually behaved historically and where I want it to go. The chart should be reasonable to compare against this.>>

# DELIVERABLE

A SINGLE HTML file named `model.html`. No build step, no npm install. React via CDN (esm.sh). Recharts via CDN. The file MUST run by simply opening it in a browser (file://) — no dev server required.

## Layout

```
+-----------------------------------------------+
|  <<title>>                                    |
+-----------------------------------------------+
|  [SVG diagram: stocks as boxes,               |
|   flows as arrows with labels]                |
+-----------------------------------------------+
|  [Recharts LineChart of primary stock         |
|   over time, plus secondary stock dashed]     |
+-----------------------------------------------+
|  Slider: <<ParamName1>> [——●——] 50            |
|  Slider: <<ParamName2>> [——●——] 4             |
|  ...                                          |
+-----------------------------------------------+
|  Equation chips (one per flow):               |
|  "<<FlowName1>>: <<equation as text>>"        |
+-----------------------------------------------+
```

## Iron constraints

1. **Equations are EXACTLY what's in MY MODEL above.** Do not add `+1`, do not introduce smoothing, do not add randomness. If an equation looks wrong to you, STOP and ASK me — do not "fix" it.
2. **Every stock is clamped at zero on each step.** If a flow would push a stock negative, clamp to 0 and `console.warn` the flow name and time step. <<IF MAX-CLAMP REQUIRED: Stock <<X>> additionally clamps at <<max value>>; same warn behavior.>>
3. **Slider min/max/default come from MY MODEL above.** Do not invent ranges.
4. **Use Euler integration with dt = 1.** Each step: `new_stock = max(0, old_stock + (sum_inflows - sum_outflows) * dt)`. Order of operations: compute all flows from current state first, THEN update all stocks. (Do not update stocks in mid-step — that gives wrong dynamics.)
5. **Time-conditional convention.** When equations contain time-conditional expressions like `(t < HireWeek ? A : B)`, the threshold fires INCLUSIVELY at `t = HireWeek`. So at `t = HireWeek - 1` the condition is true (uses A); at `t = HireWeek` the condition is false (uses B). State this explicitly in a comment near the equation.
6. **Chart redraws live as sliders move.** Use React state, recompute the full simulation on every slider change (it's cheap for <100 time steps).
7. **No external state, no localStorage, no URL params.** This is a single-screen tool. Sharing comes later.
8. **Equation chips show the literal equation string from MY MODEL.** They are read-only; this is the human-readable proof that the code matches the spec. Render in modeler-friendly notation if possible — e.g., `Resolutions = min(Backlog, agents(t) * Throughput)` with a side-note `agents(t) = StartAgents if t < HireWeek else EndAgents`. Avoid raw JS ternaries in chip text if a clearer form exists.
9. **Companion test files allowed.** You may produce one `test_sim.{mjs,js}` file (or similar) that imports/inlines the simulation logic and asserts the extraction-test value. Do NOT produce alternate `model.html` variants (no Vite version, no Vue version).

## Stack

- React 18 from `https://esm.sh/react@18`
- ReactDOM 18 from `https://esm.sh/react-dom@18/client`
- Recharts from `https://esm.sh/recharts@2`
- No bundler. No TypeScript. Plain `.html` with one `<script type="module">` block.

# EXTRACTION TEST (you must pass before declaring done)

In a comment block at the top of the script, INCLUDE the hand-computed expected value of the primary stock at t=1 using default parameters. After implementing, run the simulation in a headless browser or by opening the file and verify the chart's value at t=1 matches the comment to within 0.01.

If the values do not match, STOP. Do not declare done. Show me the diff and we'll find where the equations diverged.

Example comment block:
```
// EXTRACTION TEST
// Defaults: Backlog=200, ArrivalRate=50, Throughput=30, StartAgents=1
// At t=0: Backlog=200
// Flows at t=0: Arrivals=50, Resolutions=min(200, 1*30)=30
// At t=1: Backlog = max(0, 200 + 50 - 30) = 220
// EXPECTED Backlog[1] = 220
```

# OUTPUT

When you're done, give me ONE thing:
1. The path to `model.html` (and open it in my browser if you can)

Do NOT also give me a Vite version, a Vue version, a Streamlit version, or a Python version. One file. One framework choice. Done.

# IF SOMETHING IS UNCLEAR

Ask me ONE question at a time. Do not paraphrase the spec back at me — I wrote it. Ask only about things genuinely missing or contradictory in MY MODEL above.
```

## ↑ Stop copying here

---

## Notes for the skill (not part of the brief)

- The skill fills in `<<placeholders>>` with the confirmed model from Phase A.
- For one-stock models, the secondary-stock dashed line is omitted from layout.
- For models without ranges on a parameter, the skill must ask the user for ranges in Phase A — the brief cannot ship with `min: TBD`.
- Equation chips intentionally show the *literal string* from MY MODEL, NOT the JS-compiled version. This is the Bret Victor authorship loop: the human can verify the agent transcribed correctly by reading one chip.
- The extraction test comment block forces the agent to do the math BEFORE wiring up the UI — catches dynamics-update-order bugs early.
