import streamlit as st
import pandas as pd
from ai_insights_data_bundler import bundle_kpi_data_for_insights, generate_ai_prompt

def render_ai_insights_panel(tab_name, days=30):
    """
    Render AI Insights panel at the top of each tab
    """
    st.markdown("---")
    
    # Get bundled data
    bundled_data = bundle_kpi_data_for_insights(tab_name, days)
    
    if not bundled_data:
        st.warning("No KPI data available for AI insights")
        return
    
    # Calculate summary statistics
    total_kpis = len(bundled_data)
    above_peer = sum(1 for kpi in bundled_data if kpi['current_value'] > kpi['peer_avg'])
    improving = sum(1 for kpi in bundled_data if kpi['delta_direction'] == 'up')
    
    # Find top performer and concern
    top_performers = sorted(bundled_data, 
                          key=lambda x: (x['current_value'] - x['peer_avg']) / x['peer_avg'] 
                          if x['peer_avg'] > 0 else 0, reverse=True)
    concerns = sorted(bundled_data, 
                     key=lambda x: (x['peer_avg'] - x['current_value']) / x['peer_avg'] 
                     if x['peer_avg'] > 0 else 0, reverse=True)
    
    # Compact Header with Summary
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown(f"**🤖 AI Overview ({above_peer}/{total_kpis} Above Peer, {improving}/{total_kpis} Improving)**")
    
    with col2:
        if top_performers:
            st.success(f"🏆 **Best**: {top_performers[0]['kpi_name']} ({top_performers[0]['current_value']}{top_performers[0]['unit']})")
        if concerns and concerns[0]['current_value'] < concerns[0]['peer_avg']:
            st.error(f"⚠️ **Alert**: {concerns[0]['kpi_name']} ({concerns[0]['current_value']}{concerns[0]['unit']})")
    
    with col3:
        if st.button("🔄 Refresh", type="secondary", key=f"refresh_{tab_name}", use_container_width=True):
            st.rerun()
    
    # Expandable AI Analysis
    with st.expander("🔍 View Full AI Analysis", expanded=False):
        tab1, tab2, tab3 = st.tabs(["📊 Performance", "🎯 Details", "📝 Prompt"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Performance Overview**")
                metrics_df = pd.DataFrame({
                    'Metric': ['Total KPIs', 'Above Peer', 'Above Industry', 'Improving'],
                    'Value': [
                        total_kpis,
                        f"{above_peer}/{total_kpis}",
                        f"{sum(1 for kpi in bundled_data if kpi['current_value'] > kpi['industry_avg'])}/{total_kpis}",
                        f"{improving}/{total_kpis}"
                    ]
                })
                st.dataframe(metrics_df, hide_index=True, use_container_width=True)
            
            with col2:
                st.markdown("**Key Highlights**")
                if top_performers:
                    for kpi in top_performers[:2]:
                        st.success(f"✅ {kpi['kpi_name']}: {kpi['current_value']}{kpi['unit']}")
                if concerns and concerns[0]['current_value'] < concerns[0]['peer_avg']:
                    for kpi in concerns[:2]:
                        if kpi['current_value'] < kpi['peer_avg']:
                            st.error(f"❌ {kpi['kpi_name']}: {kpi['current_value']}{kpi['unit']}")
        
        with tab2:
            # Create a dataframe for all KPIs
            details_data = []
            for kpi in bundled_data:
                details_data.append({
                    'KPI': kpi['kpi_name'],
                    'Current': f"{kpi['current_value']}{kpi['unit']}",
                    'Prior': f"{kpi['prior_value']:.2f}{kpi['unit']}",
                    'Peer': f"{kpi['peer_avg']:.2f}{kpi['unit']}",
                    'Industry': f"{kpi['industry_avg']:.2f}{kpi['unit']}",
                    'Status': '✅' if kpi['current_value'] > kpi['peer_avg'] else '❌',
                    'Trend': '📈' if kpi['delta_direction'] == 'up' else '📉' if kpi['delta_direction'] == 'down' else '➖'
                })
            
            details_df = pd.DataFrame(details_data)
            st.dataframe(details_df, hide_index=True, use_container_width=True)
        
        with tab3:
            prompt = generate_ai_prompt(tab_name, bundled_data)
            st.code(prompt, language="text")
            st.info("💡 This prompt template can be customized in ai_insights_prompts.yaml")
    
    st.markdown("---")

def render_ai_insights_button(tab_name, days=30):
    """
    Render a simple button to trigger AI insights
    """
    if st.button(f"🤖 Generate AI Insights", type="primary", key=f"ai_insights_{tab_name}"):
        render_ai_insights_panel(tab_name, days)
        return True
    return False
