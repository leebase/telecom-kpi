"""
Test suite for environment validation and configuration management

Tests the EnvironmentValidator class and related configuration validation functionality
to ensure proper environment setup and production readiness checks.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config_manager import EnvironmentValidator, ConfigValidationError

class TestEnvironmentValidator:
    """Test environment validation functionality"""
    
    def test_validate_environment_development(self):
        """Test environment validation in development mode"""
        with patch.dict(os.environ, {}, clear=True):
            results = EnvironmentValidator.validate_environment('development')
            
            # Development should be more permissive
            assert results['environment'] == 'development'
            assert isinstance(results['valid'], bool)
            assert isinstance(results['errors'], list)
            assert isinstance(results['warnings'], list)
            assert 'summary' in results
    
    def test_validate_environment_production_missing_vars(self):
        """Test production validation with missing required variables"""
        with patch.dict(os.environ, {}, clear=True):
            results = EnvironmentValidator.validate_environment('production')
            
            assert results['environment'] == 'production'
            assert results['valid'] == False
            assert len(results['errors']) > 0
            
            # Should have errors for missing production-required vars
            error_messages = ' '.join(results['errors'])
            assert 'DATABASE_URL' in error_messages
            assert 'LLM_API_KEY' in error_messages
            assert 'LOG_LEVEL' in error_messages
    
    def test_validate_environment_production_complete(self):
        """Test production validation with all required variables"""
        production_env = {
            'ENVIRONMENT': 'production',
            'DATABASE_URL': 'postgresql://user:pass@host:5432/db',
            'LLM_API_KEY': 'sk-test-key-12345678901234567890',
            'LOG_LEVEL': 'INFO',
            'CACHE_TTL_SECONDS': '300'
        }
        
        with patch.dict(os.environ, production_env, clear=True):
            results = EnvironmentValidator.validate_environment('production')
            
            assert results['environment'] == 'production'
            assert results['valid'] == True
            assert len(results['errors']) == 0
            
            # Summary should show all required vars set
            summary = results['summary']
            assert summary['required_vars_set'] >= 1
            assert summary['total_errors'] == 0
    
    def test_validate_specific_vars_database_url(self):
        """Test DATABASE_URL format validation"""
        results = {'errors': [], 'warnings': []}
        
        # Test valid URLs
        with patch.dict(os.environ, {'DATABASE_URL': 'postgresql://user:pass@host:5432/db'}):
            EnvironmentValidator._validate_specific_vars(results)
            # Should not add warnings for valid PostgreSQL URL
        
        with patch.dict(os.environ, {'DATABASE_URL': 'sqlite:///path/to/db.sqlite'}):
            EnvironmentValidator._validate_specific_vars(results)
            # Should not add warnings for valid SQLite URL
        
        # Test invalid URL
        with patch.dict(os.environ, {'DATABASE_URL': 'invalid-url-format'}):
            EnvironmentValidator._validate_specific_vars(results)
            warning_messages = ' '.join(results['warnings'])
            assert 'DATABASE_URL format not recognized' in warning_messages
    
    def test_validate_specific_vars_log_level(self):
        """Test LOG_LEVEL validation"""
        results = {'errors': [], 'warnings': []}
        
        # Test valid log levels
        for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            with patch.dict(os.environ, {'LOG_LEVEL': level}):
                EnvironmentValidator._validate_specific_vars(results)
        
        # Should not have errors for valid levels
        assert len([e for e in results['errors'] if 'LOG_LEVEL' in e]) == 0
        
        # Test invalid log level
        with patch.dict(os.environ, {'LOG_LEVEL': 'INVALID'}):
            EnvironmentValidator._validate_specific_vars(results)
            error_messages = ' '.join(results['errors'])
            assert 'Invalid LOG_LEVEL value' in error_messages
    
    def test_validate_specific_vars_cache_ttl(self):
        """Test CACHE_TTL_SECONDS validation"""
        results = {'errors': [], 'warnings': []}
        
        # Test valid TTL values
        with patch.dict(os.environ, {'CACHE_TTL_SECONDS': '300'}):
            EnvironmentValidator._validate_specific_vars(results)
        
        # Test invalid TTL (non-integer)
        with patch.dict(os.environ, {'CACHE_TTL_SECONDS': 'invalid'}):
            EnvironmentValidator._validate_specific_vars(results)
            error_messages = ' '.join(results['errors'])
            assert 'Invalid CACHE_TTL_SECONDS value' in error_messages
        
        # Test TTL outside recommended range
        with patch.dict(os.environ, {'CACHE_TTL_SECONDS': '7200'}):  # 2 hours
            EnvironmentValidator._validate_specific_vars(results)
            warning_messages = ' '.join(results['warnings'])
            assert 'outside recommended range' in warning_messages
    
    def test_validate_specific_vars_api_key(self):
        """Test LLM_API_KEY format validation"""
        results = {'errors': [], 'warnings': []}
        
        # Test valid API key formats
        with patch.dict(os.environ, {'LLM_API_KEY': 'sk-test-key-12345678901234567890'}):
            EnvironmentValidator._validate_specific_vars(results)
        
        with patch.dict(os.environ, {'LLM_API_KEY': 'pk-test-key-12345678901234567890'}):
            EnvironmentValidator._validate_specific_vars(results)
        
        # Test invalid API key format
        with patch.dict(os.environ, {'LLM_API_KEY': 'invalid-key'}):
            EnvironmentValidator._validate_specific_vars(results)
            warning_messages = ' '.join(results['warnings'])
            assert 'format may be invalid' in warning_messages
    
    def test_validate_startup_config_success(self):
        """Test successful startup configuration validation"""
        valid_env = {
            'ENVIRONMENT': 'development',
            'LLM_API_KEY': 'sk-test-key-12345678901234567890'
        }
        
        with patch.dict(os.environ, valid_env, clear=True):
            # Should not raise exception for development
            result = EnvironmentValidator.validate_startup_config()
            assert isinstance(result, bool)
    
    def test_validate_startup_config_failure(self):
        """Test startup configuration validation failure"""
        with patch.dict(os.environ, {'ENVIRONMENT': 'production'}, clear=True):
            # Should raise exception for production with missing vars
            with pytest.raises(ConfigValidationError) as exc_info:
                EnvironmentValidator.validate_startup_config()
            
            assert 'Environment validation failed' in str(exc_info.value.message)
            assert len(exc_info.value.missing_vars) > 0

class TestConfigValidationError:
    """Test ConfigValidationError exception"""
    
    def test_config_validation_error_creation(self):
        """Test ConfigValidationError creation and attributes"""
        missing_vars = ['DATABASE_URL', 'LLM_API_KEY']
        invalid_vars = ['LOG_LEVEL']
        message = "Test validation error"
        
        error = ConfigValidationError(
            message=message,
            missing_vars=missing_vars,
            invalid_vars=invalid_vars
        )
        
        assert error.message == message
        assert error.missing_vars == missing_vars
        assert error.invalid_vars == invalid_vars
        assert str(error) == message

class TestEnvironmentValidatorIntegration:
    """Integration tests for environment validation"""
    
    def test_environment_validator_with_real_config(self):
        """Test environment validator with actual configuration loading"""
        # This test uses the actual configuration system
        try:
            from config_manager import get_config
            
            # Should be able to load config (may have warnings)
            config = get_config()
            assert config is not None
            
            # Validate current environment
            results = EnvironmentValidator.validate_environment()
            assert 'environment' in results
            assert 'valid' in results
            assert 'summary' in results
            
        except Exception as e:
            # Configuration loading should not fail completely
            pytest.fail(f"Configuration integration test failed: {e}")
    
    def test_production_readiness_scenarios(self):
        """Test various production readiness scenarios"""
        scenarios = [
            # Minimal production environment
            {
                'env': {
                    'ENVIRONMENT': 'production',
                    'DATABASE_URL': 'postgresql://prod/db',
                    'LLM_API_KEY': 'sk-prod-key-12345678901234567890',
                    'LOG_LEVEL': 'INFO'
                },
                'should_be_valid': True
            },
            # Missing critical variable
            {
                'env': {
                    'ENVIRONMENT': 'production',
                    'LLM_API_KEY': 'sk-prod-key-12345678901234567890',
                    'LOG_LEVEL': 'INFO'
                    # Missing DATABASE_URL
                },
                'should_be_valid': False
            },
            # Development environment (more permissive)
            {
                'env': {
                    'ENVIRONMENT': 'development'
                    # Minimal requirements for development
                },
                'should_be_valid': False  # Still needs ENVIRONMENT var
            }
        ]
        
        for i, scenario in enumerate(scenarios):
            with patch.dict(os.environ, scenario['env'], clear=True):
                results = EnvironmentValidator.validate_environment(scenario['env'].get('ENVIRONMENT', 'development'))
                
                if scenario['should_be_valid']:
                    assert results['valid'], f"Scenario {i} should be valid but got errors: {results['errors']}"
                else:
                    assert not results['valid'], f"Scenario {i} should be invalid but passed validation"

if __name__ == '__main__':
    # Run tests directly
    pytest.main([__file__, '-v'])
