import streamlit as st
import pandas as pd
from ai_insights_data_bundler import bundle_kpi_data_for_insights, generate_ai_prompt
from llm_service import LLMService

def render_ai_insights_panel(tab_name, days=30):
    """
    Render AI Insights panel at the top of each tab
    """
    if not st.session_state.get(f'show_ai_insights_{tab_name}'):
        return

    # Get bundled data
    bundled_data = bundle_kpi_data_for_insights(tab_name, days)
    
    if not bundled_data:
        st.warning("No KPI data available for AI insights")
        return

    # Initialize LLM service
    llm = LLMService()
    
    # Container for insights
    with st.container():
        # Check if we need to generate insights
        if st.session_state.get(f'trigger_analysis_{tab_name}', True):  # Default to True for first show
            with st.spinner("🧠 Analyzing performance data..."):
                prompt = generate_ai_prompt(tab_name, bundled_data)
                try:
                    insights = llm.generate_insights(prompt)
                    if insights:
                        st.session_state[f'insights_{tab_name}'] = llm.format_insights_for_display(insights)
                        st.session_state[f'raw_insights_{tab_name}'] = insights
                    else:
                        st.error("⚠️ Failed to generate insights. Please try again.")
                except Exception as e:
                    st.error(f"⚠️ Error generating insights: {str(e)}")
                    st.session_state[f'insights_{tab_name}'] = None
                    st.session_state[f'raw_insights_{tab_name}'] = None
            # Reset trigger
            st.session_state[f'trigger_analysis_{tab_name}'] = False
        
        # Display insights if available
        insights = st.session_state.get(f'insights_{tab_name}')
        if insights:
            # Summary
            st.markdown(f"#### {insights['summary']}")
            
            # Two-column layout for insights
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 💡 Key Insights")
                for insight in insights['key_insights']:
                    st.markdown(f"- {insight}")
                
                st.markdown("##### 📈 Trends")
                for trend in insights['trends']:
                    st.markdown(f"- {trend}")
            
            with col2:
                st.markdown("##### ✅ Recommended Actions")
                for action in insights['recommended_actions']:
                    st.markdown(f"- {action}")
            
            # Refresh and Close buttons
            col1, col2, col3 = st.columns([6, 2, 2])
            with col2:
                if st.button("🔄 Refresh", key=f"refresh_{tab_name}", type="secondary"):
                    st.session_state[f'trigger_analysis_{tab_name}'] = True
                    st.rerun()
            with col3:
                if st.button("✖️ Close", key=f"close_{tab_name}", type="secondary"):
                    st.session_state[f'show_ai_insights_{tab_name}'] = False
                    st.rerun()
        else:
            # Only show loading state on first load or refresh
            if st.session_state.get(f'trigger_analysis_{tab_name}'):
                st.info("🔄 Generating AI insights...")
            else:
                st.error("⚠️ Failed to generate insights. Please try refreshing.")