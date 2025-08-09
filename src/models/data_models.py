"""
Pydantic Data Models for Telecom Dashboard

This module defines Pydantic models for data validation, serialization,
and API documentation throughout the application.
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, Field, validator, root_validator
import re

class KPICategory(str, Enum):
    """Enumeration of KPI categories"""
    NETWORK = "network"
    CUSTOMER = "customer"
    REVENUE = "revenue"
    USAGE = "usage"
    OPERATIONS = "operations"

class TrendDirection(str, Enum):
    """Enumeration of trend directions"""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"
    UNKNOWN = "unknown"

class MetricType(str, Enum):
    """Enumeration of metric types"""
    PERCENTAGE = "percentage"
    COUNT = "count"
    CURRENCY = "currency"
    TIME = "time"
    RATIO = "ratio"
    BYTES = "bytes"

# Base Models
class TimestampedModel(BaseModel):
    """Base model with timestamp fields"""
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

class BaseKPIModel(BaseModel):
    """Base model for all KPI data"""
    name: str = Field(..., description="KPI name")
    category: KPICategory = Field(..., description="KPI category")
    metric_type: MetricType = Field(..., description="Type of metric")
    description: Optional[str] = Field(None, description="KPI description")

# Configuration Models
class DatabaseConfig(BaseModel):
    """Database configuration model"""
    path: str = Field(..., description="Database file path")
    connection_timeout: int = Field(30000, ge=1000, description="Connection timeout in ms")
    enable_foreign_keys: bool = Field(True, description="Enable foreign key constraints")
    cache_size: int = Field(32, ge=1, description="Cache size for queries")
    trend_cache_size: int = Field(16, ge=1, description="Cache size for trend data")

    @validator('path')
    def validate_path(cls, v):
        if not v.endswith('.sqlite') and not v.endswith('.db'):
            raise ValueError('Database path must end with .sqlite or .db')
        return v

class UIConfig(BaseModel):
    """UI configuration model"""
    default_theme: str = Field("verizon", description="Default theme name")
    page_title: str = Field("Telecom KPI Dashboard", description="Page title")
    page_icon: str = Field("📡", description="Page icon")
    layout: str = Field("wide", description="Page layout")
    sidebar_state: str = Field("expanded", description="Sidebar initial state")
    show_debug_info: bool = Field(False, description="Show debug information")

    @validator('layout')
    def validate_layout(cls, v):
        if v not in ['wide', 'centered']:
            raise ValueError('Layout must be either "wide" or "centered"')
        return v

    @validator('sidebar_state')
    def validate_sidebar_state(cls, v):
        if v not in ['expanded', 'collapsed', 'auto']:
            raise ValueError('Sidebar state must be "expanded", "collapsed", or "auto"')
        return v

class SecurityConfig(BaseModel):
    """Security configuration model"""
    enable_rate_limiting: bool = Field(True, description="Enable rate limiting")
    max_requests_per_minute: int = Field(60, ge=1, le=1000, description="Max requests per minute")
    enable_input_validation: bool = Field(True, description="Enable input validation")
    enable_output_sanitization: bool = Field(True, description="Enable output sanitization")
    enable_security_logging: bool = Field(True, description="Enable security logging")
    log_file: str = Field("security.log", description="Security log file")

class AIConfig(BaseModel):
    """AI/LLM configuration model"""
    model: str = Field("google/gemini-2.5-flash", description="LLM model name")
    temperature: float = Field(0.1, ge=0.0, le=2.0, description="LLM temperature")
    max_tokens: int = Field(2000, ge=100, le=10000, description="Maximum tokens")
    api_timeout: int = Field(30, ge=5, le=120, description="API timeout in seconds")
    enable_insights: bool = Field(True, description="Enable AI insights")

# KPI Data Models
class MetricValue(BaseModel):
    """Individual metric value"""
    value: Union[float, int, str] = Field(..., description="Metric value")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    formatted_value: Optional[str] = Field(None, description="Human-readable formatted value")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @validator('value')
    def validate_value(cls, v):
        if isinstance(v, str) and v.strip() == '':
            raise ValueError('String values cannot be empty')
        return v

class TrendData(BaseModel):
    """Trend analysis data"""
    direction: TrendDirection = Field(..., description="Trend direction")
    strength: float = Field(..., ge=0.0, le=100.0, description="Trend strength percentage")
    slope: float = Field(..., description="Trend slope")
    period_days: int = Field(..., ge=1, description="Analysis period in days")

class BenchmarkData(BaseModel):
    """Benchmark comparison data"""
    peer_average: Optional[float] = Field(None, description="Peer average value")
    industry_average: Optional[float] = Field(None, description="Industry average value")
    target_value: Optional[float] = Field(None, description="Target value")
    percentile_rank: Optional[float] = Field(None, ge=0.0, le=100.0, description="Percentile rank")

class KPIMetric(BaseKPIModel):
    """Complete KPI metric with all data"""
    current_value: MetricValue = Field(..., description="Current metric value")
    previous_value: Optional[MetricValue] = Field(None, description="Previous period value")
    trend: Optional[TrendData] = Field(None, description="Trend analysis")
    benchmark: Optional[BenchmarkData] = Field(None, description="Benchmark data")
    delta: Optional[str] = Field(None, description="Change from previous period")
    status: Optional[str] = Field(None, description="Status indicator")

# Network KPI Models
class NetworkMetrics(BaseModel):
    """Network performance metrics"""
    availability: KPIMetric = Field(..., description="Network availability")
    latency: KPIMetric = Field(..., description="Network latency")
    packet_loss: KPIMetric = Field(..., description="Packet loss rate")
    bandwidth_utilization: KPIMetric = Field(..., description="Bandwidth utilization")
    mttr: KPIMetric = Field(..., description="Mean time to repair")
    dropped_call_rate: KPIMetric = Field(..., description="Dropped call rate")

# Customer KPI Models
class CustomerMetrics(BaseModel):
    """Customer experience metrics"""
    satisfaction_score: KPIMetric = Field(..., description="Customer satisfaction")
    churn_rate: KPIMetric = Field(..., description="Customer churn rate")
    nps: KPIMetric = Field(..., description="Net Promoter Score")
    first_contact_resolution: KPIMetric = Field(..., description="First contact resolution")
    average_handling_time: KPIMetric = Field(..., description="Average handling time")
    customer_lifetime_value: KPIMetric = Field(..., description="Customer lifetime value")

# AI Insights Models
class AIInsight(BaseModel):
    """Individual AI insight"""
    text: str = Field(..., min_length=10, description="Insight text")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")
    category: Optional[str] = Field(None, description="Insight category")

class AIRecommendation(BaseModel):
    """AI recommendation"""
    action: str = Field(..., min_length=10, description="Recommended action")
    priority: Optional[str] = Field(None, description="Priority level")
    impact: Optional[str] = Field(None, description="Expected impact")
    timeline: Optional[str] = Field(None, description="Recommended timeline")

class AIInsightsResponse(BaseModel):
    """Complete AI insights response"""
    summary: str = Field(..., min_length=50, description="Executive summary")
    key_insights: List[AIInsight] = Field(..., min_items=1, description="Key insights")
    trends: List[str] = Field(default_factory=list, description="Identified trends")
    recommended_actions: List[AIRecommendation] = Field(default_factory=list, description="Recommendations")
    model_used: Optional[str] = Field(None, description="AI model used")
    generated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    processing_time: Optional[float] = Field(None, ge=0.0, description="Processing time in seconds")

    @validator('key_insights')
    def validate_insights(cls, v):
        if len(v) > 10:
            raise ValueError('Maximum 10 key insights allowed')
        return v

# Database Query Models
class QueryParameters(BaseModel):
    """Database query parameters"""
    days: int = Field(30, ge=1, le=365, description="Number of days to query")
    region: Optional[str] = Field(None, description="Region filter")
    customer_segment: Optional[str] = Field(None, description="Customer segment filter")
    product_category: Optional[str] = Field(None, description="Product category filter")
    start_date: Optional[date] = Field(None, description="Start date filter")
    end_date: Optional[date] = Field(None, description="End date filter")

    @root_validator
    def validate_date_range(cls, values):
        start_date = values.get('start_date')
        end_date = values.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise ValueError('Start date must be before end date')
            
            # Calculate days from date range
            delta = (end_date - start_date).days
            if delta > 365:
                raise ValueError('Date range cannot exceed 365 days')
            values['days'] = delta
        
        return values

# API Request/Response Models
class KPIRequest(BaseModel):
    """Request model for KPI data"""
    category: KPICategory = Field(..., description="KPI category to retrieve")
    parameters: QueryParameters = Field(default_factory=QueryParameters, description="Query parameters")
    include_trends: bool = Field(True, description="Include trend analysis")
    include_benchmarks: bool = Field(True, description="Include benchmark data")

class ErrorResponse(BaseModel):
    """Error response model"""
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = Field(None, description="Request ID for tracking")

# Validation Models
class FileUpload(BaseModel):
    """File upload validation"""
    filename: str = Field(..., description="Uploaded filename")
    content_type: str = Field(..., description="File content type")
    size_bytes: int = Field(..., ge=1, le=10_000_000, description="File size in bytes")
    
    @validator('filename')
    def validate_filename(cls, v):
        # Check for valid filename pattern
        if not re.match(r'^[a-zA-Z0-9_.-]+$', v):
            raise ValueError('Filename contains invalid characters')
        return v
    
    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = ['text/csv', 'application/json', 'application/xlsx']
        if v not in allowed_types:
            raise ValueError(f'Content type must be one of: {allowed_types}')
        return v

# Theme Models
class ThemeConfig(BaseModel):
    """Theme configuration model"""
    name: str = Field(..., description="Theme name")
    primary_color: str = Field(..., description="Primary color")
    secondary_color: str = Field(..., description="Secondary color")
    background_color: str = Field(..., description="Background color")
    text_color: str = Field(..., description="Text color")
    logo_url: Optional[str] = Field(None, description="Logo URL")
    
    @validator('primary_color', 'secondary_color', 'background_color', 'text_color')
    def validate_color(cls, v):
        # Validate hex color format
        if not re.match(r'^#[0-9A-Fa-f]{6}$', v):
            raise ValueError('Color must be in hex format (#RRGGBB)')
        return v

# Export all models
__all__ = [
    'KPICategory', 'TrendDirection', 'MetricType',
    'TimestampedModel', 'BaseKPIModel',
    'DatabaseConfig', 'UIConfig', 'SecurityConfig', 'AIConfig',
    'MetricValue', 'TrendData', 'BenchmarkData', 'KPIMetric',
    'NetworkMetrics', 'CustomerMetrics',
    'AIInsight', 'AIRecommendation', 'AIInsightsResponse',
    'QueryParameters', 'KPIRequest', 'ErrorResponse',
    'FileUpload', 'ThemeConfig'
]

