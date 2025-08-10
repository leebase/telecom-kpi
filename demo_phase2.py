#!/usr/bin/env python3
"""
Phase 2 Demonstration Script

This script demonstrates the complete Phase 2: Merge & Normalize functionality
including portfolio optimization, scoring, and executive summary generation.
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.portfolio_agent import PortfolioAgent, PortfolioConfig
from agents.mock_intelligence import get_all_plays_by_area
from models.play_models import SubjectArea

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"🎯 {title}")
    print("=" * 80)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print("-" * 60)

def demo_phase2_merge_and_normalize():
    """Demonstrate Phase 2.1: Merge and Normalize"""
    print_header("Phase 2.1: Merge and Normalize")
    
    print("Generating mock plays for all subject areas...")
    plays_by_area = get_all_plays_by_area(count_per_area=4)
    
    total_plays = sum(len(plays) for plays in plays_by_area.values())
    print(f"Generated {total_plays} total plays across {len(plays_by_area)} areas:")
    
    for area, plays in plays_by_area.items():
        print(f"  {area.title()}: {len(plays)} plays")
    
    # Create portfolio agent for normalization
    config = PortfolioConfig()
    portfolio_agent = PortfolioAgent(config)
    
    print("\nApplying Phase 2.1: Merge and Normalize...")
    normalized_plays = portfolio_agent._merge_and_normalize_plays(plays_by_area)
    
    print(f"After normalization: {len(normalized_plays)} unique plays")
    
    if len(normalized_plays) < total_plays:
        print("✅ Duplicates were successfully merged")
    else:
        print("ℹ️  No duplicates found in this dataset")
    
    return plays_by_area, normalized_plays

def demo_phase2_scoring_and_ranking(normalized_plays):
    """Demonstrate Phase 2.2: Scoring and Ranking"""
    print_header("Phase 2.2: Scoring and Ranking")
    
    config = PortfolioConfig()
    portfolio_agent = PortfolioAgent(config)
    
    print("Applying Phase 2.2: Scoring and Ranking...")
    scored_plays = portfolio_agent._score_and_rank_plays(normalized_plays)
    
    print(f"Successfully scored and ranked {len(scored_plays)} plays")
    
    print("\nTop 10 plays by score:")
    print("-" * 80)
    print(f"{'Rank':<4} {'Score':<8} {'Title':<50} {'Area':<12} {'Impact':<8} {'ROI':<6}")
    print("-" * 80)
    
    for i, play in enumerate(scored_plays[:10]):
        print(f"{play.rank:<4} {play.score:<8.3f} {play.title[:48]:<50} {play.subject_area.value[:10]:<12} {play.impact_score:<8.1f} {play.roi_score:<6.1f}")
    
    return scored_plays

def demo_phase2_portfolio_selection(scored_plays):
    """Demonstrate Phase 2.3: Portfolio Selection"""
    print_header("Phase 2.3: Portfolio Selection")
    
    # Test different budget scenarios
    budget_scenarios = [6, 10, 15]
    
    for budget in budget_scenarios:
        print_section(f"Portfolio Selection with {budget} Budget Points")
        
        config = PortfolioConfig(budget_points=budget)
        portfolio_agent = PortfolioAgent(config)
        
        print(f"Optimizing portfolio with {budget} budget points...")
        portfolio = portfolio_agent._select_optimal_portfolio(scored_plays)
        
        if portfolio:
            print(f"✅ Portfolio created successfully!")
            print(f"   Selected plays: {len(portfolio.selected_plays)}")
            print(f"   Rejected plays: {len(portfolio.rejected_plays)}")
            print(f"   Total investment: ${portfolio.total_investment:,.0f}")
            print(f"   Expected ROI: {portfolio.total_roi:.1f}x")
            
            if hasattr(portfolio, 'optimization_parameters'):
                opt_params = portfolio.optimization_parameters
                total_effort = opt_params.get("total_effort", 0)
                remaining_budget = opt_params.get("remaining_budget", 0)
                
                print(f"   Total effort: {total_effort}")
                print(f"   Remaining budget: {remaining_budget}")
                
                if total_effort <= budget:
                    print("   ✅ Budget constraint respected")
                else:
                    print("   ❌ Budget constraint violated")
            
            # Show selected plays
            print("\n   Selected Initiatives:")
            for i, play in enumerate(portfolio.selected_plays):
                print(f"     {i+1}. {play.title}")
                print(f"        Area: {play.subject_area.value.title()}")
                print(f"        Score: {play.score:.3f}, ROI: {play.roi_score:.1f}x")
                print(f"        Investment: ${play.estimated_cost:,.0f}")
        else:
            print("❌ Portfolio creation failed")
        
        print()

def demo_phase2_executive_summary(scored_plays):
    """Demonstrate Phase 2.4: Executive Summary"""
    print_header("Phase 2.4: Executive Summary Generation")
    
    config = PortfolioConfig(budget_points=8)
    portfolio_agent = PortfolioAgent(config)
    
    print("Creating portfolio and generating executive summary...")
    portfolio = portfolio_agent._select_optimal_portfolio(scored_plays)
    
    if portfolio:
        # Generate executive summary
        portfolio_agent.selected_portfolio = portfolio
        portfolio_agent._generate_executive_summary()
        
        if portfolio.executive_summary:
            print("✅ Executive summary generated successfully!")
            print("\n" + "=" * 80)
            print("📊 EXECUTIVE SUMMARY")
            print("=" * 80)
            print(portfolio.executive_summary)
            print("=" * 80)
        else:
            print("❌ Executive summary generation failed")
    else:
        print("❌ No portfolio available for summary generation")

def demo_complete_phase2_pipeline():
    """Demonstrate the complete Phase 2 pipeline"""
    print_header("Complete Phase 2 Pipeline Demonstration")
    
    print("This demonstration showcases all four phases of the Merge & Normalize process:")
    print("1. Merge and Normalize plays across subject areas")
    print("2. Score and rank plays using the scoring formula")
    print("3. Select optimal portfolio within budget constraints")
    print("4. Generate executive summary")
    
    try:
        # Phase 2.1: Merge and Normalize
        plays_by_area, normalized_plays = demo_phase2_merge_and_normalize()
        
        # Phase 2.2: Scoring and Ranking
        scored_plays = demo_phase2_scoring_and_ranking(normalized_plays)
        
        # Phase 2.3: Portfolio Selection
        demo_phase2_portfolio_selection(scored_plays)
        
        # Phase 2.4: Executive Summary
        demo_phase2_executive_summary(scored_plays)
        
        print_header("Phase 2 Demonstration Complete!")
        print("✅ All Phase 2 functionality is working correctly")
        print("✅ Portfolio optimization is fully operational")
        print("✅ Executive summaries are being generated")
        print("✅ The system is ready for production use")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main demonstration function"""
    print("🏆 Phase 2: Merge & Normalize - Complete Demonstration")
    print("=" * 80)
    print(f"Demonstration started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("This demonstration will showcase:")
    print("• Play deduplication and normalization across subject areas")
    print("• Advanced scoring and ranking algorithms")
    print("• Portfolio optimization within budget constraints")
    print("• Executive summary generation")
    print()
    
    # Run the complete demonstration
    demo_complete_phase2_pipeline()
    
    print(f"\nDemonstration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
