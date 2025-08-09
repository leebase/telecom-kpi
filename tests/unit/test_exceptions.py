"""
Unit tests for custom exceptions module
"""

import pytest
import logging
from unittest.mock import Mock, patch
from datetime import datetime

from src.exceptions.custom_exceptions import (
    TelecomDashboardError, DatabaseError, DatabaseConnectionError, 
    DatabaseQueryError, DataValidationError, ConfigurationError,
    SecurityError, AuthenticationError, AuthorizationError,
    APIError, LLMServiceError, DataProcessingError, CacheError,
    UIError, ErrorRecovery, handle_exceptions
)

class TestTelecomDashboardError:
    """Test base TelecomDashboardError class"""
    
    def test_basic_initialization(self):
        """Test basic error initialization"""
        error = TelecomDashboardError("Test error message")
        
        assert str(error) == "Test error message"
        assert error.message == "Test error message"
        assert error.error_code is None
        assert error.details == {}
    
    def test_initialization_with_code_and_details(self):
        """Test error initialization with code and details"""
        details = {"key": "value", "number": 42}
        error = TelecomDashboardError(
            "Test error",
            error_code="TEST_ERROR",
            details=details
        )
        
        assert error.message == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.details == details
    
    @patch('src.exceptions.custom_exceptions.logger')
    def test_logging_on_creation(self, mock_logger):
        """Test that errors are logged when created"""
        error = TelecomDashboardError(
            "Test error",
            error_code="TEST_CODE",
            details={"test": "data"}
        )
        
        mock_logger.error.assert_called_once()
        call_args = mock_logger.error.call_args
        assert "TelecomDashboardError: Test error" in call_args[0][0]

class TestDatabaseErrors:
    """Test database-related error classes"""
    
    def test_database_error(self):
        """Test DatabaseError"""
        error = DatabaseError(
            "Database operation failed",
            query="SELECT * FROM table",
            table="test_table"
        )
        
        assert error.message == "Database operation failed"
        assert error.error_code == "DB_ERROR"
        assert error.details["query"] == "SELECT * FROM table"
        assert error.details["table"] == "test_table"
    
    def test_database_connection_error(self):
        """Test DatabaseConnectionError"""
        error = DatabaseConnectionError()
        
        assert error.message == "Failed to connect to database"
        assert error.error_code == "DB_CONNECTION_ERROR"
    
    def test_database_connection_error_custom_message(self):
        """Test DatabaseConnectionError with custom message"""
        error = DatabaseConnectionError("Custom connection error")
        
        assert error.message == "Custom connection error"
        assert error.error_code == "DB_CONNECTION_ERROR"
    
    def test_database_query_error(self):
        """Test DatabaseQueryError"""
        query = "SELECT invalid_column FROM table"
        error = DatabaseQueryError("Query failed", query=query)
        
        assert error.message == "Query failed"
        assert error.error_code == "DB_QUERY_ERROR"
        assert error.details["query"] == query

class TestValidationErrors:
    """Test validation-related error classes"""
    
    def test_data_validation_error(self):
        """Test DataValidationError"""
        error = DataValidationError(
            "Invalid field value",
            field="email",
            value="invalid-email"
        )
        
        assert error.message == "Invalid field value"
        assert error.error_code == "VALIDATION_ERROR"
        assert error.details["field"] == "email"
        assert error.details["value"] == "invalid-email"
    
    def test_data_validation_error_no_field(self):
        """Test DataValidationError without field information"""
        error = DataValidationError("General validation error")
        
        assert error.message == "General validation error"
        assert error.error_code == "VALIDATION_ERROR"

class TestConfigurationError:
    """Test ConfigurationError class"""
    
    def test_configuration_error(self):
        """Test ConfigurationError"""
        error = ConfigurationError(
            "Missing configuration",
            config_key="database.host"
        )
        
        assert error.message == "Missing configuration"
        assert error.error_code == "CONFIG_ERROR"
        assert error.details["config_key"] == "database.host"

class TestSecurityErrors:
    """Test security-related error classes"""
    
    def test_security_error(self):
        """Test SecurityError"""
        error = SecurityError(
            "Security violation",
            security_type="input_validation"
        )
        
        assert error.message == "Security violation"
        assert error.error_code == "SECURITY_ERROR"
        assert error.details["security_type"] == "input_validation"
    
    def test_authentication_error(self):
        """Test AuthenticationError"""
        error = AuthenticationError()
        
        assert error.message == "Authentication failed"
        assert error.error_code == "AUTH_ERROR"
        assert error.details["security_type"] == "authentication"
    
    def test_authentication_error_custom_message(self):
        """Test AuthenticationError with custom message"""
        error = AuthenticationError("Invalid credentials")
        
        assert error.message == "Invalid credentials"
        assert error.error_code == "AUTH_ERROR"
    
    def test_authorization_error(self):
        """Test AuthorizationError"""
        error = AuthorizationError()
        
        assert error.message == "Authorization failed"
        assert error.error_code == "AUTHZ_ERROR"
        assert error.details["security_type"] == "authorization"

