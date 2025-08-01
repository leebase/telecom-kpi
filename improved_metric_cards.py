import streamlit as st
import pandas as pd
from datetime import datetime

def create_metric_card(label, value, delta, delta_direction="up", unit="", tooltip="", last_updated=None, tab_name=""):
    """
    Create a professional metric card using Streamlit components
    """
    
    # Format the value with unit
    if isinstance(value, str):
        formatted_value = value
    elif unit == "$":
        formatted_value = f"${value:,.2f}"
    elif unit == "%":
        formatted_value = f"{value:.2f}%"
    else:
        formatted_value = f"{value}{unit}"
    
    # Format delta
    if delta_direction == "up":
        delta_arrow = "▲"
        delta_color = "#10B981"  # Green
    elif delta_direction == "down":
        delta_arrow = "▼"
        delta_color = "#EF4444"  # Red
    else:  # stable
        delta_arrow = "●"
        delta_color = "#6B7280"  # Gray
    
    # Format delta value
    if isinstance(delta, str):
        formatted_delta = f"{delta_arrow} {delta}"
    elif unit == "$":
        formatted_delta = f"{delta_arrow} ${delta:,.2f}"
    elif unit == "%":
        formatted_delta = f"{delta_arrow} {delta:.2f}%"
    else:
        formatted_delta = f"{delta_arrow} {delta}{unit}"
    
    # Default last updated
    if last_updated is None:
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Create the card using Streamlit components
    with st.container():
        # Add custom CSS for the card
        st.markdown(f"""
        <style>
        .metric-card-{tab_name}-{label.replace(' ', '-').lower()} {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-left: 4px solid {delta_color};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            position: relative;
            color: white;
            min-height: 120px;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Create the card content
        st.markdown(f"""
        <div class="metric-card-{tab_name}-{label.replace(' ', '-').lower()}">
            <div style="position: absolute; top: 1rem; right: 1rem; font-size: 1.2rem; cursor: help;" title="{tooltip}">ℹ️</div>
            <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 0.5rem; font-weight: 500;">{label}</div>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem; line-height: 1;">{formatted_value}</div>
            <div style="font-size: 1rem; color: {delta_color}; font-weight: 500;">{formatted_delta}</div>
            <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.5rem;">Updated: {last_updated}</div>
        </div>
        """, unsafe_allow_html=True)

def render_metric_grid(metrics_data, tab_name=""):
    """
    Render a responsive 3x2 grid of metric cards
    
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

def get_network_metrics():
    """Get network performance metrics"""
    return [
        {
            'label': 'Network Availability',
            'value': 99.87,
            'delta': 0.12,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Percentage of time the network is operational. Critical for SLA compliance and customer satisfaction.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Latency',
            'value': 45.2,
            'delta': -2.1,
            'delta_direction': 'down',
            'unit': ' ms',
            'tooltip': 'Average round-trip time for data packets. Critical for real-time applications like VoIP and gaming.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Bandwidth Utilization',
            'value': 78.3,
            'delta': 3.2,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Percentage of total network capacity being used. Indicates congestion risk and capacity planning needs.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Dropped Call Rate',
            'value': 1.2,
            'delta': -0.3,
            'delta_direction': 'down',
            'unit': '%',
            'tooltip': 'Percentage of calls terminated unexpectedly. Key voice quality metric affecting customer satisfaction.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Packet Loss Rate',
            'value': 0.08,
            'delta': -0.02,
            'delta_direction': 'down',
            'unit': '%',
            'tooltip': 'Percentage of packets lost in transmission. Impacts streaming quality and network integrity.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'MTTR',
            'value': 2.3,
            'delta': -0.5,
            'delta_direction': 'down',
            'unit': ' hours',
            'tooltip': 'Mean Time to Repair - Average time to resolve network outages. Reflects operational responsiveness.',
            'last_updated': '2025-07-30 08:15'
        }
    ]

def get_customer_metrics():
    """Get customer experience metrics"""
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

def get_revenue_metrics():
    """Get revenue and monetization metrics"""
    return [
        {
            'label': 'Average Revenue Per User',
            'value': 42.17,
            'delta': 3.25,
            'delta_direction': 'up',
            'unit': '$',
            'tooltip': 'Average monthly revenue per subscriber. Core monetization KPI.',
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
        },
        {
            'label': 'Customer Acquisition Cost',
            'value': 156,
            'delta': -12,
            'delta_direction': 'down',
            'unit': '$',
            'tooltip': 'Average cost to acquire a new customer. Measures marketing and sales efficiency.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Subscriber Growth Rate',
            'value': 8.3,
            'delta': 1.2,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Net percentage increase in subscriber base. Reflects market momentum.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'EBITDA Margin',
            'value': 32.4,
            'delta': 2.1,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Profitability before non-cash expenses. Financial health metric watched by investors.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Monthly Recurring Revenue',
            'value': 2400000,
            'delta': 180000,
            'delta_direction': 'up',
            'unit': '$',
            'tooltip': 'Predictable monthly revenue stream. Key metric for business stability.',
            'last_updated': '2025-07-30 08:15'
        }
    ]

def get_usage_metrics():
    """Get usage and adoption metrics"""
    return [
        {
            'label': 'Data Usage per Subscriber',
            'value': 8.7,
            'delta': 1.2,
            'delta_direction': 'up',
            'unit': ' GB',
            'tooltip': 'Average GB/month per user. Helps with pricing, planning, and segmenting.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Average Data Throughput',
            'value': 45.2,
            'delta': 3.8,
            'delta_direction': 'up',
            'unit': ' Mbps',
            'tooltip': 'Average data speed. Directly affects user experience and NPS.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Feature Adoption Rate',
            'value': 67,
            'delta': 8,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Percentage of users adopting new features. Signals product innovation success.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': '5G Adoption Rate',
            'value': 34,
            'delta': 12,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Percentage of subscribers using 5G services. Tracks modernization and premium plan uptake.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Active Subscribers',
            'value': 1200000,
            'delta': 45000,
            'delta_direction': 'up',
            'unit': '',
            'tooltip': 'Number of currently active subscribers. Core business metric.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Peak Usage Time',
            'value': '8-10 PM',
            'delta': 'Stable',
            'delta_direction': 'stable',
            'unit': '',
            'tooltip': 'Time period with highest network usage. Important for capacity planning.',
            'last_updated': '2025-07-30 08:15'
        }
    ]

def get_operations_metrics():
    """Get operational efficiency metrics"""
    return [
        {
            'label': 'Service Response Time',
            'value': 2.1,
            'delta': -0.5,
            'delta_direction': 'down',
            'unit': ' hours',
            'tooltip': 'Time from issue reported to first action taken. Drives customer satisfaction and NPS.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Regulatory Compliance Rate',
            'value': 98.7,
            'delta': 0.3,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Percentage of audits or checks passed successfully. Avoids fines and reputational damage.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Capex to Revenue Ratio',
            'value': 18.2,
            'delta': -1.1,
            'delta_direction': 'down',
            'unit': '%',
            'tooltip': 'Percentage of revenue reinvested in infrastructure. Shows commitment to network quality/growth.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Network Efficiency Score',
            'value': 87.3,
            'delta': 2.1,
            'delta_direction': 'up',
            'unit': '',
            'tooltip': 'Overall operational efficiency metric combining multiple factors.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'Support Ticket Resolution',
            'value': 94.2,
            'delta': 1.8,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Percentage of support tickets resolved successfully. Key operational efficiency metric.',
            'last_updated': '2025-07-30 08:15'
        },
        {
            'label': 'System Uptime',
            'value': 99.92,
            'delta': 0.05,
            'delta_direction': 'up',
            'unit': '%',
            'tooltip': 'Overall system availability percentage. Critical for service reliability.',
            'last_updated': '2025-07-30 08:15'
        }
    ] 