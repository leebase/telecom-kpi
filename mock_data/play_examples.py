"""
Mock Play Examples for Playbook Prioritizer Agent

This module provides realistic business initiative examples for each subject area
with proper scoring, categories, and business context.
"""

from models.play_models import Play, PlayCategory, SubjectArea
import random


def generate_network_plays() -> list[Play]:
    """Generate realistic network optimization plays"""
    
    plays = [
        Play(
            title="5G Core Network Performance Optimization",
            description="Implement advanced traffic shaping algorithms and load balancing to improve 5G core network throughput by 25% and reduce latency by 40%",
            category=PlayCategory.PERFORMANCE_OPTIMIZATION,
            subject_area=SubjectArea.NETWORK,
            impact_score=8.5,
            effort_score=6.0,
            roi_score=7.8,
            risk_score=3.2,
            estimated_cost=1250000.0,
            estimated_duration_months=8,
            tags=["5G", "performance", "core-network", "traffic-shaping"]
        ),
        
        Play(
            title="Zero-Trust Network Security Framework",
            description="Deploy comprehensive zero-trust architecture with micro-segmentation, identity verification, and continuous monitoring to eliminate network-based attack vectors",
            category=PlayCategory.SECURITY_ENHANCEMENT,
            subject_area=SubjectArea.NETWORK,
            impact_score=9.2,
            effort_score=8.5,
            roi_score=8.9,
            risk_score=2.1,
            estimated_cost=2100000.0,
            estimated_duration_months=12,
            tags=["security", "zero-trust", "micro-segmentation", "compliance"]
        ),
        
        Play(
            title="Network Infrastructure Modernization",
            description="Upgrade legacy network equipment to SDN-enabled infrastructure, improving operational efficiency and enabling automated network management",
            category=PlayCategory.INFRASTRUCTURE_UPGRADE,
            subject_area=SubjectArea.NETWORK,
            impact_score=7.8,
            effort_score=9.2,
            roi_score=6.5,
            risk_score=4.8,
            estimated_cost=3500000.0,
            estimated_duration_months=18,
            tags=["infrastructure", "SDN", "automation", "modernization"]
        ),
        
        Play(
            title="Network Monitoring & Analytics Platform",
            description="Implement AI-powered network monitoring with predictive analytics to identify and resolve issues before they impact customers",
            category=PlayCategory.OPERATIONAL_EFFICIENCY,
            subject_area=SubjectArea.NETWORK,
            impact_score=6.5,
            effort_score=5.8,
            roi_score=7.2,
            risk_score=3.5,
            estimated_cost=850000.0,
            estimated_duration_months=6,
            tags=["monitoring", "analytics", "AI", "predictive-maintenance"]
        ),
        
        Play(
            title="Network Capacity Planning & Expansion",
            description="Strategic capacity planning and targeted network expansion to handle 3x traffic growth over next 24 months",
            category=PlayCategory.PERFORMANCE_OPTIMIZATION,
            subject_area=SubjectArea.NETWORK,
            impact_score=8.0,
            effort_score=7.5,
            roi_score=8.2,
            risk_score=4.0,
            estimated_cost=2800000.0,
            estimated_duration_months=15,
            tags=["capacity-planning", "expansion", "growth", "scalability"]
        )
    ]
    
    return plays


