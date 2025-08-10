"""
Portfolio Agent - Phase 2 Implementation

This module implements the core portfolio optimization logic including:
- Play deduplication and normalization across subject areas
- Scoring and ranking algorithms
- Portfolio selection within budget constraints
- Executive summary generation
"""

import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from models.play_models import Play, Portfolio, SubjectArea, PlayCategory


@dataclass
class PortfolioConfig:
    """Configuration for portfolio optimization"""
    budget_points: int = 8
    kpi_weights: Dict[str, float] = None
    title_aliases: Dict[str, str] = None
    min_confidence_threshold: float = 0.6
    max_effort_threshold: float = 8.0
    enable_dependency_checking: bool = True
    
    def __post_init__(self):
        """Set default values if not provided"""
        if self.kpi_weights is None:
            self.kpi_weights = {
                "impact": 0.35,
                "effort": 0.20,
                "roi": 0.30,
                "risk": 0.15
            }
        
        if self.title_aliases is None:
            self.title_aliases = {
                "network optimization": "network performance optimization",
                "customer retention": "customer churn reduction",
                "revenue growth": "revenue enhancement",
                "operational efficiency": "operations optimization",
                "5g deployment": "5g network rollout",
                "cybersecurity": "security enhancement",
                "data analytics": "analytics implementation"
            }


