import streamlit as st
import pandas as pd
from datetime import datetime
from database_connection import db

def create_metric_card(label, value, delta, delta_direction="up", unit="", tooltip="", last_updated=None, tab_name=""):
    """
    Create a theme-appropriate metric card using HTML
    """
    
    # Get current theme to determine styling
    try:
        from theme_manager import get_current_theme
        current_theme = get_current_theme()
    except:
        current_theme = "cognizant"  # Default fallback
    
    # Format the value with unit
    if isinstance(value, str):
        formatted_value = value
    elif unit == "$":
        formatted_value = f"${value:,.2f}"
    elif unit == "%":
        formatted_value = f"{value:.2f}%"
    else:
        formatted_value = f"{value}{unit}"
    
    # Format delta value
    if isinstance(delta, str):
        formatted_delta = f"{delta}"
    elif unit == "$":
        formatted_delta = f"${delta:,.2f}"
    elif unit == "%":
        formatted_delta = f"{delta:.2f}%"
    else:
        formatted_delta = f"{delta}{unit}"
    
    # Default last updated
    if last_updated is None:
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    if current_theme == "verizon":
        # Verizon styling
        if delta_direction == "up":
            delta_class = "verizon-kpi-delta up"
        elif delta_direction == "down":
            delta_class = "verizon-kpi-delta down"
        else:  # stable
            delta_class = "verizon-kpi-delta flat"
        
        card_html = f"""
        <div class="verizon-kpi-tile">
            <div class="verizon-kpi-head">
                <div class="verizon-kpi-label">{label}</div>
            </div>
            <div class="verizon-kpi-value">{formatted_value}</div>
            <div class="{delta_class}">
                <span class="arrow" aria-hidden="true"></span>
                <span>{formatted_delta}</span>
            </div>
            <div class="verizon-kpi-updated">Updated: {last_updated}</div>
            <div class="verizon-sparkline" aria-hidden="true">
                <div class="line" style="top: 38%"></div>
            </div>
            <div class="verizon-kpi-footer">
                <span title="{tooltip}">ℹ️ {label}</span>
                <span>Target: {formatted_value}</span>
            </div>
        </div>
        """
    else:
        # Cognizant styling (default)
        if delta_direction == "up":
            delta_class = "cognizant-kpi-delta up"
            delta_arrow = "▲"
        elif delta_direction == "down":
            delta_class = "cognizant-kpi-delta down"
            delta_arrow = "▼"
        else:  # stable
            delta_class = "cognizant-kpi-delta flat"
            delta_arrow = "●"
        
        # Format delta with arrow for Cognizant
        if isinstance(delta, str):
            formatted_delta = f"{delta_arrow} {delta}"
        elif unit == "$":
            formatted_delta = f"{delta_arrow} ${delta:,.2f}"
        elif unit == "%":
            formatted_delta = f"{delta_arrow} {delta:.2f}%"
        else:
            formatted_delta = f"{delta_arrow} {delta}{unit}"
        
        card_html = f"""
        <div class="cognizant-kpi-tile">
            <div class="cognizant-kpi-head">
                <div class="cognizant-kpi-label">{label}</div>
            </div>
            <div class="cognizant-kpi-value">{formatted_value}</div>
            <div class="{delta_class}">
                <span class="arrow" aria-hidden="true"></span>
                <span>{formatted_delta}</span>
            </div>
            <div class="cognizant-kpi-updated">Updated: {last_updated}</div>
            <div class="cognizant-sparkline" aria-hidden="true">
                <div class="line" style="top: 38%"></div>
            </div>
            <div class="cognizant-kpi-footer">
                <span title="{tooltip}">ℹ️ {label}</span>
                <span>Target: {formatted_value}</span>
            </div>
        </div>
        """
    
    st.markdown(card_html, unsafe_allow_html=True)

