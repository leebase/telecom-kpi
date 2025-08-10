"""
Playbook Prioritizer Agent - Main Orchestrator App

This is the main Streamlit application that demonstrates the multi-agent system
with real-time progress visualization, portfolio optimization, and stunning UI.
"""

import streamlit as st
import time
import json
from datetime import datetime
from typing import Dict, List, Any

from agents.orchestrator import AgentOrchestrator, OrchestrationConfig
from agents.mock_intelligence import get_mock_intelligence_engine
from models.play_models import SubjectArea, Play, Portfolio, WorkflowPhase

# Page configuration
st.set_page_config(
    page_title="AI Agent Orchestration System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for stunning visuals
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .agent-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .agent-working {
        border-color: #ff6b6b;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
    }
    
    .agent-completed {
        border-color: #51cf66;
        background: linear-gradient(135deg, #f8fff9 0%, #ebfbee 100%);
    }
    
    .progress-bar {
        height: 8px;
        border-radius: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .workflow-phase {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    
    .portfolio-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #dee2e6;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
    }
    
    .metric-highlight {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None
    if 'orchestration_started' not in st.session_state:
        st.session_state.orchestration_started = False
    if 'orchestration_completed' not in st.session_state:
        st.session_state.orchestration_completed = False
    if 'agent_results' not in st.session_state:
        st.session_state.agent_results = {}
    if 'portfolio_results' not in st.session_state:
        st.session_state.portfolio_results = None

def create_orchestrator():
    """Create and configure the agent orchestrator"""
    config = OrchestrationConfig(
        max_concurrent_agents=5,
        agent_timeout_seconds=30,
        optimization_iterations=3,
        portfolio_size_target=15,
        min_roi_threshold=7.0,
        max_risk_threshold=6.0,
        enable_parallel_execution=True,
        progress_update_interval=0.3
    )
    
    orchestrator = AgentOrchestrator(config)
    
    # Add progress callbacks
    def progress_callback(progress: float, message: str):
        st.session_state.current_progress = progress
        st.session_state.current_message = message
    
    def status_callback(message: str):
        st.session_state.current_status = message
    
    orchestrator.add_progress_callback(progress_callback)
    orchestrator.add_status_callback(status_callback)
    
    return orchestrator

def display_header():
    """Display the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Agent Orchestration System</h1>
        <h3>Enterprise-Grade Multi-Agent Portfolio Optimization</h3>
        <p>Watch as our specialized AI agents analyze your business and optimize your investment portfolio in real-time</p>
    </div>
    """, unsafe_allow_html=True)

def display_workflow_phases():
    """Display the workflow phases visualization"""
    st.markdown("### 🎯 Workflow Phases")
    
    phases = [
        ("🚀 Initialization", "Setting up agents and systems"),
        ("🔍 Agent Analysis", "5 specialized agents analyzing business areas"),
        ("⚡ Portfolio Optimization", "AI-powered portfolio selection and optimization"),
        ("📊 Results Presentation", "Executive summary and recommendations")
    ]
    
    cols = st.columns(4)
    for i, (phase, description) in enumerate(phases):
        with cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border: 2px solid #e0e0e0; border-radius: 10px;">
                <h4>{phase}</h4>
                <p style="font-size: 0.9rem; color: #666;">{description}</p>
            </div>
            """, unsafe_allow_html=True)

def display_agent_status(orchestrator):
    """Display real-time agent status"""
    st.markdown("### 🤖 Agent Status Dashboard")
    
    if not orchestrator:
        st.warning("Orchestrator not initialized")
        return
    
    status = orchestrator.get_status()
    agents = status.get('agents', {})
    
    # Create columns for agent display
    cols = st.columns(5)
    
    subject_areas = list(SubjectArea)
    for i, area in enumerate(subject_areas):
        with cols[i]:
            agent_id = f"agent_{area.value}"
            agent_status = agents.get(agent_id, {})
            
            # Determine card styling based on status
            card_class = "agent-card"
            if agent_status.get('status') == 'analyzing':
                card_class += " agent-working"
            elif agent_status.get('status') == 'completed':
                card_class += " agent-completed"
            
            # Display agent card
            st.markdown(f"""
            <div class="{card_class}">
                <h4 style="text-align: center; margin-bottom: 1rem;">{area.value.title()} Agent</h4>
                <p><strong>Status:</strong> {agent_status.get('status', 'idle').title()}</p>
                <p><strong>Progress:</strong> {agent_status.get('progress', 0):.1%}</p>
                <p><strong>Task:</strong> {agent_status.get('current_task', 'Waiting...')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar
            progress = agent_status.get('progress', 0)
            st.progress(progress)

def display_workflow_progress(orchestrator):
    """Display overall workflow progress"""
    if not orchestrator:
        return
    
    workflow_status = orchestrator.workflow_status
    
    st.markdown("### 📈 Overall Workflow Progress")
    
    # Current phase
    current_phase = workflow_status.current_phase.value.replace('_', ' ').title()
    st.markdown(f"""
    <div class="workflow-phase">
        <h4>Current Phase: {current_phase}</h4>
        <p>Phase Progress: {workflow_status.phase_progress:.1%}</p>
        <p>Total Progress: {workflow_status.total_progress:.1%}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bars
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Phase Progress", f"{workflow_status.phase_progress:.1%}")
    with col2:
        st.metric("Total Progress", f"{workflow_status.total_progress:.1%}")

def display_portfolio_results(portfolio):
    """Display portfolio optimization results"""
    if not portfolio:
        st.info("Portfolio optimization in progress...")
        return
    
    st.markdown("### 🎯 Portfolio Optimization Results")
    
    # Portfolio metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Investment", f"${portfolio.total_investment:,.0f}")
    
    with col2:
        st.metric("Expected ROI", f"{portfolio.total_roi:.1f}x")
    
    with col3:
        st.metric("Portfolio Size", len(portfolio.selected_plays))
    
    with col4:
        st.metric("Avg Priority", f"{portfolio.average_priority:.1f}")
    
    # Selected plays table
    st.markdown("#### 📋 Selected Initiatives")
    
    if portfolio.selected_plays:
        plays_data = []
        for play in portfolio.selected_plays:
            plays_data.append({
                "Rank": play.rank,
                "Title": play.title,
                "Area": play.subject_area.value.title(),
                "Impact": f"{play.impact_score:.1f}",
                "Effort": f"{play.effort_score:.1f}",
                "ROI": f"{play.roi_score:.1f}",
                "Risk": f"{play.risk_score:.1f}",
                "Score": f"{play.score:.3f}",
                "Priority": play.get_priority_label(),
                "Cost": f"${play.estimated_cost:,.0f}"
            })
        
        st.dataframe(plays_data, use_container_width=True)
    else:
        st.info("No plays selected yet. Run the orchestration to see results.")
    
    # Portfolio optimization details
    if hasattr(portfolio, 'optimization_parameters') and portfolio.optimization_parameters:
        st.markdown("#### ⚙️ Optimization Parameters")
        opt_params = portfolio.optimization_parameters
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Budget Points", opt_params.get("budget_points", "N/A"))
        with col2:
            st.metric("Total Effort", opt_params.get("total_effort", "N/A"))
        with col3:
            st.metric("Remaining Budget", opt_params.get("remaining_budget", "N/A"))

def display_executive_summary(portfolio):
    """Display executive summary"""
    if not portfolio:
        return
    
    st.markdown("### 📊 Executive Summary")
    
    # Create summary based on portfolio data
    total_plays = len(portfolio.selected_plays)
    high_priority_plays = len([p for p in portfolio.selected_plays if p.priority_level <= 2])
    low_risk_plays = len([p for p in portfolio.selected_plays if p.risk_score <= 4])
    
    summary = f"""
    **Portfolio Overview:**
    - **{total_plays}** strategic initiatives selected
    - **{high_priority_plays}** high-priority initiatives
    - **{low_risk_plays}** low-risk initiatives
    - Total investment: **${portfolio.total_investment:,.0f}**
    - Expected ROI: **{portfolio.total_roi:.1f}x**
    
    **Key Recommendations:**
    1. Focus on high-impact, low-effort initiatives first
    2. Monitor risk distribution across portfolio
    3. Track ROI metrics monthly for portfolio optimization
    4. Consider expanding successful initiatives to other areas
    """
    
    st.markdown(summary)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Sidebar controls
    st.sidebar.markdown("## 🎮 Control Panel")
    
    if st.sidebar.button("🚀 Start Orchestration", type="primary"):
        if not st.session_state.orchestrator:
            st.session_state.orchestrator = create_orchestrator()
        
        st.session_state.orchestration_started = True
        st.session_state.orchestration_completed = False
        
        # Start orchestration in background
        with st.spinner("Starting agent orchestration..."):
            orchestrator = st.session_state.orchestrator
            orchestrator.start_orchestration()
    
    if st.sidebar.button("⏹️ Stop Orchestration"):
        if st.session_state.orchestrator:
            st.session_state.orchestrator.stop_orchestration()
            st.session_state.orchestration_started = False
    
    if st.sidebar.button("🔄 Reset System"):
        st.session_state.orchestrator = None
        st.session_state.orchestration_started = False
        st.session_state.orchestration_completed = False
        st.session_state.agent_results = {}
        st.session_state.portfolio_results = None
        st.rerun()
    
    # Display workflow phases
    display_workflow_phases()
    
    # Main content area
    if st.session_state.orchestrator:
        # Display workflow progress
        display_workflow_progress(st.session_state.orchestrator)
        
        # Display agent status
        display_agent_status(st.session_state.orchestrator)
        
        # Check if orchestration is complete
        if st.session_state.orchestrator.status.value == 'completed':
            st.session_state.orchestration_completed = True
            
            # Get results
            results = st.session_state.orchestrator.get_results()
            
            # Display agent results
            if results.get('agent_results'):
                st.markdown("### 🤖 Agent Analysis Results")
                for agent_id, plays in results['agent_results'].items():
                    if plays:
                        area_name = agent_id.replace('_agent', '').title()
                        st.markdown(f"**{area_name} Area:** {len(plays)} plays generated")
            
            # Get portfolio results
            portfolio = None
            if results.get('optimized_portfolio'):
                portfolio = results['optimized_portfolio']
            elif results.get('initial_portfolio'):
                portfolio = results['initial_portfolio']
            
            if portfolio:
                # Display portfolio results
                display_portfolio_results(portfolio)
                
                # Display executive summary
                display_executive_summary(portfolio)
                
                # Export results
                st.markdown("### 📤 Export Results")
                portfolio_json = json.dumps(portfolio.to_dict(), indent=2)
                st.download_button(
                    label="Download Portfolio Results",
                    data=portfolio_json,
                    file_name=f"portfolio_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("Portfolio results not available yet. Please wait for optimization to complete.")
    
    # Auto-refresh for real-time updates
    if st.session_state.orchestration_started and not st.session_state.orchestration_completed:
        time.sleep(0.5)
        st.rerun()

if __name__ == "__main__":
    main()
