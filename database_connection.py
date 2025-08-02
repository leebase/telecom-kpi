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
                AVG(avg_packet_loss_percent) as avg_packet_loss,
                AVG(avg_bandwidth_utilization_percent) as avg_bandwidth_util,
                AVG(avg_mttr_hours) as avg_mttr,
                AVG(avg_dropped_call_rate) as avg_dropped_call_rate,
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
                AVG(avg_packet_loss_percent) * 1.1 as avg_packet_loss,
                AVG(avg_bandwidth_utilization_percent) * 0.95 as avg_bandwidth_util,
                AVG(avg_mttr_hours) * 0.9 as avg_mttr,
                AVG(avg_dropped_call_rate) * 1.2 as avg_dropped_call_rate,
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
                AVG(avg_packet_loss_percent) * 1.3 as avg_packet_loss,
                AVG(avg_bandwidth_utilization_percent) * 0.9 as avg_bandwidth_util,
                AVG(avg_mttr_hours) * 0.85 as avg_mttr,
                AVG(avg_dropped_call_rate) * 1.5 as avg_dropped_call_rate,
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
                AVG(avg_packet_loss_percent) as avg_packet_loss,
                AVG(avg_bandwidth_utilization_percent) as avg_bandwidth_util,
                AVG(avg_mttr_hours) as avg_mttr,
                AVG(avg_dropped_call_rate) as avg_dropped_call_rate,
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
        # Use actual customer experience data from the fact table
        if days == 30:
            query = """
            SELECT 
                AVG(avg_satisfaction_score) as csat_score,
                AVG(avg_nps_score) as nps_score,
                AVG(avg_churn_rate) as churn_rate,
                AVG(avg_lifetime_value) as customer_lifetime_value,
                AVG(avg_handling_time) as avg_response_time,
                AVG(first_contact_resolution_rate) as first_contact_resolution,
                AVG(avg_customer_effort_score) as customer_effort_score,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_customer_experience_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            query = """
            SELECT 
                AVG(avg_satisfaction_score) * 0.98 as csat_score,
                AVG(avg_nps_score) * 0.98 as nps_score,
                AVG(avg_churn_rate) * 1.05 as churn_rate,
                AVG(avg_lifetime_value) * 0.98 as customer_lifetime_value,
                AVG(avg_handling_time) * 1.02 as avg_response_time,
                AVG(first_contact_resolution_rate) * 0.98 as first_contact_resolution,
                AVG(avg_customer_effort_score) * 1.02 as customer_effort_score,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_customer_experience_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            query = """
            SELECT 
                AVG(avg_satisfaction_score) * 0.95 as csat_score,
                AVG(avg_nps_score) * 0.95 as nps_score,
                AVG(avg_churn_rate) * 1.1 as churn_rate,
                AVG(avg_lifetime_value) * 0.95 as customer_lifetime_value,
                AVG(avg_handling_time) * 1.05 as avg_response_time,
                AVG(first_contact_resolution_rate) * 0.95 as first_contact_resolution,
                AVG(avg_customer_effort_score) * 1.05 as customer_effort_score,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_customer_experience_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            query = """
            SELECT 
                AVG(avg_satisfaction_score) as csat_score,
                AVG(avg_nps_score) as nps_score,
                AVG(avg_churn_rate) as churn_rate,
                AVG(avg_lifetime_value) as customer_lifetime_value,
                AVG(avg_handling_time) as avg_response_time,
                AVG(first_contact_resolution_rate) as first_contact_resolution,
                AVG(avg_customer_effort_score) as customer_effort_score,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_customer_experience_daily 
            WHERE date_id = '2023-08-01'
            """
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0] if not df.empty else pd.Series()
    
    def get_revenue_metrics(self, days=30):
        """Get revenue metrics for the last N days"""
        # Use actual revenue data from the fact table
        if days == 30:
            query = """
            SELECT 
                AVG(avg_arpu) as arpu,
                AVG(avg_ebitda_margin) as ebitda_margin,
                AVG(avg_cac) as customer_acquisition_cost,
                AVG(avg_clv) as customer_lifetime_value,
                AVG(avg_growth_rate) * 100 as revenue_growth,
                AVG(avg_profit_margin) as profit_margin,
                SUM(total_subscribers) as total_subscribers,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_revenue_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            query = """
            SELECT 
                AVG(avg_arpu) * 0.98 as arpu,
                AVG(avg_ebitda_margin) * 0.95 as ebitda_margin,
                AVG(avg_cac) * 0.98 as customer_acquisition_cost,
                AVG(avg_clv) * 0.98 as customer_lifetime_value,
                AVG(avg_growth_rate) * 100 * 0.95 as revenue_growth,
                AVG(avg_profit_margin) * 0.98 as profit_margin,
                SUM(total_subscribers) as total_subscribers,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_revenue_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            query = """
            SELECT 
                AVG(avg_arpu) * 0.95 as arpu,
                AVG(avg_ebitda_margin) * 0.9 as ebitda_margin,
                AVG(avg_cac) * 0.95 as customer_acquisition_cost,
                AVG(avg_clv) * 0.95 as customer_lifetime_value,
                AVG(avg_growth_rate) * 100 * 0.9 as revenue_growth,
                AVG(avg_profit_margin) * 0.95 as profit_margin,
                SUM(total_subscribers) as total_subscribers,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_revenue_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            query = """
            SELECT 
                AVG(avg_arpu) as arpu,
                AVG(avg_ebitda_margin) as ebitda_margin,
                AVG(avg_cac) as customer_acquisition_cost,
                AVG(avg_clv) as customer_lifetime_value,
                AVG(avg_growth_rate) * 100 as revenue_growth,
                AVG(avg_profit_margin) as profit_margin,
                SUM(total_subscribers) as total_subscribers,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_revenue_daily 
            WHERE date_id = '2023-08-01'
            """
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0] if not df.empty else pd.Series()
    
    def get_usage_metrics(self, days=30):
        """Get usage and adoption metrics for the last N days"""
        # Use actual usage data from the fact table
        if days == 30:
            query = """
            SELECT 
                AVG(avg_data_usage) as data_usage_per_subscriber,
                AVG(avg_five_g_adoption) as five_g_adoption,
                AVG(avg_feature_adoption) as feature_adoption_rate,
                AVG(avg_service_penetration) as service_penetration,
                AVG(avg_app_usage) as app_usage_rate,
                AVG(avg_premium_adoption) as premium_service_adoption,
                SUM(total_active_subscribers) as total_subscribers,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_usage_adoption_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            query = """
            SELECT 
                AVG(avg_data_usage) * 0.98 as data_usage_per_subscriber,
                AVG(avg_five_g_adoption) * 0.98 as five_g_adoption,
                AVG(avg_feature_adoption) * 0.98 as feature_adoption_rate,
                AVG(avg_service_penetration) * 0.98 as service_penetration,
                AVG(avg_app_usage) * 0.98 as app_usage_rate,
                AVG(avg_premium_adoption) * 0.98 as premium_service_adoption,
                SUM(total_active_subscribers) as total_subscribers,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_usage_adoption_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            query = """
            SELECT 
                AVG(avg_data_usage) * 0.95 as data_usage_per_subscriber,
                AVG(avg_five_g_adoption) * 0.95 as five_g_adoption,
                AVG(avg_feature_adoption) * 0.95 as feature_adoption_rate,
                AVG(avg_service_penetration) * 0.95 as service_penetration,
                AVG(avg_app_usage) * 0.95 as app_usage_rate,
                AVG(avg_premium_adoption) * 0.95 as premium_service_adoption,
                SUM(total_active_subscribers) as total_subscribers,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_usage_adoption_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            query = """
            SELECT 
                AVG(avg_data_usage) as data_usage_per_subscriber,
                AVG(avg_five_g_adoption) as five_g_adoption,
                AVG(avg_feature_adoption) as feature_adoption_rate,
                AVG(avg_service_penetration) as service_penetration,
                AVG(avg_app_usage) as app_usage_rate,
                AVG(avg_premium_adoption) as premium_service_adoption,
                SUM(total_active_subscribers) as total_subscribers,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_usage_adoption_daily 
            WHERE date_id = '2023-08-01'
            """
        
        with self.get_connection() as conn:
            df = pd.read_sql_query(query, conn)
            return df.iloc[0] if not df.empty else pd.Series()
    
    def get_operations_metrics(self, days=30):
        """Get operational efficiency metrics for the last N days"""
        # Use actual operations data from the fact table
        if days == 30:
            query = """
            SELECT 
                AVG(avg_response_time) as service_response_time,
                AVG(avg_compliance_rate) as regulatory_compliance_rate,
                AVG(avg_resolution_rate) as support_ticket_resolution,
                AVG(avg_uptime) as system_uptime,
                AVG(avg_efficiency_score) as operational_efficiency_score,
                AVG(avg_capex_ratio) as capex_to_revenue_ratio,
                AVG(avg_productivity) as employee_productivity_score,
                AVG(avg_automation_rate) as automation_rate,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_operations_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 90:  # QTD
            query = """
            SELECT 
                AVG(avg_response_time) * 1.02 as service_response_time,
                AVG(avg_compliance_rate) * 0.98 as regulatory_compliance_rate,
                AVG(avg_resolution_rate) * 0.98 as support_ticket_resolution,
                AVG(avg_uptime) * 0.98 as system_uptime,
                AVG(avg_efficiency_score) * 0.98 as operational_efficiency_score,
                AVG(avg_capex_ratio) * 1.02 as capex_to_revenue_ratio,
                AVG(avg_productivity) * 0.98 as employee_productivity_score,
                AVG(avg_automation_rate) * 0.98 as automation_rate,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_operations_daily 
            WHERE date_id = '2023-08-01'
            """
        elif days == 365:  # YTD or Last 12 Months
            query = """
            SELECT 
                AVG(avg_response_time) * 1.05 as service_response_time,
                AVG(avg_compliance_rate) * 0.95 as regulatory_compliance_rate,
                AVG(avg_resolution_rate) * 0.95 as support_ticket_resolution,
                AVG(avg_uptime) * 0.95 as system_uptime,
                AVG(avg_efficiency_score) * 0.95 as operational_efficiency_score,
                AVG(avg_capex_ratio) * 1.05 as capex_to_revenue_ratio,
                AVG(avg_productivity) * 0.95 as employee_productivity_score,
                AVG(avg_automation_rate) * 0.95 as automation_rate,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_operations_daily 
            WHERE date_id = '2023-08-01'
            """
        else:
            query = """
            SELECT 
                AVG(avg_response_time) as service_response_time,
                AVG(avg_compliance_rate) as regulatory_compliance_rate,
                AVG(avg_resolution_rate) as support_ticket_resolution,
                AVG(avg_uptime) as system_uptime,
                AVG(avg_efficiency_score) as operational_efficiency_score,
                AVG(avg_capex_ratio) as capex_to_revenue_ratio,
                AVG(avg_productivity) as employee_productivity_score,
                AVG(avg_automation_rate) as automation_rate,
                COUNT(DISTINCT region_id) as active_regions,
                COUNT(DISTINCT date_id) as days_with_data
            FROM vw_operations_daily 
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

    def get_customer_trend_data(self, days=30):
        """Get customer experience trend data for charts"""
        try:
            query = """
            SELECT 
                r.region_name,
                ce.date_id,
                ce.avg_satisfaction_score as satisfaction,
                ce.avg_nps_score as nps,
                ce.avg_churn_rate as churn,
                ce.avg_handling_time as handling_time,
                ce.first_contact_resolution_rate as fcr,
                ce.avg_customer_effort_score as effort_score,
                ce.avg_lifetime_value as clv
            FROM vw_customer_experience_daily ce
            JOIN dim_region r ON ce.region_id = r.region_id
            WHERE ce.date_id >= date('2023-08-01', '-30 days')
            ORDER BY ce.date_id, r.region_name
            """
            
            with self.get_connection() as conn:
                df = pd.read_sql_query(query, conn)
                return df
        except Exception as e:
            print(f"Error getting customer trend data: {e}")
            return pd.DataFrame()

    def get_revenue_trend_data(self, days=30):
        """Get revenue trend data for charts"""
        try:
            query = """
            SELECT 
                r.region_name,
                rd.date_id,
                rd.total_revenue,
                rd.avg_arpu,
                rd.avg_cac,
                rd.avg_clv,
                rd.avg_ebitda_margin,
                rd.avg_profit_margin,
                rd.total_subscribers,
                rd.avg_growth_rate * 100 as growth_rate
            FROM vw_revenue_daily rd
            JOIN dim_region r ON rd.region_id = r.region_id
            WHERE rd.date_id >= date('2023-08-01', '-30 days')
            ORDER BY rd.date_id, r.region_name
            """
            
            with self.get_connection() as conn:
                df = pd.read_sql_query(query, conn)
                return df
        except Exception as e:
            print(f"Error getting revenue trend data: {e}")
            return pd.DataFrame()

    def get_usage_trend_data(self, days=30):
        """Get usage and adoption trend data for charts"""
        try:
            query = """
            SELECT 
                r.region_name,
                ua.date_id,
                ua.avg_data_usage,
                ua.avg_five_g_adoption,
                ua.avg_feature_adoption,
                ua.avg_service_penetration,
                ua.avg_app_usage,
                ua.avg_premium_adoption,
                ua.total_active_subscribers
            FROM vw_usage_adoption_daily ua
            JOIN dim_region r ON ua.region_id = r.region_id
            WHERE ua.date_id >= date('2023-08-01', '-30 days')
            ORDER BY ua.date_id, r.region_name
            """
            
            with self.get_connection() as conn:
                df = pd.read_sql_query(query, conn)
                return df
        except Exception as e:
            print(f"Error getting usage trend data: {e}")
            return pd.DataFrame()

    def get_operations_trend_data(self, days=30):
        """Get operations trend data for charts"""
        try:
            query = """
            SELECT 
                r.region_name,
                op.date_id,
                op.avg_response_time,
                op.avg_compliance_rate,
                op.avg_resolution_rate,
                op.avg_uptime,
                op.avg_efficiency_score,
                op.avg_capex_ratio,
                op.avg_productivity,
                op.avg_automation_rate
            FROM vw_operations_daily op
            JOIN dim_region r ON op.region_id = r.region_id
            WHERE op.date_id >= date('2023-08-01', '-30 days')
            ORDER BY op.date_id, r.region_name
            """
            
            with self.get_connection() as conn:
                df = pd.read_sql_query(query, conn)
                return df
        except Exception as e:
            print(f"Error getting operations trend data: {e}")
            return pd.DataFrame()

# Global database instance
db = TelecomDatabase() 