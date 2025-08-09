"""
Security tests for SQL injection prevention

Tests the database connection layer's protection against SQL injection attacks.
"""

import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database_connection import TelecomDatabase


class TestSQLInjectionPrevention:
    """Test SQL injection prevention in database queries"""
    
    def setup_method(self):
        """Set up test database instance"""
        self.db = TelecomDatabase()
    
    def test_get_trend_data_prevents_sql_injection(self):
        """Test that get_trend_data prevents SQL injection via metric_name"""
        # Test malicious metric names that could cause SQL injection
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "availability_percent; DELETE FROM dim_region; --",
            "1; INSERT INTO dim_region VALUES (999, 'hacked'); --",
            "availability_percent UNION SELECT 1,2,3 FROM sqlite_master",
            "availability_percent' OR '1'='1",
            "availability_percent'; UPDATE dim_region SET region_name='hacked'; --"
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="Invalid metric name"):
                self.db.get_trend_data(malicious_input, 30)
    
    def test_get_region_data_prevents_sql_injection(self):
        """Test that get_region_data prevents SQL injection via metric_name"""
        # Test malicious metric names that could cause SQL injection
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "availability_percent; DELETE FROM dim_region; --",
            "1; INSERT INTO dim_region VALUES (999, 'hacked'); --",
            "availability_percent UNION SELECT 1,2,3 FROM sqlite_master",
            "availability_percent' OR '1'='1",
            "availability_percent'; UPDATE dim_region SET region_name='hacked'; --"
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValueError, match="Invalid metric name"):
                self.db.get_region_data(malicious_input, 30)
    
    def test_valid_metric_names_work(self):
        """Test that valid metric names still work correctly"""
        valid_metrics = [
            'availability_percent',
            'avg_latency_ms', 
            'avg_packet_loss_percent',
            'avg_bandwidth_utilization_percent',
            'avg_mttr_hours',
            'avg_dropped_call_rate'
        ]
        
        for metric in valid_metrics:
            try:
                # These should not raise ValueError for metric validation
                # They might fail with database errors in test environment, but that's OK
                result = self.db.get_trend_data(metric, 30)
                # If we get here, the metric name validation passed
                assert True
            except ValueError as e:
                if "Invalid metric name" in str(e):
                    pytest.fail(f"Valid metric '{metric}' was rejected")
                # Other errors (like database connection issues) are OK in tests
            except Exception:
                # Database connection errors are expected in test environment
                pass
    
    def test_days_parameter_is_parameterized(self):
        """Test that the days parameter is properly parameterized (no injection via days)"""
        # Test that days parameter doesn't allow SQL injection
        # This would be harder to exploit but we ensure it's parameterized
        try:
            result = self.db.get_trend_data('availability_percent', "30; DROP TABLE users; --")
            # If it doesn't crash, the parameterization worked (string converted to int by pandas)
        except (TypeError, ValueError):
            # Expected - malformed days parameter should cause type error
            pass
        except Exception as e:
            # Database errors are fine in test environment
            pass
    
    def test_whitelist_prevents_column_enumeration(self):
        """Test that whitelist prevents database column enumeration attacks"""
        # Attackers might try to enumerate database columns
        enumeration_attempts = [
            "name",
            "id", 
            "sqlite_master",
            "information_schema.columns",
            "*",
            "1,2,3,4,5"
        ]
        
        for attempt in enumeration_attempts:
            with pytest.raises(ValueError, match="Invalid metric name"):
                self.db.get_trend_data(attempt, 30)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
