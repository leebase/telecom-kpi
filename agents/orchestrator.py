"""
Agent Orchestrator Engine

This module provides the central orchestration system for coordinating multiple agents,
managing workflows, and optimizing portfolio selection across all subject areas.
"""

import time
import threading
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from models.play_models import (
    Play, 
    Portfolio, 
    SubjectArea, 
    AgentStatus,
    WorkflowPhase,
    WorkflowStatus
)
from agents.base_agent import BaseAgent, SubjectAreaAgent, AgentFactory


class OrchestrationStatus(Enum):
    """Status of the orchestration process"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    OPTIMIZING = "optimizing"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class OrchestrationConfig:
    """Configuration for the orchestration process"""
    max_concurrent_agents: int = 5
    agent_timeout_seconds: int = 30
    optimization_iterations: int = 3
    portfolio_size_target: int = 15
    min_roi_threshold: float = 7.0
    max_risk_threshold: float = 6.0
    enable_parallel_execution: bool = True
    progress_update_interval: float = 0.5


@dataclass
class OrchestrationMetrics:
    """Metrics and statistics for the orchestration process"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_agents: int = 0
    successful_agents: int = 0
    failed_agents: int = 0
    total_plays_generated: int = 0
    total_execution_time: float = 0.0
    average_agent_execution_time: float = 0.0
    portfolio_optimization_time: float = 0.0
    final_portfolio_size: int = 0
    final_portfolio_roi: float = 0.0
    final_portfolio_risk: float = 0.0


