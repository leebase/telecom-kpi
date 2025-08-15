# 🚀 The Vibe Coder’s Guide to Cost-Effective Cursor 🚀
*Vibemaster Flex Edition — Pro Plan Mastery (Single-File Playbook)*

> **Audience:** Cursor Pro ($20/mo) users who want maximum output per dollar  
> **Ethos:** Producer energy. House band for the groove, virtuosos for the solo. No AI slop.

---

## 1) Introduction — Code with Vibe, Not Just an API Key 🎧

Cursor is an AI-native editor that can read your repo, reason across files, generate code, refactor features, and debug from stack traces. It’s not a toy—it’s a studio.

**But** on the Pro plan, premium model calls are a **studio expense**. Your **Auto** model is unlimited. **Named premium models** (Opus / GPT-4 / Sonnet) draw from your $20 credit pool. A Vibe Coder treats that pool like **producer budget**: intentional, surgical, high-value only.

**Goal of this guide:** turn every prompt into **AI Gold**—hours saved for pennies—by planning first, selecting the right model, and running a crash-proof execution loop that updates your working docs *as you go*.

---

## 1.5) Pre-Production — Plan Before You Play 🎚️

Never open Cursor cold. Think in a separate chat first, then **commit the plan as files** in your repo:

- **`appRequirements.md`** — *What/Why*: user stories, constraints, acceptance criteria.
- **`appArchitecture.md`** — *How*: modules, boundaries, data flow, contracts, cross-cutting concerns.
- **`actionPlan.md`** — *Now*: sequenced tasks (TASK-###), DoD, WIP/Next/Done/Blocked, timestamped notes.

**Session Rhythm**
1. **Kickoff:** In Cursor Chat, load the plan → `@appRequirements.md @appArchitecture.md @actionPlan.md`. Confirm the **smallest valuable chunk** (30–60 mins).  
2. **Work:** Use `/edit` for surgical changes; keep one chat thread per feature to preserve context.  
3. **Update live:** After each task finishes, **immediately** mark it complete in `actionPlan.md` and record deltas. Don’t wait—protect progress from context resets.

---

## 1.6) Templates (Drop-In)

### `appRequirements.md`
```md
# App Requirements
## Context
- Problem / Goal:
- Stakeholders:
- Non-Goals:

## User Stories
- US-001: As a <role>, I want <capability> so that <value>.
- US-002: ...

## Constraints
- Tech:
- Compliance/Sec:
- Performance/SLAs:

## Acceptance Criteria (by story)
- US-001:
  - [ ] AC1
  - [ ] AC2

## Risks & Assumptions
- R-001: ...
- A-001: ...

appArchitecture.md

# Architecture
## System Overview
- Modules:
- Data flow:
- External deps:

## Interfaces & Contracts
- API endpoints:
- Events/Queues:
- DB schema (link/versioned):

## Cross-Cutting
- Errors & Retries
- Observability
- Security
- Config/Secrets
- Performance considerations

## Decisions (ADR-style)
- ADR-001: <decision> — Rationale, Alternatives, Consequences

actionPlan.md

# Action Plan
_Status: YYYY-MM-DD HH:MM (Local)_

## Doing Now (WIP=1)
- [ ] TASK-013: <crisp objective with DoD>

## Next Up
- [ ] TASK-014: ...
- [ ] TASK-015: ...

## Done
- [ ] TASK-012: <result> (PR #, commit hash)

## Blocked / Parked
- [ ] TASK-010: <why, owner, unblock condition>

## Notes & Learnings
- 2025-08-15: <insight/edge-case/decision>


⸻

2) Strategizing Prompts (Outside Cursor) 💭

Use these in your “thinking” chat to generate plan files before coding.

2.1 Define Requirements

I’m building a [type of app]. Draft a precise `appRequirements.md` with:
- Problem/Goal, Stakeholders, Non-Goals
- 3–6 prioritized user stories (US-###)
- Constraints (tech, security, performance)
- Acceptance criteria per story (checklist style)
- Risks & Assumptions
Keep it terse, unambiguous, and implementation-agnostic.

2.2 Design Architecture

Given this `appRequirements.md` [paste], produce `appArchitecture.md`:
- Module decomposition and boundaries
- Data flow (inputs/outputs)
- Interfaces & contracts (API endpoints, events, DB)
- Cross-cutting concerns (errors, observability, security, config)
- 3–5 ADR entries capturing key decisions (with trade-offs)
Prefer clarity over cleverness. No code yet.

2.3 Build Action Plan

From `appArchitecture.md`, generate `actionPlan.md`:
- Break into sequenced TASK-### items with crisp objectives and DoD
- Populate Doing Now (1 item), Next Up (3–7), Blocked
- Add a Notes & Learnings section to capture insights as we go
Ensure tasks are small enough to finish within 30–60 minutes each.


⸻

3) The Golden Rule — Don’t Pay the AI to Do a Grunt’s Job 🤖

House Band vs. Virtuoso
	•	Free roadies: Prettier (format), ESLint/Stylelint (lint), IDE refactors (rename/extract), compiler/type checker.
	•	Virtuoso (premium model): reasoning, synthesis, architecture, multi-file refactors.

If a tool can do it deterministically for $0, don’t burn premium credits.

Low-Value vs High-Value Cheat Sheet

Low-Value (Avoid premium):
	•	“Format this file with Prettier.”
	•	“Find the typo/missing semicolon.”
	•	“Rename getData → fetchData across a folder.”
	•	“Explain a single line of obvious code.”

High-Value (Use premium intentionally):
	•	“Refactor a 200-line function into SOLID-compliant hooks with tests.”
	•	“Analyze this stack trace, traverse @codebase, propose a robust fix.”
	•	“Generate test suite covering null/empty/negative edge cases with mocks.”
	•	“Trace auth flow across modules and document failure modes.”

⸻

4) Model Selection Framework (Pro Plan) 🎯

Default to Auto; escalate only when necessary. Hybrid saves the most $.

Task Type	Start With	Escalate To	Rationale
Boilerplate, simple CRUD, small refactors	Auto (Unlimited)	—	Clear targets from plan docs; avoid premium spend.
Component scaffolds, basic hooks, docstrings	Auto	—	Fast and good enough with precise prompts.
Complex multi-file refactor	Premium	—	Depth of reasoning beats multiple retries.
Performance-critical algorithms	Premium	—	Correctness/complexity warrants top model.
Cross-cutting (security, tracing, error policy)	Premium	—	System-wide implications; get it right once.
Mixed features (some easy, some gnarly)	Auto → Premium polish	Premium (targeted)	Let Auto draft; spend credits only on hard parts.

Pro move: Tag tasks with a model hint in actionPlan.md:

- [ ] TASK-021: Implement JWT auth middleware (Model: Premium — cross-cutting security)
- [ ] TASK-022: Add SettingsPage skeleton UI (Model: Auto)


⸻

5) The Vibe Coder’s Toolkit 🎛️

5.1 Batch Your Asks 📦

Multiple micro-prompts = overhead. Consolidate.

Instead of 5 chats:

1) How to optimize this?
2) Can it be parallelized?
3) Edge cases?
4) Add retries?
5) Improve logs?

Do one:

Goal: Harden `processBatch()` in @src/jobs/processor.ts.
Please:
1) Optimize for throughput
2) Propose safe parallelization strategy
3) List & handle edge cases (empty, malformed, partial failure)
4) Add retry/backoff with jitter
5) Improve structured logging (fields: jobId, batchSize, duration, attempt)
Return diffed code + rationale bullets.

5.2 Context-Rich Prompts (Role → Goal → Constraints) 🎯

Before (lazy):

"Make this better."

After (vibe):

(Role) You are a senior React + Tailwind engineer.
(Goal) Refactor `UserProfile.jsx`: extract logic into `useUserProfile` hook; keep component purely presentational.
(Constraints)
- Hook handles API calls/state
- No new deps
- Match our naming conventions
- Return only the final code for both files (no commentary)

5.3 Master @ and / Commands ⚡
	•	@file / @codebase — Surgical context without pasting walls of code.
	•	@Docs — Pull official, current framework docs.
	•	@Web — Fetch recent examples or API changes.
	•	/edit (Cmd/Ctrl+K) — Highlight → instruct → apply diff inline.
	•	Manual Re-index — After big pulls/branch swaps, resync: Settings → Indexing & Docs.

Example:

@codebase Where is payment capture implemented?
Follow-up: Refactor to add idempotency key handling in @src/payments/capture.ts and update @src/routes/payments.ts.

5.4 Let the Linter Do Its Job 🛠️

If ESLint/Prettier/Type checker can fix it for free, let them. Pay AI for logic, architecture, and synthesis—not for commas.

5.5 Automate Standards with Cursor Rules 📜

Global rules = personal defaults.
Project rules = versioned .cursor/rules/ (recommended).

Example .cursor/rules/00-foundation.mdc

---
description: "Foundation: always consult and update plan"
alwaysApply: true
---

**Working Agreement**
1) Before coding, consult @appRequirements.md, @appArchitecture.md, @actionPlan.md.
2) Propose a smallest-valuable work chunk (≤60 mins), confirm scope, then proceed.
3) Update actionPlan.md immediately after each completed task (move TASKs, add results).
4) Reflect any design deltas in appArchitecture.md at the moment they occur.
5) If ambiguity is detected, ask clarifying questions before editing code.

Example .cursor/rules/react-ui.mdc

---
description: "React UI: TS + Tailwind standards"
globs: ["**/*.tsx", "**/*.jsx"]
---

- Functional components with hooks only
- Props typed via TS interfaces
- Tailwind for styling; avoid CSS-in-JS
- Co-locate tests as `<name>.test.tsx`

(Tip: search GitHub for cursor-rules and adapt community sets.)

⸻

6) Work Execution (Inside Cursor) — Kickoff & Live-Update Prompts 🎬

Key requirement: Update actionPlan.md AS SOON AS a task completes. Never wait until the end—protect progress from context limits or restarts.

6.1 Session Kickoff

Read @appRequirements.md @appArchitecture.md @actionPlan.md.

Propose the smallest valuable work chunk (≤60 mins) for the current feature:
- Goal (1–2 sentences)
- Files to touch (paths)
- Steps (5–9)
- Risks/unknowns
- Definition of Done (checklist)

Wait for my “Go” before editing.

6.2 Execute with Live Task Updates

GO.

Execute the plan step-by-step. After EACH step that completes a TASK-### or sub-step:
1) Immediately update @actionPlan.md:
   - Mark the TASK checkbox [x] if done, move to Done with a one-line result (PR # or commit hash if applicable).
   - If the step adds new follow-ups, add them to Next Up with new TASK IDs.
2) If architecture/design changed, immediately update @appArchitecture.md (diff-friendly bullets under “Decisions”).
3) If acceptance criteria were clarified or adjusted, update @appRequirements.md.

Work in small increments so updates are frequent. Never wait until the end to update docs.
If context window pressure rises, pause, summarize current state into actionPlan.md Notes & Learnings, then continue.
Return diffs for code changes and the updated markdown files each time.

6.3 Crash/Reset Recovery (If Context Was Lost)

Reload @appRequirements.md @appArchitecture.md @actionPlan.md.

Resume from the topmost unchecked item in "Doing Now" or the first item in "Next Up" if Doing Now is empty.
Reconstruct minimal context by summarizing the last 5 entries in Notes & Learnings and the last 3 “Done” items. Confirm the next step, then proceed.


⸻

7) Vibe Check — Are You Leaking Credits? 💧
	•	❌ Opus for Everything — Default to Auto; reserve premium for deep reasoning.
	•	❌ Uncapped Meter — Set a spend limit in Billing to prevent surprise overages.
	•	❌ Amnesiac Prompt — Keep related tasks in a single thread; don’t reset context unnecessarily.
	•	❌ Vague Prompts — Always use Role → Goal → Constraints; add acceptance criteria/output format.
	•	❌ Ignoring Index — Re-index after big pulls/renames/branch flips.
	•	❌ Manual Context Dumping — Use @file/@codebase, not 500-line paste walls.
	•	❌ Coding Cold Start — Start every session by loading the plan docs.
	•	❌ Regenerate Roulette — If the first reply misses, fix the prompt; don’t keep hitting regenerate.
	•	❌ Chat-as-Search — For trivial facts, use docs/web directly; save premium calls for synthesis.

⸻

8) Optional Guardrails (Tighten the Studio) 🧰

8.1 Pre-Commit Hook (bash)

Blocks commits when you forgot to update the plan.

#!/usr/bin/env bash
set -euo pipefail

CHANGED_CODE=$(git diff --cached --name-only | grep -E '^(src|app|lib)/' || true)
PLAN_TOUCHED=$(git diff --cached --name-only | grep -E '^(appRequirements|appArchitecture|actionPlan)\.md$' || true)

if [[ -n "$CHANGED_CODE" && -z "$PLAN_TOUCHED" ]]; then
  echo "❌ You changed code but didn't update appRequirements.md/appArchitecture.md/actionPlan.md."
  echo "   Update the docs (at minimum, actionPlan.md Done/Notes) and re-stage."
  exit 1
fi

8.2 PR Template (.github/pull_request_template.md)

# Summary
- What changed, why, and how it meets the DoD.

# Linked Tasks
- [ ] TASK-###

# Definition of Done
- [ ] Acceptance criteria met
- [ ] Tests updated/added
- [ ] Docs updated (actionPlan.md + architecture if needed)


⸻

9) One-Page Studio Cheatsheet (Keep Open in Split Pane) 🎟️

Plan-First Files: appRequirements.md • appArchitecture.md • actionPlan.md (TASK-###)
Model Choice: Auto for 90% • Premium for complex refactors, perf-critical, cross-cutting • Hybrid = Auto scaffold → Premium polish
Commands: @file • @codebase • @Docs • @Web • /edit (Cmd/Ctrl+K) • Manual Re-index
Prompt Shape: Role → Goal → Constraints • Output format • DoD
Live Updates: After each step, update actionPlan.md and (if needed) architecture/requirements
Anti-Patterns: Opus-for-everything • Uncapped spend • Vague prompts • New thread every time • Manual paste walls

⸻

10) Conclusion — You’re the Producer, Not Just the Client 👑

The Vibe Coder doesn’t brute-force prompts; they conduct them.
	1.	Intentionality: Plan first, Auto by default, premium only for the hard stuff.
	2.	Context: Precise prompts, surgical @ references, disciplined /edit.
	3.	Iteration: Update docs as you go so resets never set you back.

Ship fast. Ship smart. Ship with Vibe. 🚀
