#!/usr/bin/env python3
"""
Continuous runner for the Autonomous Expansion Protocol.
Keeps the protocol running in continuous mode with monitoring.
"""

import sys
import os
import time
import signal
import threading
from datetime import datetime

# Add services directory to path
sys.path.append('services')
sys.path.append('architecture/ase')

from autonomous_expansion_protocol import AutonomousExpansionProtocol
from control_interface import ControlInterface
from reporting_system import ReportingSystem

class ContinuousRunner:
    """Continuous runner for the autonomous expansion protocol."""
    
    def __init__(self):
        self.protocol = AutonomousExpansionProtocol()
        self.control = ControlInterface()
        self.reporting = ReportingSystem()
        self.running = False
        self.cycle_count = 0
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received signal {signum}. Shutting down gracefully...")
        self.stop()
    
    def start(self):
        """Start continuous operation."""
        print("🚀 STARTING CHIMERA AUTONOMOUS EXPANSION PROTOCOL")
        print("=" * 60)
        print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔄 Mode: Continuous Operation")
        print("⏱️  Cycle Interval: 2 hours")
        print("🛡️  Safety: All limits active")
        print("📊 Monitoring: Enabled")
        print()
        
        self.running = True
        
        # Start monitoring
        print("📊 Starting monitoring system...")
        monitor_success = self.control.start_monitoring()
        if monitor_success:
            print("✅ Monitoring system started")
        else:
            print("⚠️  Monitoring system failed to start")
        
        print()
        print("🔄 Beginning continuous expansion cycles...")
        print("   Use Ctrl+C to stop gracefully")
        print()
        
        # Main continuous loop
        while self.running:
            try:
                self.cycle_count += 1
                print(f"🚀 STARTING CYCLE {self.cycle_count}")
                print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 40)
                
                # Execute expansion cycle
                cycle_result = self.protocol._execute_expansion_cycle()
                
                # Display cycle results
                print(f"✅ CYCLE {self.cycle_count} COMPLETED")
                print(f"   Success: {cycle_result.success}")
                print(f"   Focus: {cycle_result.expansion_focus}")
                print(f"   Duration: {cycle_result.duration_minutes:.2f} minutes")
                print(f"   Gaps Found: {cycle_result.gaps_identified}")
                print(f"   Agent Created: {cycle_result.agent_created or 'None'}")
                
                if cycle_result.errors:
                    print(f"   ⚠️  Errors: {len(cycle_result.errors)}")
                    for error in cycle_result.errors[:3]:
                        print(f"      - {error}")
                
                # Generate and display brief status
                status_report = self.reporting.generate_status_report()
                ecosystem = status_report['ecosystem_health']
                
                print()
                print("📊 ECOSYSTEM STATUS")
                print(f"   Total Agents: {ecosystem['total_agents']}")
                print(f"   Growth Rate: {ecosystem['growth_rate']:.2f} agents/day")
                print(f"   Quality Score: {ecosystem['quality_score']:.3f}")
                print(f"   Domain Coverage: {ecosystem['domain_coverage']} domains")
                
                print()
                print(f"⏳ Waiting 2 hours before next cycle...")
                print(f"   Next cycle at: {datetime.fromtimestamp(time.time() + 7200).strftime('%Y-%m-%d %H:%M:%S')}")
                print("=" * 60)
                print()
                
                # Wait for next cycle (2 hours = 7200 seconds)
                # Break into smaller intervals to allow for graceful shutdown
                wait_time = 7200  # 2 hours
                interval = 60     # Check every minute
                
                for i in range(0, wait_time, interval):
                    if not self.running:
                        break
                    time.sleep(interval)
                    
                    # Display progress every 30 minutes
                    if i > 0 and i % 1800 == 0:
                        remaining = (wait_time - i) // 60
                        print(f"⏳ {remaining} minutes until next cycle...")
                
            except KeyboardInterrupt:
                print("\n🛑 Keyboard interrupt received")
                break
            except Exception as e:
                print(f"❌ Error in cycle {self.cycle_count}: {e}")
                print("⏳ Waiting 10 minutes before retry...")
                time.sleep(600)  # Wait 10 minutes before retry
        
        self.stop()
    
    def stop(self):
        """Stop continuous operation."""
        print("\n🛑 STOPPING AUTONOMOUS EXPANSION PROTOCOL")
        print("=" * 60)
        
        self.running = False
        
        # Stop monitoring
        print("📊 Stopping monitoring system...")
        monitor_success = self.control.stop_monitoring()
        if monitor_success:
            print("✅ Monitoring system stopped")
        else:
            print("⚠️  Error stopping monitoring system")
        
        # Display final statistics
        print(f"📊 FINAL STATISTICS")
        print(f"   Cycles Completed: {self.cycle_count}")
        print(f"   Runtime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            status_report = self.reporting.generate_status_report()
            ecosystem = status_report['ecosystem_health']
            print(f"   Final Agent Count: {ecosystem['total_agents']}")
            print(f"   Final Domain Coverage: {ecosystem['domain_coverage']}")
        except Exception as e:
            print(f"   Could not retrieve final statistics: {e}")
        
        print("✅ Shutdown complete")

def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            runner = ContinuousRunner()
            runner.start()
        elif command == "status":
            # Quick status check
            protocol = AutonomousExpansionProtocol()
            status = protocol.get_status()
            print("📊 PROTOCOL STATUS")
            print(f"   State: {status['protocol_state']}")
            print(f"   Cycles: {status['cycles_completed']}")
            print(f"   Error Rate: {status['error_rate']:.1f}%")
        elif command == "dashboard":
            # Show dashboard
            control = ControlInterface()
            data = control.get_dashboard_data()
            if 'error' not in data:
                print("📊 DASHBOARD")
                print(f"   Protocol: {data['protocol_status']['state']}")
                print(f"   Agents: {data['ecosystem_health']['total_agents']}")
                print(f"   Success Rate: {data['performance_metrics']['success_rate']:.1f}%")
                print(f"   Alerts: {data['alerts']['total_active']}")
        else:
            print("Usage: python run_continuous.py [start|status|dashboard]")
    else:
        print("Chimera Autonomous Expansion Protocol - Continuous Runner")
        print("Usage: python run_continuous.py [start|status|dashboard]")
        print()
        print("Commands:")
        print("  start     - Start continuous autonomous operation")
        print("  status    - Show current protocol status")
        print("  dashboard - Show system dashboard")

if __name__ == "__main__":
    main()
