==============
API Reference
==============

This section provides comprehensive API documentation for all modules and components 
in the Telecom KPI Dashboard.

Core Modules
============

Database Connection
-------------------

.. automodule:: database_connection
   :members:
   :undoc-members:
   :show-inheritance:

The database connection module provides secure and efficient access to the SQLite database
containing all KPI metrics and dimensional data.

**Key Features:**

* Connection pooling and caching
* Query result caching with LRU eviction
* Security validation and SQL injection protection
* Performance monitoring and logging
* Foreign key constraint enforcement

**Example Usage:**

.. code-block:: python

   from database_connection import TelecomDatabase
   
   # Initialize database connection
   db = TelecomDatabase("data/telecom_db.sqlite")
   
   # Get network metrics for the last 30 days
   metrics = db.get_network_metrics(days=30)
   
   # Get customer trend data
   trends = db.get_customer_trend_data(days=90)

Configuration Management
------------------------

.. automodule:: config_manager
   :members:
   :undoc-members:
   :show-inheritance:

Centralized configuration management using Pydantic models for type safety and validation.

**Configuration Sections:**

* **Database**: Connection settings, cache configuration
* **UI**: Theme settings, page configuration
* **Security**: Rate limiting, validation settings  
* **Performance**: Caching, optimization settings
* **AI**: LLM model configuration, API settings

**Example Usage:**

.. code-block:: python

   from config_manager import get_config, get_database_config
   
   # Get complete application configuration
   config = get_config()
   
   # Get specific configuration section
   db_config = get_database_config()
   
   # Access configuration values
   db_path = db_config.path
   cache_size = db_config.cache_size

LLM Service
-----------

.. automodule:: llm_service
   :members:
   :undoc-members:
   :show-inheritance:

Integration with Large Language Models for AI-powered insights and analysis.

**Features:**

* OpenRouter API integration
* Multiple model support (Gemini 2.5 Flash, Claude, etc.)
* Rate limiting and error handling
* Security validation of prompts
* Structured response parsing

**Example Usage:**

.. code-block:: python

   from llm_service import LLMService
   
   # Initialize LLM service
   llm = LLMService()
   
   # Generate insights from KPI data
   insights = llm.generate_insights(kpi_data, category="network")

Security Components
===================

Security Manager
----------------

.. automodule:: security_manager
   :members:
   :undoc-members:
   :show-inheritance:

Comprehensive security management including input validation, output sanitization, 
rate limiting, and security logging.

**Security Features:**

* SQL injection prevention
* XSS protection through output sanitization
* Rate limiting with configurable thresholds
* Security event logging and monitoring
* File access validation
* Input type-specific validation

Custom Exceptions
-----------------

.. automodule:: src.exceptions.custom_exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Custom exception hierarchy providing detailed error information and recovery mechanisms.

**Exception Categories:**

* **DatabaseError**: Database operation failures
* **SecurityError**: Security validation failures  
* **ConfigurationError**: Configuration issues
* **DataValidationError**: Data validation failures
* **APIError**: External API call failures

Data Models
===========

Pydantic Models
---------------

.. automodule:: src.models.data_models
   :members:
   :undoc-members:
   :show-inheritance:

Pydantic models for data validation, serialization, and API documentation.

**Model Categories:**

* **Configuration Models**: Application and component configuration
* **KPI Models**: Metric definitions and data structures
* **Request/Response Models**: API input/output validation
* **Validation Models**: File upload and data validation

**Example Model Usage:**

.. code-block:: python

   from src.models.data_models import KPIMetric, MetricValue, TrendData
   
   # Create a metric value
   value = MetricValue(value=99.9, unit="%", formatted_value="99.9%")
   
   # Create a KPI metric with trend data
   metric = KPIMetric(
       name="Network Availability",
       category="network",
       metric_type="percentage",
       current_value=value,
       trend=TrendData(direction="up", strength=85.0, slope=0.1, period_days=30)
   )