class TestAPIErrors:
    """Test API-related error classes"""
    
    def test_api_error(self):
        """Test APIError"""
        error = APIError(
            "API call failed",
            api_name="external_service",
            status_code=500,
            response_data='{"error": "Internal server error"}'
        )
        
        assert error.message == "API call failed"
        assert error.error_code == "API_ERROR"
        assert error.details["api_name"] == "external_service"
        assert error.details["status_code"] == 500
        assert error.details["response_data"] == '{"error": "Internal server error"}'
    
    def test_llm_service_error(self):
        """Test LLMServiceError"""
        error = LLMServiceError(
            "LLM request failed",
            model="google/gemini-2.5-flash"
        )
        
        assert error.message == "LLM request failed"
        assert error.error_code == "LLM_ERROR"
        assert error.details["api_name"] == "llm_service"
        assert error.details["model"] == "google/gemini-2.5-flash"

class TestOtherErrors:
    """Test other specialized error classes"""
    
    def test_data_processing_error(self):
        """Test DataProcessingError"""
        error = DataProcessingError(
            "Processing failed",
            operation="aggregation",
            data_type="metrics"
        )
        
        assert error.message == "Processing failed"
        assert error.error_code == "DATA_PROCESSING_ERROR"
        assert error.details["operation"] == "aggregation"
        assert error.details["data_type"] == "metrics"
    
    def test_cache_error(self):
        """Test CacheError"""
        error = CacheError(
            "Cache miss",
            cache_key="network_metrics_30d"
        )
        
        assert error.message == "Cache miss"
        assert error.error_code == "CACHE_ERROR"
        assert error.details["cache_key"] == "network_metrics_30d"
    
    def test_ui_error(self):
        """Test UIError"""
        error = UIError(
            "Component render failed",
            component="MetricCard"
        )
        
        assert error.message == "Component render failed"
        assert error.error_code == "UI_ERROR"
        assert error.details["component"] == "MetricCard"

class TestErrorRecovery:
    """Test ErrorRecovery utility class"""
    
    def test_with_fallback_success(self):
        """Test with_fallback when primary function succeeds"""
        def primary():
            return "primary_result"
        
        def fallback():
            return "fallback_result"
        
        result = ErrorRecovery.with_fallback(primary, fallback)
        assert result == "primary_result"
    
    def test_with_fallback_failure(self):
        """Test with_fallback when primary function fails"""
        def primary():
            raise ValueError("Primary failed")
        
        def fallback():
            return "fallback_result"
        
        with patch('src.exceptions.custom_exceptions.logger') as mock_logger:
            result = ErrorRecovery.with_fallback(primary, fallback)
            assert result == "fallback_result"
            mock_logger.warning.assert_called()
    
    def test_with_fallback_with_args(self):
        """Test with_fallback with function arguments"""
        def primary(x, y, z=None):
            if z == "fail":
                raise ValueError("Failed")
            return f"primary_{x}_{y}_{z}"
        
        def fallback(x, y, z=None):
            return f"fallback_{x}_{y}_{z}"
        
        # Success case
        result = ErrorRecovery.with_fallback(primary, fallback, "a", "b", z="success")
        assert result == "primary_a_b_success"
        
        # Fallback case
        result = ErrorRecovery.with_fallback(primary, fallback, "a", "b", z="fail")
        assert result == "fallback_a_b_fail"
    
    def test_retry_with_backoff_success(self):
        """Test retry_with_backoff when function succeeds"""
        call_count = 0
        
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        wrapped = ErrorRecovery.retry_with_backoff(test_func, max_retries=3)
        result = wrapped()
        
        assert result == "success"
        assert call_count == 1
    
    def test_retry_with_backoff_eventual_success(self):
        """Test retry_with_backoff with eventual success"""
        call_count = 0
        
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError(f"Attempt {call_count} failed")
            return "success"
        
        with patch('time.sleep'):  # Mock sleep to speed up test
            wrapped = ErrorRecovery.retry_with_backoff(test_func, max_retries=3)
            result = wrapped()
        
        assert result == "success"
        assert call_count == 3
    
    def test_retry_with_backoff_final_failure(self):
        """Test retry_with_backoff when all retries fail"""
        call_count = 0
        
        def test_func():
            nonlocal call_count
            call_count += 1
            raise ValueError(f"Attempt {call_count} failed")
        
        with patch('time.sleep'):  # Mock sleep to speed up test
            wrapped = ErrorRecovery.retry_with_backoff(test_func, max_retries=2)
            
            with pytest.raises(ValueError, match="Attempt 3 failed"):
                wrapped()
        
        assert call_count == 3  # Initial attempt + 2 retries
    
    def test_safe_execute_success(self):
        """Test safe_execute when function succeeds"""
        def test_func():
            return "success"
        
        wrapped = ErrorRecovery.safe_execute(test_func, default_value="default")
        result = wrapped()
        
        assert result == "success"
    
    def test_safe_execute_failure(self):
        """Test safe_execute when function fails"""
        def test_func():
            raise ValueError("Function failed")
        
        with patch('src.exceptions.custom_exceptions.logger') as mock_logger:
            wrapped = ErrorRecovery.safe_execute(test_func, default_value="default")
            result = wrapped()
            
            assert result == "default"
            mock_logger.error.assert_called()
    
    def test_safe_execute_no_logging(self):
        """Test safe_execute with logging disabled"""
        def test_func():
            raise ValueError("Function failed")
        
        with patch('src.exceptions.custom_exceptions.logger') as mock_logger:
            wrapped = ErrorRecovery.safe_execute(
                test_func, 
                default_value="default", 
                log_errors=False
            )
            result = wrapped()
            
            assert result == "default"
            mock_logger.error.assert_not_called()

