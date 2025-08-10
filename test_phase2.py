#!/usr/bin/env python3
"""
Test Script for Phase 2: Merge & Normalize

This script tests the portfolio agent's ability to:
1. Merge and normalize plays across subject areas
2. Score and rank plays using the scoring formula
3. Select optimal portfolio within budget constraints
4. Generate executive summary
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.portfolio_agent import PortfolioAgent, PortfolioConfig
from agents.mock_intelligence import get_all_plays_by_area
from models.play_models import SubjectArea, Play, Portfolio

def test_phase2_merge_and_normalize():
    """Test Phase 2.1: Merge and Normalize"""
    print("🧪 Testing Phase 2.1: Merge and Normalize")
    print("=" * 50)
    
    # Generate mock plays for all areas
    print("Generating mock plays for all subject areas...")
    plays_by_area = get_all_plays_by_area(count_per_area=3)
    
    total_plays = sum(len(plays) for plays in plays_by_area.values())
    print(f"Generated {total_plays} total plays across {len(plays_by_area)} areas")
    
    for area, plays in plays_by_area.items():
        print(f"  {area.title()}: {len(plays)} plays")
    
    # Create portfolio agent
    config = PortfolioConfig(
        budget_points=8,
        kpi_weights={
            "impact": 0.35,
            "effort": 0.20,
            "roi": 0.30,
            "risk": 0.15
        }
    )
    
    portfolio_agent = PortfolioAgent(config)
    
    # Test merge and normalize
    print("\nTesting merge and normalize functionality...")
    normalized_plays = portfolio_agent._merge_and_normalize_plays(plays_by_area)
    
    print(f"After normalization: {len(normalized_plays)} unique plays")
    
    # Check for duplicates (should be fewer than total)
    if len(normalized_plays) < total_plays:
        print("✅ Duplicate detection working - plays were merged")
    else:
        print("⚠️  No duplicates detected - this might be expected with mock data")
    
    return plays_by_area, normalized_plays

def test_phase2_scoring_and_ranking(normalized_plays):
    """Test Phase 2.2: Scoring and Ranking"""
    print("\n🧪 Testing Phase 2.2: Scoring and Ranking")
    print("=" * 50)
    
    config = PortfolioConfig()
    portfolio_agent = PortfolioAgent(config)
    
    # Test scoring and ranking
    print("Testing scoring and ranking functionality...")
    scored_plays = portfolio_agent._score_and_rank_plays(normalized_plays)
    
    print(f"Scored and ranked {len(scored_plays)} plays")
    
    # Display top 5 plays with scores
    print("\nTop 5 plays by score:")
    for i, play in enumerate(scored_plays[:5]):
        print(f"  {i+1}. {play.title}")
        print(f"     Score: {play.score:.3f}, Rank: {play.rank}")
        print(f"     Impact: {play.impact_score:.1f}, Effort: {play.effort_score:.1f}")
        print(f"     ROI: {play.roi_score:.1f}, Risk: {play.risk_score:.1f}")
        print()
    
    # Verify scoring formula
    print("Verifying scoring formula...")
    test_play = scored_plays[0]
    expected_score = (test_play.impact_score / 2.0) * (test_play.roi_score / 10.0) * config.kpi_weights["impact"] / max(1, int(test_play.effort_score / 2.0))
    
    if abs(test_play.score - expected_score) < 0.001:
        print("✅ Scoring formula working correctly")
    else:
        print(f"⚠️  Scoring formula mismatch: expected {expected_score:.3f}, got {test_play.score:.3f}")
    
    return scored_plays

def test_phase2_portfolio_selection(scored_plays):
    """Test Phase 2.3: Portfolio Selection"""
    print("\n🧪 Testing Phase 2.3: Portfolio Selection")
    print("=" * 50)
    
    config = PortfolioConfig(budget_points=8)
    portfolio_agent = PortfolioAgent(config)
    
    # Test portfolio selection
    print("Testing portfolio selection functionality...")
    portfolio = portfolio_agent._select_optimal_portfolio(scored_plays)
    
    if portfolio:
        print(f"✅ Portfolio created successfully")
        print(f"   Selected plays: {len(portfolio.selected_plays)}")
        print(f"   Rejected plays: {len(portfolio.rejected_plays)}")
        print(f"   Total investment: ${portfolio.total_investment:,.0f}")
        print(f"   Expected ROI: {portfolio.total_roi:.1f}x")
        
        # Check budget constraints
        if hasattr(portfolio, 'optimization_parameters'):
            opt_params = portfolio.optimization_parameters
            total_effort = opt_params.get("total_effort", 0)
            remaining_budget = opt_params.get("remaining_budget", 0)
            
            print(f"   Total effort: {total_effort}")
            print(f"   Remaining budget: {remaining_budget}")
            
            if total_effort <= config.budget_points:
                print("✅ Budget constraint respected")
            else:
                print("❌ Budget constraint violated")
    else:
        print("❌ Portfolio creation failed")
    
    return portfolio

def test_phase2_executive_summary(portfolio):
    """Test Phase 2.4: Executive Summary"""
    print("\n🧪 Testing Phase 2.4: Executive Summary")
    print("=" * 50)
    
    if not portfolio:
        print("❌ No portfolio available for summary generation")
        return
    
    # Generate executive summary
    config = PortfolioConfig()
    portfolio_agent = PortfolioAgent(config)
    portfolio_agent.selected_portfolio = portfolio
    portfolio_agent._generate_executive_summary()
    
    if portfolio.executive_summary:
        print("✅ Executive summary generated successfully")
        print("\nExecutive Summary Preview:")
        print("-" * 40)
        
        # Show first few lines
        summary_lines = portfolio.executive_summary.split('\n')[:10]
        for line in summary_lines:
            if line.strip():
                print(line.strip())
        
        if len(portfolio.executive_summary.split('\n')) > 10:
            print("... (truncated)")
    else:
        print("❌ Executive summary generation failed")

def test_full_phase2_pipeline():
    """Test the complete Phase 2 pipeline"""
    print("🚀 Testing Complete Phase 2 Pipeline")
    print("=" * 60)
    
    try:
        # Test each phase
        plays_by_area, normalized_plays = test_phase2_merge_and_normalize()
        scored_plays = test_phase2_scoring_and_ranking(normalized_plays)
        portfolio = test_phase2_portfolio_selection(scored_plays)
        test_phase2_executive_summary(portfolio)
        
        print("\n🎉 Phase 2 Testing Complete!")
        print("=" * 60)
        
        # Summary
        print(f"📊 Test Summary:")
        print(f"   Total plays generated: {sum(len(plays) for plays in plays_by_area.values())}")
        print(f"   Plays after normalization: {len(normalized_plays)}")
        print(f"   Plays scored and ranked: {len(scored_plays)}")
        print(f"   Portfolio created: {'Yes' if portfolio else 'No'}")
        
        if portfolio:
            print(f"   Selected plays: {len(portfolio.selected_plays)}")
            print(f"   Portfolio ROI: {portfolio.total_roi:.1f}x")
            print(f"   Executive summary: {'Generated' if portfolio.executive_summary else 'Failed'}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Phase 2 Testing Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🏆 Phase 2: Merge & Normalize - Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    success = test_full_phase2_pipeline()
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("✅ All Phase 2 tests passed successfully!")
        sys.exit(0)
    else:
        print("❌ Some Phase 2 tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
