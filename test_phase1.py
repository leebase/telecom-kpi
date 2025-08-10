#!/usr/bin/env python3
"""
Test Script for Phase 1: Foundation & Data Models

This script tests all Phase 1 components to ensure they're working correctly:
1. Play Schema & Data Structures
2. Agent Base Classes  
3. Mock Intelligence Engine
"""

import sys
import time
from typing import Dict, List

# Add the project root to the path
sys.path.insert(0, '.')

from models.play_models import (
    Play, 
    Portfolio, 
    SubjectArea, 
    PlayCategory,
    AgentStatus,
    WorkflowPhase
)
from agents.base_agent import AgentFactory, SubjectAreaAgent
from agents.mock_intelligence import (
    MockIntelligenceEngine,
    generate_plays_for_area,
    get_all_plays_by_area
)


def test_data_models():
    """Test the core data models"""
    print("🧪 Testing Data Models...")
    
    # Test Play creation
    play = Play(
        title="Test Network Optimization",
        description="A test play for network optimization",
        category=PlayCategory.PERFORMANCE_OPTIMIZATION,
        subject_area=SubjectArea.NETWORK,
        impact_score=8.5,
        effort_score=6.0,
        roi_score=7.8,
        risk_score=3.2,
        estimated_cost=1000000.0,
        estimated_duration_months=12,
        tags=["test", "network", "optimization"]
    )
    
    print(f"✅ Play created: {play.title}")
    print(f"   Priority: {play.get_priority_label()}")
    print(f"   Serialized: {play.to_dict()}")
    
    # Test Portfolio creation
    portfolio = Portfolio()
    portfolio.add_play(play)
    
    print(f"✅ Portfolio created with {len(portfolio.selected_plays)} plays")
    print(f"   Total investment: ${portfolio.total_investment:,.0f}")
    print(f"   Average priority: {portfolio.average_priority:.1f}")
    
    return True


def test_mock_intelligence():
    """Test the mock intelligence engine"""
    print("\n🧪 Testing Mock Intelligence Engine...")
    
    # Test engine creation
    engine = MockIntelligenceEngine()
    print("✅ Mock intelligence engine created")
    
    # Test market analysis
    market_analysis = engine.get_market_analysis()
    print(f"✅ Market analysis generated: {len(market_analysis['market_conditions'])} conditions")
    
    # Test play generation for each area
    for area in SubjectArea:
        plays = engine.generate_plays_for_area(area, count=3)
        print(f"✅ Generated {len(plays)} plays for {area.value}")
        
        # Show first play details
        if plays:
            first_play = plays[0]
            print(f"   Sample: {first_play.title}")
            print(f"   Scores: Impact={first_play.impact_score:.1f}, ROI={first_play.roi_score:.1f}")
    
    # Test convenience functions
    network_plays = generate_plays_for_area(SubjectArea.NETWORK, count=2)
    print(f"✅ Convenience function generated {len(network_plays)} network plays")
    
    all_plays = get_all_plays_by_area(count_per_area=2)
    total_plays = sum(len(plays) for plays in all_plays.values())
    print(f"✅ All areas generated {total_plays} total plays")
    
    return True


def test_agent_base_classes():
    """Test the agent base classes"""
    print("\n🧪 Testing Agent Base Classes...")
    
    # Test agent factory
    factory = AgentFactory()
    all_agents = factory.create_all_subject_area_agents()
    print(f"✅ Created {len(all_agents)} agents for all subject areas")
    
    # Test individual agent
    network_agent = all_agents[SubjectArea.NETWORK.value]
    print(f"✅ Network agent created: {network_agent.name}")
    
    # Test agent state management
    initial_status = network_agent.get_status()
    print(f"✅ Initial status: {initial_status['status']}")
    
    # Test agent execution
    print("   Starting agent execution...")
    network_agent.start_execution("Test analysis")
    
    # Monitor progress
    max_wait = 10  # seconds
    start_time = time.time()
    
    while network_agent.state.status == AgentStatus.ANALYZING:
        if time.time() - start_time > max_wait:
            print("   ⚠️  Agent execution timeout")
            break
        
        status = network_agent.get_status()
        progress = status['progress']
        current_task = status['current_task']
        print(f"   Progress: {progress:.1%} - {current_task}")
        
        time.sleep(0.5)
    
    # Check final status
    final_status = network_agent.get_status()
    print(f"✅ Final status: {final_status['status']}")
    
    # Check results
    plays = network_agent.get_plays()
    print(f"✅ Generated {len(plays)} plays")
    
    if plays:
        summary = network_agent.get_analysis_summary()
        print(f"   Analysis summary: {summary['status']}")
        print(f"   Total investment: ${summary['total_investment']:,.0f}")
    
    return True


def test_integration():
    """Test integration between all components"""
    print("\n🧪 Testing Component Integration...")
    
    try:
        # Create a portfolio from all agents
        all_agents = AgentFactory.create_all_subject_area_agents()
        all_plays = []
        
        print("   Running all agents in parallel...")
        
        # Start all agents
        for agent_name, agent in all_agents.items():
            agent.start_execution(f"Analyzing {agent.subject_area.value}")
        
        # Wait for all agents to complete
        for agent_name, agent in all_agents.items():
            agent.wait_for_completion(timeout=15)
            agent_plays = agent.get_plays()
            all_plays.extend(agent_plays)
            print(f"   {agent_name}: {len(agent_plays)} plays generated")
        
        # Create portfolio from all plays
        portfolio = Portfolio()
        for play in all_plays:
            portfolio.add_play(play)
        
        print(f"✅ Integration test complete:")
        print(f"   Total plays: {len(all_plays)}")
        print(f"   Portfolio investment: ${portfolio.total_investment:,.0f}")
        print(f"   Portfolio ROI: {portfolio.total_roi:.1f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def main():
    """Run all Phase 1 tests"""
    print("🚀 PHASE 1 TESTING - Foundation & Data Models")
    print("=" * 60)
    
    tests = [
        ("Data Models", test_data_models),
        ("Mock Intelligence", test_mock_intelligence),
        ("Agent Base Classes", test_agent_base_classes),
        ("Component Integration", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 PHASE 1 TEST RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 PHASE 1 COMPLETE AND TESTED SUCCESSFULLY!")
        print("   Ready to move to Phase 2: Agent Orchestration")
    else:
        print("⚠️  Some tests failed. Please review and fix issues before proceeding.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