def render_metric_grid(metrics_data, tab_name=""):
    """
    Render a responsive 3-column grid of metric cards
    
    Args:
        metrics_data (list): List of dictionaries with metric data
        tab_name (str): Name of the tab for unique keys
    """
    
    # Create 3 columns for the grid
    col1, col2, col3 = st.columns(3)
    
    # Render metrics in grid
    for i, metric in enumerate(metrics_data):
        # Place in appropriate column
        if i % 3 == 0:
            with col1:
                create_metric_card(
                    label=metric['label'],
                    value=metric['value'],
                    delta=metric['delta'],
                    delta_direction=metric['delta_direction'],
                    unit=metric.get('unit', ''),
                    tooltip=metric.get('tooltip', ''),
                    last_updated=metric.get('last_updated'),
                    tab_name=tab_name
                )
        elif i % 3 == 1:
            with col2:
                create_metric_card(
                    label=metric['label'],
                    value=metric['value'],
                    delta=metric['delta'],
                    delta_direction=metric['delta_direction'],
                    unit=metric.get('unit', ''),
                    tooltip=metric.get('tooltip', ''),
                    last_updated=metric.get('last_updated'),
                    tab_name=tab_name
                )
        else:
            with col3:
                create_metric_card(
                    label=metric['label'],
                    value=metric['value'],
                    delta=metric['delta'],
                    delta_direction=metric['delta_direction'],
                    unit=metric.get('unit', ''),
                    tooltip=metric.get('tooltip', ''),
                    last_updated=metric.get('last_updated'),
                    tab_name=tab_name
                )

def create_time_period_selector(tab_name=""):
    """
    Create a time period selector for dynamic delta updates
    """
    time_period = st.selectbox(
        "Select Time Period",
        ["Last 30 Days", "QTD", "YTD", "Last 12 Months"],
        key=f"time_period_selector_{tab_name}"
    )
    return time_period

