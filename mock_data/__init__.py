"""
Mock Data Package for Playbook Prioritizer Agent

This package provides realistic mock data for testing and demonstration.
"""

from .play_examples import (
    generate_network_plays,
    generate_customer_plays,
    generate_revenue_plays,
    generate_usage_plays,
    generate_operations_plays,
    get_all_plays_by_area,
    get_random_plays_by_area,
    get_total_plays_count
)

__all__ = [
    "generate_network_plays",
    "generate_customer_plays", 
    "generate_revenue_plays",
    "generate_usage_plays",
    "generate_operations_plays",
    "get_all_plays_by_area",
    "get_random_plays_by_area",
    "get_total_plays_count"
]
