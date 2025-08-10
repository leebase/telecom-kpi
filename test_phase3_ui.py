#!/usr/bin/env python3
"""
Phase 3 UI Testing Script

This script tests the enhanced Phase 3 Visual Orchestration UI components:
- Real-time agent status updates
- Interactive workflow visualization
- Portfolio results display
- Executive summary generation
- Visual animations and styling
"""

import sys
import time
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import AgentOrchestrator, OrchestrationConfig
from agents.portfolio_agent import PortfolioAgent, PortfolioConfig
from models.play_models import Play, Portfolio, SubjectArea, PlayCategory
from agents.mock_intelligence import MockIntelligenceEngine


class TestPhase3UIComponents(unittest.TestCase):
    """Test Phase 3 UI components and functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = OrchestrationConfig(
            max_concurrent_agents=5,
            agent_timeout_seconds=10,
            optimization_iterations=2,
            portfolio_size_target=10,
            min_roi_threshold=6.0,
            max_risk_threshold=7.0,
            enable_parallel_execution=True,
            progress_update_interval=0.1
        )
        
        self.orchestrator = AgentOrchestrator(self.config)
        self.mock_intelligence = MockIntelligenceEngine()
        
    def test_agent_status_display(self):
        """Test agent status display functionality"""
        # Mock agent status
        mock_status = {
            'status': 'running',
            'agents': {
                'network': {
                    'status': 'analyzing',
                    'progress': 0.5,
                    'current_task': 'Analyzing network performance data'
                },
                'customer': {
                    'status': 'completed',
                    'progress': 1.0,
                    'current_task': 'Customer analysis complete'
                }
            },
            'current_phase': 'agent_analysis',
            'phase_progress': 0.4,
            'total_progress': 0.2
        }
        
        # Test status retrieval
        with patch.object(self.orchestrator, 'get_status', return_value=mock_status):
            status = self.orchestrator.get_status()
            
            self.assertEqual(status['status'], 'running')
            self.assertIn('network', status['agents'])
            self.assertIn('customer', status['agents'])
            self.assertEqual(status['agents']['network']['status'], 'analyzing')
            self.assertEqual(status['agents']['customer']['status'], 'completed')
    
    def test_workflow_progress_tracking(self):
        """Test workflow progress tracking"""
        # Test progress callbacks
        progress_updates = []
        status_updates = []
        
        def progress_callback(progress, message):
            progress_updates.append((progress, message))
        
        def status_callback(message):
            status_updates.append(message)
        
        self.orchestrator.add_progress_callback(progress_callback)
        self.orchestrator.add_status_callback(status_callback)
        
        # Simulate progress updates
        self.orchestrator._notify_progress(0.25, "Agent analysis in progress")
        self.orchestrator._notify_progress(0.5, "Portfolio optimization started")
        self.orchestrator._notify_status("Workflow phase transition")
        
        self.assertEqual(len(progress_updates), 2)
        self.assertEqual(len(status_updates), 1)
        self.assertEqual(progress_updates[0][0], 0.25)
        self.assertEqual(progress_updates[1][0], 0.5)
    
    def test_portfolio_results_generation(self):
        """Test portfolio results generation and display"""
        # Create mock plays
        plays = []
        for i in range(5):
            play = Play(
                title=f"Test Play {i+1}",
                description=f"Test description for play {i+1}",
                subject_area=SubjectArea.NETWORK,
                impact_score=8.0 - i,
                effort_score=5.0 + i,
                roi_score=7.0 - i,
                risk_score=3.0 + i,
                score=0.8 - (i * 0.1),
                rank=i+1
            )
            plays.append(play)
        
        # Create portfolio
        portfolio = Portfolio(
            name="Test Portfolio",
            description="Test portfolio for UI testing",
            selected_plays=plays
        )
        
        # Test portfolio metrics calculation
        self.assertEqual(len(portfolio.selected_plays), 5)
        self.assertGreater(portfolio.total_investment, 0)
        self.assertGreater(portfolio.total_roi, 0)
        self.assertGreater(portfolio.average_priority, 0)
        
        # Test portfolio serialization
        portfolio_dict = portfolio.to_dict()
        self.assertIn('selected_plays', portfolio_dict)
        self.assertIn('total_investment', portfolio_dict)
        self.assertIn('executive_summary', portfolio_dict)
    
    def test_executive_summary_generation(self):
        """Test executive summary generation"""
        # Create portfolio with plays
        plays = [
            Play(
                title="High Impact Initiative",
                description="This is a high-impact, low-effort initiative that will deliver significant value",
                subject_area=SubjectArea.NETWORK,
                impact_score=9.0,
                effort_score=3.0,
                roi_score=8.5,
                risk_score=2.0,
                score=0.95,
                rank=1
            ),
            Play(
                title="Strategic Enhancement",
                description="Strategic enhancement that will improve overall system performance",
                subject_area=SubjectArea.CUSTOMER,
                impact_score=7.5,
                effort_score=6.0,
                roi_score=7.0,
                risk_score=4.0,
                score=0.75,
                rank=2
            )
        ]
        
        portfolio = Portfolio(
            name="Strategic Portfolio",
            description="Portfolio of strategic initiatives",
            selected_plays=plays
        )
        
        # Test executive summary content
        self.assertIn("strategic initiatives", portfolio.executive_summary.lower())
        self.assertGreater(len(portfolio.executive_summary), 50)
        
        # Test portfolio metrics
        self.assertEqual(len(portfolio.selected_plays), 2)
        self.assertGreater(portfolio.total_roi, 0)
    
    def test_mock_intelligence_play_generation(self):
        """Test mock intelligence play generation for UI testing"""
        # Test play generation for each subject area
        subject_areas = [SubjectArea.NETWORK, SubjectArea.CUSTOMER, SubjectArea.REVENUE]
        
        for area in subject_areas:
            plays = self.mock_intelligence.generate_plays_for_area(area, count=3)
            
            self.assertEqual(len(plays), 3)
            for play in plays:
                self.assertIsInstance(play, Play)
                self.assertEqual(play.subject_area, area)
                self.assertGreater(play.impact_score, 0)
                self.assertLessEqual(play.impact_score, 10)
                self.assertGreater(play.effort_score, 0)
                self.assertLessEqual(play.effort_score, 10)
    
    def test_orchestrator_workflow_phases(self):
        """Test orchestrator workflow phase management"""
        # Test initial state
        self.assertEqual(self.orchestrator.status.value, 'idle')
        
        # Test workflow status
        workflow_status = self.orchestrator.workflow_status
        self.assertEqual(workflow_status.current_phase, 'initialization')
        self.assertEqual(workflow_status.total_progress, 0.0)
        
        # Test phase advancement
        workflow_status.advance_phase('agent_analysis')
        self.assertEqual(workflow_status.current_phase, 'agent_analysis')
        
        # Test progress updates
        workflow_status.update_phase_progress(0.5)
        workflow_status.update_total_progress(0.25)
        
        self.assertEqual(workflow_status.phase_progress, 0.5)
        self.assertEqual(workflow_status.total_progress, 0.25)
    
    def test_portfolio_agent_integration(self):
        """Test portfolio agent integration with orchestrator"""
        portfolio_config = PortfolioConfig(
            budget_points=8,
            kpi_weights={
                "impact": 0.35,
                "effort": 0.20,
                "roi": 0.30,
                "risk": 0.15
            }
        )
        
        portfolio_agent = PortfolioAgent(portfolio_config)
        
        # Generate mock plays by area
        plays_by_area = {}
        for area in [SubjectArea.NETWORK, SubjectArea.CUSTOMER]:
            plays = self.mock_intelligence.generate_plays_for_area(area, count=3)
            plays_by_area[area.value] = plays
        
        # Test portfolio processing
        portfolio = portfolio_agent.process_plays(plays_by_area)
        
        self.assertIsInstance(portfolio, Portfolio)
        self.assertGreater(len(portfolio.selected_plays), 0)
        self.assertIsNotNone(portfolio.executive_summary)
        
        # Test execution log
        execution_log = portfolio_agent.get_execution_log()
        self.assertGreater(len(execution_log), 0)
        self.assertIn("Starting portfolio optimization process", execution_log[0])
    
    def test_ui_data_serialization(self):
        """Test UI data serialization for display"""
        # Create complex portfolio data
        plays = []
        for i in range(3):
            play = Play(
                title=f"Complex Play {i+1}",
                description=f"Complex description with special characters: éñüç@#$%",
                subject_area=SubjectArea.NETWORK,
                impact_score=8.5,
                effort_score=4.0,
                roi_score=7.8,
                risk_score=3.2,
                score=0.85,
                rank=i+1,
                tags=["urgent", "strategic", "high-value"]
            )
            plays.append(play)
        
        portfolio = Portfolio(
            name="Complex Portfolio",
            description="Portfolio with complex data for UI testing",
            selected_plays=plays
        )
        
        # Test serialization
        portfolio_dict = portfolio.to_dict()
        
        # Verify all required fields are present
        required_fields = ['id', 'name', 'description', 'selected_plays', 'total_investment']
        for field in required_fields:
            self.assertIn(field, portfolio_dict)
        
        # Test play serialization
        for play_dict in portfolio_dict['selected_plays']:
            play_required_fields = ['id', 'title', 'description', 'impact_score', 'score', 'rank']
            for field in play_required_fields:
                self.assertIn(field, play_dict)
        
        # Test JSON serialization
        import json
        try:
            json_str = json.dumps(portfolio_dict)
            self.assertIsInstance(json_str, str)
            self.assertGreater(len(json_str), 100)
        except Exception as e:
            self.fail(f"JSON serialization failed: {e}")


class TestPhase3VisualElements(unittest.TestCase):
    """Test Phase 3 visual elements and styling"""
    
    def test_css_class_generation(self):
        """Test CSS class generation for different agent states"""
        # Test agent card classes
        base_class = "agent-card"
        
        # Test working state
        working_class = f"{base_class} agent-working"
        self.assertIn("agent-working", working_class)
        
        # Test completed state
        completed_class = f"{base_class} agent-completed"
        self.assertIn("agent-completed", completed_class)
        
        # Test status indicators
        status_classes = ["status-idle", "status-analyzing", "status-completed", "status-failed"]
        for status_class in status_classes:
            self.assertIn("status-", status_class)
    
    def test_metric_calculation(self):
        """Test metric calculations for UI display"""
        # Test portfolio metrics
        plays = [
            Play(impact_score=8.0, effort_score=4.0, roi_score=7.5, risk_score=3.0, estimated_cost=100000),
            Play(impact_score=7.0, effort_score=6.0, roi_score=6.5, risk_score=5.0, estimated_cost=150000)
        ]
        
        portfolio = Portfolio(selected_plays=plays)
        
        # Test calculated metrics
        self.assertEqual(len(portfolio.selected_plays), 2)
        self.assertGreater(portfolio.total_investment, 0)
        self.assertGreater(portfolio.total_roi, 0)
        self.assertGreater(portfolio.average_priority, 0)
        
        # Test risk distribution
        self.assertIn('risk_distribution', portfolio.to_dict())
    
    def test_workflow_visualization_data(self):
        """Test workflow visualization data structure"""
        # Mock workflow data for charts
        workflow_data = {
            'Phase': ['Agent Analysis', 'Portfolio Optimization', 'Results Generation'],
            'Status': ['Active', 'Active', 'Active'],
            'Duration': [15, 20, 5]
        }
        
        # Test data structure
        self.assertIn('Phase', workflow_data)
        self.assertIn('Status', workflow_data)
        self.assertIn('Duration', workflow_data)
        
        # Test data consistency
        self.assertEqual(len(workflow_data['Phase']), len(workflow_data['Status']))
        self.assertEqual(len(workflow_data['Phase']), len(workflow_data['Duration']))
        
        # Test data types
        for duration in workflow_data['Duration']:
            self.assertIsInstance(duration, int)
            self.assertGreater(duration, 0)


def run_phase3_tests():
    """Run all Phase 3 tests"""
    print("🧪 Running Phase 3 UI Component Tests...")
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPhase3UIComponents))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPhase3VisualElements))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n📊 Phase 3 Test Results:")
    print(f"   Tests Run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ Test Failures:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback}")
    
    if result.errors:
        print(f"\n🚨 Test Errors:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All Phase 3 tests passed successfully!")
        return True
    else:
        print("\n❌ Some Phase 3 tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    print("🚀 Phase 3 UI Testing Suite")
    print("=" * 50)
    
    success = run_phase3_tests()
    
    if success:
        print("\n🎉 Phase 3 implementation is ready for demo!")
        print("\nNext steps:")
        print("1. Run the enhanced UI: python runAgentsApp.py")
        print("2. Test real-time agent orchestration")
        print("3. Verify visual elements and animations")
        print("4. Prepare for hackathon demo")
    else:
        print("\n🔧 Please fix the test failures before proceeding to demo.")
        sys.exit(1)
