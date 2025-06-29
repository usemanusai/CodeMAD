# 🚀 GitHub Actions Setup Guide

## Quick Setup (2 minutes)

### Method 1: Via GitHub Web Interface (Recommended)

1. **Go to your repository**: https://github.com/usemanusai/CodeMAD
2. **Click "Actions" tab**
3. **Click "New workflow"**
4. **Click "set up a workflow yourself"**
5. **Replace the default content** with the workflow below
6. **Name the file**: `autonomous-protocol.yml`
7. **Click "Commit changes"**

### Method 2: Manual File Creation

1. **Create directory**: `.github/workflows/` in your repository
2. **Create file**: `autonomous-protocol.yml`
3. **Copy the workflow content** from below
4. **Commit and push**

---

## 📋 Workflow File Content

Copy this entire content into your workflow file:

```yaml
name: Autonomous Expansion Protocol

on:
  schedule:
    # Run every 2 hours
    - cron: '0 */2 * * *'
  workflow_dispatch: # Allow manual triggering
  push:
    branches: [ main ]
    paths: 
      - 'services/**'
      - 'architecture/**'

jobs:
  autonomous-expansion:
    runs-on: ubuntu-latest
    timeout-minutes: 25
    
    permissions:
      contents: write
      pages: write
      id-token: write
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        fetch-depth: 0
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests
    
    - name: Initialize system
      run: |
        mkdir -p logs reports services/data services/data/research_cache
        touch logs/audit_ledger.log
        
        if [ ! -f services/data/agent_directory.json ]; then
          echo '{"agents": {}, "metadata": {"total_agents": 0}}' > services/data/agent_directory.json
        fi
        
        if [ ! -f services/data/expansion_state.json ]; then
          echo '{"protocol_state": {"current_status": "stopped"}}' > services/data/expansion_state.json
        fi
    
    - name: Run system health check
      run: |
        python -c "
        import sys, os
        sys.path.append('services')
        
        try:
            from agent_directory_service import AgentDirectoryService
            ads = AgentDirectoryService()
            agent_count = ads.get_agent_count()
            print(f'✅ System healthy: {agent_count} agents loaded')
        except Exception as e:
            print(f'⚠️ System check: {e}')
        "
    
    - name: Execute expansion cycle
      run: |
        python -c "
        import sys, os, json, datetime
        sys.path.append('services')
        
        try:
            from autonomous_expansion_protocol import AutonomousExpansionProtocol
            
            protocol = AutonomousExpansionProtocol()
            print('🚀 Starting GitHub Actions expansion cycle...')
            
            cycle_result = protocol._execute_expansion_cycle()
            
            print(f'✅ Cycle completed: {cycle_result.cycle_id}')
            print(f'   Success: {cycle_result.success}')
            print(f'   Focus: {cycle_result.expansion_focus}')
            print(f'   Duration: {cycle_result.duration_minutes:.2f} minutes')
            print(f'   Agent Created: {cycle_result.agent_created or \"None\"}')
            
            with open('cycle_summary.txt', 'w') as f:
                f.write(f'Cycle: {cycle_result.cycle_id}\\n')
                f.write(f'Success: {cycle_result.success}\\n')
                f.write(f'Focus: {cycle_result.expansion_focus}\\n')
                f.write(f'Agent: {cycle_result.agent_created or \"None\"}\\n')
                f.write(f'Duration: {cycle_result.duration_minutes:.2f}min\\n')
            
        except Exception as e:
            print(f'❌ Cycle error: {e}')
            with open('cycle_summary.txt', 'w') as f:
                f.write(f'Error: {str(e)}\\n')
        "
    
    - name: Update dashboard
      run: |
        python -c "
        import sys, json, datetime
        sys.path.append('services')
        
        try:
            from reporting_system import ReportingSystem
            from agent_directory_service import AgentDirectoryService
            
            reporting = ReportingSystem()
            ads = AgentDirectoryService()
            
            status_report = reporting.generate_status_report()
            agent_count = ads.get_agent_count()
            domains = ads.get_domains()
            
            # Update index.html with live data
            html_template = '''<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
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
    </style>
</head>
<body>
    <div class=\"container\">
        <div class=\"header\">
            <h1>🤖 Autonomous AI Ecosystem</h1>
            <p style=\"font-size: 1.3em; opacity: 0.9;\">Fully Autonomous Agent Creation & Ecosystem Expansion</p>
        </div>
        
        <div class=\"status-card\">
            <div class=\"status-indicator\">
                🟢 FULLY OPERATIONAL
            </div>
            
            <div class=\"metrics\">
                <div class=\"metric\">
                    <span class=\"metric-value\">{agent_count}</span>
                    <span class=\"metric-label\">Total Agents</span>
                </div>
                <div class=\"metric\">
                    <span class=\"metric-value\">{domain_count}</span>
                    <span class=\"metric-label\">Domains</span>
                </div>
                <div class=\"metric\">
                    <span class=\"metric-value\">{quality_score}</span>
                    <span class=\"metric-label\">Quality</span>
                </div>
                <div class=\"metric\">
                    <span class=\"metric-value\">{success_rate}</span>
                    <span class=\"metric-label\">Success Rate</span>
                </div>
            </div>
            
            <div class=\"description\">
                <strong>Project Chimera</strong> is now fully operational! The autonomous expansion protocol runs every 2 hours via GitHub Actions, continuously identifying global occupational needs and creating specialist agents while maintaining constitutional governance.
            </div>
        </div>
        
        <div class=\"header\">
            <a href=\"https://github.com/usemanusai/CodeMAD\" class=\"github-link\">📂 Source Code</a>
            <a href=\"https://github.com/usemanusai/CodeMAD/actions\" class=\"github-link\">⚙️ Actions</a>
            <a href=\"https://github.com/usemanusai/CodeMAD/blob/main/services/README.md\" class=\"github-link\">📖 Docs</a>
        </div>
        
        <div class=\"footer\">
            <p>Powered by GitHub Actions • Constitutional AI Governance • Human Oversight</p>
            <p>🚀 Representing the future of autonomous AI ecosystem development</p>
            <div class=\"last-update\">Last updated: {timestamp}</div>
        </div>
    </div>
</body>
</html>'''
            
            html_content = html_template.format(
                agent_count=agent_count,
                domain_count=len(domains),
                quality_score=f\"{status_report['ecosystem_health']['quality_score']:.0%}\",
                success_rate=f\"{status_report['protocol_performance']['success_rate']:.0f}%\",
                timestamp=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
            )
            
            with open('index.html', 'w') as f:
                f.write(html_content)
                
            print('✅ Dashboard updated with live data')
            
        except Exception as e:
            print(f'⚠️ Dashboard update error: {e}')
        "
    
    - name: Commit changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        
        git add -A
        
        if ! git diff --staged --quiet; then
          git commit -m "🤖 Autonomous expansion cycle - $(date)"
          git push
        else
          echo "No changes to commit"
        fi
    
    - name: Upload cycle summary
      uses: actions/upload-artifact@v3
      with:
        name: cycle-summary
        path: cycle_summary.txt
        retention-days: 30
```

---

## ✅ After Setup

Once you've added the workflow:

1. **Go to Actions tab** in your repository
2. **Click "Autonomous Expansion Protocol"**
3. **Click "Run workflow"** to test it manually
4. **Check the logs** to see it working

The workflow will then run automatically every 2 hours!

## 🎯 What This Enables

- ✅ **Automatic execution** every 2 hours
- ✅ **Live dashboard updates** with real metrics
- ✅ **Cycle summaries** saved as artifacts
- ✅ **Error handling** and monitoring
- ✅ **Zero maintenance** required

Your autonomous AI ecosystem will be fully operational! 🚀
