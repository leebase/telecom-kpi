"""
Performance and Load Testing

Tests for application performance, caching effectiveness, database performance,
and system resource utilization under various load conditions.
"""

import pytest
import sys
import os
import time
import threading
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database_connection import TelecomDatabase
from llm_service import LLMService
from health_check import health_checker

class TestPerformanceBenchmarks:
    """Performance benchmarking and validation tests"""
    
    def test_database_query_performance(self):
        """Test database query performance benchmarks"""
        db = TelecomDatabase()
        
        # Test query performance targets
        performance_tests = [
            (db.get_network_metrics, {}, 2.0),  # Should complete in < 2s
            (db.get_customer_metrics, {}, 2.0),
            (db.get_revenue_metrics, {}, 2.0),
            (db.get_usage_metrics, {}, 2.0),
            (db.get_operations_metrics, {}, 2.0),
        ]
        
        for func, kwargs, max_time in performance_tests:
            start_time = time.time()
            result = func(**kwargs)
            elapsed = time.time() - start_time
            
            assert elapsed < max_time, f"{func.__name__} took {elapsed:.2f}s (max: {max_time}s)"
            assert result is not None, f"{func.__name__} returned None"
    
    def test_cache_performance_effectiveness(self):
        """Test caching performance and effectiveness"""
        db = TelecomDatabase()
        
        # Clear cache if possible
        if hasattr(db.get_network_metrics, 'cache_clear'):
            db.get_network_metrics.cache_clear()
        
        # Measure first call (cache miss)
        start_time = time.time()
        result1 = db.get_network_metrics(days=30)
        first_call = time.time() - start_time
        
        # Measure second call (cache hit)
        start_time = time.time()
        result2 = db.get_network_metrics(days=30)
        second_call = time.time() - start_time
        
        # Verify results are identical
        assert result1 == result2, "Cached result differs from original"
        
        # Verify cache effectiveness (second call should be much faster)
        if second_call > 0:
            speedup = first_call / second_call
            assert speedup > 2, f"Cache not effective enough: {speedup:.2f}x speedup"
        
        print(f"Cache speedup: {first_call/second_call if second_call > 0 else 'instant'}x")
    
    def test_concurrent_request_performance(self):
        """Test performance under concurrent requests"""
        db = TelecomDatabase()
        
        def worker():
            """Worker function for concurrent testing"""
            start_time = time.time()
            result = db.get_network_metrics(days=7)
            elapsed = time.time() - start_time
            return elapsed, result is not None
        
        # Test with multiple concurrent requests
        num_workers = 10
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(worker) for _ in range(num_workers)]
            results = [future.result() for future in as_completed(futures)]
        
        # All requests should succeed
        assert all(success for _, success in results), "Some concurrent requests failed"
        
        # Performance should be reasonable even under load
        times = [elapsed for elapsed, _ in results]
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        assert avg_time < 5.0, f"Average response time too high: {avg_time:.2f}s"
        assert max_time < 10.0, f"Maximum response time too high: {max_time:.2f}s"
        
        print(f"Concurrent performance - Avg: {avg_time:.2f}s, Max: {max_time:.2f}s")
    
    def test_memory_usage_under_load(self):
        """Test memory usage under sustained load"""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        db = TelecomDatabase()
        
        # Perform sustained operations
        for i in range(50):
            db.get_network_metrics(days=30)
            db.get_customer_metrics(days=30)
            
            # Check memory every 10 operations
            if i % 10 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_increase = current_memory - initial_memory
                
                # Memory increase should be reasonable (< 100MB growth)
                assert memory_increase < 100, f"Excessive memory growth: {memory_increase:.1f}MB"
        
        final_memory = process.memory_info().rss / 1024 / 1024
        total_increase = final_memory - initial_memory
        
        print(f"Memory usage: {initial_memory:.1f}MB -> {final_memory:.1f}MB (+{total_increase:.1f}MB)")
        assert total_increase < 150, f"Total memory increase too high: {total_increase:.1f}MB"
    
    def test_cpu_usage_efficiency(self):
        """Test CPU usage efficiency during operations"""
        # Monitor CPU usage during operations
        cpu_samples = []
        
        def monitor_cpu():
            for _ in range(10):  # Monitor for 10 samples
                cpu_samples.append(psutil.cpu_percent(interval=0.1))
        
        # Start CPU monitoring
        monitor_thread = threading.Thread(target=monitor_cpu)
        monitor_thread.start()
        
        # Perform operations
        db = TelecomDatabase()
        for _ in range(20):
            db.get_network_metrics(days=30)
            db.get_customer_metrics(days=30)
        
        monitor_thread.join()
        
        # Analyze CPU usage
        avg_cpu = sum(cpu_samples) / len(cpu_samples)
        max_cpu = max(cpu_samples)
        
        print(f"CPU usage - Avg: {avg_cpu:.1f}%, Max: {max_cpu:.1f}%")
        
        # CPU usage should be reasonable
        assert avg_cpu < 80, f"Average CPU usage too high: {avg_cpu:.1f}%"
        assert max_cpu < 95, f"Peak CPU usage too high: {max_cpu:.1f}%"

