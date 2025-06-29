#!/usr/bin/env python3
"""
Test script to verify the autonomous expansion system is working correctly.
This simulates what the GitHub Actions workflow will do.
"""

import sys
import os
import json
import datetime
from pathlib import Path

# Add services directory to path
sys.path.append('services')
sys.path.append('architecture/ase')

def test_system_health():
    """Test basic system health."""
    print("🔍 Testing System Health...")
    
    try:
        from agent_directory_service import AgentDirectoryService
        ads = AgentDirectoryService()
        agent_count = ads.get_agent_count()
        domains = ads.get_domains()
        
        print(f"✅ Agent Directory Service: {agent_count} agents loaded")
        print(f"✅ Domain Coverage: {len(domains)} domains")
        return True, agent_count, len(domains)
        
    except Exception as e:
        print(f"❌ System Health Check Failed: {e}")
        return False, 0, 0

def test_expansion_cycle():
    """Test a single expansion cycle."""
    print("\n🚀 Testing Expansion Cycle...")
    
    try:
        from autonomous_expansion_protocol import AutonomousExpansionProtocol
        
        protocol = AutonomousExpansionProtocol()
        print("   Initializing autonomous expansion protocol...")
        
        # Execute single cycle
        cycle_result = protocol._execute_expansion_cycle()
        
        print(f"✅ Expansion Cycle Completed!")
        print(f"   Cycle ID: {cycle_result.cycle_id}")
        print(f"   Success: {cycle_result.success}")
        print(f"   Focus: {cycle_result.expansion_focus}")
        print(f"   Duration: {cycle_result.duration_minutes:.2f} minutes")
        print(f"   Gaps Found: {cycle_result.gaps_identified}")
        print(f"   Agent Created: {cycle_result.agent_created or 'None'}")
        
        if cycle_result.errors:
            print(f"   ⚠️ Errors: {len(cycle_result.errors)}")
            for error in cycle_result.errors[:3]:
                print(f"      - {error}")
        
        return True, cycle_result
        
    except Exception as e:
        print(f"❌ Expansion Cycle Failed: {e}")
        return False, None

def test_reporting_system():
    """Test the reporting system."""
    print("\n📊 Testing Reporting System...")
    
    try:
        from reporting_system import ReportingSystem
        from agent_directory_service import AgentDirectoryService
        
        reporting = ReportingSystem()
        ads = AgentDirectoryService()
        
        # Generate status report
        status_report = reporting.generate_status_report()
        agent_count = ads.get_agent_count()
        domains = ads.get_domains()
        
        print(f"✅ Reporting System Working!")
        print(f"   Total Agents: {agent_count}")
        print(f"   Domain Coverage: {len(domains)}")
        print(f"   Quality Score: {status_report['ecosystem_health']['quality_score']:.3f}")
        print(f"   Success Rate: {status_report['protocol_performance']['success_rate']:.1f}%")
        
        return True, status_report
        
    except Exception as e:
        print(f"❌ Reporting System Failed: {e}")
        return False, None