class TestHandleExceptionsDecorator:
    """Test handle_exceptions decorator"""
    
    def test_handle_exceptions_success(self):
        """Test decorator when function succeeds"""
        @handle_exceptions(default_return="default")
        def test_func():
            return "success"
        
        result = test_func()
        assert result == "success"
    
    def test_handle_exceptions_with_default(self):
        """Test decorator with default return value"""
        @handle_exceptions(default_return="default")
        def test_func():
            raise ValueError("Function failed")
        
        with patch('src.exceptions.custom_exceptions.logger') as mock_logger:
            result = test_func()
            assert result == "default"
            mock_logger.error.assert_called()
    
    def test_handle_exceptions_with_reraise(self):
        """Test decorator with exception reraising"""
        @handle_exceptions(reraise_as=DataProcessingError)
        def test_func():
            raise ValueError("Original error")
        
        with pytest.raises(DataProcessingError) as exc_info:
            test_func()
        
        assert "Error in test_func: Original error" in str(exc_info.value)
        assert exc_info.value.__cause__.__class__ == ValueError
    
    def test_handle_exceptions_with_args(self):
        """Test decorator with function arguments"""
        @handle_exceptions(default_return=0)
        def add_numbers(a, b):
            if a < 0:
                raise ValueError("Negative number")
            return a + b
        
        # Success case
        result = add_numbers(5, 3)
        assert result == 8
        
        # Error case
        result = add_numbers(-1, 3)
        assert result == 0

class TestErrorInheritance:
    """Test error class inheritance"""
    
    def test_inheritance_chain(self):
        """Test that all custom errors inherit from base class"""
        errors = [
            DatabaseError("test"),
            DataValidationError("test"),
            ConfigurationError("test"),
            SecurityError("test"),
            APIError("test"),
            DataProcessingError("test"),
            CacheError("test"),
            UIError("test")
        ]
        
        for error in errors:
            assert isinstance(error, TelecomDashboardError)
            assert isinstance(error, Exception)
    
    def test_specialized_inheritance(self):
        """Test specialized error inheritance"""
        # Database errors
        conn_error = DatabaseConnectionError()
        query_error = DatabaseQueryError("test", "SELECT 1")
        assert isinstance(conn_error, DatabaseError)
        assert isinstance(query_error, DatabaseError)
        
        # Security errors
        auth_error = AuthenticationError()
        authz_error = AuthorizationError()
        assert isinstance(auth_error, SecurityError)
        assert isinstance(authz_error, SecurityError)
        
        # API errors
        llm_error = LLMServiceError("test")
        assert isinstance(llm_error, APIError)

class TestErrorContextManagement:
    """Test error handling in context management scenarios"""
    
    def test_error_in_context_manager(self):
        """Test error handling within context managers"""
        class TestContext:
            def __enter__(self):
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type == ValueError:
                    # Convert ValueError to custom error
                    raise DataProcessingError("Context error") from exc_val
                return False
        
        with pytest.raises(DataProcessingError):
            with TestContext():
                raise ValueError("Original error")
    
    def test_multiple_error_types(self):
        """Test handling multiple error types"""
        def risky_operation(error_type):
            if error_type == "db":
                raise DatabaseError("DB error")
            elif error_type == "validation":
                raise DataValidationError("Validation error")
            elif error_type == "config":
                raise ConfigurationError("Config error")
            else:
                return "success"
        
        # Test different error types are raised correctly
        with pytest.raises(DatabaseError):
            risky_operation("db")
        
        with pytest.raises(DataValidationError):
            risky_operation("validation")
        
        with pytest.raises(ConfigurationError):
            risky_operation("config")
        
        # Test success case
        result = risky_operation("success")
        assert result == "success"


