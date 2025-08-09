"""
Performance Optimization Utilities

This module provides optimized utilities for DataFrame operations, data processing,
and performance monitoring specifically for the Telecom Dashboard.
"""

import pandas as pd
import numpy as np
import time
import functools
from typing import Callable, Any, Dict, List, Optional, Union
from logging_config import get_logger, log_performance

logger = get_logger('performance')

def timing_decorator(operation_name: str = None):
    """
    Decorator to measure and log execution time of functions
    
    Args:
        operation_name: Custom name for the operation
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                duration = end_time - start_time
                
                op_name = operation_name or f"{func.__module__}.{func.__name__}"
                log_performance(op_name, duration)
                
                return result
            except Exception as e:
                end_time = time.perf_counter()
                duration = end_time - start_time
                op_name = operation_name or f"{func.__module__}.{func.__name__}"
                logger.error(f"{op_name} failed after {duration:.3f}s: {e}")
                raise
        return wrapper
    return decorator

class DataFrameOptimizer:
    """Optimized DataFrame operations for better performance"""
    
    @staticmethod
    @timing_decorator("dataframe_memory_optimization")
    def optimize_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
        """
        Optimize DataFrame memory usage by downcasting numeric types
        
        Args:
            df: Input DataFrame
            
        Returns:
            Memory-optimized DataFrame
        """
        original_memory = df.memory_usage(deep=True).sum()
        
        # Optimize numeric columns
        for col in df.select_dtypes(include=['int64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')
        
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        # Optimize object columns (potential strings)
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:  # Many repeated values
                df[col] = df[col].astype('category')
        
        new_memory = df.memory_usage(deep=True).sum()
        reduction = (1 - new_memory / original_memory) * 100
        
        logger.info(f"Memory optimization: {original_memory:,} → {new_memory:,} bytes "
                   f"({reduction:.1f}% reduction)")
        
        return df
    
    @staticmethod
    @timing_decorator("dataframe_aggregation")
    def efficient_groupby_agg(df: pd.DataFrame, 
                             group_cols: List[str], 
                             agg_dict: Dict[str, Union[str, List[str]]]) -> pd.DataFrame:
        """
        Perform efficient groupby aggregation with optimization
        
        Args:
            df: Input DataFrame
            group_cols: Columns to group by
            agg_dict: Aggregation dictionary
            
        Returns:
            Aggregated DataFrame
        """
        # Use categorical data types for grouping columns if beneficial
        optimized_df = df.copy()
        for col in group_cols:
            if col in optimized_df.columns and optimized_df[col].dtype == 'object':
                unique_ratio = optimized_df[col].nunique() / len(optimized_df)
                if unique_ratio < 0.1:  # Low cardinality
                    optimized_df[col] = optimized_df[col].astype('category')
        
        return optimized_df.groupby(group_cols, observed=True).agg(agg_dict)
    
    @staticmethod
    @timing_decorator("dataframe_filtering")
    def efficient_filter(df: pd.DataFrame, conditions: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply multiple filters efficiently using query when possible
        
        Args:
            df: Input DataFrame
            conditions: Dictionary of column: value conditions
            
        Returns:
            Filtered DataFrame
        """
        if not conditions:
            return df
        
        # Build query string for simple conditions
        query_parts = []
        complex_conditions = {}
        
        for col, value in conditions.items():
            if isinstance(value, (int, float, str)):
                if isinstance(value, str):
                    query_parts.append(f"{col} == '{value}'")
                else:
                    query_parts.append(f"{col} == {value}")
            else:
                complex_conditions[col] = value
        
        # Apply query-based filtering
        result_df = df
        if query_parts:
            query_string = " & ".join(query_parts)
            result_df = result_df.query(query_string)
        
        # Apply complex conditions manually
        for col, value in complex_conditions.items():
            if isinstance(value, (list, tuple)):
                result_df = result_df[result_df[col].isin(value)]
            elif callable(value):
                result_df = result_df[result_df[col].apply(value)]
            else:
                result_df = result_df[result_df[col] == value]
        
        return result_df
    
    @staticmethod
    @timing_decorator("dataframe_merge")
    def efficient_merge(left: pd.DataFrame, 
                       right: pd.DataFrame, 
                       on: Union[str, List[str]],
                       how: str = 'inner') -> pd.DataFrame:
        """
        Perform efficient DataFrame merge with optimizations
        
        Args:
            left: Left DataFrame
            right: Right DataFrame
            on: Column(s) to merge on
            how: Type of merge
            
        Returns:
            Merged DataFrame
        """
        # Optimize merge columns if they're strings
        merge_cols = [on] if isinstance(on, str) else on
        
        left_opt = left.copy()
        right_opt = right.copy()
        
        for col in merge_cols:
            if col in left_opt.columns and left_opt[col].dtype == 'object':
                left_opt[col] = left_opt[col].astype('category')
            if col in right_opt.columns and right_opt[col].dtype == 'object':
                right_opt[col] = right_opt[col].astype('category')
        
        return pd.merge(left_opt, right_opt, on=on, how=how)

