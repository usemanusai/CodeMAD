#!/usr/bin/env python3
"""
Autonomous Expansion Protocol for Project Chimera
Main orchestration system that coordinates all phases of the fully autonomous ecosystem expansion.
Operates perpetually to identify needs, create agents, and expand the ecosystem.
"""

import json
import logging
import sys
import os
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

# Add services directory to path for imports
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'architecture', 'ase'))

class ProtocolState(Enum):
    """Protocol execution states."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    EMERGENCY_STOP = "emergency_stop"

class PhaseState(Enum):
    """Individual phase states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class CycleResult:
    """Results from a complete expansion cycle."""
    cycle_id: str
    cycle_number: int
    started_at: str
    completed_at: str
    duration_minutes: float
    success: bool
    expansion_focus: str
    agent_created: Optional[str]
    gaps_identified: int
    errors: List[str]
    warnings: List[str]
    performance_metrics: Dict[str, Any]

class AutonomousExpansionProtocol:
    """
    Main orchestration system for fully autonomous ecosystem expansion.
    Coordinates all phases in a perpetual loop to continuously expand the agent ecosystem.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.config_file = self.workspace_root / "services" / "config" / "expansion_config.json"
        self.state_file = self.workspace_root / "services" / "data" / "expansion_state.json"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load configuration and state
        self.config = self._load_config()
        self.state = self._load_state()
        
        # Protocol control
        self.protocol_state = ProtocolState.STOPPED
        self.current_cycle = None
        self.stop_requested = False
        self.emergency_stop = False
        
        # Performance tracking
        self.cycle_history = []
        self.performance_metrics = {}
        
        # Initialize subsystems
        self._initialize_subsystems()
        
        # Control thread
        self.control_thread = None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load expansion configuration."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def _load_state(self) -> Dict[str, Any]:
        """Load protocol state."""
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading state: {e}")
            return {}
    
    def _save_state(self):
        """Save protocol state."""
        try:
            self.state['protocol_state']['last_updated'] = datetime.now().isoformat()
            
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving state: {e}")
    
    def _initialize_subsystems(self):
        """Initialize all subsystem components."""
        try:
            from global_needs_analyzer import GlobalNeedsAnalyzer
            from domain_research_engine import DomainResearchEngine
            from gap_analyzer import GapAnalyzer
            from agent_synthesis_engine import AgentSynthesisEngine
            from agent_integration_system import AgentIntegrationSystem
            from reporting_system import ReportingSystem
            
            self.global_analyzer = GlobalNeedsAnalyzer(self.workspace_root)
            self.domain_engine = DomainResearchEngine(self.workspace_root)
            self.gap_analyzer = GapAnalyzer(self.workspace_root)
            self.synthesis_engine = AgentSynthesisEngine(self.workspace_root)
            self.integration_system = AgentIntegrationSystem(self.workspace_root)
            self.reporting_system = ReportingSystem(self.workspace_root)
            
            self.logger.info("All subsystems initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing subsystems: {e}")
            raise
    
    def start_autonomous_operation(self) -> bool:
        """Start the autonomous expansion protocol."""
        if self.protocol_state == ProtocolState.RUNNING:
            self.logger.warning("Protocol is already running")
            return False
        
        try:
            self.logger.info("Starting Autonomous Expansion Protocol")
            self._log_audit_event("PROTOCOL_STARTED", "Autonomous expansion protocol initiated")
            
            # Update state
            self.protocol_state = ProtocolState.RUNNING
            self.stop_requested = False
            self.emergency_stop = False
            
            # Update state file
            self.state['protocol_state']['current_status'] = 'running'
            self.state['protocol_state']['protocol_enabled'] = True
            self._save_state()
            
            # Start control thread
            self.control_thread = threading.Thread(target=self._autonomous_loop, daemon=True)
            self.control_thread.start()
            
            self.logger.info("Autonomous expansion protocol started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting protocol: {e}")
            self.protocol_state = ProtocolState.ERROR
            return False
    
    def stop_autonomous_operation(self) -> bool:
        """Stop the autonomous expansion protocol."""
        try:
            self.logger.info("Stopping Autonomous Expansion Protocol")
            self._log_audit_event("PROTOCOL_STOP_REQUESTED", "Autonomous expansion protocol stop requested")
            
            self.stop_requested = True
            self.protocol_state = ProtocolState.STOPPED
            
            # Wait for current cycle to complete
            if self.control_thread and self.control_thread.is_alive():
                self.control_thread.join(timeout=30)
            
            # Update state
            self.state['protocol_state']['current_status'] = 'stopped'
            self.state['protocol_state']['protocol_enabled'] = False
            self._save_state()
            
            self.logger.info("Autonomous expansion protocol stopped")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping protocol: {e}")
            return False
    
    def emergency_stop(self) -> bool:
        """Emergency stop of the protocol."""
        try:
            self.logger.critical("EMERGENCY STOP activated")
            self._log_audit_event("EMERGENCY_STOP", "Emergency stop activated")
            
            self.emergency_stop = True
            self.stop_requested = True
            self.protocol_state = ProtocolState.EMERGENCY_STOP
            
            # Update state
            self.state['protocol_state']['current_status'] = 'emergency_stop'
            self.state['error_tracking']['emergency_stops'] += 1
            self._save_state()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during emergency stop: {e}")
            return False
    
    def _autonomous_loop(self):
        """Main autonomous operation loop."""
        self.logger.info("Autonomous loop started")
        
        try:
            while not self.stop_requested and not self.emergency_stop:
                # Check if we should continue
                if not self._should_continue_operation():
                    break
                
                # Execute expansion cycle
                cycle_result = self._execute_expansion_cycle()
                
                # Process cycle results
                self._process_cycle_results(cycle_result)
                
                # Check for errors and safety limits
                if not self._check_safety_limits():
                    break
                
                # Wait before next cycle
                self._wait_for_next_cycle()
                
        except Exception as e:
            self.logger.error(f"Error in autonomous loop: {e}")
            self.protocol_state = ProtocolState.ERROR
            self._log_audit_event("PROTOCOL_ERROR", f"Autonomous loop error: {str(e)}")
        
        finally:
            self.protocol_state = ProtocolState.STOPPED
            self.logger.info("Autonomous loop stopped")
    
    def _execute_expansion_cycle(self) -> CycleResult:
        """Execute a complete expansion cycle."""
        cycle_id = f"cycle_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        cycle_number = self.state.get('performance_metrics', {}).get('total_cycles_completed', 0) + 1
        started_at = datetime.now().isoformat()
        
        self.logger.info(f"Starting expansion cycle {cycle_number}: {cycle_id}")
        self._log_audit_event("CYCLE_STARTED", f"Expansion cycle {cycle_number} started: {cycle_id}")
        
        cycle_result = CycleResult(
            cycle_id=cycle_id,
            cycle_number=cycle_number,
            started_at=started_at,
            completed_at="",
            duration_minutes=0.0,
            success=False,
            expansion_focus="",
            agent_created=None,
            gaps_identified=0,
            errors=[],
            warnings=[],
            performance_metrics={}
        )
        
        try:
            # Phase 1: Strategic Focus & Gap Analysis
            phase1_result = self._execute_phase_1()
            if not phase1_result['success']:
                cycle_result.errors.extend(phase1_result['errors'])
                return cycle_result
            
            cycle_result.expansion_focus = phase1_result['expansion_focus']
            cycle_result.gaps_identified = len(phase1_result['gaps'])
            
            # Phase 2: Agent Implementation (if gaps found)
            if phase1_result['gaps']:
                selected_gap = phase1_result['gaps'][0]  # Top priority gap
                
                phase2_result = self._execute_phase_2(selected_gap)
                if phase2_result['success']:
                    cycle_result.agent_created = phase2_result['agent_id']
                else:
                    cycle_result.errors.extend(phase2_result['errors'])
            
            # Phase 3: Analysis & Reporting
            phase3_result = self._execute_phase_3(cycle_result)
            cycle_result.warnings.extend(phase3_result.get('warnings', []))
            
            # Mark as successful if we got this far
            cycle_result.success = True
            
        except Exception as e:
            cycle_result.errors.append(f"Cycle execution error: {str(e)}")
            self.logger.error(f"Error in expansion cycle: {e}")
        
        finally:
            cycle_result.completed_at = datetime.now().isoformat()
            start_time = datetime.fromisoformat(started_at)
            end_time = datetime.fromisoformat(cycle_result.completed_at)
            cycle_result.duration_minutes = (end_time - start_time).total_seconds() / 60.0
            
            self._log_audit_event("CYCLE_COMPLETED", 
                f"Cycle {cycle_number} completed: Success={cycle_result.success}, Agent={cycle_result.agent_created}")
        
        return cycle_result
    
    def _execute_phase_1(self) -> Dict[str, Any]:
        """Execute Phase 1: Strategic Focus & Gap Analysis."""
        self.logger.info("Executing Phase 1: Strategic Focus & Gap Analysis")
        
        result = {
            'success': False,
            'expansion_focus': '',
            'gaps': [],
            'errors': []
        }
        
        try:
            # Step 1: Global needs analysis (simplified for demo)
            # In production, this would use the GlobalNeedsAnalyzer
            expansion_focus = self._select_strategic_focus()
            result['expansion_focus'] = expansion_focus
            
            # Step 2: Domain research
            occupation_profiles = self.domain_engine.research_domain(expansion_focus)
            
            # Step 3: Gap analysis
            gaps = self.gap_analyzer.analyze_gaps(expansion_focus, occupation_profiles)
            result['gaps'] = gaps
            
            result['success'] = True
            self.logger.info(f"Phase 1 completed: Focus={expansion_focus}, Gaps={len(gaps)}")
            
        except Exception as e:
            result['errors'].append(f"Phase 1 error: {str(e)}")
            self.logger.error(f"Phase 1 error: {e}")
        
        return result
    
    def _execute_phase_2(self, gap_data: Any) -> Dict[str, Any]:
        """Execute Phase 2: Agent Implementation."""
        self.logger.info(f"Executing Phase 2: Agent Implementation for {gap_data.occupation_title}")
        
        result = {
            'success': False,
            'agent_id': None,
            'errors': []
        }
        
        try:
            # Step 1: Agent synthesis
            blueprint = self.synthesis_engine.synthesize_agent(gap_data)
            if not blueprint:
                result['errors'].append("Agent synthesis failed")
                return result
            
            # Step 2: Integration
            integration_result = self.integration_system.integrate_agent(blueprint)
            if integration_result['success']:
                result['success'] = True
                result['agent_id'] = blueprint.agent_id
                self.logger.info(f"Phase 2 completed: Agent {blueprint.agent_id} created and integrated")
            else:
                result['errors'].extend(integration_result['errors'])
            
        except Exception as e:
            result['errors'].append(f"Phase 2 error: {str(e)}")
            self.logger.error(f"Phase 2 error: {e}")
        
        return result
    
    def _execute_phase_3(self, cycle_result: CycleResult) -> Dict[str, Any]:
        """Execute Phase 3: Analysis & Reporting."""
        self.logger.info("Executing Phase 3: Analysis & Reporting")
        
        result = {
            'success': False,
            'warnings': []
        }
        
        try:
            # Generate cycle report
            report = self.reporting_system.generate_cycle_report(cycle_result)
            
            # Update performance metrics
            self._update_performance_metrics(cycle_result)
            
            result['success'] = True
            self.logger.info("Phase 3 completed: Report generated and metrics updated")
            
        except Exception as e:
            result['warnings'].append(f"Phase 3 warning: {str(e)}")
            self.logger.warning(f"Phase 3 warning: {e}")
        
        return result
    
    def _select_strategic_focus(self) -> str:
        """Select strategic focus for this cycle."""
        # Simplified focus selection - in production this would use GlobalNeedsAnalyzer
        focus_options = [
            "AI Healthcare",
            "Renewable Energy",
            "Cybersecurity",
            "Quantum Computing",
            "Sustainable Technology",
            "Digital Health",
            "Clean Energy",
            "Autonomous Systems"
        ]
        
        # For demo, cycle through options
        cycle_num = self.state.get('performance_metrics', {}).get('total_cycles_completed', 0)
        selected_focus = focus_options[cycle_num % len(focus_options)]
        
        self.logger.info(f"Selected strategic focus: {selected_focus}")
        return selected_focus
    
    def _should_continue_operation(self) -> bool:
        """Check if operation should continue."""
        # Check daily limits
        cycles_today = self._get_cycles_today()
        max_cycles = self.config.get('autonomous_operation', {}).get('max_cycles_per_day', 24)
        
        if cycles_today >= max_cycles:
            self.logger.info(f"Daily cycle limit reached: {cycles_today}/{max_cycles}")
            return False
        
        # Check error rates
        error_rate = self._calculate_error_rate()
        max_error_rate = self.config.get('safety_limits', {}).get('error_thresholds', {}).get('max_failure_rate_percent', 20)
        
        if error_rate > max_error_rate:
            self.logger.warning(f"Error rate too high: {error_rate}% > {max_error_rate}%")
            return False
        
        return True
    
    def _check_safety_limits(self) -> bool:
        """Check safety limits and constraints."""
        # Check consecutive failures
        consecutive_failures = self.state.get('error_tracking', {}).get('consecutive_failures', 0)
        max_failures = self.config.get('safety_limits', {}).get('error_thresholds', {}).get('max_consecutive_failures', 5)
        
        if consecutive_failures >= max_failures:
            self.logger.error(f"Too many consecutive failures: {consecutive_failures}")
            self.emergency_stop()
            return False
        
        return True
    
    def _wait_for_next_cycle(self):
        """Wait for the next cycle based on configuration."""
        interval_hours = self.config.get('autonomous_operation', {}).get('cycle_interval_hours', 1)
        wait_seconds = interval_hours * 3600
        
        self.logger.info(f"Waiting {interval_hours} hours before next cycle")
        
        # Wait in small increments to allow for stop requests
        for _ in range(int(wait_seconds)):
            if self.stop_requested or self.emergency_stop:
                break
            time.sleep(1)
    
    def _process_cycle_results(self, cycle_result: CycleResult):
        """Process and store cycle results."""
        # Add to history
        self.cycle_history.append(cycle_result)
        
        # Update state
        self.state['current_cycle'] = {
            'cycle_id': cycle_result.cycle_id,
            'cycle_number': cycle_result.cycle_number,
            'started_at': cycle_result.started_at,
            'current_phase': 'completed',
            'progress_percentage': 100
        }
        
        # Update performance metrics
        metrics = self.state.setdefault('performance_metrics', {})
        metrics['total_cycles_completed'] = cycle_result.cycle_number
        
        if cycle_result.agent_created:
            metrics['total_agents_created'] = metrics.get('total_agents_created', 0) + 1
        
        # Update error tracking
        if cycle_result.errors:
            error_tracking = self.state.setdefault('error_tracking', {})
            error_tracking['total_errors'] = error_tracking.get('total_errors', 0) + len(cycle_result.errors)
            error_tracking['consecutive_failures'] = error_tracking.get('consecutive_failures', 0) + 1
        else:
            self.state.setdefault('error_tracking', {})['consecutive_failures'] = 0
        
        self._save_state()
    
    def _get_cycles_today(self) -> int:
        """Get number of cycles executed today."""
        today = datetime.now().date()
        cycles_today = 0
        
        for cycle in self.cycle_history:
            cycle_date = datetime.fromisoformat(cycle.started_at).date()
            if cycle_date == today:
                cycles_today += 1
        
        return cycles_today
    
    def _calculate_error_rate(self) -> float:
        """Calculate recent error rate."""
        if len(self.cycle_history) < 5:
            return 0.0
        
        recent_cycles = self.cycle_history[-10:]  # Last 10 cycles
        failed_cycles = sum(1 for cycle in recent_cycles if cycle.errors)
        
        return (failed_cycles / len(recent_cycles)) * 100
    
    def _update_performance_metrics(self, cycle_result: CycleResult):
        """Update performance metrics."""
        metrics = self.performance_metrics
        
        # Update averages
        durations = [cycle.duration_minutes for cycle in self.cycle_history]
        metrics['average_cycle_duration'] = sum(durations) / len(durations) if durations else 0
        
        # Update success rate
        successful_cycles = sum(1 for cycle in self.cycle_history if cycle.success)
        metrics['success_rate'] = (successful_cycles / len(self.cycle_history)) * 100 if self.cycle_history else 0
    
    def get_status(self) -> Dict[str, Any]:
        """Get current protocol status."""
        return {
            'protocol_state': self.protocol_state.value,
            'current_cycle': self.current_cycle,
            'cycles_completed': len(self.cycle_history),
            'cycles_today': self._get_cycles_today(),
            'error_rate': self._calculate_error_rate(),
            'performance_metrics': self.performance_metrics,
            'last_updated': datetime.now().isoformat()
        }
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} AUTONOMOUS_EXPANSION_PROTOCOL {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing and control
if __name__ == "__main__":
    import sys
    
    protocol = AutonomousExpansionProtocol()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            print("Starting Autonomous Expansion Protocol...")
            success = protocol.start_autonomous_operation()
            if success:
                print("✅ Protocol started successfully")
                print("Use 'python autonomous_expansion_protocol.py status' to check progress")
                print("Use 'python autonomous_expansion_protocol.py stop' to stop")
            else:
                print("❌ Failed to start protocol")
        
        elif command == "stop":
            print("Stopping Autonomous Expansion Protocol...")
            success = protocol.stop_autonomous_operation()
            if success:
                print("✅ Protocol stopped successfully")
            else:
                print("❌ Failed to stop protocol")
        
        elif command == "emergency":
            print("Activating Emergency Stop...")
            success = protocol.emergency_stop()
            if success:
                print("🚨 Emergency stop activated")
            else:
                print("❌ Failed to activate emergency stop")
        
        elif command == "status":
            status = protocol.get_status()
            print("📊 Protocol Status:")
            print(f"   State: {status['protocol_state']}")
            print(f"   Cycles Completed: {status['cycles_completed']}")
            print(f"   Cycles Today: {status['cycles_today']}")
            print(f"   Error Rate: {status['error_rate']:.1f}%")
            print(f"   Last Updated: {status['last_updated']}")
        
        elif command == "test":
            print("Testing single expansion cycle...")
            cycle_result = protocol._execute_expansion_cycle()
            print(f"✅ Test cycle completed")
            print(f"   Success: {cycle_result.success}")
            print(f"   Focus: {cycle_result.expansion_focus}")
            print(f"   Agent Created: {cycle_result.agent_created}")
            print(f"   Duration: {cycle_result.duration_minutes:.2f} minutes")
        
        else:
            print("Usage: python autonomous_expansion_protocol.py [start|stop|emergency|status|test]")
    else:
        print("Autonomous Expansion Protocol initialized")
        print("Commands: start, stop, emergency, status, test")