UI Components
=============

KPI Components
--------------

.. automodule:: kpi_components
   :members:
   :undoc-members:
   :show-inheritance:

Reusable UI components for displaying KPI metrics, charts, and interactive elements.

**Component Types:**

* **Metric Cards**: Display individual KPI values with trends
* **Charts**: Line, bar, area, and distribution charts
* **KPI Expanders**: Detailed metric information panels
* **Metric Grids**: Organized layouts of multiple metrics

Theme Management
----------------

.. automodule:: theme_manager
   :members:
   :undoc-members:
   :show-inheritance:

Dynamic theme switching and corporate branding management.

**Supported Themes:**

* **Verizon**: Red and black corporate branding
* **Cognizant**: Blue and white corporate branding
* **Custom**: Configurable color schemes and logos

Utility Modules
===============

Performance Utils
-----------------

.. automodule:: performance_utils
   :members:
   :undoc-members:
   :show-inheritance:

Performance optimization utilities including timing decorators and DataFrame optimization.

**Optimization Features:**

* Execution timing measurement
* DataFrame memory optimization
* Cache performance monitoring
* Query performance analysis

Logging Configuration
---------------------

.. automodule:: logging_config
   :members:
   :undoc-members:
   :show-inheritance:

Centralized logging configuration with multiple handlers and formatters.

**Logging Features:**

* Console and file logging
* Rotating log files
* Component-specific loggers
* Configurable log levels
* Security event logging

Function Reference
==================

Database Functions
------------------

.. autofunction:: database_connection.TelecomDatabase.get_network_metrics
.. autofunction:: database_connection.TelecomDatabase.get_customer_metrics  
.. autofunction:: database_connection.TelecomDatabase.get_revenue_metrics
.. autofunction:: database_connection.TelecomDatabase.get_usage_metrics
.. autofunction:: database_connection.TelecomDatabase.get_operations_metrics

Configuration Functions
-----------------------

.. autofunction:: config_manager.get_config
.. autofunction:: config_manager.get_database_config
.. autofunction:: config_manager.get_ui_config
.. autofunction:: config_manager.get_security_config

Security Functions  
------------------

.. autofunction:: security_manager.validate_input
.. autofunction:: security_manager.sanitize_output
.. autofunction:: security_manager.rate_limit_check
.. autofunction:: security_manager.log_security_event

UI Component Functions
----------------------

.. autofunction:: kpi_components.render_metric_card
.. autofunction:: kpi_components.render_line_chart
.. autofunction:: kpi_components.render_bar_chart
.. autofunction:: kpi_components.render_area_chart

Constants and Enums
===================

KPI Categories
--------------

.. autodata:: src.models.data_models.KPICategory
   :annotation:

Predefined KPI categories for metric classification.

Trend Directions
----------------

.. autodata:: src.models.data_models.TrendDirection
   :annotation:

Enumeration of possible trend directions (up, down, stable, unknown).

Metric Types
------------

.. autodata:: src.models.data_models.MetricType
   :annotation:

Supported metric data types (percentage, count, currency, time, ratio, bytes).

Error Codes
-----------

.. autodata:: src.exceptions.custom_exceptions.TelecomDashboardError.error_code
   :annotation:

Standard error codes used throughout the application for error categorization.

Type Hints
==========

The codebase extensively uses type hints for better code documentation and IDE support:

.. code-block:: python

   from typing import Optional, List, Dict, Any, Union
   from datetime import datetime
   import pandas as pd
   
   def get_metrics(
       days: int = 30,
       region: Optional[str] = None,
       include_trends: bool = True
   ) -> pd.Series:
       """Get KPI metrics with optional filtering."""
       pass
   
   def process_data(
       data: Dict[str, Any],
       filters: Optional[List[str]] = None
   ) -> Union[Dict[str, Any], None]:
       """Process raw data with optional filters."""  
       pass

For complete type information, refer to the individual module documentation above.


