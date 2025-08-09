# 📡 API Documentation: Telecom KPI Dashboard

## 📋 Overview

This document provides comprehensive documentation for the internal APIs and data access layer of the Telecom KPI Dashboard. It covers database operations, configuration management, health check endpoints, and integration interfaces for enterprise deployment and operations.

## 🏗️ API Architecture

### API Layers
```
API Architecture:
┌─────────────────────────────────────────────────────────┐
│ REST API Layer (Health Checks & Management)            │
├─────────────────────────────────────────────────────────┤
│ Configuration Management API                           │
│ ├── Environment Validation                             │
│ ├── Feature Flag Management                            │
│ └── Production Readiness Checks                        │
├─────────────────────────────────────────────────────────┤
│ Data Access Layer (Database API)                       │
│ ├── KPI Metrics Retrieval                             │
│ ├── Trend Data Analysis                               │
│ ├── Benchmark Comparison                               │
│ └── Connection Management                              │
├─────────────────────────────────────────────────────────┤
│ External Service Integration                            │
│ ├── LLM Service API (OpenRouter)                      │
│ ├── Database Adapters (PostgreSQL/Snowflake)          │
│ └── Monitoring & Logging                              │
└─────────────────────────────────────────────────────────┘
```

## 🩺 Health Check API

### Simple Health Check
**Endpoint**: `GET /?health=simple`

**Description**: Basic health check endpoint for load balancers and uptime monitoring.

**Response Format**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-09T12:00:00Z",
  "version": "2.2.0"
}
```

**Status Codes**:
- `200 OK`: Application is healthy
- `503 Service Unavailable`: Application is unhealthy

**Usage Example**:
```bash
curl -s http://localhost:8501/?health=simple
```

### Detailed Health Check
**Endpoint**: `GET /?health=detailed`

**Description**: Comprehensive health check with system diagnostics for monitoring systems.

**Response Format**:
```json
{
  "status": "healthy",
  "timestamp": "2025-08-09T12:00:00Z",
  "version": "2.2.0",
  "checks": {
    "database": {
      "status": "healthy",
      "response_time_ms": 45,
      "connection_pool": {
        "active": 2,
        "idle": 3,
        "total": 5
      }
    },
    "external_apis": {
      "llm_service": {
        "status": "healthy",
        "response_time_ms": 120,
        "last_check": "2025-08-09T11:59:30Z"
      }
    },
    "system_resources": {
      "cpu_percent": 25.4,
      "memory_percent": 68.2,
      "disk_usage_percent": 45.1
    },
    "application": {
      "uptime_seconds": 3600,
      "cache_hit_rate": 0.85,
      "active_sessions": 12
    }
  },
  "feature_flags": {
    "ai_insights": true,
    "structured_logging": true,
    "security_headers": true,
    "debug_mode": false
  }
}
```

**Usage Example**:
```bash
curl -s http://localhost:8501/?health=detailed | jq .
```

### Feature Status Check
**Endpoint**: `GET /?health=features`

**Description**: Returns current feature flag configuration for operations visibility.

**Response Format**:
```json
{
  "timestamp": "2025-08-09T12:00:00Z",
  "environment": "production",
  "feature_flags": {
    "ai_insights": true,
    "ai_insights_beta": false,
    "pii_scrubbing": true,
    "cache_ttl": true,
    "circuit_breaker": true,
    "connection_pooling": true,
    "structured_logging": true,
    "security_headers": true,
    "rate_limiting": true,
    "debug_mode": false
  },
  "environment_overrides": [
    "FEATURE_STRUCTURED_LOGGING=true",
    "FEATURE_SECURITY_HEADERS=true"
  ]
}
```

## ⚙️ Configuration Management API

### Environment Validation API

#### Validate Environment Configuration
**Function**: `EnvironmentValidator.validate_environment(environment)`

**Description**: Validates environment variables and configuration for deployment readiness.

**Parameters**:
- `environment` (str, optional): Target environment ('production', 'staging', 'development')

**Return Type**: `Dict[str, Any]`

**Response Format**:
```python
{
    'environment': 'production',
    'valid': True,
    'errors': [],
    'warnings': ['Missing recommended variable: CACHE_TTL_SECONDS'],
    'missing_required': [],
    'missing_recommended': ['CACHE_TTL_SECONDS'],
    'summary': {
        'required_vars_set': 1,
        'recommended_vars_set': 4,
        'total_errors': 0,
        'total_warnings': 1
    }
}
```

**Usage Example**:
```python
from config_manager import EnvironmentValidator