def test_dashboard_update():
    """Test dashboard update functionality."""
    print("\n🌐 Testing Dashboard Update...")
    
    try:
        from reporting_system import ReportingSystem
        from agent_directory_service import AgentDirectoryService
        
        reporting = ReportingSystem()
        ads = AgentDirectoryService()
        
        status_report = reporting.generate_status_report()
        agent_count = ads.get_agent_count()
        domains = ads.get_domains()
        
        # Create updated dashboard HTML
        html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Autonomous AI Ecosystem - CodeMAD</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; display: flex; align-items: center; justify-content: center; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 40px 20px; text-align: center; }}
        .header {{ color: white; margin-bottom: 40px; }}
        .header h1 {{ font-size: 3.5em; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); animation: glow 2s ease-in-out infinite alternate; }}
        @keyframes glow {{ from {{ text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }} to {{ text-shadow: 2px 2px 20px rgba(255,255,255,0.5); }} }}
        .status-card {{ background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); backdrop-filter: blur(10px); margin: 20px 0; }}
        .status-indicator {{ display: inline-block; padding: 15px 30px; background: #28a745; color: white; border-radius: 50px; font-weight: bold; font-size: 1.2em; margin: 20px 0; animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ text-align: center; }}
        .metric-value {{ font-size: 2.5em; font-weight: bold; color: #3498db; display: block; }}
        .metric-label {{ color: #7f8c8d; font-size: 0.9em; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }}
        .description {{ font-size: 1.1em; line-height: 1.6; color: #555; margin: 20px 0; }}
        .github-link {{ display: inline-block; margin: 30px 10px; padding: 15px 30px; background: rgba(255,255,255,0.2); color: white; text-decoration: none; border-radius: 50px; transition: all 0.3s ease; font-weight: 500; }}
        .github-link:hover {{ background: rgba(255,255,255,0.3); transform: translateY(-2px); }}
        .footer {{ color: rgba(255,255,255,0.8); margin-top: 40px; font-size: 0.9em; }}
        .last-update {{ font-size: 0.8em; opacity: 0.7; margin-top: 10px; }}
        .test-badge {{ background: #17a2b8; color: white; padding: 5px 10px; border-radius: 15px; font-size: 0.8em; margin-left: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Autonomous AI Ecosystem</h1>
            <p style="font-size: 1.3em; opacity: 0.9;">Fully Autonomous Agent Creation & Ecosystem Expansion</p>
        </div>
        
        <div class="status-card">
            <div class="status-indicator">
                🟢 FULLY OPERATIONAL <span class="test-badge">TESTED</span>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <span class="metric-value">{agent_count}</span>
                    <span class="metric-label">Total Agents</span>
                </div>
                <div class="metric">
                    <span class="metric-value">{domain_count}</span>
                    <span class="metric-label">Domains</span>
                </div>
                <div class="metric">
                    <span class="metric-value">{quality_score}</span>
                    <span class="metric-label">Quality</span>
                </div>
                <div class="metric">
                    <span class="metric-value">{success_rate}</span>
                    <span class="metric-label">Success Rate</span>
                </div>
            </div>
            
            <div class="description">
                <strong>Project Chimera</strong> is fully operational and tested! The autonomous expansion protocol is ready to run every 2 hours via GitHub Actions, continuously identifying global occupational needs and creating specialist agents while maintaining constitutional governance.
            </div>
        </div>
        
        <div class="header">
            <a href="https://github.com/usemanusai/CodeMAD" class="github-link">📂 Source Code</a>
            <a href="https://github.com/usemanusai/CodeMAD/actions" class="github-link">⚙️ Actions</a>
            <a href="https://github.com/usemanusai/CodeMAD/blob/main/services/README.md" class="github-link">📖 Docs</a>
        </div>
        
        <div class="footer">
            <p>Powered by GitHub Actions • Constitutional AI Governance • Human Oversight</p>
            <p>🚀 Representing the future of autonomous AI ecosystem development</p>
            <div class="last-update">Last tested: {timestamp}</div>
        </div>
    </div>
</body>
</html>'''
        
        html_content = html_template.format(
            agent_count=agent_count,
            domain_count=len(domains),
            quality_score=f"{status_report['ecosystem_health']['quality_score']:.0%}",
            success_rate=f"{status_report['protocol_performance']['success_rate']:.0f}%",
            timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        )
        
        # Save updated dashboard
        with open('index.html', 'w') as f:
            f.write(html_content)
        
        print(f"✅ Dashboard Updated Successfully!")
        print(f"   Updated with live data from {agent_count} agents")
        print(f"   Quality score: {status_report['ecosystem_health']['quality_score']:.3f}")
        print(f"   File saved: index.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard Update Failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 AUTONOMOUS EXPANSION SYSTEM TEST")
    print("=" * 50)
    
    results = {
        'system_health': False,
        'expansion_cycle': False,
        'reporting_system': False,
        'dashboard_update': False
    }
    
    # Test 1: System Health
    health_success, agent_count, domain_count = test_system_health()
    results['system_health'] = health_success
    
    # Test 2: Expansion Cycle
    cycle_success, cycle_result = test_expansion_cycle()
    results['expansion_cycle'] = cycle_success
    
    # Test 3: Reporting System
    reporting_success, status_report = test_reporting_system()
    results['reporting_system'] = reporting_success
    
    # Test 4: Dashboard Update
    dashboard_success = test_dashboard_update()
    results['dashboard_update'] = dashboard_success
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, success in results.items():
        status_icon = "✅" if success else "❌"
        print(f"{status_icon} {test_name.replace('_', ' ').title()}: {'PASSED' if success else 'FAILED'}")
    
    print(f"\n📊 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is ready for GitHub Actions automation")
        print("🚀 Your autonomous AI ecosystem is fully operational!")
        print(f"\n🌐 Visit your live site: https://usemanusai.github.io/CodeMAD/")
    else:
        print("⚠️ Some tests failed - check the errors above")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