class TestLLMServicePerformance:
    """Test LLM service performance and reliability"""
    
    @patch('requests.post')
    def test_llm_response_time(self, mock_post):
        """Test LLM service response time"""
        # Mock successful API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{
                "message": {
                    "content": '{"summary": "Test response", "key_insights": ["Test"], "trends": ["Test"], "recommended_actions": ["Test"]}'
                }
            }]
        }
        
        llm = LLMService()
        
        # Test response time
        start_time = time.time()
        result = llm.generate_insights("Test prompt")
        elapsed = time.time() - start_time
        
        # Should complete reasonably quickly (excluding actual API call)
        assert elapsed < 5.0, f"LLM processing took too long: {elapsed:.2f}s"
        assert isinstance(result, dict)
    
    @patch('requests.post')
    def test_llm_circuit_breaker_performance(self, mock_post):
        """Test circuit breaker performance impact"""
        llm = LLMService()
        
        # First, test normal operation
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": '{"summary": "Test", "key_insights": [], "trends": [], "recommended_actions": []}'}}]
        }
        
        normal_times = []
        for _ in range(3):
            start_time = time.time()
            llm.generate_insights("Test")
            normal_times.append(time.time() - start_time)
        
        # Trigger circuit breaker
        for _ in range(6):
            llm.circuit_breaker.record_failure()
        
        # Test fallback performance
        fallback_times = []
        for _ in range(3):
            start_time = time.time()
            result = llm.generate_insights("Test")
            fallback_times.append(time.time() - start_time)
            assert isinstance(result, dict)
            assert "temporarily unavailable" in result["summary"].lower()
        
        # Fallback should be faster than API calls
        avg_normal = sum(normal_times) / len(normal_times)
        avg_fallback = sum(fallback_times) / len(fallback_times)
        
        print(f"Response times - Normal: {avg_normal:.3f}s, Fallback: {avg_fallback:.3f}s")
        assert avg_fallback < avg_normal, "Fallback not faster than normal operation"
        assert avg_fallback < 0.1, f"Fallback too slow: {avg_fallback:.3f}s"

class TestHealthCheckPerformance:
    """Test health check system performance"""
    
    def test_simple_health_check_speed(self):
        """Test simple health check response time"""
        start_time = time.time()
        health_data = health_checker.get_simple_health()
        elapsed = time.time() - start_time
        
        # Simple health check should be very fast
        assert elapsed < 1.0, f"Simple health check too slow: {elapsed:.2f}s"
        assert isinstance(health_data, dict)
        assert "status" in health_data
    
    def test_comprehensive_health_check_speed(self):
        """Test comprehensive health check response time"""
        start_time = time.time()
        health_data = health_checker.get_comprehensive_health()
        elapsed = time.time() - start_time
        
        # Comprehensive check should complete in reasonable time
        assert elapsed < 10.0, f"Comprehensive health check too slow: {elapsed:.2f}s"
        assert isinstance(health_data, dict)
        assert "checks" in health_data
        assert len(health_data["checks"]) > 0
    
    def test_health_check_under_load(self):
        """Test health check performance under concurrent load"""
        def worker():
            start_time = time.time()
            result = health_checker.get_simple_health()
            elapsed = time.time() - start_time
            return elapsed, result["status"] == "healthy"
        
        # Test concurrent health checks
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(worker) for _ in range(10)]
            results = [future.result() for future in as_completed(futures)]
        
        # All should succeed
        assert all(success for _, success in results), "Some health checks failed"
        
        # Performance should remain good under load
        times = [elapsed for elapsed, _ in results]
        avg_time = sum(times) / len(times)
        max_time = max(times)
        
        assert avg_time < 2.0, f"Average health check time too high: {avg_time:.2f}s"
        assert max_time < 5.0, f"Maximum health check time too high: {max_time:.2f}s"