# Validate production environment
results = EnvironmentValidator.validate_environment('production')
print(f"Environment valid: {results['valid']}")
print(f"Errors: {results['errors']}")
print(f"Warnings: {results['warnings']}")
```

#### Production Readiness Check
**Function**: `EnvironmentValidator.validate_startup_config()`

**Description**: Performs comprehensive validation for production deployment.

**Return Type**: `bool`

**Raises**: `ConfigValidationError` for critical validation failures

**Usage Example**:
```python
from config_manager import EnvironmentValidator, ConfigValidationError

try:
    is_ready = EnvironmentValidator.validate_startup_config()
    print(f"Production ready: {is_ready}")
except ConfigValidationError as e:
    print(f"Validation failed: {e.message}")
    print(f"Missing variables: {e.missing_vars}")
```

### Feature Flag Management API

#### Get Feature Configuration
**Function**: `get_config().features`

**Description**: Retrieves current feature flag configuration.

**Return Type**: `FeatureConfig`

**Usage Example**:
```python
from config_manager import get_config

config = get_config()
features = config.features

print(f"AI Insights enabled: {features.ai_insights}")
print(f"Debug mode enabled: {features.debug_mode}")
print(f"Security headers enabled: {features.security_headers}")
```

#### Feature Flag Categories
**Available Feature Flags**:

```python
# AI and ML Features
ai_insights: bool = True
ai_insights_beta: bool = False
pii_scrubbing: bool = True

# Performance Features
cache_ttl: bool = True
circuit_breaker: bool = True
connection_pooling: bool = True

# Enterprise Features
structured_logging: bool = False
snowflake_query_tagging: bool = True
health_checks_detailed: bool = True

# UI and UX Features
theme_switching: bool = True
benchmark_management: bool = True
print_mode: bool = True

# Security Features
security_headers: bool = True
rate_limiting: bool = True
sql_injection_protection: bool = True

# Development Features
debug_mode: bool = False
test_mode: bool = False
performance_monitoring: bool = True
```

## 🗄️ Database Access Layer API

### Core Database Operations

#### TelecomDatabase Class
**Class**: `TelecomDatabase`

**Description**: Primary database interface for KPI data operations with connection pooling and caching.

**Initialization**:
```python
from database_connection import TelecomDatabase

db = TelecomDatabase()
```

### KPI Metrics API

#### Get Network Metrics
**Method**: `db.get_network_metrics(days=30)`

**Description**: Retrieves network performance KPI metrics.

**Parameters**:
- `days` (int): Number of days for historical data (default: 30)

**Return Type**: `Optional[Dict[str, Any]]`

**Response Format**:
```python
{
    'latency': 45.2,
    'throughput': 98.5,
    'packet_loss': 0.1,
    'availability': 99.9,
    'response_time': 120,
    'concurrent_users': 1500,
    'data_timestamp': '2025-08-09T12:00:00Z'
}
```

**Usage Example**:
```python
db = TelecomDatabase()
metrics = db.get_network_metrics(days=7)
if metrics:
    print(f"Network Latency: {metrics['latency']}ms")
    print(f"Availability: {metrics['availability']}%")
