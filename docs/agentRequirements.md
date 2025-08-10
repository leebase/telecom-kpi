Playbook Prioritizer Agent — Requirements & Phased Implementation Plan

1. Overview

The Playbook Prioritizer Agent automates the process of:
	1.	Calling AI Insights for each of the 5 subject areas.
	2.	Normalizing and merging overlapping plays.
	3.	Scoring plays by bang-for-buck.
	4.	Optionally selecting an optimal portfolio of plays within a budget.
	5.	Publishing a structured artifact for the dashboard.
	6.	Presenting a workflow visual and “agents in progress” UI for judges.

The agent must run in simulated mode for the hackathon (deterministic results), but be easily switched to live mode.

⸻

2. Subject Areas
	•	Acquisition
	•	Retention
	•	Network QoE
	•	Support
	•	Revenue

⸻

3. Inputs
	•	Function per area:

call_insights(area: str) -> list[Play]


	•	Config values:
	•	budget_points (e.g., 8)
	•	kpi_weights (dict of KPI importance multipliers)
	•	title_aliases (map of duplicate play names)

⸻

4. Play Schema

{
  "title": "Weekend install crews",
  "area": "Support",
  "effort_points": 3,
  "impact_score": 5,
  "confidence": 0.70,
  "kpi_targets": {"Churn_Rate": -0.3, "Install_Backlog": -12},
  "dependencies": [],
  "notes": "Backlog up 12% in Midwest; peer best-in-class lower."
}


⸻

5. Output Schema

{
  "prioritizer": {
    "prioritized_plays": [
      {
        "rank": 1,
        "title": "Overnight capacity tune (MW)",
        "area": "Network QoE",
        "score": 1.60,
        "effort_points": 2,
        "impact_score": 4,
        "confidence": 0.80,
        "kpi_targets": {"QoE_MOS": 0.2},
        "why": "Largest negative mover linked to churn; peer gap present",
        "dependencies": []
      }
    ],
    "portfolio_pick": {
      "selected": ["Overnight capacity tune (MW)", "Weekend install crews"],
      "total_effort": 5,
      "expected_effect": {"Churn_Rate": -0.45, "QoE_MOS": 0.2}
    },
    "exec_summary": "Do these first to cut churn quickly within an 8-point sprint budget…"
  }
}


⸻

6. Functional Requirements

FR-1: Call call_insights() for all 5 subject areas.
FR-2: Normalize and merge duplicates using title_aliases.
FR-3: Score each play:

score = (impact_score / 5) * confidence * kpi_weight / effort_points

FR-4: Rank by score, break ties by KPI weight → lower effort → alpha.
FR-5: If budget_points provided, select highest-scoring plays until budget exhausted.
FR-6: Summarize top plays in exec_summary.
FR-7: Write results to agent artifact JSON.
FR-8: Display “agent in progress” in orchestrator app.
FR-9: Show workflow diagram in pitch deck/UI.

⸻

7. Workflow Visual (for slide/UI)

[Acquisition Insights Agent] → [Retention Insights Agent] → [Network QoE Insights Agent] → [Support Insights Agent] → [Revenue Insights Agent] → [Merge & Normalize Plays] → [Score & Rank Plays] → [Portfolio Selection] → [Executive Summary Output]

Each box should visually indicate “working” in sequence during demo.

⸻

8. Phased Implementation Plan

Phase 1 — Mock Insights Calls & Logging

Goal: Have orchestrator loop through all 5 subject areas with dummy data and show step-by-step logs.
	•	Create call_insights(area) that returns 3–5 mock plays with random scores.
	•	In orchestrator:
	•	Loop through all areas.
	•	Log start/finish for each.
	•	Sleep 0.3–0.5s between steps for realism.
	•	Test: Confirm progress log and “agents in progress” UI works.

⸻

Phase 2 — Merge & Normalize

Goal: Deduplicate plays across areas.
	•	Implement normalize_and_merge():
	•	Lowercase titles.
	•	Replace using title_aliases config.
	•	Merge confidence, effort_points, kpi_targets.
	•	Test: Use mock inputs with known duplicates to confirm merging.

⸻

Phase 3 — Scoring & Ranking

Goal: Rank plays by bang-for-buck.
	•	Implement scoring formula.
	•	Sort and add rank numbers.
	•	Test: Confirm scores match manual calculations.

⸻

Phase 4 — Portfolio Selection

Goal: Select best plays within budget.
	•	Implement greedy selection respecting dependencies.
	•	Sum kpi_targets for expected effect.
	•	Test: Vary budget and confirm selection changes.

⸻

Phase 5 — Exec Summary

Goal: Summarize top 3–5 plays in plain English.
	•	Use template fill (mock LLM call later).
	•	Test: Confirm summary updates when top plays change.

⸻

Phase 6 — Artifact Integration

Goal: Write prioritizer block to artifact JSON.
	•	Append to existing orchestrator output.
	•	Test: Dashboard reads and renders table, portfolio, summary.

⸻

Phase 7 — Workflow Visual

Goal: Visual representation of process for judges.
	•	Create static image for deck.
	•	Optionally animate in orchestrator using graphviz_chart() or st.columns() highlight.
	•	Test: Ensure visual matches actual steps.

⸻

9. Testing Strategy
	•	Unit test:
	•	Merge logic with alias map.
	•	Scoring formula with/without KPI weights.
	•	Portfolio selection algorithm.
	•	Integration test:
	•	Run full pipeline in sim mode and validate deterministic output.

⸻

10. Deliverables
	•	prioritizer.py with core functions.
	•	Updated run_agents_app.py with Playbook Prioritizer step.
	•	Updated artifact JSON with prioritizer block.
	•	Dashboard UI for Prioritized Plays table + Portfolio Pick card.
	•	Workflow diagram for deck.