def generate_customer_plays() -> list[Play]:
    """Generate realistic customer experience plays"""
    
    plays = [
        Play(
            title="Predictive Customer Churn Prevention",
            description="Implement ML-based customer behavior analysis and proactive retention strategies to reduce churn by 35% and increase customer lifetime value",
            category=PlayCategory.CUSTOMER_RETENTION,
            subject_area=SubjectArea.CUSTOMER,
            impact_score=8.8,
            effort_score=7.2,
            roi_score=8.1,
            risk_score=4.0,
            estimated_cost=1650000.0,
            estimated_duration_months=10,
            tags=["churn-prevention", "ML", "retention", "customer-value"]
        ),
        
        Play(
            title="Omnichannel Customer Experience Platform",
            description="Unified customer experience across all touchpoints with seamless integration between web, mobile, and call center channels",
            category=PlayCategory.CUSTOMER_RETENTION,
            subject_area=SubjectArea.CUSTOMER,
            impact_score=7.5,
            effort_score=8.8,
            roi_score=6.8,
            risk_score=5.2,
            estimated_cost=2400000.0,
            estimated_duration_months=14,
            tags=["omnichannel", "customer-experience", "integration", "unified-platform"]
        ),
        
        Play(
            title="Customer Self-Service Portal Enhancement",
            description="Advanced self-service capabilities with AI-powered chatbots, knowledge base, and automated issue resolution to reduce support costs by 40%",
            category=PlayCategory.OPERATIONAL_EFFICIENCY,
            subject_area=SubjectArea.CUSTOMER,
            impact_score=6.8,
            effort_score=5.5,
            roi_score=7.5,
            risk_score=3.8,
            estimated_cost=950000.0,
            estimated_duration_months=7,
            tags=["self-service", "chatbots", "AI", "cost-reduction"]
        ),
        
        Play(
            title="Customer Feedback & Sentiment Analysis",
            description="Real-time customer feedback collection and sentiment analysis to drive product improvements and service enhancements",
            category=PlayCategory.CUSTOMER_RETENTION,
            subject_area=SubjectArea.CUSTOMER,
            impact_score=6.2,
            effort_score=4.8,
            roi_score=6.5,
            risk_score=2.5,
            estimated_cost=650000.0,
            estimated_duration_months=5,
            tags=["feedback", "sentiment-analysis", "product-improvement", "service-enhancement"]
        ),
        
        Play(
            title="Customer Journey Mapping & Optimization",
            description="Comprehensive customer journey analysis and optimization to identify friction points and improve conversion rates by 25%",
            category=PlayCategory.CUSTOMER_RETENTION,
            subject_area=SubjectArea.CUSTOMER,
            impact_score=7.2,
            effort_score=6.8,
            roi_score=7.8,
            risk_score=3.0,
            estimated_cost=1200000.0,
            estimated_duration_months=9,
            tags=["journey-mapping", "optimization", "conversion", "friction-reduction"]
        )
    ]
    
    return plays


def generate_revenue_plays() -> list[Play]:
    """Generate realistic revenue growth plays"""
    
    plays = [
        Play(
            title="Dynamic Pricing & Revenue Optimization",
            description="AI-powered dynamic pricing strategies and revenue optimization algorithms to maximize ARPU and market competitiveness",
            category=PlayCategory.REVENUE_GROWTH,
            subject_area=SubjectArea.REVENUE,
            impact_score=9.0,
            effort_score=7.8,
            roi_score=9.2,
            risk_score=4.5,
            estimated_cost=1850000.0,
            estimated_duration_months=11,
            tags=["dynamic-pricing", "revenue-optimization", "AI", "ARPU"]
        ),
        
        Play(
            title="New Product & Service Launch Platform",
            description="Rapid product development and launch platform enabling 50% faster time-to-market for new services and features",
            category=PlayCategory.REVENUE_GROWTH,
            subject_area=SubjectArea.REVENUE,
            impact_score=8.5,
            effort_score=8.2,
            roi_score=8.0,
            risk_score=5.5,
            estimated_cost=2200000.0,
            estimated_duration_months=16,
            tags=["product-launch", "time-to-market", "innovation", "platform"]
        ),
        
        Play(
            title="B2B Sales & Enterprise Solutions Expansion",
            description="Expand enterprise sales capabilities and develop B2B solutions to capture high-value business customers and increase enterprise revenue by 60%",
            category=PlayCategory.REVENUE_GROWTH,
            subject_area=SubjectArea.REVENUE,
            impact_score=8.8,
            effort_score=9.0,
            roi_score=8.5,
            risk_score=6.2,
            estimated_cost=3200000.0,
            estimated_duration_months=20,
            tags=["B2B", "enterprise", "sales-expansion", "high-value-customers"]
        ),
        
        Play(
            title="Subscription & Recurring Revenue Optimization",
            description="Optimize subscription models, pricing tiers, and recurring revenue streams to improve customer retention and increase monthly recurring revenue",
            category=PlayCategory.REVENUE_GROWTH,
            subject_area=SubjectArea.REVENUE,
            impact_score=7.5,
            effort_score=6.5,
            roi_score=7.8,
            risk_score=3.8,
            estimated_cost=1100000.0,
            estimated_duration_months=8,
            tags=["subscription", "recurring-revenue", "pricing-tiers", "retention"]
        ),
        
        Play(
            title="Revenue Analytics & Forecasting Platform",
            description="Advanced revenue analytics, forecasting, and predictive modeling to improve revenue planning and identify growth opportunities",
            category=PlayCategory.REVENUE_GROWTH,
            subject_area=SubjectArea.REVENUE,
            impact_score=6.8,
            effort_score=5.2,
            roi_score=7.2,
            risk_score=2.8,
            estimated_cost=780000.0,
            estimated_duration_months=6,
            tags=["analytics", "forecasting", "predictive-modeling", "growth-opportunities"]
        )
    ]
    
    return plays