```

#### Get Customer Metrics
**Method**: `db.get_customer_metrics(days=30)`

**Description**: Retrieves customer experience and satisfaction KPI metrics.

**Parameters**:
- `days` (int): Number of days for historical data (default: 30)

**Return Type**: `Optional[Dict[str, Any]]`

**Response Format**:
```python
{
    'satisfaction_score': 8.2,
    'nps_score': 42,
    'churn_rate': 2.5,
    'avg_handling_time': 180,
    'first_contact_resolution': 85.5,
    'customer_lifetime_value': 2400,
    'data_timestamp': '2025-08-09T12:00:00Z'
}
```

#### Get Revenue Metrics
**Method**: `db.get_revenue_metrics(days=30)`

**Description**: Retrieves revenue and financial KPI metrics.

**Return Type**: `Optional[Dict[str, Any]]`

**Response Format**:
```python
{
    'total_revenue': 1250000,
    'arpu': 45.50,
    'revenue_growth': 12.3,
    'profit_margin': 18.7,
    'operational_efficiency': 92.1,
    'data_timestamp': '2025-08-09T12:00:00Z'
}
```

#### Get Usage Metrics
**Method**: `db.get_usage_metrics(days=30)`

**Description**: Retrieves service usage and adoption KPI metrics.

**Return Type**: `Optional[Dict[str, Any]]`

**Response Format**:
```python
{
    'data_usage_gb': 15.8,
    'voice_minutes': 420,
    'active_users': 95000,
    'feature_adoption_rate': 68.2,
    'service_utilization': 74.5,
    'data_timestamp': '2025-08-09T12:00:00Z'
}
```

#### Get Operations Metrics
**Method**: `db.get_operations_metrics(days=30)`

**Description**: Retrieves operational efficiency KPI metrics.

**Return Type**: `Optional[Dict[str, Any]]`

**Response Format**:
```python
{
    'incident_resolution_time': 240,
    'system_uptime': 99.95,
    'maintenance_efficiency': 88.3,
    'resource_utilization': 76.8,
    'automation_rate': 65.2,
    'data_timestamp': '2025-08-09T12:00:00Z'
}
```

### Trend Analysis API

#### Get Trend Data
**Method**: `db.get_trend_data(metric_name, days=30)`

**Description**: Retrieves historical trend data for specific metrics with SQL injection protection.

**Parameters**:
- `metric_name` (str): Name of the metric (validated against whitelist)
- `days` (int): Number of days for historical data

**Allowed Metrics**:
- `latency`, `throughput`, `packet_loss`, `availability`
- `satisfaction_score`, `nps_score`, `churn_rate`
- `total_revenue`, `arpu`, `revenue_growth`
- `data_usage_gb`, `voice_minutes`, `active_users`
- `incident_resolution_time`, `system_uptime`

**Return Type**: `pd.DataFrame`

**Response Format**:
```python
# DataFrame with columns:
{
    'date_id': ['2025-08-01', '2025-08-02', ...],
    'value': [45.2, 44.8, 46.1, ...]
}
```

**Usage Example**:
```python
trend_data = db.get_trend_data('latency', days=14)
print(f"Trend data points: {len(trend_data)}")
print(f"Latest latency: {trend_data.iloc[-1]['value']}ms")
```

#### Get Region Data
**Method**: `db.get_region_data(metric_name, days=30)`

**Description**: Retrieves metric data by geographic region.

**Parameters**:
- `metric_name` (str): Name of the metric (validated against whitelist)
- `days` (int): Number of days for historical data

**Return Type**: `pd.DataFrame`

**Response Format**:
```python
# DataFrame with columns:
{
    'region_name': ['North', 'South', 'East', 'West'],
    'value': [45.2, 48.1, 44.8, 46.5]
}
```

### Benchmark Comparison API

#### Get Benchmark Targets
**Method**: `db.get_benchmark_targets()`

**Description**: Retrieves peer and industry benchmark data for comparison.

**Return Type**: `Optional[pd.DataFrame]`

**Response Format**:
```python
# DataFrame with columns:
{
    'metric_name': ['latency', 'throughput', ...],
    'peer_benchmark': [50.0, 95.0, ...],
    'industry_benchmark': [55.0, 90.0, ...]
}
```

## 🤖 LLM Service API

### LLMService Class
**Class**: `LLMService`

**Description**: Interface for AI-powered insights generation with circuit breaker protection and PII scrubbing.

#### Generate Insights
**Method**: `llm.generate_insights(prompt)`

**Description**: Generates AI insights from KPI data with security protections.

**Parameters**:
- `prompt` (str): Input prompt for insight generation

**Return Type**: `Optional[Dict[str, Any]]`

**Response Format**:
```python
{
    "summary": "Analysis summary of KPI performance...",
    "key_insights": [
        "Network latency improved by 15% this quarter",
        "Customer satisfaction remains above industry average"
    ],
    "trends": [
        "Upward trend in customer retention",
        "Stable network performance metrics"
    ],
    "recommended_actions": [
        "Continue monitoring network optimization",
        "Implement customer feedback program"
    ]
}
```

**Usage Example**:
```python
from llm_service import LLMService

