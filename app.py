import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
from kpi_components import *
from generate_test_data import *
from improved_metric_cards import *
from theme_manager import get_current_theme_css, get_current_theme_header, get_current_theme_page_header
from theme_switcher import create_theme_switcher

# Page configuration
st.set_page_config(
    page_title="Telecom KPI Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply current theme
st.markdown(get_current_theme_css(), unsafe_allow_html=True)

# Add print-specific CSS to show all tabs when printing
print_css = """
<style>
@media print {
    /* Hide the tab navigation completely */
    [data-testid="stTabs"] > div:first-child {
        display: none !important;
    }
    
    /* Force all tab content to be visible */
    [data-testid="stTabs"] > div:not(:first-child) {
        display: block !important;
        page-break-inside: avoid;
        margin-bottom: 30px;
    }
    
    /* Add page breaks between each tab content */
    [data-testid="stTabs"] > div:not(:first-child):not(:last-child) {
        page-break-after: always;
    }
    
    /* Hide sidebar when printing */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Ensure proper spacing */
    .main .block-container {
        padding: 0 !important;
        max-width: none !important;
    }
    
    /* Make sure all content is visible */
    * {
        visibility: visible !important;
    }
    
    /* Override any hidden elements */
    [style*="display: none"] {
        display: block !important;
    }
    
    /* Force all content to be visible in print mode */
    .print-mode * {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Ensure charts are visible */
    .vega-embed {
        display: block !important;
        visibility: visible !important;
    }
    
    /* Force all containers to be visible */
    [data-testid="stVerticalBlock"] {
        display: block !important;
        visibility: visible !important;
    }
}
</style>
"""
st.markdown(print_css, unsafe_allow_html=True)

# Add theme header
st.markdown(get_current_theme_header(), unsafe_allow_html=True)

# Render functions for each section
def render_network_performance(network_data):
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

def render_customer_experience(customer_data):
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
                
                # Create NPS by region chart (aggregated by region)
                nps_data = customer_trend_data.groupby('region_name')['nps'].mean().reset_index()
                nps_data['category'] = nps_data['region_name']
                nps_data['value'] = nps_data['nps']
                render_bar_chart(nps_data, "Net Promoter Score by Region", "Score")
            else:
                st.warning("No customer trend data available")
        
    with col2:
            if not customer_trend_data.empty:
                # Create churn rate by region chart (aggregated by region)
                churn_data = customer_trend_data.groupby('region_name')['churn'].mean().reset_index()
                churn_data['category'] = churn_data['region_name']
                churn_data['value'] = churn_data['churn']
                render_bar_chart(churn_data, "Churn Rate by Region", "%")
                
                # Create support duration by region chart (aggregated by region)
                duration_data = customer_trend_data.groupby('region_name')['handling_time'].mean().reset_index()
                duration_data['category'] = duration_data['region_name']
                duration_data['value'] = duration_data['handling_time']
                render_bar_chart(duration_data, "Support Call Duration by Region", "Minutes")
            else:
                st.warning("No customer trend data available")
    
    # KPI Expanders
    st.subheader("📘 Detailed KPI Information")
    if not customer_trend_data.empty:
        render_kpi_expander("Customer Satisfaction", 
                           "Average satisfaction score from customer surveys", 
                           lambda: render_bar_chart(satisfaction_data, "Customer Satisfaction by Region", "Score"))
        
        render_kpi_expander("Net Promoter Score (NPS)", 
                           "Likelihood of customers recommending the service", 
                           lambda: render_bar_chart(nps_data, "NPS by Region", "Score"))
    else:
        st.warning("No customer trend data available for detailed analysis")

def render_revenue_monetization(revenue_data):
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
            
            # Create subscribers by region chart (aggregated by region)
            subscribers_data = revenue_trend_data.groupby('region_name')['total_subscribers'].mean().reset_index()
            subscribers_data['category'] = subscribers_data['region_name']
            subscribers_data['value'] = subscribers_data['total_subscribers']
            render_bar_chart(subscribers_data, "Subscribers by Region", "Count")
        else:
            st.warning("No revenue trend data available")
    
    with col2:
        if not revenue_trend_data.empty:
            # Create EBITDA margin by region chart (aggregated by region)
            ebitda_data = revenue_trend_data.groupby('region_name')['avg_ebitda_margin'].mean().reset_index()
            ebitda_data['category'] = ebitda_data['region_name']
            ebitda_data['value'] = ebitda_data['avg_ebitda_margin']
            render_bar_chart(ebitda_data, "EBITDA Margin by Region", "%")
            
            # Create customer lifetime value by region chart (aggregated by region)
            clv_data = revenue_trend_data.groupby('region_name')['avg_clv'].mean().reset_index()
            clv_data['category'] = clv_data['region_name']
            clv_data['value'] = clv_data['avg_clv']
            render_bar_chart(clv_data, "Customer Lifetime Value by Region", "$")
        else:
            st.warning("No revenue trend data available")
    
    # KPI Expanders
    st.subheader("📘 Detailed KPI Information")
    if not revenue_trend_data.empty:
        render_kpi_expander("Average Revenue Per User (ARPU)", 
                           "Monthly revenue per active subscriber", 
                           lambda: render_bar_chart(arpu_data, "ARPU by Region", "$"))
        
        render_kpi_expander("EBITDA Margin", 
                           "Earnings before interest, taxes, depreciation, and amortization", 
                           lambda: render_bar_chart(ebitda_data, "EBITDA Margin by Region", "%"))
    else:
        st.warning("No revenue trend data available for detailed analysis")

def render_usage_adoption(usage_data):
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
            
            # Create 5G adoption by region chart (aggregated by region)
            five_g_data = usage_trend_data.groupby('region_name')['avg_five_g_adoption'].mean().reset_index()
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

def render_operational_efficiency(operations_data):
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

def main():
    # Check if we're in print mode (must be first!)
    print_mode = st.query_params.get("print", None) == "true"
    
    # Theme switcher in sidebar
    create_theme_switcher()
    
    # Print button in sidebar
    if st.sidebar.button("🖨️ Print All Tabs"):
        # Get the current URL and add print parameter
        import urllib.parse
        current_url = st.query_params.to_dict()
        current_url["print"] = "true"
        query_string = urllib.parse.urlencode(current_url, doseq=True)
        print_url = f"http://localhost:8501/?{query_string}"
        
        # Open in new tab for printing
        st.markdown(f"""
        <script>
        window.open('{print_url}', '_blank');
        </script>
        """, unsafe_allow_html=True)
    
    # Direct link to print mode for testing
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Quick Print Links:**")
    if st.sidebar.button("📄 Open Print Mode"):
        st.markdown(f"""
        <script>
        window.open('http://localhost:8501/?print=true', '_blank');
        </script>
        """, unsafe_allow_html=True)
    
    # Add JavaScript to force all content visibility when printing
    if print_mode:
        st.markdown("""
        <script>
        // Force all content to be visible when printing
        window.addEventListener('load', function() {
            // Wait a bit for content to load
            setTimeout(function() {
                // Force all elements to be visible
                var allElements = document.querySelectorAll('*');
                for (var i = 0; i < allElements.length; i++) {
                    allElements[i].style.display = 'block';
                    allElements[i].style.visibility = 'visible';
                }
                
                // Ensure charts are visible
                var charts = document.querySelectorAll('.vega-embed');
                for (var i = 0; i < charts.length; i++) {
                    charts[i].style.display = 'block';
                    charts[i].style.visibility = 'visible';
                }
            }, 2000);
        });
        </script>
        """, unsafe_allow_html=True)
    
    # Debug: Show print mode status
    if print_mode:
        st.sidebar.info("🖨️ Print Mode Active - All tabs will be visible")
    
    # Page header with current theme styling
    st.markdown(get_current_theme_page_header(
        "Network Performance & Reliability",
        "Select a time period and explore KPIs across Network Performance, Customer Experience, Revenue & Monetization, Usage & Adoption, and Operational Efficiency."
    ), unsafe_allow_html=True)
    
    # Generate test data
    network_data = generate_network_data()
    customer_data = generate_customer_data()
    revenue_data = generate_revenue_data()
    usage_data = generate_usage_data()
    operations_data = generate_operations_data()
    
    # Create tabs for each KPI pillar
    if not print_mode:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📡 Network Performance", 
            "😊 Customer Experience", 
            "💰 Revenue & Monetization", 
            "📶 Usage & Adoption", 
            "🛠️ Operational Efficiency"
        ])
        
        # Tab 1: Network Performance
        with tab1:
            render_network_performance(network_data)
        
        # Tab 2: Customer Experience
        with tab2:
            render_customer_experience(customer_data)
        
        # Tab 3: Revenue & Monetization
        with tab3:
            render_revenue_monetization(revenue_data)
        
        # Tab 4: Usage & Adoption
        with tab4:
            render_usage_adoption(usage_data)
        
        # Tab 5: Operational Efficiency
        with tab5:
            render_operational_efficiency(operations_data)
    else:
        # In print mode, render all content directly with print-specific styling
        st.markdown('<div class="print-mode">', unsafe_allow_html=True)
        
        st.markdown("## 📡 Network Performance")
        render_network_performance(network_data)
        st.markdown("---")
        
        st.markdown("## 😊 Customer Experience")
        render_customer_experience(customer_data)
        st.markdown("---")
        
        st.markdown("## 💰 Revenue & Monetization")
        render_revenue_monetization(revenue_data)
        st.markdown("---")
        
        st.markdown("## 📶 Usage & Adoption")
        render_usage_adoption(usage_data)
        st.markdown("---")
        
        st.markdown("## 🛠️ Operational Efficiency")
        render_operational_efficiency(operations_data)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 