class TestSystemResourceMonitoring:
    """Test system resource monitoring and thresholds"""
    
    def test_system_resource_thresholds(self):
        """Test system resource monitoring thresholds"""
        health_check = health_checker.check_system_resources()
        
        assert health_check.name == "system_resources"
        assert health_check.status in ["healthy", "degraded", "unhealthy"]
        assert "cpu_percent" in health_check.details
        assert "memory_percent" in health_check.details
        assert "disk_percent" in health_check.details
        
        # Verify threshold logic
        cpu_percent = health_check.details["cpu_percent"]
        memory_percent = health_check.details["memory_percent"]
        disk_percent = health_check.details["disk_percent"]
        
        # If high resource usage, status should reflect it
        if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
            assert health_check.status == "unhealthy"
        elif cpu_percent > 80 or memory_percent > 80 or disk_percent > 80:
            assert health_check.status in ["degraded", "unhealthy"]
    
    def test_resource_monitoring_accuracy(self):
        """Test resource monitoring accuracy"""
        # Get system resources directly
        cpu_direct = psutil.cpu_percent(interval=1)
        memory_direct = psutil.virtual_memory().percent
        disk_direct = psutil.disk_usage('/').percent
        
        # Get resources via health check
        health_check = health_checker.check_system_resources()
        cpu_health = health_check.details["cpu_percent"]
        memory_health = health_check.details["memory_percent"]
        disk_health = health_check.details["disk_percent"]
        
        # Should be reasonably close (within 10% tolerance)
        assert abs(cpu_direct - cpu_health) < 10, f"CPU mismatch: {cpu_direct} vs {cpu_health}"
        assert abs(memory_direct - memory_health) < 5, f"Memory mismatch: {memory_direct} vs {memory_health}"
        assert abs(disk_direct - disk_health) < 2, f"Disk mismatch: {disk_direct} vs {disk_health}"

class TestPerformanceRegression:
    """Test for performance regressions"""
    
    def test_baseline_performance_metrics(self):
        """Test baseline performance metrics to detect regressions"""
        db = TelecomDatabase()
        
        # Baseline performance targets (adjust based on your system)
        baseline_targets = {
            'single_query': 2.0,  # Single query should complete in < 2s
            'cache_hit': 0.1,     # Cache hit should be < 0.1s
            'concurrent_avg': 5.0, # Concurrent queries avg < 5s
            'memory_growth': 50,   # Memory growth < 50MB per 100 operations
        }
        
        # Test single query performance
        start_time = time.time()
        db.get_network_metrics(days=30)
        single_query_time = time.time() - start_time
        
        assert single_query_time < baseline_targets['single_query'], \
            f"Single query regression: {single_query_time:.2f}s > {baseline_targets['single_query']}s"
        
        # Test cache hit performance
        start_time = time.time()
        db.get_network_metrics(days=30)  # Should hit cache
        cache_hit_time = time.time() - start_time
        
        assert cache_hit_time < baseline_targets['cache_hit'], \
            f"Cache hit regression: {cache_hit_time:.2f}s > {baseline_targets['cache_hit']}s"
        
        print(f"Performance baseline - Single: {single_query_time:.2f}s, Cache: {cache_hit_time:.2f}s")
    
    def test_memory_leak_detection(self):
        """Test for memory leaks during sustained operations"""
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        db = TelecomDatabase()
        
        # Perform many operations to detect memory leaks
        for cycle in range(5):
            for _ in range(20):  # 20 operations per cycle
                db.get_network_metrics(days=30)
                db.get_customer_metrics(days=30)
            
            # Check memory after each cycle
            current_memory = process.memory_info().rss / 1024 / 1024
            growth = current_memory - initial_memory
            
            # Memory growth should be bounded
            max_allowed_growth = 20 * (cycle + 1)  # 20MB per cycle
            assert growth < max_allowed_growth, \
                f"Potential memory leak: {growth:.1f}MB growth after cycle {cycle + 1}"
        
        final_memory = process.memory_info().rss / 1024 / 1024
        total_growth = final_memory - initial_memory
        
        print(f"Memory leak test - Growth: {total_growth:.1f}MB over 100 operations")
        assert total_growth < 100, f"Excessive memory growth: {total_growth:.1f}MB"

if __name__ == "__main__":
    # Run performance tests
    pytest.main([__file__, "-v", "--tb=short", "-s"])  # -s to show print statements
