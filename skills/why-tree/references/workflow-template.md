# Workflow blueprint - the engine

This is the copy-paste `Workflow` script that powers Phase 2. It fans out lenses, dedups, deepens + grades, refutes, and converges. **Scale it to the chosen depth** by adjusting `LENSES`, `LOOP_UNTIL_DRY`, and the refute vote count (see the DEPTH block).

The script is plain JavaScript (no TypeScript). `agent()`, `parallel()`, `pipeline()`, `phase()`, `log()` are the workflow hooks. Pass research-source paths/URLs into the agent prompts via a constant you fill in from Phase 1. Agents reach web tools (Exa/firecrawl) and Read/Grep via ToolSearch on their own.

## The tree-JSON schema (the contract for the visualization)

The workflow must end by returning an object matching this shape. `assets/tree-template.html` renders exactly this.

```json
{
  "apex": "Why are we short of the N target by <date>?",
  "verdict": "One-line answer / headline (the so-what) - rendered prominently under the apex. apex is the QUESTION; verdict is the ANSWER.",
  "depth": "standard",
  "stages": [
    {
      "id": "S1", "title": "Stage 1 - Arrive",
      "nodes": [
        {
          "id": "A", "text": "Discovery gap - net-new users never find the surface",
          "kind": "INFERENCE", "grade": "Strong", "role": "LEVER",
          "cite": "web: 3 competitor listings rank; ours absent (SERP Jun)",
          "children": [
            { "id": "A1", "text": "...", "kind": "MEASURED", "grade": "Mod", "cite": "..." }
          ]
        }
      ]
    }
  ],
  "roots": [
    { "id": "R0", "title": "No one owns activation because it falls between PM and Growth (POLICY, not tooling)",
      "from": ["M","Q"], "action": "Name a DRI; break the evaporating cloud", "isConstraint": true,
      "children": [
        { "id": "R0a", "text": "Activation has no DRI because it spans two orgs", "kind": "INFERENCE", "grade": "Mod", "cite": "...",
          "children": [
            { "id": "R0b", "text": "Each org optimizes its own metric, so the cross-org gap is nobody's number", "kind": "CLAIM", "grade": "Strong", "cite": "...",
              "children": [ { "id": "R0c", "text": "BEDROCK: the comp plan rewards per-org KPIs, not the shared funnel (deliberate policy)", "kind": "EXTERNAL", "grade": "Strong", "cite": "..." } ] }
          ] }
      ] },
    { "id": "R1", "title": "...", "from": ["A1","L"], "action": "...", "isConstraint": false, "children": [] }
  ],
  "constraint": { "rootId": "R0", "type": "policy",
    "statement": "System constraint = ownership/policy; located, needs no more data.",
    "unlocated": "Mechanism constraint still unlocated - one query pins it." },
  "negatives": [
    "Auto-remove the human gate -> non-completable artifacts + RBAC collisions",
    "Keystone on a behavior the data says doesn't exist (0/74)"
  ],
  "tests": [
    { "test": "Join origin -> completion + signup-date (1 query)",
      "decides": "Adjudicates C, D, G at once; arrival-starved vs conversion-problem" }
  ],
  "census": { "measured": 0.45, "inference": 0.25, "hypothesis": 0.20, "claim": 0.07, "external": 0.03,
    "bottomLine": "Broad but shallow at the decision point - the constraint-locating nodes are HYPOTHESIS. Map, not verdict." }
}
```

`kind` ∈ MEASURED|INSTANCE|EXTERNAL|CLAIM|INFERENCE|HYPOTHESIS|FRAMING. `grade` ∈ Strong|Mod|Weak. `role` ∈ ROOT|CONSTRAINT|LEVER|NEGATIVE|REFUTED|DOWNGRADED|"" (see `answer-kinds.md`).

## Converge schema (paste into the converge `agent()` call) — prevents the two bugs seen in testing

Use this STRICT JSON Schema for the converge step. A **loose schema lets the agent invent its own structure that won't render** (observed in the first smoke run), and without a length/semantic constraint the agent **overstuffs `apex` with the whole verdict** (observed in a real run, broke the header). The schema + prompt below fix both: `apex` is a SHORT undesirable-effect STATEMENT (≤140 chars, NOT a question), the one-line answer goes in `verdict`, and `constraint.statement` stays ≤ ~280 chars.

