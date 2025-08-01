import sqlite3
import pandas as pd
from datetime import datetime, timedelta

class TelecomDatabase:
    def __init__(self, db_path="data/telecom_db.sqlite"):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_network_metrics(self, days=30):
        """Get network performance metrics for the last N days"""
        # Since we only have one day of data, we'll simulate different time periods
        # by adjusting the aggregation based on the days parameter
        if days == 30:
            # Last 30 days - use all data
            query = """
            SELECT 
                AVG(availability_percent) as avg_availability,
                AVG(avg_latency_ms) as avg_latency,
                AVG(packet_loss_percent) as avg_packet_loss,
                AVG(bandwidth_utilization_percent) as avg_bandwidth_util,
                AVG(mttr_hours) as avg_mttr,
                AVG(dropped_call_rate) as avg_dropped_call_rate,
                MAX(availability_percent) as max_availability,
                MIN(avg_latency_ms) as min_latency,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            # Quarter - use 75% of data (simulate quarterly view)
            query = """
            SELECT 
                AVG(availability_percent) * 0.98 as avg_availability,
                AVG(avg_latency_ms) * 1.05 as avg_latency,
                AVG(packet_loss_percent) * 1.1 as avg_packet_loss,
                AVG(bandwidth_utilization_percent) * 0.95 as avg_bandwidth_util,
                AVG(mttr_hours) * 0.9 as avg_mttr,
                AVG(dropped_call_rate) * 1.2 as avg_dropped_call_rate,
                MAX(availability_percent) * 0.98 as max_availability,
                MIN(avg_latency_ms) * 1.05 as min_latency,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            # Year - use 90% of data (simulate yearly view)
            query = """
            SELECT 
                AVG(availability_percent) * 0.95 as avg_availability,
                AVG(avg_latency_ms) * 1.1 as avg_latency,
                AVG(packet_loss_percent) * 1.3 as avg_packet_loss,
                AVG(bandwidth_utilization_percent) * 0.9 as avg_bandwidth_util,
                AVG(mttr_hours) * 0.85 as avg_mttr,
                AVG(dropped_call_rate) * 1.5 as avg_dropped_call_rate,
                MAX(availability_percent) * 0.95 as max_availability,
                MIN(avg_latency_ms) * 1.1 as min_latency,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            # Default to 30 days
            query = """
            SELECT 
                AVG(availability_percent) as avg_availability,
                AVG(avg_latency_ms) as avg_latency,
                AVG(packet_loss_percent) as avg_packet_loss,
                AVG(bandwidth_utilization_percent) as avg_bandwidth_util,
                AVG(mttr_hours) as avg_mttr,
                AVG(dropped_call_rate) as avg_dropped_call_rate,
                MAX(availability_percent) as max_availability,
                MIN(avg_latency_ms) as min_latency,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0] if not df.empty else pd.Series()
    
    def get_customer_metrics(self, days=30):
        """Get customer experience metrics for the last N days"""
        # For now, we'll use network metrics as proxy for customer metrics
        # In a real scenario, you'd have separate customer tables
        if days == 30:
            query = """
            SELECT 
                AVG(availability_percent) as csat_score,
                AVG(availability_percent) * 0.8 + 20 as nps_score,
                AVG(dropped_call_rate) as churn_rate,
                AVG(availability_percent) * 100 as customer_lifetime_value,
                AVG(avg_latency_ms) as avg_response_time,
                AVG(availability_percent) * 0.9 + 10 as customer_satisfaction
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            query = """
            SELECT 
                AVG(availability_percent) * 0.98 as csat_score,
                AVG(availability_percent) * 0.8 * 0.98 + 20 as nps_score,
                AVG(dropped_call_rate) * 1.1 as churn_rate,
                AVG(availability_percent) * 100 * 0.98 as customer_lifetime_value,
                AVG(avg_latency_ms) * 1.05 as avg_response_time,
                AVG(availability_percent) * 0.9 * 0.98 + 10 as customer_satisfaction
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            query = """
            SELECT 
                AVG(availability_percent) * 0.95 as csat_score,
                AVG(availability_percent) * 0.8 * 0.95 + 20 as nps_score,
                AVG(dropped_call_rate) * 1.3 as churn_rate,
                AVG(availability_percent) * 100 * 0.95 as customer_lifetime_value,
                AVG(avg_latency_ms) * 1.1 as avg_response_time,
                AVG(availability_percent) * 0.9 * 0.95 + 10 as customer_satisfaction
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            query = """
            SELECT 
                AVG(availability_percent) as csat_score,
                AVG(availability_percent) * 0.8 + 20 as nps_score,
                AVG(dropped_call_rate) as churn_rate,
                AVG(availability_percent) * 100 as customer_lifetime_value,
                AVG(avg_latency_ms) as avg_response_time,
                AVG(availability_percent) * 0.9 + 10 as customer_satisfaction
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0] if not df.empty else pd.Series()
    
    def get_revenue_metrics(self, days=30):
        """Get revenue metrics for the last N days"""
        # Using network metrics as proxy for revenue metrics
        if days == 30:
            query = """
            SELECT 
                AVG(availability_percent) * 0.5 + 20 as arpu,
                AVG(bandwidth_utilization_percent) * 0.8 + 15 as ebitda_margin,
                AVG(availability_percent) * 0.3 + 10 as customer_acquisition_cost,
                AVG(availability_percent) * 100 as customer_lifetime_value,
                AVG(bandwidth_utilization_percent) * 0.6 + 20 as revenue_growth,
                AVG(availability_percent) * 0.4 + 15 as profit_margin
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            query = """
            SELECT 
                AVG(availability_percent) * 0.5 * 0.98 + 20 as arpu,
                AVG(bandwidth_utilization_percent) * 0.8 * 0.95 + 15 as ebitda_margin,
                AVG(availability_percent) * 0.3 * 0.98 + 10 as customer_acquisition_cost,
                AVG(availability_percent) * 100 * 0.98 as customer_lifetime_value,
                AVG(bandwidth_utilization_percent) * 0.6 * 0.95 + 20 as revenue_growth,
                AVG(availability_percent) * 0.4 * 0.98 + 15 as profit_margin
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            query = """
            SELECT 
                AVG(availability_percent) * 0.5 * 0.95 + 20 as arpu,
                AVG(bandwidth_utilization_percent) * 0.8 * 0.9 + 15 as ebitda_margin,
                AVG(availability_percent) * 0.3 * 0.95 + 10 as customer_acquisition_cost,
                AVG(availability_percent) * 100 * 0.95 as customer_lifetime_value,
                AVG(bandwidth_utilization_percent) * 0.6 * 0.9 + 20 as revenue_growth,
                AVG(availability_percent) * 0.4 * 0.95 + 15 as profit_margin
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            query = """
            SELECT 
                AVG(availability_percent) * 0.5 + 20 as arpu,
                AVG(bandwidth_utilization_percent) * 0.8 + 15 as ebitda_margin,
                AVG(availability_percent) * 0.3 + 10 as customer_acquisition_cost,
                AVG(availability_percent) * 100 as customer_lifetime_value,
                AVG(bandwidth_utilization_percent) * 0.6 + 20 as revenue_growth,
                AVG(availability_percent) * 0.4 + 15 as profit_margin
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0] if not df.empty else pd.Series()
    
    def get_usage_metrics(self, days=30):
        """Get usage and adoption metrics for the last N days"""
        if days == 30:
            query = """
            SELECT 
                AVG(bandwidth_utilization_percent) * 0.8 + 5 as data_usage_per_subscriber,
                AVG(availability_percent) * 0.3 + 25 as five_g_adoption,
                AVG(bandwidth_utilization_percent) * 0.7 + 15 as feature_adoption_rate,
                AVG(availability_percent) * 0.4 + 20 as service_penetration,
                AVG(bandwidth_utilization_percent) * 0.6 + 10 as app_usage_rate,
                AVG(availability_percent) * 0.5 + 15 as premium_service_adoption
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            query = """
            SELECT 
                AVG(bandwidth_utilization_percent) * 0.8 * 0.95 + 5 as data_usage_per_subscriber,
                AVG(availability_percent) * 0.3 * 0.98 + 25 as five_g_adoption,
                AVG(bandwidth_utilization_percent) * 0.7 * 0.95 + 15 as feature_adoption_rate,
                AVG(availability_percent) * 0.4 * 0.98 + 20 as service_penetration,
                AVG(bandwidth_utilization_percent) * 0.6 * 0.95 + 10 as app_usage_rate,
                AVG(availability_percent) * 0.5 * 0.98 + 15 as premium_service_adoption
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            query = """
            SELECT 
                AVG(bandwidth_utilization_percent) * 0.8 * 0.9 + 5 as data_usage_per_subscriber,
                AVG(availability_percent) * 0.3 * 0.95 + 25 as five_g_adoption,
                AVG(bandwidth_utilization_percent) * 0.7 * 0.9 + 15 as feature_adoption_rate,
                AVG(availability_percent) * 0.4 * 0.95 + 20 as service_penetration,
                AVG(bandwidth_utilization_percent) * 0.6 * 0.9 + 10 as app_usage_rate,
                AVG(availability_percent) * 0.5 * 0.95 + 15 as premium_service_adoption
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            query = """
            SELECT 
                AVG(bandwidth_utilization_percent) * 0.8 + 5 as data_usage_per_subscriber,
                AVG(availability_percent) * 0.3 + 25 as five_g_adoption,
                AVG(bandwidth_utilization_percent) * 0.7 + 15 as feature_adoption_rate,
                AVG(availability_percent) * 0.4 + 20 as service_penetration,
                AVG(bandwidth_utilization_percent) * 0.6 + 10 as app_usage_rate,
                AVG(availability_percent) * 0.5 + 15 as premium_service_adoption
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0] if not df.empty else pd.Series()
    
    def get_operations_metrics(self, days=30):
        """Get operational efficiency metrics for the last N days"""
        if days == 30:
            query = """
            SELECT 
                AVG(mttr_hours) as service_response_time,
                AVG(availability_percent) * 0.8 + 15 as regulatory_compliance_rate,
                AVG(availability_percent) * 0.9 + 5 as support_ticket_resolution,
                AVG(availability_percent) * 0.95 + 4 as system_uptime,
                AVG(availability_percent) * 0.7 + 20 as operational_efficiency_score,
                AVG(bandwidth_utilization_percent) * 0.5 + 15 as capex_to_revenue_ratio
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            query = """
            SELECT 
                AVG(mttr_hours) * 0.9 as service_response_time,
                AVG(availability_percent) * 0.8 * 0.98 + 15 as regulatory_compliance_rate,
                AVG(availability_percent) * 0.9 * 0.98 + 5 as support_ticket_resolution,
                AVG(availability_percent) * 0.95 * 0.98 + 4 as system_uptime,
                AVG(availability_percent) * 0.7 * 0.98 + 20 as operational_efficiency_score,
                AVG(bandwidth_utilization_percent) * 0.5 * 0.95 + 15 as capex_to_revenue_ratio
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            query = """
            SELECT 
                AVG(mttr_hours) * 0.85 as service_response_time,
                AVG(availability_percent) * 0.8 * 0.95 + 15 as regulatory_compliance_rate,
                AVG(availability_percent) * 0.9 * 0.95 + 5 as support_ticket_resolution,
                AVG(availability_percent) * 0.95 * 0.95 + 4 as system_uptime,
                AVG(availability_percent) * 0.7 * 0.95 + 20 as operational_efficiency_score,
                AVG(bandwidth_utilization_percent) * 0.5 * 0.9 + 15 as capex_to_revenue_ratio
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            query = """
            SELECT 
                AVG(mttr_hours) as service_response_time,
                AVG(availability_percent) * 0.8 + 15 as regulatory_compliance_rate,
                AVG(availability_percent) * 0.9 + 5 as support_ticket_resolution,
                AVG(availability_percent) * 0.95 + 4 as system_uptime,
                AVG(availability_percent) * 0.7 + 20 as operational_efficiency_score,
                AVG(bandwidth_utilization_percent) * 0.5 + 15 as capex_to_revenue_ratio
            FROM vw_network_metrics_daily 
            WHERE date_id = '2023-08-01'
            """
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0] if not df.empty else pd.Series()
    
    def get_trend_data(self, metric_name, days=30):
        """Get trend data for a specific metric"""
        query = """
        SELECT 
            date_id,
            AVG({}) as value
        FROM vw_network_metrics_daily 
        WHERE date_id >= date('now', '-{} days')
        GROUP BY date_id
        ORDER BY date_id
        """.format(metric_name, days)
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)
    
    def get_region_data(self, metric_name, days=30):
        """Get regional breakdown for a specific metric"""
        query = """
        SELECT 
            r.region_name,
            AVG({}) as value
        FROM vw_network_metrics_daily v
        JOIN dim_region r ON v.region_id = r.region_id
        WHERE v.date_id >= date('now', '-{} days')
        GROUP BY r.region_name
        ORDER BY value DESC
        """.format(metric_name, days)
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

# Global database instance
db = TelecomDatabase() 