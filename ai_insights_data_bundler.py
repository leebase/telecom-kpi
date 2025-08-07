import streamlit as st
import pandas as pd
import yaml
from datetime import datetime
from improved_metric_cards import get_network_metrics, get_customer_metrics, get_revenue_metrics, get_usage_metrics, get_operations_metrics
from database_connection import db

def load_prompt_config():
    """Load prompt configuration from YAML file"""
    try:
        with open('ai_insights_prompts.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Error loading prompt config: {e}")
        return None

def get_prior_period_value(current_value, delta):
    """Calculate prior period value based on current value and delta"""
    if isinstance(delta, str):
        # Handle string deltas (like "N/A")
        return current_value
    return current_value - delta

def bundle_kpi_data_for_insights(tab_name, days=30):
    """
    Bundle KPI data with peer and industry benchmarks for AI insights
    Returns standardized format ready for LLM processing
    """
    
    # Get current KPI data based on tab
    if tab_name == "network":
        metrics_data = get_network_metrics(days)
    elif tab_name == "customer":
        metrics_data = get_customer_metrics(days)
    elif tab_name == "revenue":
        metrics_data = get_revenue_metrics(days)
    elif tab_name == "usage":
        metrics_data = get_usage_metrics(days)
    elif tab_name == "operations":
        metrics_data = get_operations_metrics(days)
    else:
        return []
    
    bundled_data = []
    
    for metric in metrics_data:
        kpi_name = metric['label']
        current_value = metric['value']
        delta = metric['delta']
        prior_value = get_prior_period_value(current_value, delta)
        
        # Get benchmarks for this KPI from database
        try:
            benchmark_data = db.get_benchmark_targets([kpi_name])
            if not benchmark_data.empty:
                benchmark = benchmark_data.iloc[0]
                peer_avg = benchmark['peer_avg']
                industry_avg = benchmark['industry_avg']
                unit = benchmark['unit']
                direction = benchmark['direction']
                threshold_low = benchmark['threshold_low']
                threshold_high = benchmark['threshold_high']
            else:
                # Fallback to default values if not found in database
                peer_avg = 0
                industry_avg = 0
                unit = metric.get('unit', '')
                direction = 'neutral'
                threshold_low = None
                threshold_high = None
        except Exception as e:
            st.warning(f"Error loading benchmarks for {kpi_name}: {e}")
            peer_avg = 0
            industry_avg = 0
            unit = metric.get('unit', '')
            direction = 'neutral'
            threshold_low = None
            threshold_high = None
        
        # Create standardized KPI entry
        kpi_entry = {
            "kpi_name": kpi_name,
            "current_value": current_value,
            "prior_value": prior_value,
            "peer_avg": peer_avg,
            "industry_avg": industry_avg,
            "unit": unit,
            "direction": direction,
            "threshold_low": threshold_low,
            "threshold_high": threshold_high,
            "delta": delta,
            "delta_direction": metric.get('delta_direction', 'stable'),
            "tooltip": metric.get('tooltip', ''),
            "last_updated": metric.get('last_updated', datetime.now().strftime('%Y-%m-%d %H:%M'))
        }
        
        bundled_data.append(kpi_entry)
    
    return bundled_data

def display_bundled_kpi_data(tab_name, days=30):
    """
    Display bundled KPI data in a formatted way for debugging/preview
    """
    st.subheader(f"🤖 AI Insights Data Bundle - {tab_name.title()} Tab")
    st.write("This shows the data that would be sent to the AI evaluator:")
    
    bundled_data = bundle_kpi_data_for_insights(tab_name, days)
    
    if not bundled_data:
        st.warning("No KPI data available for this tab")
        return
    
    # Display each KPI with its benchmarks
    for i, kpi in enumerate(bundled_data):
        with st.expander(f"📊 {kpi['kpi_name']}", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Current Value",
                    f"{kpi['current_value']}{kpi['unit']}",
                    f"{kpi['delta']:.2f}{kpi['unit']}"
                )
            
            with col2:
                st.metric(
                    "Prior Period",
                    f"{kpi['prior_value']:.2f}{kpi['unit']}"
                )
            
            with col3:
                st.metric(
                    "Peer Average",
                    f"{kpi['peer_avg']:.2f}{kpi['unit']}"
                )
            
            with col4:
                st.metric(
                    "Industry Average",
                    f"{kpi['industry_avg']:.2f}{kpi['unit']}"
                )
            
            # Show performance indicators
            current = kpi['current_value']
            peer = kpi['peer_avg']
            industry = kpi['industry_avg']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if current > peer:
                    st.success(f"✅ Above Peer ({current - peer:.2f} better)")
                elif current < peer:
                    st.error(f"❌ Below Peer ({peer - current:.2f} worse)")
                else:
                    st.info("➖ At Peer Level")
            
            with col2:
                if current > industry:
                    st.success(f"✅ Above Industry ({current - industry:.2f} better)")
                elif current < industry:
                    st.error(f"❌ Below Industry ({industry - current:.2f} worse)")
                else:
                    st.info("➖ At Industry Level")
            
            with col3:
                if kpi['delta_direction'] == 'up':
                    st.success("📈 Improving")
                elif kpi['delta_direction'] == 'down':
                    st.error("📉 Declining")
                else:
                    st.info("➖ Stable")
    
    # Show raw JSON for debugging
    with st.expander("🔧 Raw Data (JSON Format)"):
        st.json(bundled_data)

def create_ai_insights_button(tab_name, days=30):
    """
    Create a button to trigger AI insights data bundling
    """
    if st.button(f"🤖 Preview AI Insights Data for {tab_name.title()} Tab", type="primary"):
        display_bundled_kpi_data(tab_name, days)
        return True
    return False

def get_insights_prompt_context(bundled_data):
    """
    Generate a context string for the LLM prompt based on bundled data
    """
    context = f"Analyzing {len(bundled_data)} KPIs:\n\n"
    
    for kpi in bundled_data:
        # Format the KPI data with all available information
        context += f"• {kpi['kpi_name']}: {kpi['current_value']}{kpi['unit']} "
        context += f"(Prior: {kpi['prior_value']:.2f}{kpi['unit']}, "
        context += f"Peer: {kpi['peer_avg']:.2f}{kpi['unit']}, "
        context += f"Industry: {kpi['industry_avg']:.2f}{kpi['unit']}, "
        context += f"Direction: {kpi['direction']}, "
        context += f"Trend: {kpi['delta_direction']})\n"
        
        # Add threshold information if available
        if kpi.get('threshold_low') is not None and kpi.get('threshold_high') is not None:
            context += f"  - Thresholds: {kpi['threshold_low']:.2f} - {kpi['threshold_high']:.2f}{kpi['unit']}\n"
    
    return context

def generate_ai_prompt(tab_name, bundled_data):
    """
    Generate AI prompt using configurable templates
    """
    config = load_prompt_config()
    if not config:
        return "Error: Could not load prompt configuration"
    
    # Get prompt template for this tab
    if tab_name not in config['prompts']:
        return f"Error: No prompt template found for {tab_name}"
    
    prompt_config = config['prompts'][tab_name]
    
    # Generate context
    kpi_context = get_insights_prompt_context(bundled_data)
    
    # Build the complete prompt
    system_prompt = prompt_config['system_prompt']
    user_prompt = prompt_config['user_prompt_template'].format(kpi_context=kpi_context)
    output_format = prompt_config['output_format']
    
    full_prompt = f"""
{system_prompt}

{user_prompt}

{output_format}
"""
    
    return full_prompt

def preview_llm_prompt(tab_name, days=30):
    """
    Preview what the LLM prompt would look like
    """
    bundled_data = bundle_kpi_data_for_insights(tab_name, days)
    
    if not bundled_data:
        st.warning("No data available for prompt preview")
        return
    
    st.subheader("📝 LLM Prompt Preview")
    st.write("This is what would be sent to the AI model:")
    
    prompt = generate_ai_prompt(tab_name, bundled_data)
    
    st.code(prompt, language="text")
    
    st.info("💡 This prompt uses configurable templates from ai_insights_prompts.yaml. You can modify the prompts without changing code.")
