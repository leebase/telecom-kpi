import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_network_data():
    """
    Generate realistic network performance data
    """
    # Generate 30 days of data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    # Latency trend (improving slightly)
    latency_base = 50
    latency_trend = pd.DataFrame({
        'date': dates,
        'value': [latency_base + np.random.normal(0, 2) - i*0.1 for i in range(len(dates))]
    })
    
    # Uptime trend (stable with slight improvement)
    uptime_trend = pd.DataFrame({
        'date': dates,
        'value': [99.8 + np.random.normal(0, 0.05) + i*0.001 for i in range(len(dates))]
    })
    
    # Bandwidth by region
    regions = ['North', 'South', 'East', 'West', 'Central']
    bandwidth_by_region = pd.DataFrame({
        'category': regions,
        'value': [75 + np.random.normal(0, 5) for _ in regions]
    })
    
    # Packet loss trend (decreasing)
    packet_loss_trend = pd.DataFrame({
        'date': dates,
        'value': [0.1 + np.random.normal(0, 0.02) - i*0.001 for i in range(len(dates))]
    })
    
    # DCR trend (improving)
    dcr_trend = pd.DataFrame({
        'date': dates,
        'value': [1.5 + np.random.normal(0, 0.1) - i*0.01 for i in range(len(dates))]
    })
    
    return {
        'latency_trend': latency_trend,
        'uptime_trend': uptime_trend,
        'bandwidth_by_region': bandwidth_by_region,
        'packet_loss_trend': packet_loss_trend,
        'dcr_trend': dcr_trend
    }

def generate_customer_data():
    """
    Generate realistic customer experience data
    """
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    # CSAT trend (improving)
    csat_trend = pd.DataFrame({
        'date': dates,
        'value': [4.0 + np.random.normal(0, 0.1) + i*0.005 for i in range(len(dates))]
    })
    
    # NPS trend (improving)
    nps_trend = pd.DataFrame({
        'date': dates,
        'value': [35 + np.random.normal(0, 2) + i*0.2 for i in range(len(dates))]
    })
    
    # Churn by region
    regions = ['North', 'South', 'East', 'West', 'Central']
    churn_by_region = pd.DataFrame({
        'category': regions,
        'value': [2.0 + np.random.normal(0, 0.5) for _ in regions]
    })
    
    # Handling time distribution
    handling_times = np.random.normal(4.2, 1.5, 1000)
    handling_time_dist = pd.DataFrame({
        'value': handling_times
    })
    
    return {
        'csat_trend': csat_trend,
        'nps_trend': nps_trend,
        'churn_by_region': churn_by_region,
        'handling_time_dist': handling_time_dist
    }

def generate_revenue_data():
    """
    Generate realistic revenue and monetization data
    """
    dates = pd.date_range(start=datetime.now() - timedelta(days=365), end=datetime.now(), freq='ME')
    
    # ARPU trend (growing)
    arpu_trend = pd.DataFrame({
        'date': dates,
        'value': [38 + np.random.normal(0, 1) + i*0.3 for i in range(len(dates))]
    })
    
    # CLV trend (growing)
    clv_trend = pd.DataFrame({
        'date': dates,
        'value': [1100 + np.random.normal(0, 50) + i*10 for i in range(len(dates))]
    })
    
    # Revenue by plan type
    plan_types = ['Basic', 'Standard', 'Premium', 'Enterprise']
    revenue_by_plan = pd.DataFrame({
        'category': plan_types,
        'value': [300000, 800000, 1200000, 100000]
    })
    
    # Subscriber growth
    subscriber_growth = pd.DataFrame({
        'date': dates,
        'value': [1000000 + np.random.normal(0, 50000) + i*15000 for i in range(len(dates))]
    })
    
    # EBITDA trend
    ebitda_trend = pd.DataFrame({
        'date': dates,
        'value': [30 + np.random.normal(0, 1) + i*0.1 for i in range(len(dates))]
    })
    
    return {
        'arpu_trend': arpu_trend,
        'clv_trend': clv_trend,
        'revenue_by_plan': revenue_by_plan,
        'subscriber_growth': subscriber_growth,
        'ebitda_trend': ebitda_trend
    }

def generate_usage_data():
    """
    Generate realistic usage and adoption data
    """
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    # Data usage trend (increasing)
    data_usage_trend = pd.DataFrame({
        'date': dates,
        'value': [7.5 + np.random.normal(0, 0.5) + i*0.02 for i in range(len(dates))]
    })
    
    # Throughput by region
    regions = ['North', 'South', 'East', 'West', 'Central']
    throughput_by_region = pd.DataFrame({
        'category': regions,
        'value': [40 + np.random.normal(0, 5) for _ in regions]
    })
    
    # 5G adoption trend (growing)
    adoption_5g_trend = pd.DataFrame({
        'date': dates,
        'value': [25 + np.random.normal(0, 2) + i*0.3 for i in range(len(dates))]
    })
    
    # Usage distribution
    usage_distribution = pd.DataFrame({
        'value': np.random.lognormal(2, 0.5, 1000)  # Log-normal distribution for usage
    })
    
    return {
        'data_usage_trend': data_usage_trend,
        'throughput_by_region': throughput_by_region,
        '5g_adoption_trend': adoption_5g_trend,
        'usage_distribution': usage_distribution
    }

def generate_operations_data():
    """
    Generate realistic operational efficiency data
    """
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    
    # Response time trend (improving)
    response_time_trend = pd.DataFrame({
        'date': dates,
        'value': [2.5 + np.random.normal(0, 0.2) - i*0.01 for i in range(len(dates))]
    })
    
    # Compliance by region
    regions = ['North', 'South', 'East', 'West', 'Central']
    compliance_by_region = pd.DataFrame({
        'category': regions,
        'value': [98 + np.random.normal(0, 0.5) for _ in regions]
    })
    
    # Efficiency trend (improving)
    efficiency_trend = pd.DataFrame({
        'date': dates,
        'value': [85 + np.random.normal(0, 1) + i*0.05 for i in range(len(dates))]
    })
    
    # Capex trend
    capex_trend = pd.DataFrame({
        'date': dates,
        'value': [20 + np.random.normal(0, 1) - i*0.02 for i in range(len(dates))]
    })
    
    return {
        'response_time_trend': response_time_trend,
        'compliance_by_region': compliance_by_region,
        'efficiency_trend': efficiency_trend,
        'capex_trend': capex_trend
    }

def generate_all_data():
    """
    Generate all test data for the dashboard
    """
    return {
        'network': generate_network_data(),
        'customer': generate_customer_data(),
        'revenue': generate_revenue_data(),
        'usage': generate_usage_data(),
        'operations': generate_operations_data()
    } 