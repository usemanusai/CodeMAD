#!/bin/bash

# Entrypoint script for Chimera Autonomous Expansion Protocol
set -e

echo "🚀 Starting Chimera Autonomous Expansion Protocol"
echo "=================================================="

# Set environment variables
export PYTHONPATH=/app
export WORKSPACE_ROOT=/app

# Initialize logging
echo "📝 Initializing logging system..."
mkdir -p /app/logs
touch /app/logs/audit_ledger.log

# Initialize data directories
echo "📁 Initializing data directories..."
mkdir -p /app/services/data/research_cache
mkdir -p /app/reports
mkdir -p /app/memory

# Check system health
echo "🔍 Performing system health check..."
cd /app

# Test agent directory service
echo "   Testing Agent Directory Service..."
python services/agent_directory_service.py count > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Agent Directory Service: OK"
else
    echo "   ❌ Agent Directory Service: FAILED"
    exit 1
fi

# Test reporting system
echo "   Testing Reporting System..."
python services/reporting_system.py status > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Reporting System: OK"
else
    echo "   ❌ Reporting System: FAILED"
    exit 1
fi

# Test control interface
echo "   Testing Control Interface..."
python services/control_interface.py dashboard > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Control Interface: OK"
else
    echo "   ❌ Control Interface: FAILED"
    exit 1
fi

echo "✅ System health check completed successfully"

# Start based on command
case "$1" in
    "autonomous")
        echo "🤖 Starting Autonomous Expansion Protocol..."
        echo "   Mode: Fully Autonomous"
        echo "   Monitoring: Enabled"
        echo "   Safety: All limits active"
        echo ""
        
        # Start monitoring in background
        echo "📊 Starting monitoring system..."
        python services/control_interface.py start &
        MONITOR_PID=$!
        
        # Wait a moment for monitoring to initialize
        sleep 5
        
        # Start the autonomous protocol
        echo "🚀 Launching autonomous expansion protocol..."
        python services/autonomous_expansion_protocol.py start
        
        # Keep the container running
        echo "🔄 Protocol started. Monitoring operations..."
        
        # Monitor the protocol
        while true; do
            # Check if protocol is still running
            if ! python services/autonomous_expansion_protocol.py status > /dev/null 2>&1; then
                echo "⚠️  Protocol stopped. Attempting restart..."
                python services/autonomous_expansion_protocol.py start
            fi
            
            # Display status every 5 minutes
            sleep 300
            echo "📊 $(date): Protocol Status Check"
            python services/autonomous_expansion_protocol.py status
        done
        ;;
        
    "monitor")
        echo "📊 Starting Monitoring Mode..."
        echo "   Mode: Monitor Only"
        echo "   Protocol: External"
        echo ""
        
        # Start monitoring
        python services/control_interface.py start
        
        # Keep monitoring running
        while true; do
            sleep 60
            echo "📊 $(date): Monitoring active"
            python services/control_interface.py dashboard
        done
        ;;
        
    "test")
        echo "🧪 Running System Tests..."
        echo "   Mode: Testing"
        echo "   Safety: Test mode"
        echo ""
        
        # Run comprehensive tests
        echo "Phase A Tests:"
        python services/agent_directory_service.py count
        
        echo ""
        echo "Phase B Tests:"
        python services/test_phase_b.py
        
        echo ""
        echo "Phase C Tests:"
        python services/test_phase_c.py
        
        echo ""
        echo "Phase D Tests:"
        python services/test_phase_d.py
        
        echo ""
        echo "✅ All tests completed"
        ;;
        
    "dashboard")
        echo "📊 Displaying Dashboard..."
        python services/control_interface.py dashboard
        ;;
        
    "status")
        echo "📊 Protocol Status:"
        python services/autonomous_expansion_protocol.py status
        echo ""
        echo "📊 System Status:"
        python services/reporting_system.py status
        ;;
        
    *)
        echo "Usage: $0 {autonomous|monitor|test|dashboard|status}"
        echo ""
        echo "Commands:"
        echo "  autonomous  - Start full autonomous expansion protocol"
        echo "  monitor     - Start monitoring only (protocol runs externally)"
        echo "  test        - Run comprehensive system tests"
        echo "  dashboard   - Display current dashboard"
        echo "  status      - Show protocol and system status"
        exit 1
        ;;
esac