def get_network_metrics(days=30):
    """Get network performance metrics from database"""
    try:
        metrics = db.get_network_metrics(days)
        
        if metrics.empty:
            # Fallback to default values if no data
            return [
                {
                    'label': 'Network Availability',
                    'value': 99.87,
                    'delta': 0.12,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of time the network is operational. Critical for SLA compliance and customer satisfaction.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Latency',
                    'value': 45.2,
                    'delta': -2.1,
                    'delta_direction': 'down',
                    'unit': ' ms',
                    'tooltip': 'Average round-trip time for data packets. Critical for real-time applications like VoIP and gaming.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Bandwidth Utilization',
                    'value': 78.3,
                    'delta': 3.2,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of total network capacity being used. Indicates congestion risk and capacity planning needs.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Dropped Call Rate',
                    'value': 1.2,
                    'delta': -0.3,
                    'delta_direction': 'down',
                    'unit': '%',
                    'tooltip': 'Percentage of calls terminated unexpectedly. Key voice quality metric affecting customer satisfaction.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Packet Loss Rate',
                    'value': 0.08,
                    'delta': -0.02,
                    'delta_direction': 'down',
                    'unit': '%',
                    'tooltip': 'Percentage of packets lost in transmission. Impacts streaming quality and network integrity.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'MTTR',
                    'value': 2.3,
                    'delta': -0.5,
                    'delta_direction': 'down',
                    'unit': ' hours',
                    'tooltip': 'Mean Time to Repair - Average time to resolve network outages. Reflects operational responsiveness.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            ]
        
        # Calculate deltas (simplified - in real scenario you'd compare with previous period)
        delta_availability = round(metrics['avg_availability'] - 99.5, 2)
        delta_latency = round(metrics['avg_latency'] - 50, 2)
        delta_packet_loss = round(metrics['avg_packet_loss'] - 0.1, 3)
        delta_bandwidth = round(metrics['avg_bandwidth_util'] - 65, 1)
        delta_mttr = round(metrics['avg_mttr'] - 2.5, 1)
        delta_dropped_calls = round(metrics['avg_dropped_call_rate'] - 1.0, 2)
        
        return [
            {
                'label': 'Network Availability',
                'value': round(metrics['avg_availability'], 2),
                'delta': delta_availability,
                'delta_direction': 'up' if delta_availability > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of time the network is operational. Critical for SLA compliance and customer satisfaction.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Latency',
                'value': round(metrics['avg_latency'], 1),
                'delta': delta_latency,
                'delta_direction': 'down' if delta_latency < 0 else 'up',
                'unit': ' ms',
                'tooltip': 'Average round-trip time for data packets. Critical for real-time applications like VoIP and gaming.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Bandwidth Utilization',
                'value': round(metrics['avg_bandwidth_util'], 1),
                'delta': delta_bandwidth,
                'delta_direction': 'up' if delta_bandwidth > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of total network capacity being used. Indicates congestion risk and capacity planning needs.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Dropped Call Rate',
                'value': round(metrics['avg_dropped_call_rate'], 2),
                'delta': delta_dropped_calls,
                'delta_direction': 'down' if delta_dropped_calls < 0 else 'up',
                'unit': '%',
                'tooltip': 'Percentage of calls terminated unexpectedly. Key voice quality metric affecting customer satisfaction.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Packet Loss Rate',
                'value': round(metrics['avg_packet_loss'], 3),
                'delta': delta_packet_loss,
                'delta_direction': 'down' if delta_packet_loss < 0 else 'up',
                'unit': '%',
                'tooltip': 'Percentage of packets lost in transmission. Impacts streaming quality and network integrity.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'MTTR',
                'value': round(metrics['avg_mttr'], 1),
                'delta': delta_mttr,
                'delta_direction': 'down' if delta_mttr < 0 else 'up',
                'unit': ' hours',
                'tooltip': 'Mean Time to Repair - Average time to resolve network outages. Reflects operational responsiveness.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        ]
    except Exception as e:
        st.error(f"Error loading network metrics: {e}")
        return []

def get_customer_metrics(days=30):
    """Get customer experience metrics from database"""
    try:
        metrics = db.get_customer_metrics(days)
        
        if metrics.empty:
            # Fallback to default values if no data
            return [
                {
                    'label': 'Customer Satisfaction',
                    'value': 4.2,
                    'delta': 0.3,
                    'delta_direction': 'up',
                    'unit': '/5.0',
                    'tooltip': 'Post-interaction satisfaction score (1-5 scale). Short-term measure of service quality.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Net Promoter Score',
                    'value': 42,
                    'delta': 5,
                    'delta_direction': 'up',
                    'unit': '',
                    'tooltip': 'Net Promoter Score - % Promoters - % Detractors (0-10 scale). Predicts loyalty and referrals.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Customer Churn Rate',
                    'value': 2.1,
                    'delta': -0.4,
                    'delta_direction': 'down',
                    'unit': '%',
                    'tooltip': 'Percentage of customers who cancel service. Indicates dissatisfaction and financial risk.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Average Handling Time',
                    'value': 4.2,
                    'delta': -0.8,
                    'delta_direction': 'down',
                    'unit': ' min',
                    'tooltip': 'Average duration of customer support interactions. Key efficiency metric for support teams.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'First Contact Resolution',
                    'value': 78.5,
                    'delta': 2.1,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of issues resolved on first contact. Key efficiency and satisfaction metric.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Customer Lifetime Value',
                    'value': 1250,
                    'delta': 45,
                    'delta_direction': 'up',
                    'unit': '$',
                    'tooltip': 'Total expected profit per customer over time. Key metric for customer acquisition decisions.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            ]
        
        # Calculate deltas based on actual customer experience data
        delta_csat = round(metrics['csat_score'] - 85.0, 1)
        delta_nps = round(metrics['nps_score'] - 45.0, 1)
        delta_churn = round(metrics['churn_rate'] - 4.8, 1)
        delta_handling = round(metrics['avg_response_time'] - 4.1, 1)
        delta_fcr = round(metrics['first_contact_resolution'] - 86.4, 1)
        delta_clv = round(metrics['customer_lifetime_value'] - 2500, 0)
        
        return [
            {
                'label': 'Customer Satisfaction',
                'value': round(metrics['csat_score'], 1),
                'delta': delta_csat,
                'delta_direction': 'up' if delta_csat > 0 else 'down',
                'unit': '/100',
                'tooltip': 'Customer satisfaction score (0-100 scale). Post-interaction satisfaction measure.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Net Promoter Score',
                'value': round(metrics['nps_score'], 0),
                'delta': delta_nps,
                'delta_direction': 'up' if delta_nps > 0 else 'down',
                'unit': '',
                'tooltip': 'Net Promoter Score - % Promoters - % Detractors (-100 to +100 scale). Predicts loyalty and referrals.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Customer Churn Rate',
                'value': round(metrics['churn_rate'], 1),
                'delta': delta_churn,
                'delta_direction': 'down' if delta_churn < 0 else 'up',
                'unit': '%',
                'tooltip': 'Percentage of customers who cancel service. Indicates dissatisfaction and financial risk.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Average Handling Time',
                'value': round(metrics['avg_response_time'], 1),
                'delta': delta_handling,
                'delta_direction': 'down' if delta_handling < 0 else 'up',
                'unit': ' min',
                'tooltip': 'Average duration of customer support interactions. Key efficiency metric for support teams.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'First Contact Resolution',
                'value': round(metrics['first_contact_resolution'], 1),
                'delta': delta_fcr,
                'delta_direction': 'up' if delta_fcr > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of issues resolved on first contact. Key efficiency and satisfaction metric.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Customer Lifetime Value',
                'value': round(metrics['customer_lifetime_value'], 0),
                'delta': delta_clv,
                'delta_direction': 'up' if delta_clv > 0 else 'down',
                'unit': '$',
                'tooltip': 'Total expected profit per customer over time. Key metric for customer acquisition decisions.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        ]
    except Exception as e:
        st.error(f"Error loading customer metrics: {e}")
        return []
    return [
        {
            'label': 'Customer Satisfaction',
            'value': 4.2,
            'delta': 0.3,
            'delta_direction': 'up',
            'unit': '/5.0',
            'tooltip': 'Post-interaction satisfaction score (1-5 scale). Short-term measure of service quality.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Net Promoter Score',
            'value': 42,
            'delta': 5,
            'delta_direction': 'up',
            'unit': '',
            'tooltip': 'Net Promoter Score - % Promoters - % Detractors (0-10 scale). Predicts loyalty and referrals.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Customer Churn Rate',
            'value': 2.1,
            'delta': -0.4,
            'delta_direction': 'down',
            'unit': '%',
            'tooltip': 'Percentage of customers who cancel service. Indicates dissatisfaction and financial risk.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Average Handling Time',
            'value': 4.2,
            'delta': -0.8,
            'delta_direction': 'down',
            'unit': ' min',
            'tooltip': 'Average duration of customer support interactions. Key efficiency metric for support teams.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'First Contact Resolution',
            'value': 78,
            'delta': 3,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Percentage of issues resolved in one interaction. Ties to lower costs and higher satisfaction.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Customer Lifetime Value',
            'value': 1247,
            'delta': 89,
            'delta_direction': 'up',
            'unit': '$',
            'tooltip': 'Total expected profit per user over time. Guides acquisition and retention spend.',
            'last_updated': '2025-07-30 08:15'
        }
    ]

def get_revenue_metrics(days=30):
    """Get revenue and monetization metrics from database"""
    try:
        metrics = db.get_revenue_metrics(days)
        
        if metrics.empty:
            # Fallback to default values if no data
            return [
                {
                    'label': 'ARPU',
                    'value': 42.17,
                    'delta': 3.2,
                    'delta_direction': 'up',
                    'unit': '$',
                    'tooltip': 'Average Revenue Per User - Total revenue divided by number of subscribers.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'EBITDA Margin',
                    'value': 28.5,
                    'delta': 2.1,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Earnings Before Interest, Taxes, Depreciation, and Amortization margin.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Customer Acquisition Cost',
                    'value': 125,
                    'delta': -8.5,
                    'delta_direction': 'down',
                    'unit': '$',
                    'tooltip': 'Total cost to acquire a new customer. Key metric for marketing efficiency.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Customer Lifetime Value',
                    'value': 1850,
                    'delta': 125,
                    'delta_direction': 'up',
                    'unit': '$',
                    'tooltip': 'Total expected profit per customer over time. Key metric for customer acquisition decisions.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Revenue Growth',
                    'value': 12.3,
                    'delta': 1.8,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Year-over-year revenue growth rate. Indicates business expansion and market share gains.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Profit Margin',
                    'value': 18.7,
                    'delta': 1.2,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Net profit margin - percentage of revenue that becomes profit after all expenses.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            ]
        
        # Calculate deltas based on actual revenue data
        delta_arpu = round(metrics['arpu'] - 76.0, 2)
        delta_ebitda = round(metrics['ebitda_margin'] - 32.7, 1)
        delta_cac = round(metrics['customer_acquisition_cost'] - 170.0, 1)
        delta_clv = round(metrics['customer_lifetime_value'] - 2600.0, 0)
        delta_growth = round(metrics['revenue_growth'] - 9.8, 1)
        delta_profit = round(metrics['profit_margin'] - 19.9, 1)
        
        return [
            {
                'label': 'ARPU',
                'value': round(metrics['arpu'], 2),
                'delta': delta_arpu,
                'delta_direction': 'up' if delta_arpu > 0 else 'down',
                'unit': '$',
                'tooltip': 'Average Revenue Per User - Total revenue divided by number of subscribers.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'EBITDA Margin',
                'value': round(metrics['ebitda_margin'], 1),
                'delta': delta_ebitda,
                'delta_direction': 'up' if delta_ebitda > 0 else 'down',
                'unit': '%',
                'tooltip': 'Earnings Before Interest, Taxes, Depreciation, and Amortization margin.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Customer Acquisition Cost',
                'value': round(metrics['customer_acquisition_cost'], 0),
                'delta': delta_cac,
                'delta_direction': 'down' if delta_cac < 0 else 'up',
                'unit': '$',
                'tooltip': 'Total cost to acquire a new customer. Key metric for marketing efficiency.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Customer Lifetime Value',
                'value': round(metrics['customer_lifetime_value'], 0),
                'delta': delta_clv,
                'delta_direction': 'up' if delta_clv > 0 else 'down',
                'unit': '$',
                'tooltip': 'Total expected profit per customer over time. Key metric for customer acquisition decisions.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Revenue Growth',
                'value': round(metrics['revenue_growth'], 1),
                'delta': delta_growth,
                'delta_direction': 'up' if delta_growth > 0 else 'down',
                'unit': '%',
                'tooltip': 'Year-over-year revenue growth rate. Indicates business expansion and market share gains.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Profit Margin',
                'value': round(metrics['profit_margin'], 1),
                'delta': delta_profit,
                'delta_direction': 'up' if delta_profit > 0 else 'down',
                'unit': '%',
                'tooltip': 'Net profit margin - percentage of revenue that becomes profit after all expenses.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        ]
    except Exception as e:
        st.error(f"Error loading revenue metrics: {e}")
        return []

def get_usage_metrics(days=30):
    """Get usage and service adoption metrics from database"""
    try:
        metrics = db.get_usage_metrics(days)
        
        if metrics.empty:
            # Fallback to default values if no data
            return [
                {
                    'label': 'Data Usage per Subscriber',
                    'value': 8.5,
                    'delta': 0.7,
                    'delta_direction': 'up',
                    'unit': 'GB',
                    'tooltip': 'Average data consumption per subscriber per month. Indicates service utilization.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': '5G Adoption Rate',
                    'value': 45.2,
                    'delta': 8.3,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of subscribers using 5G services. Key indicator of network modernization.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Feature Adoption Rate',
                    'value': 32.8,
                    'delta': 4.1,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of subscribers using premium features. Revenue optimization metric.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Service Penetration',
                    'value': 78.5,
                    'delta': 2.3,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of addressable market using our services. Market share indicator.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'App Usage Rate',
                    'value': 65.3,
                    'delta': 5.2,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of subscribers using our mobile app. Digital engagement metric.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Premium Service Adoption',
                    'value': 28.7,
                    'delta': 3.8,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of subscribers on premium service tiers. Revenue optimization metric.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            ]
        
        # Calculate deltas based on actual usage data
        delta_data_usage = round(metrics['data_usage_per_subscriber'] - 11.5, 1)
        delta_5g = round(metrics['five_g_adoption'] - 71.0, 1)
        delta_feature = round(metrics['feature_adoption_rate'] - 70.4, 1)
        delta_penetration = round(metrics['service_penetration'] - 86.2, 1)
        delta_app = round(metrics['app_usage_rate'] - 82.6, 1)
        delta_premium = round(metrics['premium_service_adoption'] - 56.2, 1)
        
        return [
            {
                'label': 'Data Usage per Subscriber',
                'value': round(metrics['data_usage_per_subscriber'], 1),
                'delta': delta_data_usage,
                'delta_direction': 'up' if delta_data_usage > 0 else 'down',
                'unit': 'GB',
                'tooltip': 'Average data consumption per subscriber per month. Indicates service utilization.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': '5G Adoption Rate',
                'value': round(metrics['five_g_adoption'], 1),
                'delta': delta_5g,
                'delta_direction': 'up' if delta_5g > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of subscribers using 5G services. Key indicator of network modernization.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Feature Adoption Rate',
                'value': round(metrics['feature_adoption_rate'], 1),
                'delta': delta_feature,
                'delta_direction': 'up' if delta_feature > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of subscribers using premium features. Revenue optimization metric.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Service Penetration',
                'value': round(metrics['service_penetration'], 1),
                'delta': delta_penetration,
                'delta_direction': 'up' if delta_penetration > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of addressable market using our services. Market share indicator.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'App Usage Rate',
                'value': round(metrics['app_usage_rate'], 1),
                'delta': delta_app,
                'delta_direction': 'up' if delta_app > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of subscribers using our mobile app. Digital engagement metric.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Premium Service Adoption',
                'value': round(metrics['premium_service_adoption'], 1),
                'delta': delta_premium,
                'delta_direction': 'up' if delta_premium > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of subscribers on premium service tiers. Revenue optimization metric.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        ]
    except Exception as e:
        st.error(f"Error loading usage metrics: {e}")
        return []

def get_operations_metrics(days=30):
    """Get operational efficiency metrics from database"""
    try:
        metrics = db.get_operations_metrics(days)
        
        if metrics.empty:
            # Fallback to default values if no data
            return [
                {
                    'label': 'Service Response Time',
                    'value': 2.1,
                    'delta': -0.5,
                    'delta_direction': 'down',
                    'unit': ' hours',
                    'tooltip': 'Time from issue reported to first action taken. Drives customer satisfaction and NPS.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Regulatory Compliance Rate',
                    'value': 98.7,
                    'delta': 0.3,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of audits or checks passed successfully. Avoids fines and reputational damage.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Capex to Revenue Ratio',
                    'value': 18.2,
                    'delta': -1.1,
                    'delta_direction': 'down',
                    'unit': '%',
                    'tooltip': 'Percentage of revenue reinvested in infrastructure. Shows commitment to network quality/growth.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Network Efficiency Score',
                    'value': 87.3,
                    'delta': 2.1,
                    'delta_direction': 'up',
                    'unit': '',
                    'tooltip': 'Overall operational efficiency metric combining multiple factors.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'Support Ticket Resolution',
                    'value': 94.2,
                    'delta': 1.8,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Percentage of support tickets resolved successfully. Key operational efficiency metric.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                },
                {
                    'label': 'System Uptime',
                    'value': 99.92,
                    'delta': 0.05,
                    'delta_direction': 'up',
                    'unit': '%',
                    'tooltip': 'Overall system availability percentage. Critical for service reliability.',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
            ]
        
        # Calculate deltas based on actual operations data
        delta_response = round(metrics['service_response_time'] - 2.3, 1)
        delta_compliance = round(metrics['regulatory_compliance_rate'] - 98.7, 1)
        delta_capex = round(metrics['capex_to_revenue_ratio'] - 18.4, 1)
        delta_efficiency = round(metrics['operational_efficiency_score'] - 86.7, 1)
        delta_tickets = round(metrics['support_ticket_resolution'] - 94.6, 1)
        delta_uptime = round(metrics['system_uptime'] - 99.91, 2)
        
        return [
            {
                'label': 'Service Response Time',
                'value': round(metrics['service_response_time'], 1),
                'delta': delta_response,
                'delta_direction': 'down' if delta_response < 0 else 'up',
                'unit': ' hours',
                'tooltip': 'Time from issue reported to first action taken. Drives customer satisfaction and NPS.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Regulatory Compliance Rate',
                'value': round(metrics['regulatory_compliance_rate'], 1),
                'delta': delta_compliance,
                'delta_direction': 'up' if delta_compliance > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of audits or checks passed successfully. Avoids fines and reputational damage.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Capex to Revenue Ratio',
                'value': round(metrics['capex_to_revenue_ratio'], 1),
                'delta': delta_capex,
                'delta_direction': 'down' if delta_capex < 0 else 'up',
                'unit': '%',
                'tooltip': 'Percentage of revenue reinvested in infrastructure. Shows commitment to network quality/growth.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Network Efficiency Score',
                'value': round(metrics['operational_efficiency_score'], 1),
                'delta': delta_efficiency,
                'delta_direction': 'up' if delta_efficiency > 0 else 'down',
                'unit': '',
                'tooltip': 'Overall operational efficiency metric combining multiple factors.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'Support Ticket Resolution',
                'value': round(metrics['support_ticket_resolution'], 1),
                'delta': delta_tickets,
                'delta_direction': 'up' if delta_tickets > 0 else 'down',
                'unit': '%',
                'tooltip': 'Percentage of support tickets resolved successfully. Key operational efficiency metric.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            },
            {
                'label': 'System Uptime',
                'value': round(metrics['system_uptime'], 2),
                'delta': delta_uptime,
                'delta_direction': 'up' if delta_uptime > 0 else 'down',
                'unit': '%',
                'tooltip': 'Overall system availability percentage. Critical for service reliability.',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
        ]
    except Exception as e:
        st.error(f"Error loading operations metrics: {e}")
        return [] 