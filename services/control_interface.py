#!/usr/bin/env python3
"""
Control & Monitoring Interface for Project Chimera
Provides human oversight, monitoring, and control capabilities for the autonomous expansion protocol.
Includes emergency controls, performance monitoring, and configuration management.
"""

import json
import logging
import sys
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import threading

# Add services directory to path for imports
sys.path.append(os.path.dirname(__file__))

class ControlInterface:
    """
    Human oversight and control interface for autonomous expansion protocol.
    Provides monitoring, control, and emergency intervention capabilities.
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
        
        # Initialize subsystems
        self._initialize_subsystems()
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        self.alerts = []
    
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
    
    def _initialize_subsystems(self):
        """Initialize subsystem interfaces."""
        try:
            from autonomous_expansion_protocol import AutonomousExpansionProtocol
            from reporting_system import ReportingSystem
            from agent_directory_service import AgentDirectoryService
            
            self.protocol = AutonomousExpansionProtocol(self.workspace_root)
            self.reporting = ReportingSystem(self.workspace_root)
            self.agent_directory = AgentDirectoryService(self.workspace_root)
            
            self.logger.info("Control interface subsystems initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing subsystems: {e}")
            raise
    
    def start_monitoring(self) -> bool:
        """Start continuous monitoring of the protocol."""
        if self.monitoring_active:
            self.logger.warning("Monitoring is already active")
            return False
        
        try:
            self.logger.info("Starting protocol monitoring")
            self.monitoring_active = True
            
            # Start monitoring thread
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            
            self._log_audit_event("MONITORING_STARTED", "Protocol monitoring activated")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop protocol monitoring."""
        try:
            self.logger.info("Stopping protocol monitoring")
            self.monitoring_active = False
            
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=10)
            
            self._log_audit_event("MONITORING_STOPPED", "Protocol monitoring deactivated")
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping monitoring: {e}")
            return False
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        self.logger.info("Monitoring loop started")
        
        try:
            while self.monitoring_active:
                # Check protocol health
                self._check_protocol_health()
                
                # Check performance metrics
                self._check_performance_metrics()
                
                # Check safety limits
                self._check_safety_limits()
                
                # Check resource usage
                self._check_resource_usage()
                
                # Wait before next check
                time.sleep(30)  # Check every 30 seconds
                
        except Exception as e:
            self.logger.error(f"Error in monitoring loop: {e}")
        
        finally:
            self.logger.info("Monitoring loop stopped")
    
    def _check_protocol_health(self):
        """Check overall protocol health."""
        try:
            status = self.protocol.get_status()
            
            # Check for error state
            if status['protocol_state'] == 'error':
                self._create_alert('CRITICAL', 'Protocol in error state', 
                                 'The autonomous expansion protocol has entered an error state')
            
            # Check for emergency stop
            if status['protocol_state'] == 'emergency_stop':
                self._create_alert('CRITICAL', 'Emergency stop activated', 
                                 'Emergency stop has been activated for the protocol')
            
            # Check error rate
            if status['error_rate'] > 50:
                self._create_alert('HIGH', 'High error rate detected', 
                                 f"Error rate is {status['error_rate']:.1f}%, exceeding safe thresholds")
            
        except Exception as e:
            self.logger.error(f"Error checking protocol health: {e}")
    
    def _check_performance_metrics(self):
        """Check performance metrics for anomalies."""
        try:
            # Reload state to get latest data
            self.state = self._load_state()
            
            # Check cycle completion rate
            cycles_today = self._get_cycles_today()
            expected_cycles = self._get_expected_cycles_today()
            
            if cycles_today < expected_cycles * 0.5:  # Less than 50% of expected
                self._create_alert('MEDIUM', 'Low cycle completion rate', 
                                 f"Only {cycles_today} cycles completed today, expected {expected_cycles}")
            
            # Check agent creation rate
            agents_created = self.state.get('performance_metrics', {}).get('total_agents_created', 0)
            total_cycles = self.state.get('performance_metrics', {}).get('total_cycles_completed', 0)
            
            if total_cycles > 10 and agents_created / total_cycles < 0.3:  # Less than 30% success rate
                self._create_alert('MEDIUM', 'Low agent creation rate', 
                                 f"Agent creation rate is {(agents_created/total_cycles)*100:.1f}%")
            
        except Exception as e:
            self.logger.error(f"Error checking performance metrics: {e}")
    
    def _check_safety_limits(self):
        """Check safety limits and constraints."""
        try:
            # Check consecutive failures
            consecutive_failures = self.state.get('error_tracking', {}).get('consecutive_failures', 0)
            max_failures = self.config.get('safety_limits', {}).get('error_thresholds', {}).get('max_consecutive_failures', 5)
            
            if consecutive_failures >= max_failures * 0.8:  # 80% of limit
                self._create_alert('HIGH', 'Approaching failure limit', 
                                 f"Consecutive failures: {consecutive_failures}/{max_failures}")
            
            # Check daily limits
            cycles_today = self._get_cycles_today()
            max_cycles = self.config.get('autonomous_operation', {}).get('max_cycles_per_day', 24)
            
            if cycles_today >= max_cycles:
                self._create_alert('INFO', 'Daily cycle limit reached', 
                                 f"Reached daily limit of {max_cycles} cycles")
            
        except Exception as e:
            self.logger.error(f"Error checking safety limits: {e}")
    
    def _check_resource_usage(self):
        """Check resource usage and constraints."""
        try:
            # Check memory usage (simplified)
            memory_usage = self.state.get('resource_usage', {}).get('memory_usage_mb', 0)
            max_memory = self.config.get('safety_limits', {}).get('resource_limits', {}).get('max_memory_usage_mb', 1024)
            
            if memory_usage > max_memory * 0.9:  # 90% of limit
                self._create_alert('HIGH', 'High memory usage', 
                                 f"Memory usage: {memory_usage}MB/{max_memory}MB")
            
            # Check disk usage
            disk_usage = self.state.get('resource_usage', {}).get('disk_usage_mb', 0)
            max_disk = self.config.get('safety_limits', {}).get('resource_limits', {}).get('max_disk_usage_mb', 500)
            
            if disk_usage > max_disk * 0.9:  # 90% of limit
                self._create_alert('HIGH', 'High disk usage', 
                                 f"Disk usage: {disk_usage}MB/{max_disk}MB")
            
        except Exception as e:
            self.logger.error(f"Error checking resource usage: {e}")
    
    def _create_alert(self, severity: str, title: str, description: str):
        """Create a monitoring alert."""
        alert = {
            'id': f"alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'title': title,
            'description': description,
            'acknowledged': False
        }
        
        self.alerts.append(alert)
        
        # Log alert
        self.logger.warning(f"ALERT [{severity}]: {title} - {description}")
        self._log_audit_event("ALERT_CREATED", f"{severity}: {title}")
        
        # Keep only last 100 alerts
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        try:
            # Get protocol status
            protocol_status = self.protocol.get_status()
            
            # Get ecosystem metrics
            ecosystem_metrics = self.reporting._calculate_ecosystem_metrics()
            
            # Get performance metrics
            performance_metrics = self.reporting._analyze_performance()
            
            # Get recent alerts
            recent_alerts = [alert for alert in self.alerts if not alert['acknowledged']][-10:]
            
            return {
                'timestamp': datetime.now().isoformat(),
                'protocol_status': {
                    'state': protocol_status['protocol_state'],
                    'cycles_completed': protocol_status['cycles_completed'],
                    'cycles_today': protocol_status['cycles_today'],
                    'error_rate': protocol_status['error_rate'],
                    'last_updated': protocol_status['last_updated']
                },
                'ecosystem_health': {
                    'total_agents': ecosystem_metrics.total_agents,
                    'agents_today': ecosystem_metrics.agents_created_today,
                    'agents_week': ecosystem_metrics.agents_created_this_week,
                    'domains_covered': ecosystem_metrics.domains_covered,
                    'average_quality': ecosystem_metrics.average_agent_quality,
                    'growth_rate': ecosystem_metrics.ecosystem_growth_rate,
                    'coverage_percentage': ecosystem_metrics.coverage_completeness
                },
                'performance_metrics': {
                    'success_rate': performance_metrics.success_rate,
                    'efficiency_score': performance_metrics.efficiency_score,
                    'average_duration': performance_metrics.average_cycle_duration,
                    'cycles_per_day': performance_metrics.cycles_per_day
                },
                'alerts': {
                    'total_active': len(recent_alerts),
                    'critical': len([a for a in recent_alerts if a['severity'] == 'CRITICAL']),
                    'high': len([a for a in recent_alerts if a['severity'] == 'HIGH']),
                    'medium': len([a for a in recent_alerts if a['severity'] == 'MEDIUM']),
                    'recent': recent_alerts[:5]
                },
                'system_health': {
                    'monitoring_active': self.monitoring_active,
                    'last_check': datetime.now().isoformat(),
                    'uptime_hours': self._calculate_uptime_hours()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting dashboard data: {e}")
            return {'error': str(e)}
    
    def execute_control_command(self, command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute control commands."""
        parameters = parameters or {}
        
        try:
            if command == "start_protocol":
                success = self.protocol.start_autonomous_operation()
                return {'success': success, 'message': 'Protocol started' if success else 'Failed to start protocol'}
            
            elif command == "stop_protocol":
                success = self.protocol.stop_autonomous_operation()
                return {'success': success, 'message': 'Protocol stopped' if success else 'Failed to stop protocol'}
            
            elif command == "emergency_stop":
                success = self.protocol.emergency_stop()
                return {'success': success, 'message': 'Emergency stop activated' if success else 'Failed to activate emergency stop'}
            
            elif command == "acknowledge_alert":
                alert_id = parameters.get('alert_id')
                success = self._acknowledge_alert(alert_id)
                return {'success': success, 'message': 'Alert acknowledged' if success else 'Failed to acknowledge alert'}
            
            elif command == "clear_alerts":
                self.alerts = []
                return {'success': True, 'message': 'All alerts cleared'}
            
            elif command == "update_config":
                config_updates = parameters.get('config_updates', {})
                success = self._update_config(config_updates)
                return {'success': success, 'message': 'Configuration updated' if success else 'Failed to update configuration'}
            
            elif command == "force_cycle":
                cycle_result = self.protocol._execute_expansion_cycle()
                return {'success': cycle_result.success, 'message': f'Forced cycle completed: {cycle_result.cycle_id}'}
            
            else:
                return {'success': False, 'message': f'Unknown command: {command}'}
                
        except Exception as e:
            self.logger.error(f"Error executing command {command}: {e}")
            return {'success': False, 'message': f'Command execution error: {str(e)}'}
    
    def _acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge a specific alert."""
        for alert in self.alerts:
            if alert['id'] == alert_id:
                alert['acknowledged'] = True
                alert['acknowledged_at'] = datetime.now().isoformat()
                return True
        return False
    
    def _update_config(self, updates: Dict[str, Any]) -> bool:
        """Update configuration with new values."""
        try:
            # Update config in memory
            for key, value in updates.items():
                if '.' in key:
                    # Handle nested keys like 'autonomous_operation.max_cycles_per_day'
                    keys = key.split('.')
                    current = self.config
                    for k in keys[:-1]:
                        current = current.setdefault(k, {})
                    current[keys[-1]] = value
                else:
                    self.config[key] = value
            
            # Save updated config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            self._log_audit_event("CONFIG_UPDATED", f"Configuration updated: {list(updates.keys())}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating config: {e}")
            return False
    
    def _get_cycles_today(self) -> int:
        """Get number of cycles executed today."""
        # This would need to be implemented based on actual cycle tracking
        return self.state.get('performance_metrics', {}).get('cycles_today', 0)
    
    def _get_expected_cycles_today(self) -> int:
        """Get expected number of cycles for today."""
        interval_hours = self.config.get('autonomous_operation', {}).get('cycle_interval_hours', 1)
        hours_elapsed = datetime.now().hour
        return int(hours_elapsed / interval_hours) if interval_hours > 0 else 0
    
    def _calculate_uptime_hours(self) -> float:
        """Calculate system uptime in hours."""
        # Simplified calculation - in production this would track actual start time
        return 24.0  # Placeholder
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} CONTROL_INTERFACE {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for control operations
if __name__ == "__main__":
    import sys
    
    control = ControlInterface()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "dashboard":
            print("📊 AUTONOMOUS EXPANSION PROTOCOL DASHBOARD")
            print("=" * 60)
            
            data = control.get_dashboard_data()
            
            if 'error' in data:
                print(f"❌ Error: {data['error']}")
            else:
                # Protocol Status
                print("🤖 PROTOCOL STATUS")
                print(f"   State: {data['protocol_status']['state']}")
                print(f"   Cycles Completed: {data['protocol_status']['cycles_completed']}")
                print(f"   Cycles Today: {data['protocol_status']['cycles_today']}")
                print(f"   Error Rate: {data['protocol_status']['error_rate']:.1f}%")
                print()
                
                # Ecosystem Health
                print("🌐 ECOSYSTEM HEALTH")
                print(f"   Total Agents: {data['ecosystem_health']['total_agents']}")
                print(f"   Created Today: {data['ecosystem_health']['agents_today']}")
                print(f"   Created This Week: {data['ecosystem_health']['agents_week']}")
                print(f"   Domains Covered: {data['ecosystem_health']['domains_covered']}")
                print(f"   Average Quality: {data['ecosystem_health']['average_quality']:.3f}")
                print(f"   Growth Rate: {data['ecosystem_health']['growth_rate']:.2f} agents/day")
                print(f"   Coverage: {data['ecosystem_health']['coverage_percentage']:.1f}%")
                print()
                
                # Performance
                print("📈 PERFORMANCE METRICS")
                print(f"   Success Rate: {data['performance_metrics']['success_rate']:.1f}%")
                print(f"   Efficiency Score: {data['performance_metrics']['efficiency_score']:.3f}")
                print(f"   Average Duration: {data['performance_metrics']['average_duration']:.1f} min")
                print(f"   Cycles Per Day: {data['performance_metrics']['cycles_per_day']:.1f}")
                print()
                
                # Alerts
                print("🚨 ALERTS")
                print(f"   Active Alerts: {data['alerts']['total_active']}")
                print(f"   Critical: {data['alerts']['critical']}")
                print(f"   High: {data['alerts']['high']}")
                print(f"   Medium: {data['alerts']['medium']}")
                
                if data['alerts']['recent']:
                    print("   Recent Alerts:")
                    for alert in data['alerts']['recent']:
                        print(f"     - [{alert['severity']}] {alert['title']}")
        
        elif command == "start":
            print("Starting monitoring...")
            success = control.start_monitoring()
            if success:
                print("✅ Monitoring started")
            else:
                print("❌ Failed to start monitoring")
        
        elif command == "stop":
            print("Stopping monitoring...")
            success = control.stop_monitoring()
            if success:
                print("✅ Monitoring stopped")
            else:
                print("❌ Failed to stop monitoring")
        
        elif command == "control":
            if len(sys.argv) > 2:
                control_cmd = sys.argv[2]
                result = control.execute_control_command(control_cmd)
                print(f"Command result: {result['message']}")
            else:
                print("Available control commands: start_protocol, stop_protocol, emergency_stop, clear_alerts, force_cycle")
        
        else:
            print("Usage: python control_interface.py [dashboard|start|stop|control <command>]")
    else:
        print("Control Interface initialized")
        print("Commands: dashboard, start, stop, control")
