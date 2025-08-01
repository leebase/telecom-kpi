# 🔧 Metric Cards UI - Requirements for KPI Card Redesign

## 🎯 Goal

Redesign the existing KPI dashboard cards to improve:
- Visual clarity and contrast
- Interactive info behavior
- Layout alignment and responsiveness
- Color-blind accessibility
- Clean, modern Streamlit implementation with light custom CSS

## 🧱 Layout Requirements
- Display six metric cards in a responsive 3x2 grid using st.columns()
- Each metric card must:
  - Have a gradient background (you can keep the purple, but make it consistent and contrast-friendly)
  - Use rounded corners, padding, and drop shadow for separation
  - Contain:
    - Metric title
    - Metric value
    - Delta indicator (with arrow + value)
    - Info icon (ℹ️) in the top-right corner, inside the card

## 🎨 Visual & Color Requirements
- Avoid red/green-only cues for deltas. Use:
  - Arrow icons: ▲ / ▼
  - Neutral delta text (white or light gray)
  - Left-border color stripe: green for up, red for down
- All text must pass WCAG AA contrast against the background
- Delta text should be aligned with value, not floating

## 🧑‍🦯 Accessibility + Clarity
- Arrows or left-border colors must provide direction independent of color
- Font sizes:
  - Metric value: 2rem, bold
  - Delta: 1rem
  - Label: 0.9rem
- Ensure the info icon works for keyboard navigation (optional bonus)

## 🧠 Info Icon Behavior
- Info icon (ℹ️) should reveal a tooltip on hover or click:
  - Use help= if using st.metric() OR
  - Simulate tooltip with CSS/HTML fallback
- Tooltip should include:
  - Definition of the metric
  - Last updated timestamp (mock data ok)
  - Link to underlying logic or query (just show dummy text)

## ⚙️ Component Inputs (for dynamic code)

Each card should be created using a function like:

```python
create_metric_card(
    label="Average Revenue Per User",
    value=42.17,
    delta=3.25,
    delta_direction="up",   # or "down"
    unit="$",
    tooltip="ARPU = Total Revenue / Active Users"
)
```

This should generate a complete, styled card with interactive tooltip and correct visual cues.

## 🧪 Testing Requirements (Optional but Ideal)
- Add a mock st.selectbox() to choose time period (e.g., "Last 30d", "QTD", "YTD") and dynamically update deltas
- Track st.session_state["selected_kpi"] when a card is clicked to load a detail view (even just a placeholder chart)

## ✅ Success Criteria
- Clear, legible metrics on all screen sizes
- Delta direction visible to colorblind users
- ℹ️ tooltips work and are visually unobtrusive
- Entire layout feels professional and modern
- Code is clean, reusable, and Cursor-friendly for future extensions 