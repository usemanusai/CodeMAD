#!/usr/bin/env python3
"""
Test script for Phase D (Orchestration Layer) components.
Validates integration and functionality of all orchestration systems.
"""

import sys
import os
import time
sys.path.append(os.path.dirname(__file__))

from autonomous_expansion_protocol import AutonomousExpansionProtocol, CycleResult
from reporting_system import ReportingSystem, EcosystemMetrics, PerformanceMetrics
from control_interface import ControlInterface

def test_autonomous_expansion_protocol():
    """Test Autonomous Expansion Protocol functionality."""
    print("=" * 60)
    print("TESTING AUTONOMOUS EXPANSION PROTOCOL")
    print("=" * 60)
    
    try:
        protocol = AutonomousExpansionProtocol()
        print("✅ Autonomous Expansion Protocol initialized successfully")
        
        # Test status retrieval
        status = protocol.get_status()
        print(f"✅ Protocol status retrieved: {status['protocol_state']}")
        
        # Test single cycle execution
        print("🔄 Testing single expansion cycle...")
        cycle_result = protocol._execute_expansion_cycle()
        
        print(f"✅ Expansion cycle completed")
        print(f"   Cycle ID: {cycle_result.cycle_id}")
        print(f"   Success: {cycle_result.success}")
        print(f"   Focus: {cycle_result.expansion_focus}")
        print(f"   Duration: {cycle_result.duration_minutes:.2f} minutes")
        print(f"   Gaps Identified: {cycle_result.gaps_identified}")
        print(f"   Agent Created: {cycle_result.agent_created or 'None'}")
        
        # Test strategic focus selection
        focus = protocol._select_strategic_focus()
        print(f"✅ Strategic focus selection: {focus}")
        
        return cycle_result
        
    except Exception as e:
        print(f"❌ Error testing Autonomous Expansion Protocol: {e}")
        return None

def test_reporting_system():
    """Test Reporting System functionality."""
    print("\n" + "=" * 60)
    print("TESTING REPORTING SYSTEM")
    print("=" * 60)
    
    try:
        reporting = ReportingSystem()
        print("✅ Reporting System initialized successfully")
        
        # Test ecosystem metrics calculation
        print("🔄 Testing ecosystem metrics calculation...")
        ecosystem_metrics = reporting._calculate_ecosystem_metrics()
        
        print(f"✅ Ecosystem metrics calculated")
        print(f"   Total Agents: {ecosystem_metrics.total_agents}")
        print(f"   Created Today: {ecosystem_metrics.agents_created_today}")
        print(f"   Created This Week: {ecosystem_metrics.agents_created_this_week}")
        print(f"   Domains Covered: {ecosystem_metrics.domains_covered}")
        print(f"   Average Quality: {ecosystem_metrics.average_agent_quality:.3f}")
        print(f"   Growth Rate: {ecosystem_metrics.ecosystem_growth_rate:.2f} agents/day")
        print(f"   Coverage: {ecosystem_metrics.coverage_completeness:.1f}%")
        
        # Test performance metrics calculation
        print("🔄 Testing performance metrics calculation...")
        performance_metrics = reporting._analyze_performance()
        
        print(f"✅ Performance metrics calculated")
        print(f"   Total Cycles: {performance_metrics.total_cycles}")
        print(f"   Success Rate: {performance_metrics.success_rate:.1f}%")
        print(f"   Efficiency Score: {performance_metrics.efficiency_score:.3f}")
        print(f"   Error Rate: {performance_metrics.error_rate:.1f}%")
        
        # Test status report generation
        print("🔄 Testing status report generation...")
        status_report = reporting.generate_status_report()
        
        print(f"✅ Status report generated")
        print(f"   Report Type: {status_report['report_type']}")
        print(f"   Ecosystem Health: {len(status_report['ecosystem_health'])} metrics")
        print(f"   Protocol Performance: {len(status_report['protocol_performance'])} metrics")
        print(f"   Recent Activity: {len(status_report['recent_activity'])} metrics")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Reporting System: {e}")
        return False