```javascript
const NODE = { type:'object', properties:{
  id:{type:'string'}, text:{type:'string'},
  kind:{type:'string', enum:['MEASURED','INSTANCE','EXTERNAL','CLAIM','INFERENCE','HYPOTHESIS','FRAMING']},
  grade:{type:'string', enum:['Strong','Mod','Weak']},
  role:{type:'string', enum:['ROOT','CONSTRAINT','CONSTRAINT?','LEVER','NEGATIVE','REFUTED','DOWNGRADED','critic-added','']},
  cite:{type:'string'}, children:{type:'array'} }, required:['text','kind','grade'] }
const TREE_JSON_SCHEMA = { type:'object', properties:{
  apex:{type:'string'},          // SHORT undesirable-effect STATEMENT (<=140 chars; declarative, NOT a question, NOT the answer)
  verdict:{type:'string'},       // the one-line answer / headline
  stages:{ type:'array', items:{ type:'object', properties:{
    id:{type:'string'}, title:{type:'string'}, crosscut:{type:'boolean'}, nodes:{type:'array', items:NODE} },
    required:['title','nodes'] }},
  roots:{ type:'array', items:{ type:'object', properties:{
    id:{type:'string'}, title:{type:'string'}, from:{type:'array', items:{type:'string'}},
    action:{type:'string'}, isConstraint:{type:'boolean'},
    // children = the nested causal chain UNDER this root (root -> sub-cause -> ... -> bedrock).
    // REQUIRED and non-empty for the constraint root; other roots may keep it shallow/empty.
    children:{type:'array', items:NODE} }, required:['id','title'] }},
  constraint:{ type:'object', properties:{
    rootId:{type:'string'}, type:{type:'string'}, statement:{type:'string'}, unlocated:{type:'string'},
    loadBearing:{type:'string'},  // id of the ONE node the constraint most rests on (its weakest-grade support) — drives the viz stress-test
    ifFalse:{type:'string'} },    // what changes if loadBearing is wrong: which root takes over / verdict reverts to map
    required:['rootId','statement'] },
  negatives:{ type:'array', items:{type:'string'} },
  tests:{ type:'array', items:{ type:'object', properties:{
    test:{type:'string'}, decides:{type:'string'}, rank:{type:'string'} }, required:['test','decides'] }},
  census:{ type:'object', properties:{
    measured:{type:'number'}, inference:{type:'number'}, hypothesis:{type:'number'},
    instance:{type:'number'}, claim:{type:'number'}, external:{type:'number'}, bottomLine:{type:'string'} },
    required:['bottomLine'] } },
  required:['apex','verdict','stages','roots','constraint','census'] }
```

In the converge prompt, say explicitly: "**apex** = the undesirable-effect STATEMENT (≤140 chars, a declarative 'the bad thing', NOT a question); put the one-line answer in **verdict**; **PRESERVE THE CAUSAL CHAIN — do NOT flatten it.** 'Collapse to 3-5 roots' means *group* the branches, NOT compress a chain into a one-line root. The constraint root (`isConstraint:true`) MUST carry a nested `children[]` why-chain from the apex down to bedrock (root → because X → because Y → … → a bedrock cause: a market fact / deliberate policy / law of the domain / something outside our control), every node graded. A childless constraint root is a generation bug — the tree must read as a multi-level *tree*, not a 3-band funnel; phrase every `root[].title` and node `text` as a **declarative problem/cause statement** readable as 'X because Y' (never a topic/phase label like 'Cost denominator' or 'DM stage'); set exactly ONE root `isConstraint:true` and make `constraint.rootId` match it; keep `constraint.statement` tight. **Stages are the problem's journey/funnel phases ONLY — do NOT create a stage for apex / verdict / framing / scope content** (that belongs in `apex` + `verdict`, never a stage bucket), and use `role` values only from the enum (no invented roles like 'apex-answer'). Tag any test/recommendation that rests on an un-refuted CLAIM/HYPOTHESIS node with '(verify first)'. Set `constraint.loadBearing` = the id of the single node the constraint most rests on (its weakest-grade support — usually what the #1 cheapest test targets), and `constraint.ifFalse` = what changes if that node is wrong (which root takes over / the verdict reverts to a map). These drive the viz's stress-test."

## The script