class PortfolioAgent:
    """Advanced portfolio optimization agent with deduplication and scoring"""
    
    def __init__(self, config: PortfolioConfig = None):
        """Initialize the portfolio agent"""
        self.config = config or PortfolioConfig()
        self.normalized_plays: List[Play] = []
        self.scored_plays: List[Play] = []
        self.selected_portfolio: Optional[Portfolio] = None
        self.execution_log: List[str] = []
        
    def process_plays(self, plays_by_area: Dict[str, List[Play]]) -> Portfolio:
        """Main processing pipeline for plays"""
        self._log("Starting portfolio optimization process")
        
        # Step 1: Merge and normalize plays
        self._log("Phase 2.1: Merging and normalizing plays across areas")
        self.normalized_plays = self._merge_and_normalize_plays(plays_by_area)
        self._log(f"Normalized {len(self.normalized_plays)} unique plays from {sum(len(plays) for plays in plays_by_area.values())} total plays")
        
        # Step 2: Score and rank plays
        self._log("Phase 2.2: Scoring and ranking plays")
        self.scored_plays = self._score_and_rank_plays(self.normalized_plays)
        self._log(f"Scored and ranked {len(self.scored_plays)} plays")
        
        # Step 3: Select optimal portfolio
        self._log("Phase 2.3: Selecting optimal portfolio within budget")
        self.selected_portfolio = self._select_optimal_portfolio(self.scored_plays)
        self._log(f"Selected portfolio with {len(self.selected_portfolio.selected_plays)} plays")
        
        # Step 4: Generate executive summary
        self._log("Phase 2.4: Generating executive summary")
        self._generate_executive_summary()
        
        self._log("Portfolio optimization completed successfully")
        return self.selected_portfolio
    
    def _merge_and_normalize_plays(self, plays_by_area: Dict[str, List[Play]]) -> List[Play]:
        """Merge and normalize plays across subject areas with deduplication"""
        all_plays = []
        
        # Collect all plays with area information
        for area, plays in plays_by_area.items():
            for play in plays:
                # Create a copy with normalized data
                normalized_play = self._normalize_play(play, area)
                all_plays.append(normalized_play)
        
        # Group plays by normalized title
        title_groups = {}
        for play in all_plays:
            normalized_title = self._normalize_title(play.title)
            
            if normalized_title not in title_groups:
                title_groups[normalized_title] = []
            title_groups[normalized_title].append(play)
        
        # Merge plays with same normalized title
        merged_plays = []
        for title, plays in title_groups.items():
            if len(plays) == 1:
                # Single play, no merging needed
                merged_plays.append(plays[0])
            else:
                # Multiple plays, merge them
                merged_play = self._merge_duplicate_plays(plays, title)
                merged_plays.append(merged_play)
        
        return merged_plays
    
    def _normalize_play(self, play: Play, area: str) -> Play:
        """Normalize individual play data"""
        # Create a copy to avoid modifying original
        normalized = Play(
            id=play.id,
            title=play.title,
            description=play.description,
            category=play.category,
            subject_area=SubjectArea(area),
            impact_score=play.impact_score,
            effort_score=play.effort_score,
            roi_score=play.roi_score,
            risk_score=play.risk_score,
            estimated_cost=play.estimated_cost,
            estimated_duration_months=play.estimated_duration_months,
            priority_level=play.priority_level,
            tags=play.tags.copy() if play.tags else []
        )
        
        # Add area tag if not present
        if area not in normalized.tags:
            normalized.tags.append(area)
        
        return normalized
    
    def _normalize_title(self, title: str) -> str:
        """Normalize play title for deduplication"""
        # Convert to lowercase
        normalized = title.lower().strip()
        
        # Apply title aliases
        for alias, canonical in self.config.title_aliases.items():
            if alias in normalized:
                normalized = normalized.replace(alias, canonical)
        
        # Remove common words that don't affect meaning
        common_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
        words = normalized.split()
        filtered_words = [word for word in words if word not in common_words]
        
        return ' '.join(filtered_words)
    
    def _merge_duplicate_plays(self, plays: List[Play], normalized_title: str) -> Play:
        """Merge multiple plays with the same normalized title"""
        if not plays:
            return None
        
        if len(plays) == 1:
            return plays[0]
        
        # Use the first play as base
        base_play = plays[0]
        
        # Merge scores (weighted average by area importance)
        total_weight = 0
        weighted_impact = 0
        weighted_effort = 0
        weighted_roi = 0
        weighted_risk = 0
        weighted_cost = 0
        weighted_duration = 0
        
        area_weights = {
            SubjectArea.NETWORK: 1.2,    # Network is critical
            SubjectArea.CUSTOMER: 1.1,   # Customer is important
            SubjectArea.REVENUE: 1.0,    # Revenue is baseline
            SubjectArea.USAGE: 0.9,      # Usage is secondary
            SubjectArea.OPERATIONS: 0.8   # Operations is supporting
        }
        
        for play in plays:
            weight = area_weights.get(play.subject_area, 1.0)
            total_weight += weight
            
            weighted_impact += play.impact_score * weight
            weighted_effort += play.effort_score * weight
            weighted_roi += play.roi_score * weight
            weighted_risk += play.risk_score * weight
            weighted_cost += play.estimated_cost * weight
            weighted_duration += play.estimated_duration_months * weight
        
        # Create merged play
        merged_play = Play(
            id=f"merged_{base_play.id}",
            title=base_play.title,  # Use original title
            description=self._merge_descriptions(plays),
            category=base_play.category,
            subject_area=base_play.subject_area,  # Use primary area
            impact_score=weighted_impact / total_weight,
            effort_score=weighted_effort / total_weight,
            roi_score=weighted_roi / total_weight,
            risk_score=weighted_risk / total_weight,
            estimated_cost=weighted_cost / total_weight,
            estimated_duration_months=int(weighted_duration / total_weight),
            tags=list(set([tag for play in plays for tag in play.tags]))
        )
        
        return merged_play
    
    def _merge_descriptions(self, plays: List[Play]) -> str:
        """Merge descriptions from multiple plays"""
        if len(plays) == 1:
            return plays[0].description
        
        # Combine descriptions with area context
        descriptions = []
        for play in plays:
            area_context = f"[{play.subject_area.value.title()}] "
            descriptions.append(area_context + play.description)
        
        return " | ".join(descriptions)
    
    def _score_and_rank_plays(self, plays: List[Play]) -> List[Play]:
        """Score and rank plays using the scoring formula from requirements"""
        scored_plays = []
        
        for play in plays:
            # Calculate score using the formula from requirements:
            # score = (impact_score / 5) * confidence * kpi_weight / effort_points
            
            # Convert scores to 0-5 scale for impact
            impact_normalized = play.impact_score / 2.0  # Convert from 0-10 to 0-5
            
            # Use ROI as confidence proxy (higher ROI = higher confidence)
            confidence = min(1.0, play.roi_score / 10.0)
            
            # Calculate effort points (1-5 scale)
            effort_points = max(1, int(play.effort_score / 2.0))
            
            # Calculate weighted score
            score = (impact_normalized * confidence * self.config.kpi_weights["impact"]) / effort_points
            
            # Add score to play
            play.score = score
            scored_plays.append(play)
        
        # Sort by score (descending), then by KPI weight, then by effort, then alphabetically
        scored_plays.sort(
            key=lambda p: (
                -p.score,  # Higher score first
                -self.config.kpi_weights["impact"],  # Higher impact weight first
                p.effort_score,  # Lower effort first
                p.title.lower()  # Alphabetical
            )
        )
        
        # Add rank numbers
        for i, play in enumerate(scored_plays):
            play.rank = i + 1
        
        return scored_plays
    
    def _select_optimal_portfolio(self, scored_plays: List[Play]) -> Portfolio:
        """Select optimal portfolio within budget constraints"""
        selected_plays = []
        remaining_budget = self.config.budget_points
        total_effort = 0
        
        # Filter plays by confidence and effort thresholds
        eligible_plays = [
            play for play in scored_plays
            if (play.roi_score / 10.0) >= self.config.min_confidence_threshold
            and play.effort_score <= self.config.max_effort_threshold
        ]
        
        # Greedy selection: pick highest scoring plays until budget exhausted
        for play in eligible_plays:
            effort_cost = max(1, int(play.effort_score / 2.0))  # Convert to effort points
            
            if effort_cost <= remaining_budget:
                selected_plays.append(play)
                remaining_budget -= effort_cost
                total_effort += effort_cost
                
                if remaining_budget <= 0:
                    break
        
        # Create portfolio
        portfolio = Portfolio(
            name="AI-Optimized Portfolio",
            description=f"Portfolio optimized within {self.config.budget_points} effort points",
            selected_plays=selected_plays,
            rejected_plays=[p for p in scored_plays if p not in selected_plays]
        )
        
        # Add portfolio metadata
        portfolio.optimization_parameters = {
            "budget_points": self.config.budget_points,
            "remaining_budget": remaining_budget,
            "total_effort": total_effort,
            "selection_algorithm": "greedy_optimization",
            "confidence_threshold": self.config.min_confidence_threshold,
            "effort_threshold": self.config.max_effort_threshold
        }
        
        return portfolio
    
    def _generate_executive_summary(self):
        """Generate executive summary for the selected portfolio"""
        if not self.selected_portfolio:
            return
        
        portfolio = self.selected_portfolio
        selected_plays = portfolio.selected_plays
        
        if not selected_plays:
            return
        
        # Calculate summary metrics
        total_plays = len(selected_plays)
        high_priority = len([p for p in selected_plays if p.priority_level <= 2])
        low_risk = len([p for p in selected_plays if p.risk_score <= 4])
        
        # Calculate expected effects (simplified)
        expected_effects = {
            "Total_Investment": sum(p.estimated_cost for p in selected_plays),
            "Expected_ROI": sum(p.roi_score for p in selected_plays) / len(selected_plays),
            "Risk_Level": sum(p.risk_score for p in selected_plays) / len(selected_plays)
        }
        
        # Generate summary text
        summary = f"""
        **Executive Summary**
        
        Our AI-powered portfolio optimization has selected {total_plays} strategic initiatives 
        within your {self.config.budget_points}-point budget constraint.
        
        **Portfolio Highlights:**
        - {high_priority} high-priority initiatives
        - {low_risk} low-risk initiatives  
        - Total investment: ${expected_effects['Total_Investment']:,.0f}
        - Expected ROI: {expected_effects['Expected_ROI']:.1f}x
        - Average risk level: {expected_effects['Risk_Level']:.1f}/10
        
        **Top Recommendations:**
        """
        
        # Add top 3 plays
        for i, play in enumerate(selected_plays[:3]):
            summary += f"\n{i+1}. **{play.title}** - {play.subject_area.value.title()} area"
            summary += f"\n   Impact: {play.impact_score:.1f}/10, Effort: {play.effort_score:.1f}/10"
            summary += f"\n   ROI: {play.roi_score:.1f}/10, Risk: {play.risk_score:.1f}/10"
        
        summary += f"""
        
        **Implementation Strategy:**
        Focus on high-impact, low-effort initiatives first. Monitor ROI metrics monthly 
        and adjust portfolio allocation based on performance. Consider expanding successful 
        initiatives to other business areas.
        """
        
        # Store summary in portfolio
        portfolio.executive_summary = summary.strip()
    
    def _log(self, message: str):
        """Log execution messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.execution_log.append(log_entry)
        print(log_entry)  # Also print to console
    
    def get_execution_log(self) -> List[str]:
        """Get the execution log"""
        return self.execution_log.copy()
    
    def get_portfolio_metrics(self) -> Dict[str, Any]:
        """Get portfolio performance metrics"""
        if not self.selected_portfolio:
            return {}
        
        portfolio = self.selected_portfolio
        
        return {
            "total_plays": len(portfolio.selected_plays),
            "total_investment": portfolio.total_investment,
            "average_roi": portfolio.total_roi,
            "average_priority": portfolio.average_priority,
            "risk_distribution": portfolio.risk_distribution,
            "budget_utilization": portfolio.optimization_parameters.get("total_effort", 0) / self.config.budget_points,
            "execution_log": self.execution_log
        }


def create_portfolio_agent(config: PortfolioConfig = None) -> PortfolioAgent:
    """Factory function to create a portfolio agent"""
    return PortfolioAgent(config)


def optimize_portfolio(plays_by_area: Dict[str, List[Play]], config: PortfolioConfig = None) -> Portfolio:
    """Convenience function to optimize portfolio in one call"""
    agent = PortfolioAgent(config)
    return agent.process_plays(plays_by_area)