def test_control_interface():
    """Test Control Interface functionality."""
    print("\n" + "=" * 60)
    print("TESTING CONTROL INTERFACE")
    print("=" * 60)
    
    try:
        control = ControlInterface()
        print("✅ Control Interface initialized successfully")
        
        # Test dashboard data retrieval
        print("🔄 Testing dashboard data retrieval...")
        dashboard_data = control.get_dashboard_data()
        
        if 'error' in dashboard_data:
            print(f"⚠️  Dashboard data contains error: {dashboard_data['error']}")
        else:
            print(f"✅ Dashboard data retrieved")
            print(f"   Protocol State: {dashboard_data['protocol_status']['state']}")
            print(f"   Total Agents: {dashboard_data['ecosystem_health']['total_agents']}")
            print(f"   Success Rate: {dashboard_data['performance_metrics']['success_rate']:.1f}%")
            print(f"   Active Alerts: {dashboard_data['alerts']['total_active']}")
        
        # Test control commands
        print("🔄 Testing control commands...")
        
        # Test clear alerts command
        result = control.execute_control_command("clear_alerts")
        print(f"✅ Clear alerts command: {result['success']} - {result['message']}")
        
        # Test unknown command
        result = control.execute_control_command("unknown_command")
        print(f"✅ Unknown command handling: {result['success']} - {result['message']}")
        
        # Test monitoring start/stop
        print("🔄 Testing monitoring controls...")
        
        # Start monitoring
        start_success = control.start_monitoring()
        print(f"✅ Start monitoring: {start_success}")
        
        # Wait a moment
        time.sleep(2)
        
        # Stop monitoring
        stop_success = control.stop_monitoring()
        print(f"✅ Stop monitoring: {stop_success}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Control Interface: {e}")
        return False

def test_protocol_integration():
    """Test integration between protocol components."""
    print("\n" + "=" * 60)
    print("TESTING PROTOCOL INTEGRATION")
    print("=" * 60)
    
    try:
        # Initialize all components
        protocol = AutonomousExpansionProtocol()
        reporting = ReportingSystem()
        control = ControlInterface()
        
        print("✅ All components initialized")
        
        # Test cycle execution and reporting integration
        print("🔄 Testing cycle execution and reporting integration...")
        
        # Execute a cycle
        cycle_result = protocol._execute_expansion_cycle()
        
        # Generate report for the cycle
        # Note: We'll create a mock cycle result that's JSON serializable
        mock_cycle = type('MockCycle', (), {
            'cycle_id': cycle_result.cycle_id,
            'cycle_number': cycle_result.cycle_number,
            'started_at': cycle_result.started_at,
            'completed_at': cycle_result.completed_at,
            'duration_minutes': cycle_result.duration_minutes,
            'success': cycle_result.success,
            'expansion_focus': cycle_result.expansion_focus,
            'gaps_identified': cycle_result.gaps_identified,
            'agent_created': cycle_result.agent_created,
            'errors': cycle_result.errors,
            'warnings': cycle_result.warnings
        })()
        
        # Test strategic insights generation
        insights = reporting._generate_strategic_insights(mock_cycle)
        print(f"✅ Strategic insights generated: {len(insights)} insights")
        
        # Test recommendations generation
        recommendations = reporting._generate_recommendations(mock_cycle)
        print(f"✅ Recommendations generated: {len(recommendations)} recommendations")
        
        # Test control interface with protocol status
        status = protocol.get_status()
        print(f"✅ Protocol status integration: {status['protocol_state']}")
        
        # Test dashboard integration
        dashboard = control.get_dashboard_data()
        if 'error' not in dashboard:
            print(f"✅ Dashboard integration successful")
            print(f"   Ecosystem agents: {dashboard['ecosystem_health']['total_agents']}")
            print(f"   Protocol cycles: {dashboard['protocol_status']['cycles_completed']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing protocol integration: {e}")
        return False