```javascript
export const meta = {
  name: 'why-tree',
  description: 'Build an evidence-graded Goldratt Why Tree for a problem',
  phases: [
    { title: 'Branch fan-out' }, { title: 'Deepen + grade' },
    { title: 'Refute' }, { title: 'Converge' }, { title: 'Drill constraint' },
  ],
}

// ---- DEPTH KNOBS (set from Phase 0 choice) ----
const APEX = args.apex
const SOURCES = args.sources || 'web only (Exa/firecrawl)'  // Phase-1 inventory, injected into prompts
const DEPTH = args.depth || 'standard'                       // 'standard' | 'deep'  (Quick REMOVED — for a cheap sketch, ask ONE agent, not this skill)
const LENSES = {
  standard: ['funnel/mechanics', 'data-skeptic', 'competitive/external', 'customer-psychology', 'economics/incentives', 'product-eng-constraint'],
  deep:     ['funnel/mechanics', 'data-skeptic', 'competitive/external', 'customer-psychology', 'economics/incentives', 'product-eng-constraint', 'metrics/measurement', 'distribution/discovery', 'org/ownership'],
}[DEPTH]
const REFUTE_VOTES = { standard: 1, deep: 3 }[DEPTH]
const LOOP_UNTIL_DRY = DEPTH === 'deep'
// HARD CAPS — without these, dedup misses + loop-until-dry + the refute fan-out compound into a
// runaway agent count (an early Deep run spawned 171 agents vs ~25-30 advertised, and the blowup
// rate-limited and DEGRADED its own refute pass). Cap the two fan-out stages explicitly.
const MAX_DEEPEN = { standard: 12, deep: 20 }[DEPTH]   // max branches that get a deepen agent
const MAX_REFUTE = { standard: 8,  deep: 14 }[DEPTH]   // max load-bearing branches sent to the refute panel

const BRANCH_SCHEMA = { type:'object', properties:{ branches:{ type:'array', items:{ type:'object',
  properties:{ text:{type:'string'}, stage:{type:'string'}, kind:{type:'string'}, grade:{type:'string'}, cite:{type:'string'} },
  required:['text','stage','kind','grade','cite'] }}}, required:['branches'] }

// 1) BRANCH-SPACE FAN-OUT - one agent per lens, blind to each other
phase('Branch fan-out')
const lensResults = await parallel(LENSES.map(lens => () =>
  agent(
    `You are diagnosing this problem through ONE lens: ${lens}.\n` +
    `APEX (undesirable effect / gap-vs-goal): "${APEX}"\n` +
    `Evidence sources you may use: ${SOURCES}. Use web research (Exa/firecrawl) and read any named files.\n` +
    `Emit candidate WHY-branches under the apex from your lens ONLY. For each: a clear causal statement, ` +
    `the journey stage it sits in, and - critically - its answer-kind (MEASURED/INSTANCE/EXTERNAL/CLAIM/INFERENCE/HYPOTHESIS), ` +
    `a confidence grade (Strong/Mod/Weak), and a citation (n + window for MEASURED). Do not invent numbers; if you can't measure it, mark HYPOTHESIS and name the test.`,
    { label:`lens:${lens}`, phase:'Branch fan-out', schema:BRANCH_SCHEMA }
  )))
const allBranches = lensResults.filter(Boolean).flatMap(r => r.branches)

// 2) DEDUP + BUCKET + HARD CAP (plain code - genuinely needs all branches at once)
const merged = rankByLoadBearing(dedupeByMeaning(allBranches)).slice(0, MAX_DEEPEN)  // dedup, rank, THEN cap
log(`${allBranches.length} raw branches -> ${merged.length} after dedup+cap (MAX_DEEPEN=${MAX_DEEPEN})`)

// 3) DEEPEN + GRADE (+ optional loop-until-dry), per branch, no barrier
const deepened = await pipeline(merged,
  b => agent(
    `Branch: "${b.text}" (stage ${b.stage}).\n` +
    `Ask "why does this happen?" ${LOOP_UNTIL_DRY ? 'recursively until you hit bedrock (loop-until-dry)' : 'ONE level down'}.\n` +
    `Sources: ${SOURCES}. Grade EVERY child node (answer-kind + grade + citation). ` +
    `Return the branch as a node that KEEPS its own top-level kind + grade (+ a lensCount) AND carries a nested children[] tree — the downstream load-bearing filter reads those top-level fields, so do NOT drop them.`,
    { label:`deepen:${b.stage}`, phase:'Deepen + grade', schema: NODE_TREE_SCHEMA }
  ))