def generate_usage_plays() -> list[Play]:
    """Generate realistic usage optimization plays"""
    
    plays = [
        Play(
            title="Data Usage Analytics & Optimization",
            description="Comprehensive data usage analytics and optimization strategies to improve network efficiency and reduce operational costs by 30%",
            category=PlayCategory.OPERATIONAL_EFFICIENCY,
            subject_area=SubjectArea.USAGE,
            impact_score=7.8,
            effort_score=6.2,
            roi_score=7.5,
            risk_score=3.5,
            estimated_cost=1350000.0,
            estimated_duration_months=9,
            tags=["data-usage", "analytics", "optimization", "cost-reduction"]
        ),
        
        Play(
            title="Bandwidth Management & Traffic Shaping",
            description="Advanced bandwidth management and traffic shaping to optimize network utilization and improve quality of service for all customers",
            category=PlayCategory.PERFORMANCE_OPTIMIZATION,
            subject_area=SubjectArea.USAGE,
            impact_score=7.2,
            effort_score=7.8,
            roi_score=6.8,
            risk_score=4.2,
            estimated_cost=1650000.0,
            estimated_duration_months=12,
            tags=["bandwidth", "traffic-shaping", "QoS", "network-utilization"]
        ),
        
        Play(
            title="Usage-Based Billing & Monetization",
            description="Implement usage-based billing models and monetization strategies to capture value from high-usage customers and optimize revenue",
            category=PlayCategory.REVENUE_GROWTH,
            subject_area=SubjectArea.USAGE,
            impact_score=8.2,
            effort_score=8.5,
            roi_score=8.8,
            risk_score=4.8,
            estimated_cost=1950000.0,
            estimated_duration_months=13,
            tags=["usage-billing", "monetization", "high-usage", "revenue-optimization"]
        ),
        
        Play(
            title="Predictive Usage Forecasting",
            description="ML-based usage forecasting and capacity planning to anticipate demand spikes and optimize resource allocation",
            category=PlayCategory.OPERATIONAL_EFFICIENCY,
            subject_area=SubjectArea.USAGE,
            impact_score=6.5,
            effort_score=5.8,
            roi_score=6.8,
            risk_score=3.2,
            estimated_cost=850000.0,
            estimated_duration_months=7,
            tags=["forecasting", "ML", "capacity-planning", "resource-allocation"]
        ),
        
        Play(
            title="Usage Optimization Recommendations Engine",
            description="AI-powered recommendations engine to help customers optimize their usage patterns and reduce unnecessary costs",
            category=PlayCategory.CUSTOMER_RETENTION,
            subject_area=SubjectArea.USAGE,
            impact_score=6.8,
            effort_score=6.5,
            roi_score=7.0,
            risk_score=3.8,
            estimated_cost=1100000.0,
            estimated_duration_months=8,
            tags=["recommendations", "AI", "usage-optimization", "cost-reduction"]
        )
    ]
    
    return plays


