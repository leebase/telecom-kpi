import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
from kpi_components import *
from generate_test_data import *
from improved_metric_cards import *

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
    
    /* Print-optimized styles for PDF output */
    @media print {
        /* Hide Streamlit elements that shouldn't print */
        .stDeployButton, .stApp > header, .stApp > footer {
            display: none !important;
        }
        
        /* Ensure all content is visible for printing */
        .stTabs [data-baseweb="tab-panel"] {
            display: block !important;
            page-break-inside: avoid;
        }
        
        /* Force all tabs to be visible when printing */
        .stTabs [data-baseweb="tab-panel"] {
            opacity: 1 !important;
            visibility: visible !important;
            position: static !important;
            transform: none !important;
        }
        
        /* Optimize for PDF layout */
        body {
            font-size: 12pt;
            line-height: 1.4;
        }
        
        .main-header {
            font-size: 24pt;
            margin-bottom: 1rem;
        }
        
        .metric-card {
            break-inside: avoid;
            margin-bottom: 1rem;
        }
        
        /* Ensure charts are visible in print */
        .element-container {
            break-inside: avoid;
            page-break-inside: avoid;
        }
        
        /* Add page breaks between major sections */
        .stTabs [data-baseweb="tab-panel"] {
            page-break-before: always;
        }
        
        .stTabs [data-baseweb="tab-panel"]:first-child {
            page-break-before: auto;
        }
    }
    
    /* Print instruction overlay */
    .print-instructions {
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 12px;
        z-index: 1000;
        display: none;
    }
    
    .print-instructions.show {
        display: block;
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
        
        # Time period selector
        time_period = create_time_period_selector("network")
        
        # Convert time period to days
        time_period_days = {
            "Last 30 Days": 30,
            "QTD": 90,
            "YTD": 365,
            "Last 12 Months": 365
        }.get(time_period, 30)
        
        # Render improved metric grid
        network_metrics = get_network_metrics(time_period_days)
        render_metric_grid(network_metrics, "network")
        
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
        
        # Time period selector
        time_period = create_time_period_selector("customer")
        
        # Convert time period to days
        time_period_days = {
            "Last 30 Days": 30,
            "QTD": 90,
            "YTD": 365,
            "Last 12 Months": 365
        }.get(time_period, 30)
        
        # Render improved metric grid
        customer_metrics = get_customer_metrics(time_period_days)
        render_metric_grid(customer_metrics, "customer")
        
        # Get real customer experience data for charts
        customer_trend_data = db.get_customer_trend_data(time_period_days)
        
        # Charts
        st.subheader("📈 Customer Experience Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not customer_trend_data.empty:
                # Create satisfaction trend chart
                satisfaction_data = customer_trend_data[['region_id', 'satisfaction']].copy()
                satisfaction_data['date'] = '2023-08-01'
                satisfaction_data['value'] = satisfaction_data['satisfaction']
                render_line_chart(satisfaction_data, "Customer Satisfaction by Region", "Score")
                
                # Create churn by region chart
                churn_data = customer_trend_data[['region_id', 'churn']].copy()
                churn_data['category'] = churn_data['region_id'].astype(str)
                churn_data['value'] = churn_data['churn']
                render_bar_chart(churn_data, "Churn Rate by Region", "%")
            else:
                st.warning("No customer trend data available")
        
        with col2:
            if not customer_trend_data.empty:
                # Create NPS trend chart
                nps_data = customer_trend_data[['region_id', 'nps']].copy()
                nps_data['date'] = '2023-08-01'
                nps_data['value'] = nps_data['nps']
                render_area_chart(nps_data, "Net Promoter Score by Region", "Score")
                
                # Create handling time distribution chart
                handling_data = customer_trend_data[['region_id', 'handling_time']].copy()
                handling_data['value'] = handling_data['handling_time']
                render_distribution(handling_data, "Support Call Duration by Region", "Minutes")
            else:
                st.warning("No customer trend data available")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        if not customer_trend_data.empty:
            render_kpi_expander("Customer Satisfaction (CSAT)", 
                               "Post-interaction score (0-100 scale)", 
                               lambda: render_line_chart(satisfaction_data, "CSAT by Region", "Score"))
            
            render_kpi_expander("Net Promoter Score (NPS)", 
                               "% Promoters - % Detractors (-100 to +100 scale)", 
                               lambda: render_area_chart(nps_data, "NPS by Region", "Score"))
        else:
            st.warning("No customer trend data available for detailed analysis")
    
    # Tab 3: Revenue & Monetization
    with tab3:
        st.header("💰 Revenue & Monetization")
        
        # Time period selector
        time_period = create_time_period_selector("revenue")
        
        # Convert time period to days
        time_period_days = {
            "Last 30 Days": 30,
            "QTD": 90,
            "YTD": 365,
            "Last 12 Months": 365
        }.get(time_period, 30)
        
        # Render improved metric grid
        revenue_metrics = get_revenue_metrics(time_period_days)
        render_metric_grid(revenue_metrics, "revenue")
        
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
        
        # Time period selector
        time_period = create_time_period_selector("usage")
        
        # Convert time period to days
        time_period_days = {
            "Last 30 Days": 30,
            "QTD": 90,
            "YTD": 365,
            "Last 12 Months": 365
        }.get(time_period, 30)
        
        # Render improved metric grid
        usage_metrics = get_usage_metrics(time_period_days)
        render_metric_grid(usage_metrics, "usage")
        
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
        
        # Time period selector
        time_period = create_time_period_selector("operations")
        
        # Convert time period to days
        time_period_days = {
            "Last 30 Days": 30,
            "QTD": 90,
            "YTD": 365,
            "Last 12 Months": 365
        }.get(time_period, 30)
        
        # Render improved metric grid
        operations_metrics = get_operations_metrics(time_period_days)
        render_metric_grid(operations_metrics, "operations")
        
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