class AgentOrchestrator:
    """Main orchestrator for coordinating multiple agents and optimizing portfolios"""
    
    def __init__(self, config: OrchestrationConfig = None):
        """Initialize the agent orchestrator"""
        self.config = config or OrchestrationConfig()
        self.status = OrchestrationStatus.IDLE
        self.metrics = OrchestrationMetrics()
        self.workflow_status = WorkflowStatus()
        
        # Agent management
        self.agents: Dict[str, SubjectAreaAgent] = {}
        self.agent_results: Dict[str, List[Play]] = {}
        self.agent_status: Dict[str, AgentStatus] = {}
        
        # Portfolio management
        self.initial_portfolio: Optional[Portfolio] = None
        self.optimized_portfolio: Optional[Portfolio] = None
        
        # Execution control
        self._execution_thread: Optional[threading.Thread] = None
        self._stop_execution = threading.Event()
        self._lock = threading.Lock()
        
        # Progress callbacks
        self._progress_callbacks: List[Callable] = []
        self._status_callbacks: List[Callable] = []
        
        # Initialize agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all subject area agents"""
        try:
            self.agents = AgentFactory.create_all_subject_area_agents()
            self.metrics.total_agents = len(self.agents)
            
            # Initialize agent status tracking
            for agent_id, agent in self.agents.items():
                self.agent_status[agent_id] = AgentStatus.IDLE
                self.agent_results[agent_id] = []
            
            self._log_orchestration("All agents initialized successfully", "INFO")
            
        except Exception as e:
            self._log_orchestration(f"Failed to initialize agents: {e}", "ERROR")
            raise
    
    def start_orchestration(self, callback: Callable = None) -> bool:
        """Start the orchestration process"""
        if self.status != OrchestrationStatus.IDLE:
            self._log_orchestration("Orchestrator is not in idle state", "WARNING")
            return False
        
        if callback:
            self._progress_callbacks.append(callback)
        
        try:
            self.status = OrchestrationStatus.INITIALIZING
            self.metrics.start_time = datetime.now()
            self.workflow_status.update_phase(WorkflowPhase.AGENT_EXECUTION)
            
            # Start execution in background thread
            self._execution_thread = threading.Thread(
                target=self._execute_orchestration,
                daemon=True
            )
            self._execution_thread.start()
            
            self._log_orchestration("Orchestration started successfully", "INFO")
            return True
            
        except Exception as e:
            self._log_orchestration(f"Failed to start orchestration: {e}", "ERROR")
            self.status = OrchestrationStatus.FAILED
            return False
    
    def _execute_orchestration(self):
        """Execute the main orchestration workflow"""
        try:
            self.status = OrchestrationStatus.RUNNING
            self._log_orchestration("Starting agent execution phase", "INFO")
            
            # Phase 1: Execute all agents
            if not self._execute_all_agents():
                raise RuntimeError("Agent execution phase failed")
            
            # Phase 2: Create initial portfolio
            if not self._create_initial_portfolio():
                raise RuntimeError("Portfolio creation failed")
            
            # Phase 3: Optimize portfolio
            if not self._optimize_portfolio():
                raise RuntimeError("Portfolio optimization failed")
            
            # Phase 4: Finalize results
            self._finalize_orchestration()
            
        except Exception as e:
            self._log_orchestration(f"Orchestration execution failed: {e}", "ERROR")
            self.status = OrchestrationStatus.FAILED
            self.workflow_status.update_phase(WorkflowPhase.FAILED)
    
    def _execute_all_agents(self) -> bool:
        """Execute all agents in parallel or sequence"""
        self._log_orchestration("Executing all agents", "INFO")
        
        if self.config.enable_parallel_execution:
            return self._execute_agents_parallel()
        else:
            return self._execute_agents_sequential()
    
    def _execute_agents_parallel(self) -> bool:
        """Execute all agents in parallel"""
        self._log_orchestration("Executing agents in parallel", "INFO")
        
        # Start all agents
        for agent_id, agent in self.agents.items():
            if self._should_stop_execution():
                return False
            
            try:
                agent.start_execution(f"Analyzing {agent.subject_area.value}")
                self.agent_status[agent_id] = AgentStatus.ANALYZING
                self._log_orchestration(f"Started {agent_id}", "INFO")
                
            except Exception as e:
                self._log_orchestration(f"Failed to start {agent_id}: {e}", "ERROR")
                self.agent_status[agent_id] = AgentStatus.FAILED
                self.metrics.failed_agents += 1
        
        # Wait for all agents to complete
        start_time = time.time()
        while not self._should_stop_execution():
            # Check completion status
            completed_agents = 0
            failed_agents = 0
            
            for agent_id, agent in self.agents.items():
                if self.agent_status[agent_id] == AgentStatus.ANALYZING:
                    if agent.state.status == AgentStatus.COMPLETED:
                        self.agent_status[agent_id] = AgentStatus.COMPLETED
                        self.agent_results[agent_id] = agent.get_plays()
                        self.metrics.successful_agents += 1
                        self.metrics.total_plays_generated += len(self.agent_results[agent_id])
                        self._log_orchestration(f"{agent_id} completed", "INFO")
                        
                    elif agent.state.status == AgentStatus.FAILED:
                        self.agent_status[agent_id] = AgentStatus.FAILED
                        self.metrics.failed_agents += 1
                        self._log_orchestration(f"{agent_id} failed", "ERROR")
                
                if self.agent_status[agent_id] in [AgentStatus.COMPLETED, AgentStatus.FAILED]:
                    completed_agents += 1
            
            # Update progress
            progress = completed_agents / len(self.agents)
            self.workflow_status.update_progress(progress)
            self._notify_progress(progress, f"Agents completed: {completed_agents}/{len(self.agents)}")
            
            # Check if all agents are done
            if completed_agents == len(self.agents):
                break
            
            # Check timeout
            if time.time() - start_time > self.config.agent_timeout_seconds:
                self._log_orchestration("Agent execution timeout", "WARNING")
                break
            
            time.sleep(self.config.progress_update_interval)
        
        # Final status check
        successful = self.metrics.successful_agents > 0
        self._log_orchestration(f"Agent execution complete: {self.metrics.successful_agents} successful, {self.metrics.failed_agents} failed", "INFO")
        
        return successful
    
    def _execute_agents_sequential(self) -> bool:
        """Execute all agents sequentially"""
        self._log_orchestration("Executing agents sequentially", "INFO")
        
        for agent_id, agent in self.agents.items():
            if self._should_stop_execution():
                return False
            
            try:
                self._log_orchestration(f"Executing {agent_id}", "INFO")
                agent.start_execution(f"Analyzing {agent.subject_area.value}")
                
                # Wait for completion
                if agent.wait_for_completion(timeout=self.config.agent_timeout_seconds):
                    self.agent_status[agent_id] = AgentStatus.COMPLETED
                    self.agent_results[agent_id] = agent.get_plays()
                    self.metrics.successful_agents += 1
                    self.metrics.total_plays_generated += len(self.agent_results[agent_id])
                    self._log_orchestration(f"{agent_id} completed successfully", "INFO")
                else:
                    self.agent_status[agent_id] = AgentStatus.FAILED
                    self.metrics.failed_agents += 1
                    self._log_orchestration(f"{agent_id} execution timeout", "WARNING")
                
            except Exception as e:
                self._log_orchestration(f"Failed to execute {agent_id}: {e}", "ERROR")
                self.agent_status[agent_id] = AgentStatus.FAILED
                self.metrics.failed_agents += 1
        
        # Update progress
        progress = self.metrics.successful_agents / len(self.agents)
        self.workflow_status.update_progress(progress)
        
        return self.metrics.successful_agents > 0
    
    def _create_initial_portfolio(self) -> bool:
        """Create initial portfolio from all agent results"""
        self._log_orchestration("Creating initial portfolio", "INFO")
        
        try:
            # Collect all plays from successful agents
            all_plays = []
            for agent_id, plays in self.agent_results.items():
                if self.agent_status[agent_id] == AgentStatus.COMPLETED:
                    all_plays.extend(plays)
            
            if not all_plays:
                self._log_orchestration("No plays available for portfolio creation", "ERROR")
                return False
            
            # Create portfolio
            self.initial_portfolio = Portfolio()
            for play in all_plays:
                self.initial_portfolio.add_play(play)
            
            self._log_orchestration(f"Initial portfolio created with {len(all_plays)} plays", "INFO")
            self.workflow_status.update_phase(WorkflowPhase.PORTFOLIO_OPTIMIZATION)
            
            return True
            
        except Exception as e:
            self._log_orchestration(f"Failed to create initial portfolio: {e}", "ERROR")
            return False
    
    def _optimize_portfolio(self) -> bool:
        """Optimize the portfolio using the portfolio agent"""
        self._log_orchestration("Starting portfolio optimization", "INFO")
        
        try:
            from agents.portfolio_agent import PortfolioAgent, PortfolioConfig
            
            # Create portfolio configuration
            portfolio_config = PortfolioConfig(
                budget_points=self.config.portfolio_size_target,
                kpi_weights={
                    "impact": 0.35,
                    "effort": 0.20,
                    "roi": 0.30,
                    "risk": 0.15
                }
            )
            
            # Create and run portfolio agent
            portfolio_agent = PortfolioAgent(portfolio_config)
            
            # Convert portfolio to plays_by_area format for the agent
            plays_by_area = {}
            for agent_id, plays in self.agent_results.items():
                if self.agent_status[agent_id] == AgentStatus.COMPLETED:
                    area = agent_id.replace('_agent', '')  # Extract area from agent_id
                    plays_by_area[area] = plays
            
            # Process plays through portfolio agent
            self.optimized_portfolio = portfolio_agent.process_plays(plays_by_area)
            
            # Update metrics
            if self.optimized_portfolio:
                self.metrics.final_portfolio_size = len(self.optimized_portfolio.selected_plays)
                self.metrics.final_portfolio_roi = self.optimized_portfolio.total_roi
                self.metrics.final_portfolio_risk = self.optimized_portfolio.average_priority  # Use priority as risk proxy
                self.metrics.portfolio_optimization_time = time.time()  # Simple timing
            
            self._log_orchestration("Portfolio optimization completed", "INFO")
            return True
            
        except ImportError:
            self._log_orchestration("Portfolio agent not available, using basic optimization", "WARNING")
            return self._basic_portfolio_optimization()
        except Exception as e:
            self._log_orchestration(f"Portfolio optimization failed: {e}", "ERROR")
            return False
    
    def _basic_portfolio_optimization(self) -> bool:
        """Basic portfolio optimization fallback"""
        self._log_orchestration("Using basic portfolio optimization", "INFO")
        
        try:
            # Simple optimization: select top plays by ROI
            all_plays = self.initial_portfolio.selected_plays.copy()
            all_plays.sort(key=lambda p: p.roi_score, reverse=True)
            
            # Create optimized portfolio with top plays
            self.optimized_portfolio = Portfolio()
            target_size = min(self.config.portfolio_size_target, len(all_plays))
            
            for play in all_plays[:target_size]:
                self.optimized_portfolio.add_play(play)
            
            self._log_orchestration(f"Basic optimization completed: {len(self.optimized_portfolio.selected_plays)} plays selected", "INFO")
            return True
            
        except Exception as e:
            self._log_orchestration(f"Basic optimization failed: {e}", "ERROR")
            return False
    
    def _finalize_orchestration(self):
        """Finalize the orchestration process"""
        self._log_orchestration("Finalizing orchestration", "INFO")
        
        try:
            # Update final metrics
            self.metrics.end_time = datetime.now()
            if self.metrics.start_time:
                self.metrics.total_execution_time = (self.metrics.end_time - self.metrics.start_time).total_seconds()
            
            if self.metrics.successful_agents > 0:
                self.metrics.average_agent_execution_time = self.metrics.total_execution_time / self.metrics.successful_agents
            
            # Update workflow status
            self.workflow_status.update_phase(WorkflowPhase.COMPLETED)
            self.workflow_status.update_progress(1.0)
            
            # Set final status
            self.status = OrchestrationStatus.COMPLETED
            
            self._log_orchestration("Orchestration completed successfully", "INFO")
            self._notify_status("Orchestration completed successfully")
            
        except Exception as e:
            self._log_orchestration(f"Failed to finalize orchestration: {e}", "ERROR")
            self.status = OrchestrationStatus.FAILED
    
    def stop_orchestration(self) -> bool:
        """Stop the orchestration process"""
        if self.status not in [OrchestrationStatus.RUNNING, OrchestrationStatus.OPTIMIZING]:
            return False
        
        try:
            self._stop_execution.set()
            
            # Stop all running agents
            for agent in self.agents.values():
                if agent.state.status == AgentStatus.ANALYZING:
                    agent.stop_execution()
            
            # Wait for execution thread
            if self._execution_thread and self._execution_thread.is_alive():
                self._execution_thread.join(timeout=5.0)
            
            self.status = OrchestrationStatus.PAUSED
            self._log_orchestration("Orchestration stopped", "INFO")
            return True
            
        except Exception as e:
            self._log_orchestration(f"Failed to stop orchestration: {e}", "ERROR")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current orchestration status"""
        with self._lock:
            return {
                "status": self.status.value,
                "workflow_phase": self.workflow_status.current_phase.value,
                "workflow_progress": self.workflow_status.total_progress,
                "metrics": {
                    "total_agents": self.metrics.total_agents,
                    "successful_agents": self.metrics.successful_agents,
                    "failed_agents": self.metrics.failed_agents,
                    "total_plays": self.metrics.total_plays_generated,
                    "execution_time": self.metrics.total_execution_time,
                    "portfolio_size": self.metrics.final_portfolio_size,
                    "portfolio_roi": self.metrics.final_portfolio_roi,
                    "portfolio_risk": self.metrics.final_portfolio_risk
                },
                "agent_status": {agent_id: status.value for agent_id, status in self.agent_status.items()},
                "timestamp": datetime.now().isoformat()
            }
    
    def get_results(self) -> Dict[str, Any]:
        """Get orchestration results"""
        if self.status != OrchestrationStatus.COMPLETED:
            return {"error": "Orchestration not completed"}
        
        return {
            "status": "completed",
            "initial_portfolio": self.initial_portfolio.to_dict() if self.initial_portfolio else None,
            "optimized_portfolio": self.optimized_portfolio.to_dict() if self.optimized_portfolio else None,
            "agent_results": {
                agent_id: [play.to_dict() for play in plays] 
                for agent_id, plays in self.agent_results.items()
            },
            "metrics": {
                "total_execution_time": self.metrics.total_execution_time,
                "total_plays_generated": self.metrics.total_plays_generated,
                "final_portfolio_size": self.metrics.final_portfolio_size,
                "final_portfolio_roi": self.metrics.final_portfolio_roi,
                "final_portfolio_risk": self.metrics.final_portfolio_risk
            }
        }
    
    def add_progress_callback(self, callback: Callable):
        """Add a progress callback function"""
        self._progress_callbacks.append(callback)
    
    def add_status_callback(self, callback: Callable):
        """Add a status callback function"""
        self._status_callbacks.append(callback)
    
    def _notify_progress(self, progress: float, message: str):
        """Notify progress callbacks"""
        for callback in self._progress_callbacks:
            try:
                callback(progress, message)
            except Exception as e:
                self._log_orchestration(f"Progress callback error: {e}", "WARNING")
    
    def _notify_status(self, message: str):
        """Notify status callbacks"""
        for callback in self._status_callbacks:
            try:
                callback(message)
            except Exception as e:
                self._log_orchestration(f"Status callback error: {e}", "WARNING")
    
    def _should_stop_execution(self) -> bool:
        """Check if execution should stop"""
        return self._stop_execution.is_set()
    
    def _log_orchestration(self, message: str, level: str = "INFO"):
        """Log orchestration messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [ORCHESTRATOR] [{level}] {message}")


# Convenience functions
def create_orchestrator(config: OrchestrationConfig = None) -> AgentOrchestrator:
    """Create a configured orchestrator instance"""
    return AgentOrchestrator(config)


def run_orchestration(config: OrchestrationConfig = None, timeout: int = 60) -> Dict[str, Any]:
    """Run orchestration with default configuration"""
    orchestrator = create_orchestrator(config)
    
    # Add progress callback
    def progress_callback(progress: float, message: str):
        print(f"Progress: {progress:.1%} - {message}")
    
    orchestrator.add_progress_callback(progress_callback)
    
    # Start orchestration
    if not orchestrator.start_orchestration():
        return {"error": "Failed to start orchestration"}
    
    # Wait for completion
    start_time = time.time()
    while orchestrator.status not in [OrchestrationStatus.COMPLETED, OrchestrationStatus.FAILED]:
        if time.time() - start_time > timeout:
            orchestrator.stop_orchestration()
            return {"error": "Orchestration timeout"}
        time.sleep(0.5)
    
    return orchestrator.get_results()