// 4) ADVERSARIAL REFUTE - perspective-diverse skeptics try to KILL each load-bearing branch
phase('Refute')
const REFUTE_LENSES = ['data-says-otherwise','mechanism-broken','survivorship/selection','mis-attribution']
// LOUD refute-failure guard (a live run silently ran refute on 0 branches because the deepen
// node lost its kind/grade and isLoadBearing filtered everything out — the core value-add vanished
// with no warning). If REFUTE_VOTES>0 and nothing is load-bearing, WARN and surface it in converge.
const lbBranches = deepened.filter(Boolean).filter(isLoadBearing).slice(0, MAX_REFUTE);
let refuteWarning = '';
if (REFUTE_VOTES > 0 && lbBranches.length === 0) {
  refuteWarning = 'REFUTE PASS RAN ON 0 BRANCHES — no independent adversarial verification happened this run (check that deepen nodes carry kind/grade/lensCount for isLoadBearing, and watch for rate-limited deepen agents). Treat every load-bearing node as UN-REFUTED.';
  log('⚠ ' + refuteWarning);
}
const refuted = (REFUTE_VOTES === 0 || lbBranches.length === 0) ? deepened.filter(Boolean) : await pipeline(
  lbBranches,   // cap the refute fan-out too
  branch => parallel(
    REFUTE_LENSES.slice(0, REFUTE_VOTES + 1).map(angle => () =>
      agent(`Try to REFUTE this branch from the "${angle}" angle. Default to refuted=true if the evidence is thin or selection-biased. ` +
            `Branch: ${JSON.stringify(branch)}. Sources: ${SOURCES}.`,
            { label:`refute:${angle}`, phase:'Refute', schema: VERDICT_SCHEMA }))
  ).then(votes => {
    const kills = votes.filter(Boolean).filter(v => v.refuted)
    if (kills.length > REFUTE_LENSES.slice(0, REFUTE_VOTES+1).length / 2)
      return { ...branch, role: kills.some(k=>k.demote) ? 'DOWNGRADED' : 'REFUTED', killedBy: kills.map(k=>k.evidence) }
    return branch
  })
)

// 5) CONVERGE - collapse to roots + locate THE constraint (needs ALL surviving branches -> barrier)
phase('Converge')
const converged = await agent(
  `Here are the surviving, graded, refute-tested branches (each already carries a nested children[] why-chain):\n${JSON.stringify(refuted)}\n` +
  `1) GROUP them into 3-5 ROOT causes (group ≠ flatten — keep each branch's children[] chain intact under its root). ` +
  `2) Locate THE single system constraint (the root that, if removed, unblocks the most); set its isConstraint:true. ` +
  `3) On the constraint root, attach the FULL nested children[] why-chain from apex down to bedrock (do NOT compress it to a one-line title). ` +
  `4) Say whether it's POLICY/ownership vs TOOLING; if it's a goal-conflict, apply the Evaporating Cloud (name the false assumption). ` +
  `5) List NEGATIVE branches (fixes that backfire). 6) Rank 1-3 CHEAPEST tests by (verdict-movement ÷ cost). ` +
  `7) Compute the answer-kind census and write the honest bottom line (verdict vs map). ` +
  `8) Set constraint.loadBearing to an id that EXISTS in the tree you are emitting (a real stage-node or constraint-chain node id — do NOT invent one), and ifFalse to what changes if it falls (reference only real ids). ` +
  (refuteWarning ? `IMPORTANT — ${refuteWarning} Say this explicitly in census.bottomLine and treat the verdict as a MAP, not settled. ` : '') +
  `Return the FULL tree-JSON object per the schema.`,
  { label:'converge', phase:'Converge', schema: TREE_JSON_SCHEMA, effort:'high' }
)

// 6) DRILL THE CONSTRAINT BRANCH to bedrock — guarantees the ONE branch that matters is a real
//    multi-level chain even if converge flattened it. Runs every tier. This is the adaptive-depth fix:
//    deep recursion is spent where it counts (the constraint), not uniformly across all branches.
phase('Drill constraint')
const cRoot = (converged.roots || []).find(r => r.isConstraint)
if (cRoot && (!cRoot.children || cRoot.children.length === 0)) {
  const feed = (converged.stages||[]).flatMap(s => s.nodes||[]).filter(n => (cRoot.from||[]).includes(n.id))
  const chain = await agent(
    `The located system constraint is: "${cRoot.title}".\nSupporting evidence nodes: ${JSON.stringify(feed)}.\n` +
    `Build the EXPLICIT causal chain UNDER it as a nested children[] tree: each node a declarative graded cause statement ` +
    `("X because Y"), recursing "why does THIS happen?" until you hit BEDROCK (a market fact / deliberate policy / law of ` +
    `the domain / something outside our control — where the next 'why' yields nothing new). 3-6 levels is typical. Grade ` +
    `every node (kind + grade + cite). Return {children:[...]} only.`,
    { label:'drill:constraint', phase:'Drill constraint', schema: NODE_TREE_SCHEMA, effort:'high' })
  cRoot.children = chain.children || []
}