class MetricsCalculator:
    """Optimized calculations for KPI metrics"""
    
    @staticmethod
    @timing_decorator("percentage_change_calculation")
    def calculate_percentage_change(current: float, previous: float) -> str:
        """
        Calculate percentage change with proper formatting
        
        Args:
            current: Current value
            previous: Previous value
            
        Returns:
            Formatted percentage change string
        """
        if previous == 0:
            return "+∞%" if current > 0 else "0.0%"
        
        change = ((current - previous) / previous) * 100
        sign = "+" if change >= 0 else ""
        return f"{sign}{change:.1f}%"
    
    @staticmethod
    @timing_decorator("trend_analysis")
    def analyze_trend(values: List[float], periods: int = 3) -> Dict[str, Any]:
        """
        Analyze trend in a series of values
        
        Args:
            values: List of numeric values
            periods: Number of periods to consider for trend
            
        Returns:
            Dictionary with trend analysis
        """
        if len(values) < 2:
            return {"trend": "insufficient_data", "strength": 0, "direction": "unknown"}
        
        # Calculate recent trend
        recent_values = values[-periods:] if len(values) >= periods else values
        
        # Simple linear trend calculation
        x = np.arange(len(recent_values))
        slope = np.polyfit(x, recent_values, 1)[0]
        
        # Determine trend direction and strength
        avg_value = np.mean(recent_values)
        relative_slope = abs(slope) / avg_value if avg_value != 0 else 0
        
        if relative_slope < 0.01:
            trend = "stable"
            strength = 0
        elif slope > 0:
            trend = "increasing"
            strength = min(relative_slope * 100, 100)
        else:
            trend = "decreasing"
            strength = min(relative_slope * 100, 100)
        
        direction = "up" if slope > 0 else "down" if slope < 0 else "stable"
        
        return {
            "trend": trend,
            "direction": direction,
            "strength": round(strength, 2),
            "slope": slope
        }
    
    @staticmethod
    @timing_decorator("statistical_summary")
    def calculate_statistical_summary(values: Union[List[float], pd.Series]) -> Dict[str, float]:
        """
        Calculate comprehensive statistical summary
        
        Args:
            values: Numeric values
            
        Returns:
            Dictionary with statistical measures
        """
        if isinstance(values, list):
            values = pd.Series(values)
        
        return {
            "mean": values.mean(),
            "median": values.median(),
            "std": values.std(),
            "min": values.min(),
            "max": values.max(),
            "q25": values.quantile(0.25),
            "q75": values.quantile(0.75),
            "count": len(values),
            "null_count": values.isnull().sum()
        }

class ChartDataOptimizer:
    """Optimizations specific to chart data preparation"""
    
    @staticmethod
    @timing_decorator("chart_data_sampling")
    def sample_for_visualization(df: pd.DataFrame, 
                                max_points: int = 1000,
                                time_col: str = None) -> pd.DataFrame:
        """
        Sample DataFrame for visualization without losing important patterns
        
        Args:
            df: Input DataFrame
            max_points: Maximum number of points to keep
            time_col: Time column for time-series sampling
            
        Returns:
            Sampled DataFrame
        """
        if len(df) <= max_points:
            return df
        
        if time_col and time_col in df.columns:
            # Time-based sampling - keep evenly spaced points
            df_sorted = df.sort_values(time_col)
            step = len(df_sorted) // max_points
            return df_sorted.iloc[::step].reset_index(drop=True)
        else:
            # Random sampling
            return df.sample(n=max_points, random_state=42).reset_index(drop=True)
    
    @staticmethod
    @timing_decorator("chart_data_aggregation")
    def aggregate_for_chart(df: pd.DataFrame,
                           x_col: str,
                           y_col: str,
                           agg_func: str = 'mean',
                           bins: Optional[int] = None) -> pd.DataFrame:
        """
        Aggregate data for chart display
        
        Args:
            df: Input DataFrame
            x_col: X-axis column
            y_col: Y-axis column
            agg_func: Aggregation function
            bins: Number of bins for continuous x values
            
        Returns:
            Aggregated DataFrame
        """
        if bins and df[x_col].dtype in ['int64', 'float64']:
            # Bin continuous data
            df['x_binned'] = pd.cut(df[x_col], bins=bins)
            return df.groupby('x_binned')[y_col].agg(agg_func).reset_index()
        else:
            # Group by discrete values
            return df.groupby(x_col)[y_col].agg(agg_func).reset_index()

# Global instances
df_optimizer = DataFrameOptimizer()
metrics_calculator = MetricsCalculator()
chart_optimizer = ChartDataOptimizer()

# Convenience functions
def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame for memory and performance"""
    return df_optimizer.optimize_memory_usage(df)

def calculate_kpi_change(current: float, previous: float) -> str:
    """Calculate and format KPI percentage change"""
    return metrics_calculator.calculate_percentage_change(current, previous)

def prepare_chart_data(df: pd.DataFrame, max_points: int = 1000) -> pd.DataFrame:
    """Prepare DataFrame for chart visualization"""
    return chart_optimizer.sample_for_visualization(df, max_points)

def efficient_groupby(df: pd.DataFrame, 
                     group_cols: List[str], 
                     agg_dict: Dict[str, Union[str, List[str]]]) -> pd.DataFrame:
    """Perform efficient groupby operation"""
    return df_optimizer.efficient_groupby_agg(df, group_cols, agg_dict)
