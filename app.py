import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
from kpi_components import *
from generate_test_data import *

# Page configuration
st.set_page_config(
    page_title="Telecom KPI Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-delta {
        font-size: 1rem;
        opacity: 0.9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">📡 Telecom KPI Dashboard</h1>', unsafe_allow_html=True)
    
    # Generate test data
    network_data = generate_network_data()
    customer_data = generate_customer_data()
    revenue_data = generate_revenue_data()
    usage_data = generate_usage_data()
    operations_data = generate_operations_data()
    
    # Create tabs for each KPI pillar
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📡 Network Performance", 
        "😊 Customer Experience", 
        "💰 Revenue & Monetization", 
        "📶 Usage & Adoption", 
        "🛠️ Operational Efficiency"
    ])
    
    # Tab 1: Network Performance
    with tab1:
        st.header("📡 Network Performance & Reliability")
        
        # Create 3 columns for metric cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card("Network Availability", "99.87%", "+0.12%", "uptime")
            render_metric_card("Latency", "45.2 ms", "-2.1 ms", "latency")
        
        with col2:
            render_metric_card("Bandwidth Utilization", "78.3%", "+3.2%", "bandwidth")
            render_metric_card("Dropped Call Rate", "1.2%", "-0.3%", "dcr")
        
        with col3:
            render_metric_card("Packet Loss Rate", "0.08%", "-0.02%", "packet_loss")
            render_metric_card("MTTR", "2.3 hours", "-0.5 hours", "mttr")
        
        # Charts section
        st.subheader("📈 Network Performance Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_line_chart(network_data['latency_trend'], "Network Latency Trend (30 days)", "ms")
            render_line_chart(network_data['uptime_trend'], "Network Availability Trend", "%")
        
        with col2:
            render_bar_chart(network_data['bandwidth_by_region'], "Bandwidth Utilization by Region", "%")
            render_area_chart(network_data['packet_loss_trend'], "Packet Loss Rate Trend", "%")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        render_kpi_expander("Network Availability", 
                           "Percentage of time the network is operational", 
                           lambda: render_line_chart(network_data['uptime_trend'], "Network Availability", "%"))
        
        render_kpi_expander("Dropped Call Rate (DCR)", 
                           "Percentage of calls terminated unexpectedly", 
                           lambda: render_line_chart(network_data['dcr_trend'], "Dropped Call Rate", "%"))
    
    # Tab 2: Customer Experience
    with tab2:
        st.header("😊 Customer Experience & Retention")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card("Customer Satisfaction", "4.2/5.0", "+0.3", "csat")
            render_metric_card("Net Promoter Score", "42", "+5", "nps")
        
        with col2:
            render_metric_card("Customer Churn Rate", "2.1%", "-0.4%", "churn")
            render_metric_card("Average Handling Time", "4.2 min", "-0.8 min", "aht")
        
        with col3:
            render_metric_card("First Contact Resolution", "78%", "+3%", "fcr")
            render_metric_card("Customer Lifetime Value", "$1,247", "+$89", "clv")
        
        # Charts
        st.subheader("📈 Customer Experience Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_line_chart(customer_data['csat_trend'], "Customer Satisfaction Trend", "Score")
            render_bar_chart(customer_data['churn_by_region'], "Churn Rate by Region", "%")
        
        with col2:
            render_area_chart(customer_data['nps_trend'], "Net Promoter Score Trend", "Score")
            render_distribution(customer_data['handling_time_dist'], "Support Call Duration Distribution", "Minutes")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        render_kpi_expander("Customer Satisfaction (CSAT)", 
                           "Post-interaction score (1-5 scale)", 
                           lambda: render_line_chart(customer_data['csat_trend'], "CSAT Trend", "Score"))
        
        render_kpi_expander("Net Promoter Score (NPS)", 
                           "% Promoters - % Detractors (0-10 scale)", 
                           lambda: render_area_chart(customer_data['nps_trend'], "NPS Trend", "Score"))
    
    # Tab 3: Revenue & Monetization
    with tab3:
        st.header("💰 Revenue & Monetization")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card("Average Revenue Per User", "$42.17", "+$3.25", "arpu")
            render_metric_card("Customer Lifetime Value", "$1,247", "+$89", "clv")
        
        with col2:
            render_metric_card("Customer Acquisition Cost", "$156", "-$12", "cac")
            render_metric_card("Subscriber Growth Rate", "8.3%", "+1.2%", "growth")
        
        with col3:
            render_metric_card("EBITDA Margin", "32.4%", "+2.1%", "ebitda")
            render_metric_card("Monthly Recurring Revenue", "$2.4M", "+$180K", "mrr")
        
        # Charts
        st.subheader("📈 Revenue Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_line_chart(revenue_data['arpu_trend'], "ARPU Trend (12 months)", "$")
            render_bar_chart(revenue_data['revenue_by_plan'], "Revenue by Plan Type", "$")
        
        with col2:
            render_area_chart(revenue_data['subscriber_growth'], "Subscriber Growth", "Count")
            render_line_chart(revenue_data['ebitda_trend'], "EBITDA Margin Trend", "%")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        render_kpi_expander("Average Revenue Per User (ARPU)", 
                           "Average monthly revenue per subscriber", 
                           lambda: render_line_chart(revenue_data['arpu_trend'], "ARPU Trend", "$"))
        
        render_kpi_expander("Customer Lifetime Value (CLV)", 
                           "Total expected profit per user over time", 
                           lambda: render_area_chart(revenue_data['clv_trend'], "CLV Trend", "$"))
    
    # Tab 4: Usage & Adoption
    with tab4:
        st.header("📶 Usage & Service Adoption")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card("Data Usage per Subscriber", "8.7 GB", "+1.2 GB", "data_usage")
            render_metric_card("Average Data Throughput", "45.2 Mbps", "+3.8 Mbps", "throughput")
        
        with col2:
            render_metric_card("Feature Adoption Rate", "67%", "+8%", "adoption")
            render_metric_card("5G Adoption Rate", "34%", "+12%", "5g_adoption")
        
        with col3:
            render_metric_card("Active Subscribers", "1.2M", "+45K", "active_subs")
            render_metric_card("Peak Usage Time", "8-10 PM", "Stable", "peak_time")
        
        # Charts
        st.subheader("📈 Usage Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_line_chart(usage_data['data_usage_trend'], "Data Usage Trend", "GB")
            render_bar_chart(usage_data['throughput_by_region'], "Throughput by Region", "Mbps")
        
        with col2:
            render_area_chart(usage_data['5g_adoption_trend'], "5G Adoption Trend", "%")
            render_distribution(usage_data['usage_distribution'], "Data Usage Distribution", "GB")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        render_kpi_expander("Data Usage per Subscriber", 
                           "Average GB/month per user", 
                           lambda: render_line_chart(usage_data['data_usage_trend'], "Data Usage Trend", "GB"))
        
        render_kpi_expander("5G Adoption Rate", 
                           "Percentage of subscribers using 5G services", 
                           lambda: render_area_chart(usage_data['5g_adoption_trend'], "5G Adoption", "%"))
    
    # Tab 5: Operational Efficiency
    with tab5:
        st.header("🛠️ Operational Efficiency")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            render_metric_card("Service Response Time", "2.1 hours", "-0.5 hours", "response_time")
            render_metric_card("Regulatory Compliance Rate", "98.7%", "+0.3%", "compliance")
        
        with col2:
            render_metric_card("Capex to Revenue Ratio", "18.2%", "-1.1%", "capex_ratio")
            render_metric_card("Network Efficiency Score", "87.3", "+2.1", "efficiency")
        
        with col3:
            render_metric_card("Support Ticket Resolution", "94.2%", "+1.8%", "resolution")
            render_metric_card("System Uptime", "99.92%", "+0.05%", "system_uptime")
        
        # Charts
        st.subheader("📈 Operational Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_line_chart(operations_data['response_time_trend'], "Service Response Time", "Hours")
            render_bar_chart(operations_data['compliance_by_region'], "Compliance Rate by Region", "%")
        
        with col2:
            render_area_chart(operations_data['efficiency_trend'], "Operational Efficiency Score", "Score")
            render_line_chart(operations_data['capex_trend'], "Capex to Revenue Ratio", "%")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        render_kpi_expander("Service Response Time", 
                           "Time from issue reported to first action taken", 
                           lambda: render_line_chart(operations_data['response_time_trend'], "Response Time", "Hours"))
        
        render_kpi_expander("Regulatory Compliance Rate", 
                           "Percentage of audits or checks passed successfully", 
                           lambda: render_bar_chart(operations_data['compliance_by_region'], "Compliance by Region", "%"))

if __name__ == "__main__":
    main() 