// 7) VALIDATE constraint.loadBearing / ifFalse against real ids — converge has been observed to
//    emit phantom ids (e.g. "r1-3a"), which silently breaks the viz stress-test. Re-point if invalid.
const allIds = new Set();
;(converged.stages||[]).forEach(s=>(s.nodes||[]).forEach(function w(n){ if(n.id)allIds.add(n.id); (n.children||[]).forEach(w); }))
;(converged.roots||[]).forEach(r=>(r.children||[]).forEach(function w(n){ if(n.id)allIds.add(n.id); (n.children||[]).forEach(w); }))
if (converged.constraint && converged.constraint.loadBearing && !allIds.has(converged.constraint.loadBearing)) {
  const cr = (converged.roots||[]).find(r=>r.isConstraint) || {}
  const repoint = (cr.from||[]).find(id=>allIds.has(id)) || (cr.children&&cr.children[0]&&cr.children[0].id) || null
  log(`⚠ phantom loadBearing id "${converged.constraint.loadBearing}" — re-pointing to ${repoint}`)
  converged.constraint.loadBearing = repoint
}
if (refuteWarning) converged._refuteWarning = refuteWarning  // carried through so the decision-doc/CLR can surface it
// Stamp provenance from the ORCHESTRATOR, not the converge agent — converge has been observed copying a
// stray number (e.g. "171") from context it read into provenance.depth/agents. DEPTH + the real count win.
converged.provenance = { method:'Goldratt CRT', ...(converged.provenance||{}), depth: DEPTH /*, agents: <real count if tracked> */ }

return converged
```

## Notes for adapting

- **Pre-compute the hard evidence ONCE in Phase 1 and pass it as a frozen brief** into every lens prompt (e.g., real DB counts) with "do NOT re-query". This grounds nodes as MEASURED instead of HYPOTHESIS and stops N parallel agents from re-hammering the same DB/API. (A real data-grounded run: the lens agents shared one pre-pulled metrics brief; none re-hit the DB.)
- Helper functions to fill in when you instantiate (keep schemas strict so agents retry on mismatch):
  - `dedupeByMeaning(branches)` — **must actually merge near-duplicates.** Use **token-set-ratio ≥ ~0.55** on normalized text (lowercase, strip punctuation/stopwords), keep the best-graded representative per group, union its `cite`s. **Do NOT use a sorted 6-word prefix key — it's too strict and merges nothing** (a live run went 33→33, and only the cap reduced it, which defeats the point of deduping before the cap).
  - `rankByLoadBearing(branches)` — sort so the cap keeps the important ones: MEASURED/Strong and nodes many lenses surfaced first; FRAMING / single-lens / Weak last. The `.slice(0, MAX_DEEPEN)` then drops the tail safely. **`log()` how many were dropped** — never silently truncate.
  - `isLoadBearing(branch)` — true if the branch is a plausible constraint candidate (not FRAMING, grade ≥ Mod, or flagged by ≥2 lenses). **CRITICAL: this reads the branch's TOP-LEVEL `kind`/`grade`/`lensCount` — the deepen agent MUST propagate those up to the returned branch node, not bury them only inside `children[]`. If it doesn't, `isLoadBearing` returns 0 for everything and the refute pass SILENTLY does nothing** (observed live). The refute-failure guard above turns that silence into a loud warning, but the real fix is propagating the metadata.
  - `NODE_TREE_SCHEMA` = a single branch object that REQUIRES top-level `kind`/`grade` (+ optional `lensCount`) and a recursive `children:[NODE]` (used by deepen + the constraint drill); `VERDICT_SCHEMA` = `{refuted:boolean, demote:boolean, evidence:string}`; `TREE_JSON_SCHEMA` = the strict schema above (its `roots[].children` is what makes the tree multi-level — do not drop it).
- **Standard** = 6 lenses, 1-vote refute, one-level deepen + constraint drill. **Deep** = 9 lenses, 3-vote refute, loop-until-dry + constraint drill. (Quick was REMOVED — for a cheap gut-check, ask a single agent; this skill only earns its cost when one mind can confidently go wrong.)
- **Honest agent count** = lenses + deepen(≤`MAX_DEEPEN`) + refute(≤`MAX_REFUTE` × (`REFUTE_VOTES`+1)) + converge + drill. The **refute fan-out is the multiplier**: Standard ≈ **20-36**, Deep ≈ **30-55+**. The "~12-16 / ~25-30" figures in older docs predate the caps and the drill step — SKILL.md's gate now quotes the realistic ranges. The caps bound the worst case (no 171-blowup); they don't make it cheap.
- For data-grounded problems, name the file paths / DB tables explicitly in `SOURCES` so the deepen/refute agents read them (this is what produced real refutations like "6/6 sends had a signer" in the source case).
- Save `converged` to `why-tree-output.json` before rendering, so a render failure never loses the analysis.
- If the user set a token budget, gate the deep loop on `budget.remaining()`.