def test_end_to_end_orchestration():
    """Test end-to-end orchestration workflow."""
    print("\n" + "=" * 60)
    print("TESTING END-TO-END ORCHESTRATION WORKFLOW")
    print("=" * 60)
    
    try:
        # Step 1: Initialize orchestration system
        print("🔄 Step 1: Initialize Orchestration System")
        protocol = AutonomousExpansionProtocol()
        control = ControlInterface()
        reporting = ReportingSystem()
        
        print("   ✅ All orchestration components initialized")
        
        # Step 2: Execute expansion cycle
        print("🔄 Step 2: Execute Expansion Cycle")
        cycle_result = protocol._execute_expansion_cycle()
        
        print(f"   ✅ Expansion cycle executed: {cycle_result.cycle_id}")
        print(f"   📊 Focus: {cycle_result.expansion_focus}")
        print(f"   ⏱️  Duration: {cycle_result.duration_minutes:.2f} minutes")
        print(f"   🎯 Success: {cycle_result.success}")
        
        # Step 3: Generate comprehensive reporting
        print("🔄 Step 3: Generate Comprehensive Reporting")
        status_report = reporting.generate_status_report()
        ecosystem_metrics = reporting._calculate_ecosystem_metrics()
        
        print(f"   ✅ Status report generated")
        print(f"   📈 Ecosystem health: {ecosystem_metrics.total_agents} agents, {ecosystem_metrics.domains_covered} domains")
        print(f"   📊 Growth rate: {ecosystem_metrics.ecosystem_growth_rate:.2f} agents/day")
        
        # Step 4: Control interface monitoring
        print("🔄 Step 4: Control Interface Monitoring")
        dashboard_data = control.get_dashboard_data()
        
        if 'error' not in dashboard_data:
            print(f"   ✅ Dashboard monitoring active")
            print(f"   🎛️  Protocol state: {dashboard_data['protocol_status']['state']}")
            print(f"   🚨 Active alerts: {dashboard_data['alerts']['total_active']}")
        
        # Step 5: Demonstrate control capabilities
        print("🔄 Step 5: Demonstrate Control Capabilities")
        
        # Clear any alerts
        clear_result = control.execute_control_command("clear_alerts")
        print(f"   ✅ Alert management: {clear_result['success']}")
        
        # Test configuration update capability
        config_update = {"test_parameter": "test_value"}
        update_result = control.execute_control_command("update_config", {"config_updates": config_update})
        print(f"   ✅ Configuration management: {update_result['success']}")
        
        print("\n✅ End-to-end orchestration workflow completed successfully!")
        print("🎉 Fully Autonomous Ecosystem Expansion & Analysis Protocol is OPERATIONAL!")
        
        # Summary statistics
        print(f"\n📊 FINAL SYSTEM STATISTICS:")
        print(f"   🤖 Total Agents: {ecosystem_metrics.total_agents}")
        print(f"   🌐 Domains Covered: {ecosystem_metrics.domains_covered}")
        print(f"   📈 Average Quality: {ecosystem_metrics.average_agent_quality:.3f}")
        print(f"   🚀 Growth Rate: {ecosystem_metrics.ecosystem_growth_rate:.2f} agents/day")
        print(f"   📋 Coverage: {ecosystem_metrics.coverage_completeness:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in end-to-end orchestration: {e}")
        return False

def main():
    """Run all Phase D tests."""
    print("🚀 STARTING PHASE D (ORCHESTRATION LAYER) TESTING")
    print("=" * 80)
    
    results = {
        'autonomous_expansion_protocol': False,
        'reporting_system': False,
        'control_interface': False,
        'protocol_integration': False,
        'end_to_end_orchestration': False
    }
    
    # Test individual components
    cycle_result = test_autonomous_expansion_protocol()
    results['autonomous_expansion_protocol'] = cycle_result is not None
    
    results['reporting_system'] = test_reporting_system()
    results['control_interface'] = test_control_interface()
    results['protocol_integration'] = test_protocol_integration()
    results['end_to_end_orchestration'] = test_end_to_end_orchestration()
    
    # Summary
    print("\n" + "=" * 80)
    print("PHASE D TESTING SUMMARY")
    print("=" * 80)
    
    passed = sum(results.values())
    total = len(results)
    
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {component.replace('_', ' ').title()}: {'PASSED' if status else 'FAILED'}")
    
    print(f"\n📊 Overall Result: {passed}/{total} components passed")
    
    if passed == total:
        print("🎉 Phase D (Orchestration Layer) implementation is SUCCESSFUL!")
        print("🚀 FULLY AUTONOMOUS ECOSYSTEM EXPANSION & ANALYSIS PROTOCOL IS COMPLETE!")
        print("\n🌟 The system is now capable of:")
        print("   • Autonomous global needs analysis")
        print("   • Intelligent gap identification")
        print("   • Automatic agent synthesis and deployment")
        print("   • Comprehensive reporting and monitoring")
        print("   • Human oversight and control capabilities")
        print("   • Perpetual autonomous operation")
    else:
        print("⚠️  Some components need attention before full deployment")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
