#!/usr/bin/env python3
"""
Phase 2 Integration Test

This script tests the complete Phase 2 pipeline including:
- Orchestrator integration with portfolio agent
- End-to-end play processing
- Portfolio optimization
- Executive summary generation
"""

import sys
import os
import time
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import AgentOrchestrator
from agents.portfolio_agent import PortfolioAgent, PortfolioConfig
from agents.mock_intelligence import get_all_plays_by_area
from models.play_models import SubjectArea, Play, Portfolio

def test_orchestrator_integration():
    """Test orchestrator integration with portfolio agent"""
    print("🧪 Testing Orchestrator Integration")
    print("=" * 50)
    
    try:
        # Create orchestrator
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrator created successfully")
        
        # Check if portfolio agent is properly integrated
        if hasattr(orchestrator, '_optimize_portfolio'):
            print("✅ Portfolio optimization method found")
        else:
            print("❌ Portfolio optimization method missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Orchestrator integration failed: {e}")
        return False

def test_end_to_end_pipeline():
    """Test the complete end-to-end pipeline"""
    print("\n🧪 Testing End-to-End Pipeline")
    print("=" * 50)
    
    try:
        # Generate mock data
        print("1. Generating mock plays...")
        plays_by_area = get_all_plays_by_area(count_per_area=4)
        total_plays = sum(len(plays) for plays in plays_by_area.values())
        print(f"   Generated {total_plays} plays across {len(plays_by_area)} areas")
        
        # Create portfolio agent
        print("2. Creating portfolio agent...")
        config = PortfolioConfig(
            budget_points=10,
            kpi_weights={
                "impact": 0.35,
                "effort": 0.20,
                "roi": 0.30,
                "risk": 0.15
            }
        )
        portfolio_agent = PortfolioAgent(config)
        print("   Portfolio agent created with budget: 10 points")
        
        # Process plays through the complete pipeline
        print("3. Processing plays through pipeline...")
        portfolio = portfolio_agent.process_plays(plays_by_area)
        
        if portfolio:
            print("✅ Portfolio created successfully")
            print(f"   Selected plays: {len(portfolio.selected_plays)}")
            print(f"   Rejected plays: {len(portfolio.rejected_plays)}")
            print(f"   Total investment: ${portfolio.total_investment:,.0f}")
            print(f"   Expected ROI: {portfolio.total_roi:.1f}x")
            
            # Check portfolio metrics
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
                    return False
        else:
            print("❌ Portfolio creation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-end pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_portfolio_quality():
    """Test the quality of the generated portfolio"""
    print("\n🧪 Testing Portfolio Quality")
    print("=" * 50)
    
    try:
        # Generate plays and create portfolio
        plays_by_area = get_all_plays_by_area(count_per_area=5)
        config = PortfolioConfig(budget_points=8)
        portfolio_agent = PortfolioAgent(config)
        portfolio = portfolio_agent.process_plays(plays_by_area)
        
        if not portfolio:
            print("❌ No portfolio available for quality testing")
            return False
        
        # Test portfolio quality metrics
        print("1. Testing portfolio diversity...")
        selected_areas = set(play.subject_area for play in portfolio.selected_plays)
        print(f"   Areas represented: {len(selected_areas)} out of {len(SubjectArea)}")
        
        if len(selected_areas) >= 2:
            print("✅ Good area diversity")
        else:
            print("⚠️  Limited area diversity")
        
        print("2. Testing risk distribution...")
        risk_scores = [play.risk_score for play in portfolio.selected_plays]
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0
        print(f"   Average risk score: {avg_risk:.1f}")
        
        if avg_risk <= 4.0:
            print("✅ Acceptable risk level")
        else:
            print("⚠️  High risk level")
        
        print("3. Testing ROI distribution...")
        roi_scores = [play.roi_score for play in portfolio.selected_plays]
        avg_roi = sum(roi_scores) / len(roi_scores) if roi_scores else 0
        print(f"   Average ROI score: {avg_roi:.1f}")
        
        if avg_roi >= 7.0:
            print("✅ Good ROI potential")
        else:
            print("⚠️  Low ROI potential")
        
        print("4. Testing effort distribution...")
        effort_scores = [play.effort_score for play in portfolio.selected_plays]
        avg_effort = sum(effort_scores) / len(effort_scores) if effort_scores else 0
        print(f"   Average effort score: {avg_effort:.1f}")
        
        if avg_effort <= 7.0:
            print("✅ Manageable effort level")
        else:
            print("⚠️  High effort level")
        
        return True
        
    except Exception as e:
        print(f"❌ Portfolio quality testing failed: {e}")
        return False

def test_executive_summary_quality():
    """Test the quality of the generated executive summary"""
    print("\n🧪 Testing Executive Summary Quality")
    print("=" * 50)
    
    try:
        # Generate portfolio with summary
        plays_by_area = get_all_plays_by_area(count_per_area=3)
        config = PortfolioConfig(budget_points=6)
        portfolio_agent = PortfolioAgent(config)
        portfolio = portfolio_agent.process_plays(plays_by_area)
        
        if not portfolio or not portfolio.executive_summary:
            print("❌ No executive summary available")
            return False
        
        summary = portfolio.executive_summary
        
        print("1. Testing summary content...")
        print(f"   Summary length: {len(summary)} characters")
        
        if len(summary) > 100:
            print("✅ Adequate summary length")
        else:
            print("⚠️  Summary too short")
        
        print("2. Testing key sections...")
        required_sections = [
            "Executive Summary",
            "Portfolio Highlights",
            "Investment",
            "ROI"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section.lower() in summary.lower():
                print(f"   ✅ {section} section found")
            else:
                print(f"   ❌ {section} section missing")
                missing_sections.append(section)
        
        if not missing_sections:
            print("✅ All required sections present")
        else:
            print(f"⚠️  Missing sections: {', '.join(missing_sections)}")
        
        print("3. Testing summary preview...")
        print("\nSummary Preview:")
        print("-" * 40)
        summary_lines = summary.split('\n')[:8]
        for line in summary_lines:
            if line.strip():
                print(line.strip())
        
        if len(summary.split('\n')) > 8:
            print("... (truncated)")
        
        return len(missing_sections) == 0
        
    except Exception as e:
        print(f"❌ Executive summary quality testing failed: {e}")
        return False

def test_performance():
    """Test the performance of the portfolio optimization"""
    print("\n🧪 Testing Performance")
    print("=" * 50)
    
    try:
        # Test with different data sizes
        test_cases = [
            (3, "Small dataset"),
            (5, "Medium dataset"),
            (8, "Large dataset")
        ]
        
        for count_per_area, description in test_cases:
            print(f"\nTesting {description} ({count_per_area} plays per area)...")
            
            start_time = time.time()
            
            plays_by_area = get_all_plays_by_area(count_per_area=count_per_area)
            config = PortfolioConfig(budget_points=count_per_area * 2)
            portfolio_agent = PortfolioAgent(config)
            portfolio = portfolio_agent.process_plays(plays_by_area)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"   Processing time: {processing_time:.3f} seconds")
            print(f"   Plays processed: {sum(len(plays) for plays in plays_by_area.values())}")
            print(f"   Portfolio created: {'Yes' if portfolio else 'No'}")
            
            if processing_time < 5.0:  # Should complete within 5 seconds
                print("   ✅ Performance acceptable")
            else:
                print("   ⚠️  Performance slow")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance testing failed: {e}")
        return False

def main():
    """Main test function"""
    print("🏆 Phase 2: Integration Testing Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = []
    
    # Run all tests
    test_results.append(("Orchestrator Integration", test_orchestrator_integration()))
    test_results.append(("End-to-End Pipeline", test_end_to_end_pipeline()))
    test_results.append(("Portfolio Quality", test_portfolio_quality()))
    test_results.append(("Executive Summary Quality", test_executive_summary_quality()))
    test_results.append(("Performance", test_performance()))
    
    # Display results
    print("\n📊 Integration Test Results")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Phase 2 integration tests passed!")
        print("✅ Phase 2 is fully functional and ready for production")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed")
        print("❌ Phase 2 needs additional fixes")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