llm = LLMService()
insights = llm.generate_insights("Analyze current network performance trends")

if insights:
    print(f"Summary: {insights['summary']}")
    for insight in insights['key_insights']:
        print(f"- {insight}")
```

#### Format Insights for Display
**Method**: `llm.format_insights_for_display(insights)`

**Description**: Formats insights with UI-friendly formatting and sanitization.

**Parameters**:
- `insights` (Dict[str, Any]): Raw insights from generate_insights

**Return Type**: `Dict[str, Any]`

**Response Format**:
```python
{
    "summary": "📊 Formatted summary with emoji indicators...",
    "key_insights": ["💡 Formatted insight 1", "💡 Formatted insight 2"],
    "trends": ["📈 Formatted trend 1", "📈 Formatted trend 2"],
    "recommended_actions": ["✅ Formatted action 1", "✅ Formatted action 2"]
}
```

### Circuit Breaker API

#### Circuit Breaker States
**Enum**: `CircuitBreakerState`

```python
class CircuitBreakerState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, requests blocked
    HALF_OPEN = "half_open" # Testing recovery
```

#### CircuitBreaker Class
**Class**: `CircuitBreaker`

**Initialization**:
```python
circuit_breaker = CircuitBreaker(
    failure_threshold=5,  # Number of failures before opening
    timeout=60           # Seconds before attempting recovery
)
```

**Methods**:
- `can_execute()`: Returns `bool` - whether requests are allowed
- `record_success()`: Records successful operation
- `record_failure()`: Records failed operation

### PII Scrubbing API

#### PIIScrubber Class
**Class**: `PIIScrubber`

**Description**: Removes personally identifiable information from text and data structures.

**Supported PII Types**:
- Email addresses
- Phone numbers (US and international)
- Social Security Numbers
- Credit card numbers
- IP addresses
- MAC addresses
- Names (when enabled)

**Methods**:

#### Scrub Text
**Method**: `scrubber.scrub_text(text)`

**Parameters**:
- `text` (str): Input text containing potential PII

**Return Type**: `str`

**Usage Example**:
```python
from llm_service import PIIScrubber

scrubber = PIIScrubber()
cleaned_text = scrubber.scrub_text("Contact john.doe@company.com at 555-123-4567")
print(cleaned_text)  # "Contact [EMAIL_REDACTED] at [PHONE_REDACTED]"
```

#### Scrub Data Dictionary
**Method**: `scrubber.scrub_data_dict(data)`

**Parameters**:
- `data` (Dict[str, Any]): Dictionary containing potential PII

**Return Type**: `Dict[str, Any]`

**Usage Example**:
```python
data = {
    "user_email": "user@example.com",
    "phone": "555-123-4567",
    "metrics": {"latency": 45.2}
}

cleaned_data = scrubber.scrub_data_dict(data)
# Result: {"user_email": "[EMAIL_REDACTED]", "phone": "[PHONE_REDACTED]", "metrics": {"latency": 45.2}}
```

## 🔗 Enterprise Database Adapters API

### DatabaseAdapter Interface
**Abstract Class**: `DatabaseAdapter`

**Description**: Base interface for enterprise database connectivity.

**Required Methods**:
- `get_connection()`: Get database connection
- `execute_query(query, params)`: Execute parameterized query
- `test_connection()`: Test connection validity

### PostgreSQL Adapter
**Class**: `PostgreSQLAdapter`

**Description**: Production PostgreSQL database adapter with connection pooling.

**Initialization**:
```python
from enterprise_database_adapter import PostgreSQLAdapter, DatabaseCredentials