def generate_operations_plays() -> list[Play]:
    """Generate realistic operations optimization plays"""
    
    plays = [
        Play(
            title="AI-Powered Operations Automation",
            description="Comprehensive automation of operational processes using AI and machine learning to reduce manual work by 60% and improve efficiency",
            category=PlayCategory.OPERATIONAL_EFFICIENCY,
            subject_area=SubjectArea.OPERATIONS,
            impact_score=8.8,
            effort_score=8.8,
            roi_score=8.5,
            risk_score=5.2,
            estimated_cost=2800000.0,
            estimated_duration_months=18,
            tags=["automation", "AI", "ML", "efficiency", "manual-work-reduction"]
        ),
        
        Play(
            title="Predictive Maintenance & Asset Management",
            description="IoT-enabled predictive maintenance and intelligent asset management to reduce downtime by 45% and extend equipment lifespan",
            category=PlayCategory.OPERATIONAL_EFFICIENCY,
            subject_area=SubjectArea.OPERATIONS,
            impact_score=7.5,
            effort_score=7.2,
            roi_score=7.8,
            risk_score=4.0,
            estimated_cost=1850000.0,
            estimated_duration_months=12,
            tags=["predictive-maintenance", "IoT", "asset-management", "downtime-reduction"]
        ),
        
        Play(
            title="Operations Center Modernization",
            description="Modernize operations center with advanced monitoring, analytics, and collaboration tools to improve incident response and decision-making",
            category=PlayCategory.INFRASTRUCTURE_UPGRADE,
            subject_area=SubjectArea.OPERATIONS,
            impact_score=7.8,
            effort_score=8.2,
            roi_score=7.2,
            risk_score=4.5,
            estimated_cost=2200000.0,
            estimated_duration_months=15,
            tags=["operations-center", "modernization", "monitoring", "collaboration"]
        ),
        
        Play(
            title="Compliance & Regulatory Automation",
            description="Automate compliance monitoring, reporting, and regulatory submissions to ensure 100% compliance and reduce audit risks",
            category=PlayCategory.COMPLIANCE_IMPROVEMENT,
            subject_area=SubjectArea.OPERATIONS,
            impact_score=8.2,
            effort_score=6.8,
            roi_score=7.5,
            risk_score=2.8,
            estimated_cost=1450000.0,
            estimated_duration_months=10,
            tags=["compliance", "automation", "regulatory", "audit-risk-reduction"]
        ),
        
        Play(
            title="Operations Performance Analytics",
            description="Comprehensive operations performance analytics and KPI dashboard to drive continuous improvement and operational excellence",
            category=PlayCategory.OPERATIONAL_EFFICIENCY,
            subject_area=SubjectArea.OPERATIONS,
            impact_score=6.8,
            effort_score=5.5,
            roi_score=6.5,
            risk_score=3.0,
            estimated_cost=950000.0,
            estimated_duration_months=7,
            tags=["analytics", "KPI", "dashboard", "continuous-improvement"]
        )
    ]
    
    return plays


def get_all_plays_by_area() -> dict[str, list[Play]]:
    """Get all plays organized by subject area"""
    return {
        SubjectArea.NETWORK.value: generate_network_plays(),
        SubjectArea.CUSTOMER.value: generate_customer_plays(),
        SubjectArea.REVENUE.value: generate_revenue_plays(),
        SubjectArea.USAGE.value: generate_usage_plays(),
        SubjectArea.OPERATIONS.value: generate_operations_plays()
    }


def get_random_plays_by_area(area: str, count: int = 3) -> list[Play]:
    """Get random plays for a specific subject area"""
    all_plays = get_all_plays_by_area()
    area_plays = all_plays.get(area, [])
    
    if len(area_plays) <= count:
        return area_plays
    
    return random.sample(area_plays, count)


def get_total_plays_count() -> int:
    """Get total number of available plays"""
    all_plays = get_all_plays_by_area()
    return sum(len(plays) for plays in all_plays.values())


if __name__ == "__main__":
    # Test the mock data generation
    print("🎯 Mock Play Examples Generated Successfully!")
    print(f"Total plays available: {get_total_plays_count()}")
    
    for area, plays in get_all_plays_by_area().items():
        print(f"\n📊 {area.upper()} Area: {len(plays)} plays")
        for play in plays[:2]:  # Show first 2 plays
            print(f"  • {play.title} (Priority: {play.get_priority_label()})")
