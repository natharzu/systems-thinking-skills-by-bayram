# Leverage Finder — Test cases

Pre-workshop validation. Each case is a real cohort participant from W3 + Office Hours #1. Tests verify (a) skill respects the goal-gate, (b) returns sensible Meadows mappings, (c) doesn't invent structure.

---

## Test 1: Andrey — Delegation model (from OH#1, lines 4:40-25:48)

### Input

**Goal candidate (Andrey's own framing):** "Перенести 60% рабочего времени в принятие решений (а не в исполнение) — к концу года."

**Model (paraphrased from OH#1):**
- Stocks: cognitive_resource (current ~ 50), team_competence, in_flight_projects, delegated_tasks_quality
- Flows:
  - delegation_rate (currently low — Andrey delegates at threshold "8"; lower threshold = more delegation)
  - training_rate (3 hours/week → team_competence)
  - new_unique_projects_intake (currently active; Andrey concluded: stop taking these)
- Parameters: delegation_threshold (currently 8, Andrey wants 2), training_hours_per_week (3), uniqueness_filter
- Feedback loops: lower threshold → more delegation → if competence low → reputation hit → cognitive load increases (balancing loop B1); training → competence → reduces oversight need → cognitive resource recovers (reinforcing loop R1)
- Encoded goal in model: NONE (this is Andrey's gap — he derived actions without explicit goal sentence in the model)

### Expected skill output

**Phase 0 check:** Goal is measurable (60%, time-bound to "by end of year"). Passes gate.

**3 candidates:**

**LEVERAGE CANDIDATE #1**
Meadows knob: 3 (Goals of the system)
What to change: Add an explicit goal node to the model: "decision-mode hours / total hours ≥ 0.6 by week 52". Currently the model optimizes implicitly for "task throughput". Re-anchor on decision-mode fraction.
Why it has leverage: Without the goal in the model, every parameter tweak (threshold, training hours) is solving a different optimization problem than the one Andrey actually wants. Once the goal is encoded, the model will reveal that lowering threshold below ~4 hits diminishing returns because the bottleneck shifts to team_competence growth rate.
What to test: Re-run the simulation with explicit goal function. Observe which parameter most increases the goal function under realistic constraints. (2 weeks: rebuild model + 2 scenarios.)
Caveat: Re-encoding the goal may reveal that Andrey's current solution (threshold = 2) is locally good but globally suboptimal — uncomfortable but informative.

**LEVERAGE CANDIDATE #2**
Meadows knob: 5 (Rules of the system)
What to change: The rule "new unique projects taken into pipeline" — currently filtered by Andrey's intuition. Replace with explicit rule: "no new unique project unless current pipeline competence-coverage ≥ X."
Why it has leverage: Andrey already concluded "stop taking unique projects" — but as a one-off decision, not a rule. Encoded as a rule, it doesn't depend on his discipline week to week. Rule-level changes (knob 5) outlast personality.
What to test: For 2 weeks, write the rule down and apply it to every inbound project. Track: how many projects declined, how that affects cognitive_resource over 14 days.
Caveat: This rule has revenue impact. Andrey should know what revenue threshold he's willing to forgo.

**LEVERAGE CANDIDATE #3**
Meadows knob: 12 (Parameters)
What to change: training_hours_per_week (currently 3). Andrey's conclusion: bring to 3+. Could test 4 or 5 hours/week.
Why it has leverage: Direct lever, easy to change. But weakest of the three — training_hours feeds team_competence which feeds delegation_quality, with a 20-week delay. Acting only here means waiting 20 weeks for any signal.
What to test: Increase training to 5h/week for 2 weeks. Will not move cognitive_resource in 2 weeks (delay too long), but Andrey can measure: did team_competence indicators (project_quality, escalation_rate) move?
Caveat: Don't act ONLY here. The delay makes this the slowest of the three candidates. Combine with candidate #2.

**Asymmetry paragraph:**
Notice that candidate #1 (knob 3 — goal) is the strongest but feels least like an "action" — it's a re-encoding, not a tweak. Candidate #3 (knob 12 — parameter) is the most natural to reach for and the weakest. Most founders default to "more training" or "lower threshold" because those have numbers. The Meadows lesson is that the goal-encoding (candidate #1) reorganizes which parameters even matter. You already concluded "delegate more, train more, no unique projects" — that's good intuition. The question is whether your model can prove it, or whether re-encoding the goal would show a different answer. Pick the lever that scares you a little.

### Pass criteria
- ✅ Phase 0 gate respected (goal was measurable, skill proceeded)
- ✅ 3 candidates with at least one at knob ≤5 (got #1=knob 3, #2=knob 5)
- ✅ At least one testable in 2 weeks (#2 and #3 both are)
- ✅ No invented structure (all elements come from Andrey's OH#1 description)
- ✅ Asymmetry paragraph tailored, not boilerplate

---

## Test 2: Marfa — 1k active users (from OH#1, lines 15:57-66:00)

### Input

**Goal candidate:** "1000 active users by month 3."

**Model (paraphrased from OH#1):**
- Stocks: active_users (current low), potential_pool (assumed large), marketing_budget (constraint)
- Flows: acquisition_rate (funded by marketing_budget), activation_rate (potential → active), churn_rate
- Parameters: budget_per_channel (channel mix), content_units_per_week, conversion_rate
- Feedback loops: NOT EXPLICITLY ENCODED in Marfa's model — Bayram in OH#1 suggested adding financial_result as second stock for trade-off
- Encoded goal: "1000 active users" — but no economic constraint

### Expected skill output

**Phase 0 check:** Goal is measurable and time-bound. BUT — Bayram noted in OH#1 that Marfa also implicitly cares about cost ("я наверное хочу тратить не больше стольки-то на маркетинг"). Skill should flag this.

The skill should output something like:
> "Goal accepted: '1000 active users by month 3.' Note: your model currently has no economic constraint, but in OH#1 you mentioned a budget cap. Two paths: (a) keep goal as-is, treat budget as a hard ceiling; (b) extend goal to '1000 active users with positive unit economics by month 3.' Path (b) changes the leverage analysis significantly. Pick one." [AskUserQuestion]

Assume Marfa picks (b).

**Updated goal:** "1000 active users by month 3, with positive unit economics."

**3 candidates:**

**LEVERAGE CANDIDATE #1**
Meadows knob: 3 (Goals of the system)
What to change: Just by adding "+ positive unit economics" to your goal, your model's leverage structure changes. Previously, "more budget → more users" was always positive leverage. Now, channel cost-per-user becomes a constraint, and high-cost paid channels look worse than organic. Re-rank your channels against the new goal.
Why it has leverage: This is the goal-redefinition move from Office Hours #1. You don't need new data or a new model — you need the model to optimize for the goal you actually have, not the simpler one.
What to test: For 2 weeks, track cost-per-active-user per channel. Reallocate at least one budget unit from the highest-cost channel to the lowest-cost. Measure: did total active users grow OR shrink with the same total budget?
Caveat: Organic channels often have longer delays than paid. Two weeks may not show the full effect.

**LEVERAGE CANDIDATE #2**
Meadows knob: 5 (Rules)
What to change: The acquisition rule. Currently your model assumes acquisition_rate = f(budget). Add a rule: "no spend on a channel with cost-per-user > X for 4 weeks running." This is a stopping rule that prevents structural overspend on weak channels.
Why it has leverage: Rules-level (knob 5) discipline is stronger than parameter tweaks because it doesn't rely on you re-checking allocations weekly. It enforces the new goal even when attention drifts.
What to test: Write down your X threshold. Apply for 2 weeks. Track: how many channels would have been cut by this rule retroactively?
Caveat: Threshold X depends on your unit economics. Don't pick X by intuition — derive it from your gross margin.

**LEVERAGE CANDIDATE #3**
Meadows knob: 12 (Parameters)
What to change: content_units_per_week — direct parameter. Increase from current to 2x.
Why it has leverage: Direct lever, you control it. But weakest — assumes the conversion_rate per content unit stays constant, which it usually doesn't (saturation). Useful as a fast feedback signal, not as primary strategy.
What to test: 2 weeks at 2x content output. Track active_users AND cost-per-user. If cost-per-user rises (saturation), pull back.
Caveat: Without changing the goal (#1) or the rule (#2), more content just amplifies whatever the current channel mix is doing — including its mistakes.

**Asymmetry paragraph:**
Candidates #1 and #2 are strong (goal and rule levels — knob 3 and knob 5). #3 is the weakest but the one you're most likely to reach for first because it has a number to double. Notice: in Office Hours yesterday, you said "I want to play with where to put the money" — that is exactly the knob-12 instinct. The Meadows lesson is that "where to put money" matters much less than "what is money supposed to buy" (knob 3) and "when do we stop buying" (knob 5). Pick the lever that scares you a little — for you that's probably writing down the unit-economics threshold.

### Pass criteria
- ✅ Phase 0 gate flagged the implicit economic constraint
- ✅ 3 candidates with at least one at knob ≤5
- ✅ All testable in 2 weeks
- ✅ No invented structure (the financial_result stock was suggested by Bayram in OH#1 — skill could mention it but didn't have to invent it)
- ✅ Asymmetry paragraph references Marfa's actual OH#1 quote

---

## Test 3: Failed goal gate (negative test)

### Input

**Goal:** "Improve the system."

### Expected behavior

Skill MUST refuse to produce ranking. Output:
> "Your goal 'improve the system' is not measurable. I can't rank leverage without knowing what to maximize or minimize. Three questions:
> 1. Improve along which axis? (number of users? speed? quality? cost?)
> 2. By when? (4 weeks? 6 months?)
> 3. With what constraint? (budget cap? quality floor? compliance limit?)
>
> Pick one of:
> - 'Help me sharpen this' (I'll ask the three questions and draft a goal)
> - 'I'll come back with a sharper goal'"

### Pass criteria
- ✅ No leverage candidates produced
- ✅ Skill offers structured help, doesn't just refuse and stop

---

## Test execution notes (for Bayram pre-workshop)

Run all three tests in:
1. Claude Code with `/leverage-finder`
2. ChatGPT (free tier) with PROMPT.md pasted
3. Claude.ai (free tier) with PROMPT.md pasted

Verify:
- Phase 0 gate triggers on Test 3 in all three runtimes
- Tests 1 and 2 produce 3 candidates with at least one at knob ≤5
- No runtime invents stocks/parameters not in the original model
- Output is readable on mobile (paste it into Telegram and look at it on phone)

**Time budget for this validation: 25 min total. If any runtime fails: drop PROMPT.md from the workshop and require Claude Code or Claude.ai (both passed in W3).**
