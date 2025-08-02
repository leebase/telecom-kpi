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
                # Create satisfaction by region chart (aggregated by region)
                satisfaction_data = customer_trend_data.groupby('region_name')['satisfaction'].mean().reset_index()
                satisfaction_data['category'] = satisfaction_data['region_name']
                satisfaction_data['value'] = satisfaction_data['satisfaction']
                render_bar_chart(satisfaction_data, "Customer Satisfaction by Region", "Score")
                
                # Create churn by region chart
                churn_data = customer_trend_data[['region_name', 'churn']].copy()
                churn_data['category'] = churn_data['region_name']
                churn_data['value'] = churn_data['churn']
                render_bar_chart(churn_data, "Churn Rate by Region", "%")
            else:
                st.warning("No customer trend data available")
        
        with col2:
            if not customer_trend_data.empty:
                # Create NPS by region chart (aggregated by region)
                nps_data = customer_trend_data.groupby('region_name')['nps'].mean().reset_index()
                nps_data['category'] = nps_data['region_name']
                nps_data['value'] = nps_data['nps']
                render_bar_chart(nps_data, "Net Promoter Score by Region", "Score")
                
                # Create handling time chart (Duration on x-axis, Region on y-axis)
                handling_data = customer_trend_data[['region_name', 'handling_time']].copy()
                handling_data['category'] = handling_data['region_name']
                handling_data['value'] = handling_data['handling_time']
                render_bar_chart(handling_data, "Support Call Duration by Region", "Minutes")
            else:
                st.warning("No customer trend data available")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        if not customer_trend_data.empty:
            render_kpi_expander("Customer Satisfaction (CSAT)", 
                               "Post-interaction score (0-100 scale)", 
                               lambda: render_bar_chart(satisfaction_data, "Customer Satisfaction by Region", "Score"))
            
            render_kpi_expander("Net Promoter Score (NPS)", 
                               "% Promoters - % Detractors (-100 to +100 scale)", 
                               lambda: render_bar_chart(nps_data, "Net Promoter Score by Region", "Score"))
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
        
        # Get real revenue data for charts
        revenue_trend_data = db.get_revenue_trend_data(time_period_days)
        
        # Charts
        st.subheader("📈 Revenue Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not revenue_trend_data.empty:
                # Create ARPU by region chart (aggregated by region)
                arpu_data = revenue_trend_data.groupby('region_name')['avg_arpu'].mean().reset_index()
                arpu_data['category'] = arpu_data['region_name']
                arpu_data['value'] = arpu_data['avg_arpu']
                render_bar_chart(arpu_data, "ARPU by Region", "$")
                
                # Create revenue by region chart
                revenue_by_region = revenue_trend_data[['region_name', 'total_revenue']].copy()
                revenue_by_region['category'] = revenue_by_region['region_name']
                revenue_by_region['value'] = revenue_by_region['total_revenue']
                render_bar_chart(revenue_by_region, "Revenue by Region", "$")
            else:
                st.warning("No revenue trend data available")
        
        with col2:
            if not revenue_trend_data.empty:
                # Create subscriber by region chart (aggregated by region)
                subscriber_data = revenue_trend_data.groupby('region_name')['total_subscribers'].mean().reset_index()
                subscriber_data['category'] = subscriber_data['region_name']
                subscriber_data['value'] = subscriber_data['total_subscribers']
                render_bar_chart(subscriber_data, "Subscribers by Region", "Count")
                
                # Create EBITDA margin by region chart (aggregated by region)
                ebitda_data = revenue_trend_data.groupby('region_name')['avg_ebitda_margin'].mean().reset_index()
                ebitda_data['category'] = ebitda_data['region_name']
                ebitda_data['value'] = ebitda_data['avg_ebitda_margin']
                render_bar_chart(ebitda_data, "EBITDA Margin by Region", "%")
            else:
                st.warning("No revenue trend data available")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        if not revenue_trend_data.empty:
            render_kpi_expander("Average Revenue Per User (ARPU)", 
                               "Average monthly revenue per subscriber", 
                               lambda: render_bar_chart(arpu_data, "ARPU by Region", "$"))
            
            render_kpi_expander("Customer Lifetime Value (CLV)", 
                               "Total expected profit per user over time", 
                               lambda: render_bar_chart(revenue_trend_data.groupby('region_name')['avg_clv'].mean().reset_index().assign(category=lambda x: x['region_name'], value=lambda x: x['avg_clv']), "CLV by Region", "$"))
        else:
            st.warning("No revenue trend data available for detailed analysis")
    
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
        
        # Get real usage data for charts
        usage_trend_data = db.get_usage_trend_data(time_period_days)
        
        # Charts
        st.subheader("📈 Usage Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not usage_trend_data.empty:
                # Create data usage by region chart (aggregated by region)
                data_usage_data = usage_trend_data.groupby('region_name')['avg_data_usage'].mean().reset_index()
                data_usage_data['category'] = data_usage_data['region_name']
                data_usage_data['value'] = data_usage_data['avg_data_usage']
                render_bar_chart(data_usage_data, "Data Usage by Region", "GB")
                
                # Create 5G adoption chart
                five_g_data = usage_trend_data[['region_name', 'avg_five_g_adoption']].copy()
                five_g_data['category'] = five_g_data['region_name']
                five_g_data['value'] = five_g_data['avg_five_g_adoption']
                render_bar_chart(five_g_data, "5G Adoption by Region", "%")
            else:
                st.warning("No usage trend data available")
        
        with col2:
            if not usage_trend_data.empty:
                # Create service penetration by region chart (aggregated by region)
                penetration_data = usage_trend_data.groupby('region_name')['avg_service_penetration'].mean().reset_index()
                penetration_data['category'] = penetration_data['region_name']
                penetration_data['value'] = penetration_data['avg_service_penetration']
                render_bar_chart(penetration_data, "Service Penetration by Region", "%")
                
                # Create app usage by region chart (aggregated by region)
                app_usage_data = usage_trend_data.groupby('region_name')['avg_app_usage'].mean().reset_index()
                app_usage_data['category'] = app_usage_data['region_name']
                app_usage_data['value'] = app_usage_data['avg_app_usage']
                render_bar_chart(app_usage_data, "App Usage by Region", "%")
            else:
                st.warning("No usage trend data available")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        if not usage_trend_data.empty:
            render_kpi_expander("Data Usage per Subscriber", 
                               "Average GB/month per user", 
                               lambda: render_bar_chart(data_usage_data, "Data Usage by Region", "GB"))
            
            render_kpi_expander("5G Adoption Rate", 
                               "Percentage of subscribers using 5G services", 
                               lambda: render_bar_chart(five_g_data, "5G Adoption by Region", "%"))
        else:
            st.warning("No usage trend data available for detailed analysis")
    
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
        
        # Get real operations data for charts
        operations_trend_data = db.get_operations_trend_data(time_period_days)
        
        # Charts
        st.subheader("📈 Operational Trends")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if not operations_trend_data.empty:
                # Create response time by region chart (aggregated by region)
                response_data = operations_trend_data.groupby('region_name')['avg_response_time'].mean().reset_index()
                response_data['category'] = response_data['region_name']
                response_data['value'] = response_data['avg_response_time']
                render_bar_chart(response_data, "Service Response Time by Region", "Hours")
                
                # Create compliance rate chart
                compliance_data = operations_trend_data[['region_name', 'avg_compliance_rate']].copy()
                compliance_data['category'] = compliance_data['region_name']
                compliance_data['value'] = compliance_data['avg_compliance_rate']
                render_bar_chart(compliance_data, "Compliance Rate by Region", "%")
            else:
                st.warning("No operations trend data available")
        
        with col2:
            if not operations_trend_data.empty:
                # Create efficiency score by region chart (aggregated by region)
                efficiency_data = operations_trend_data.groupby('region_name')['avg_efficiency_score'].mean().reset_index()
                efficiency_data['category'] = efficiency_data['region_name']
                efficiency_data['value'] = efficiency_data['avg_efficiency_score']
                render_bar_chart(efficiency_data, "Operational Efficiency by Region", "Score")
                
                # Create capex ratio by region chart (aggregated by region)
                capex_data = operations_trend_data.groupby('region_name')['avg_capex_ratio'].mean().reset_index()
                capex_data['category'] = capex_data['region_name']
                capex_data['value'] = capex_data['avg_capex_ratio']
                render_bar_chart(capex_data, "Capex to Revenue Ratio by Region", "%")
            else:
                st.warning("No operations trend data available")
        
        # KPI Expanders
        st.subheader("📘 Detailed KPI Information")
        if not operations_trend_data.empty:
            render_kpi_expander("Service Response Time", 
                               "Time from issue reported to first action taken", 
                               lambda: render_bar_chart(response_data, "Service Response Time by Region", "Hours"))
            
            render_kpi_expander("Regulatory Compliance Rate", 
                               "Percentage of audits or checks passed successfully", 
                               lambda: render_bar_chart(compliance_data, "Compliance Rate by Region", "%"))
        else:
            st.warning("No operations trend data available for detailed analysis")

if __name__ == "__main__":
    main() 