credentials = DatabaseCredentials(
    host='localhost',
    port=5432,
    database='telecom_dashboard',
    username='telecom_user',
    password='secure_password'
)

adapter = PostgreSQLAdapter(credentials, use_pooling=True)
```

**Methods**:

#### Execute Query
**Method**: `adapter.execute_query(query, params=None)`

**Parameters**:
- `query` (str): SQL query with parameter placeholders
- `params` (tuple, optional): Query parameters

**Return Type**: `pd.DataFrame`

**Usage Example**:
```python
# Safe parameterized query
query = "SELECT * FROM fact_network_metrics WHERE date_id >= %s"
params = ('2025-08-01',)
results = adapter.execute_query(query, params)
```

### Snowflake Adapter
**Class**: `SnowflakeAdapter`

**Description**: Enterprise Snowflake adapter with query tagging for compliance.

**Query Tagging**:
```python
# Execute query with user context for audit trails
results = adapter.execute_query(
    query="SELECT * FROM TELECOM_SCHEMA.NETWORK_METRICS",
    user_context="admin_user"
)

# Generates query tag: telecom_dashboard_20250809_120000_app_v2.2.0_prod_env_user_admin_user_soc2_audit_gdpr_compliant
```

## 📊 Data Models API

### KPI Data Models
**Module**: `src.models.data_models`

#### NetworkMetrics
**Class**: `NetworkMetrics`

```python
@dataclass
class NetworkMetrics:
    latency: float
    throughput: float
    packet_loss: float
    availability: float
    response_time: int
    concurrent_users: int
    timestamp: datetime
```

#### CustomerMetrics
**Class**: `CustomerMetrics`

```python
@dataclass
class CustomerMetrics:
    satisfaction_score: float
    nps_score: int
    churn_rate: float
    avg_handling_time: int
    first_contact_resolution: float
    customer_lifetime_value: float
    timestamp: datetime
```

## 🚨 Error Handling API

### Custom Exceptions
**Module**: `src.exceptions.custom_exceptions`

#### ConfigValidationError
**Exception**: `ConfigValidationError`

```python
class ConfigValidationError(Exception):
    def __init__(self, message: str, missing_vars: List[str] = None, invalid_vars: List[str] = None):
        self.message = message
        self.missing_vars = missing_vars or []
        self.invalid_vars = invalid_vars or []
```

#### DatabaseConnectionError
**Exception**: `DatabaseConnectionError`

```python
class DatabaseConnectionError(Exception):
    def __init__(self, message: str, connection_string: str = None):
        self.message = message
        self.connection_string = connection_string
```

### Error Response Format
**Standard Error Response**:
```python
{
    "error": {
        "type": "ConfigValidationError",
        "message": "Environment validation failed",
        "details": {
            "missing_vars": ["DATABASE_URL", "LLM_API_KEY"],
            "invalid_vars": ["LOG_LEVEL"]
        },
        "timestamp": "2025-08-09T12:00:00Z"
    }
}
```

## 🔧 Utility Functions API

### Performance Decorators
**Module**: `performance_utils`

#### Timing Decorator
**Decorator**: `@timing_decorator(operation_name)`

**Description**: Measures and logs function execution time.

**Usage Example**:
```python
from performance_utils import timing_decorator

@timing_decorator("database_query")
def get_metrics():
    # Function implementation
    pass
```

#### Cache with TTL
**Decorator**: `@cache_with_ttl(ttl_seconds=300)`

**Description**: Caches function results with time-to-live expiration.

**Usage Example**:
```python
from database_connection import cache_with_ttl

@cache_with_ttl(ttl_seconds=600)  # 10-minute cache
def expensive_operation():
    # Expensive computation
    return result
```

### Security Utilities
**Module**: `security_manager`

#### Sanitize Output
**Function**: `sanitize_streamlit_output(text)`

**Description**: Sanitizes text for safe display in Streamlit UI.

**Parameters**:
- `text` (str): Input text to sanitize

**Return Type**: `str`

**Usage Example**:
```python
from security_manager import sanitize_streamlit_output

safe_text = sanitize_streamlit_output(user_input)
st.write(safe_text)
```

## 📈 Performance Monitoring API

### Performance Metrics Collection
**Functions for monitoring API performance**:

```python
# Database query performance
query_time = time.time()
results = db.get_network_metrics()
execution_time = time.time() - query_time

# Cache hit rate monitoring
cache_hits = function.cache_info()['hits']
cache_misses = function.cache_info()['misses']
hit_rate = cache_hits / (cache_hits + cache_misses)

# API response time tracking
response_times = []
for i in range(100):
    start = time.time()
    health_check = requests.get("http://localhost:8501/?health=simple")
    response_times.append(time.time() - start)

avg_response_time = sum(response_times) / len(response_times)
```

## 🔐 Authentication & Authorization API

### Future Enhancement: API Authentication
**Planned Features** (not yet implemented):

```python
# API Key Authentication
@api_key_required
def get_sensitive_metrics():
    pass

# Role-Based Access Control
@require_role("dashboard_admin")
def admin_operations():
    pass

# JWT Token Validation
@jwt_required
def authenticated_endpoint():
    pass
```

## 📚 API Usage Examples

### Complete Integration Example
```python
#!/usr/bin/env python3
"""
Complete API integration example
"""

from config_manager import get_config, EnvironmentValidator
from database_connection import TelecomDatabase
from llm_service import LLMService
import logging

def main():
    # 1. Validate environment
    try:
        EnvironmentValidator.validate_startup_config()
        print("✅ Environment validation passed")
    except Exception as e:
        print(f"❌ Environment validation failed: {e}")
        return

    # 2. Load configuration
    config = get_config()
    print(f"✅ Configuration loaded - AI insights: {config.features.ai_insights}")

    # 3. Initialize database
    db = TelecomDatabase()
    
    # 4. Retrieve metrics
    network_metrics = db.get_network_metrics(days=7)
    if network_metrics:
        print(f"✅ Network metrics retrieved - Latency: {network_metrics['latency']}ms")
    
    # 5. Generate AI insights
    if config.features.ai_insights:
        llm = LLMService()
        insights = llm.generate_insights("Analyze current network performance")
        if insights:
            print(f"✅ AI insights generated: {insights['summary']}")

    # 6. Health check
    print("✅ All API operations completed successfully")

if __name__ == "__main__":
    main()
```

### Monitoring Integration Example
```python
#!/usr/bin/env python3
"""
Monitoring and alerting integration
"""

import requests
import json
import time

def monitor_application():
    """Monitor application health and performance"""
    
    # Health check monitoring
    health_response = requests.get("http://localhost:8501/?health=detailed")
    health_data = health_response.json()
    
    # Check critical metrics
    if health_data['checks']['database']['response_time_ms'] > 1000:
        send_alert("Database response time exceeded threshold")
    
    if health_data['checks']['system_resources']['cpu_percent'] > 80:
        send_alert("High CPU usage detected")
    
    # Feature flag monitoring
    features_response = requests.get("http://localhost:8501/?health=features")
    features_data = features_response.json()
    
    # Ensure security features are enabled
    required_features = ['security_headers', 'rate_limiting', 'sql_injection_protection']
    for feature in required_features:
        if not features_data['feature_flags'].get(feature, False):
            send_alert(f"Critical security feature {feature} is disabled")

def send_alert(message):
    """Send alert to monitoring system"""
    print(f"🚨 ALERT: {message}")
    # Integration with monitoring system (PagerDuty, Slack, etc.)

if __name__ == "__main__":
    monitor_application()
```

---

**This API documentation serves as the definitive reference for integrating with and extending the Telecom KPI Dashboard. It should be updated whenever new APIs are added or existing APIs are modified.**
