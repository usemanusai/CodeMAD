#!/usr/bin/env python3
"""
Reporting & Analysis System for Project Chimera
Generates comprehensive reports and analytics for the autonomous expansion protocol.
Tracks performance, progress, and provides strategic insights.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
import sys

# Add services directory to path for imports
sys.path.append(os.path.dirname(__file__))

@dataclass
class EcosystemMetrics:
    """Ecosystem health and performance metrics."""
    total_agents: int
    agents_created_today: int
    agents_created_this_week: int
    agents_created_this_month: int
    domains_covered: int
    average_agent_quality: float
    ecosystem_growth_rate: float
    coverage_completeness: float

@dataclass
class PerformanceMetrics:
    """Protocol performance metrics."""
    total_cycles: int
    successful_cycles: int
    failed_cycles: int
    success_rate: float
    average_cycle_duration: float
    cycles_per_day: float
    error_rate: float
    efficiency_score: float

class ReportingSystem:
    """
    Comprehensive reporting and analysis system for autonomous expansion protocol.
    Generates insights, tracks performance, and provides strategic recommendations.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.config_file = self.workspace_root / "services" / "config" / "expansion_config.json"
        self.state_file = self.workspace_root / "services" / "data" / "expansion_state.json"
        self.reports_dir = self.workspace_root / "reports"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Create reports directory
        self.reports_dir.mkdir(exist_ok=True)
        
        # Load configuration and state
        self.config = self._load_config()
        self.state = self._load_state()
        
        # Initialize agent directory service
        from agent_directory_service import AgentDirectoryService
        self.agent_directory = AgentDirectoryService(workspace_root)
    
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
    
    def generate_cycle_report(self, cycle_result: Any) -> Dict[str, Any]:
        """Generate comprehensive report for a completed cycle."""
        self.logger.info(f"Generating cycle report for: {cycle_result.cycle_id}")
        
        report = {
            'report_id': f"cycle_report_{cycle_result.cycle_id}",
            'generated_at': datetime.now().isoformat(),
            'cycle_summary': self._generate_cycle_summary(cycle_result),
            'ecosystem_metrics': self._calculate_ecosystem_metrics(),
            'performance_analysis': self._analyze_performance(),
            'strategic_insights': self._generate_strategic_insights(cycle_result),
            'recommendations': self._generate_recommendations(cycle_result),
            'next_actions': self._determine_next_actions(cycle_result)
        }
        
        # Save report to file
        self._save_report(report)
        
        # Log report generation
        self._log_audit_event("CYCLE_REPORT_GENERATED", f"Report generated for cycle {cycle_result.cycle_number}")
        
        return report
    
    def _generate_cycle_summary(self, cycle_result: Any) -> Dict[str, Any]:
        """Generate summary of cycle execution."""
        return {
            'cycle_id': cycle_result.cycle_id,
            'cycle_number': cycle_result.cycle_number,
            'execution_time': {
                'started_at': cycle_result.started_at,
                'completed_at': cycle_result.completed_at,
                'duration_minutes': cycle_result.duration_minutes
            },
            'results': {
                'success': cycle_result.success,
                'expansion_focus': cycle_result.expansion_focus,
                'gaps_identified': cycle_result.gaps_identified,
                'agent_created': cycle_result.agent_created,
                'errors_count': len(cycle_result.errors),
                'warnings_count': len(cycle_result.warnings)
            },
            'quality_indicators': {
                'execution_efficiency': self._calculate_execution_efficiency(cycle_result),
                'outcome_quality': self._assess_outcome_quality(cycle_result),
                'strategic_alignment': self._assess_strategic_alignment(cycle_result)
            }
        }
    
    def _calculate_ecosystem_metrics(self) -> EcosystemMetrics:
        """Calculate current ecosystem health metrics."""
        # Get current agent count and details
        total_agents = self.agent_directory.get_agent_count()
        all_agents = self.agent_directory.get_all_agents()
        
        # Calculate time-based metrics
        now = datetime.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        agents_today = 0
        agents_week = 0
        agents_month = 0
        quality_scores = []
        
        for agent in all_agents.values():
            created_date_str = agent.get('created_date')
            if created_date_str:
                try:
                    created_date = datetime.fromisoformat(created_date_str).date()
                    
                    if created_date == today:
                        agents_today += 1
                    if datetime.fromisoformat(created_date_str) >= week_ago:
                        agents_week += 1
                    if datetime.fromisoformat(created_date_str) >= month_ago:
                        agents_month += 1
                        
                except ValueError:
                    pass
            
            # Collect quality scores
            quality_score = agent.get('quality_score')
            if quality_score:
                quality_scores.append(quality_score)
        
        # Calculate domain coverage
        domains = self.agent_directory.get_domains()
        domains_covered = len(domains)
        
        # Calculate averages
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        # Calculate growth rate (agents per week)
        growth_rate = agents_week / 7.0 if agents_week > 0 else 0.0
        
        # Estimate coverage completeness (simplified)
        estimated_total_occupations = 1000  # Rough estimate
        coverage_completeness = min(100.0, (total_agents / estimated_total_occupations) * 100)
        
        return EcosystemMetrics(
            total_agents=total_agents,
            agents_created_today=agents_today,
            agents_created_this_week=agents_week,
            agents_created_this_month=agents_month,
            domains_covered=domains_covered,
            average_agent_quality=avg_quality,
            ecosystem_growth_rate=growth_rate,
            coverage_completeness=coverage_completeness
        )
    
    def _analyze_performance(self) -> PerformanceMetrics:
        """Analyze protocol performance metrics."""
        # Get performance data from state
        perf_data = self.state.get('performance_metrics', {})
        
        total_cycles = perf_data.get('total_cycles_completed', 0)
        total_agents_created = perf_data.get('total_agents_created', 0)
        avg_duration = perf_data.get('average_cycle_duration_minutes', 0)
        
        # Calculate error metrics
        error_data = self.state.get('error_tracking', {})
        total_errors = error_data.get('total_errors', 0)
        
        # Calculate rates
        success_rate = ((total_cycles - total_errors) / total_cycles * 100) if total_cycles > 0 else 100.0
        error_rate = (total_errors / total_cycles * 100) if total_cycles > 0 else 0.0
        
        # Calculate efficiency (agents created per cycle)
        efficiency_score = (total_agents_created / total_cycles) if total_cycles > 0 else 0.0
        
        # Estimate cycles per day (based on recent activity)
        cycles_per_day = self._estimate_cycles_per_day()
        
        return PerformanceMetrics(
            total_cycles=total_cycles,
            successful_cycles=total_cycles - total_errors,
            failed_cycles=total_errors,
            success_rate=success_rate,
            average_cycle_duration=avg_duration or 0.0,
            cycles_per_day=cycles_per_day,
            error_rate=error_rate,
            efficiency_score=efficiency_score
        )
    
    def _generate_strategic_insights(self, cycle_result: Any) -> List[str]:
        """Generate strategic insights from cycle results."""
        insights = []
        
        # Analyze expansion focus effectiveness
        if cycle_result.agent_created:
            insights.append(f"Successfully expanded into {cycle_result.expansion_focus} domain with new {cycle_result.agent_created} agent")
        else:
            insights.append(f"No agent created for {cycle_result.expansion_focus} - may indicate market saturation or high similarity to existing agents")
        
        # Analyze gap identification
        if cycle_result.gaps_identified == 0:
            insights.append("No gaps identified - consider expanding research scope or exploring new domains")
        elif cycle_result.gaps_identified > 5:
            insights.append(f"High number of gaps identified ({cycle_result.gaps_identified}) - rich opportunity space in this domain")
        
        # Performance insights
        ecosystem_metrics = self._calculate_ecosystem_metrics()
        if ecosystem_metrics.ecosystem_growth_rate > 1.0:
            insights.append("High ecosystem growth rate indicates strong expansion momentum")
        elif ecosystem_metrics.ecosystem_growth_rate < 0.1:
            insights.append("Low growth rate - may need to adjust strategy or explore new domains")
        
        # Quality insights
        if ecosystem_metrics.average_agent_quality > 0.9:
            insights.append("Excellent agent quality maintained - synthesis engine performing optimally")
        elif ecosystem_metrics.average_agent_quality < 0.7:
            insights.append("Agent quality below optimal - consider reviewing synthesis parameters")
        
        return insights
    
    def _generate_recommendations(self, cycle_result: Any) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Performance-based recommendations
        if cycle_result.errors:
            recommendations.append("Review and address cycle errors to improve success rate")
        
        if cycle_result.duration_minutes > 60:
            recommendations.append("Cycle duration exceeding 1 hour - consider optimizing research processes")
        
        # Strategic recommendations
        ecosystem_metrics = self._calculate_ecosystem_metrics()
        
        if ecosystem_metrics.domains_covered < 20:
            recommendations.append("Expand domain coverage to increase ecosystem diversity")
        
        if ecosystem_metrics.coverage_completeness < 10:
            recommendations.append("Focus on high-impact domains to accelerate coverage growth")
        
        # Operational recommendations
        if cycle_result.gaps_identified == 0:
            recommendations.append("Consider adjusting gap analysis thresholds or exploring emerging domains")
        
        return recommendations
    
    def _determine_next_actions(self, cycle_result: Any) -> List[str]:
        """Determine specific next actions for the protocol."""
        actions = []
        
        # Immediate actions based on cycle results
        if cycle_result.agent_created:
            actions.append(f"Monitor integration and performance of new agent: {cycle_result.agent_created}")
        
        if cycle_result.errors:
            actions.append("Investigate and resolve cycle errors before next execution")
        
        # Strategic actions
        ecosystem_metrics = self._calculate_ecosystem_metrics()
        
        if ecosystem_metrics.agents_created_today == 0:
            actions.append("Prioritize agent creation in next cycle to maintain growth momentum")
        
        # Maintenance actions
        if ecosystem_metrics.total_agents % 50 == 0:  # Every 50 agents
            actions.append("Conduct ecosystem health assessment and optimization review")
        
        return actions
    
    def generate_status_report(self) -> Dict[str, Any]:
        """Generate current status report."""
        ecosystem_metrics = self._calculate_ecosystem_metrics()
        performance_metrics = self._analyze_performance()
        
        return {
            'report_type': 'status_report',
            'generated_at': datetime.now().isoformat(),
            'ecosystem_health': {
                'total_agents': ecosystem_metrics.total_agents,
                'growth_rate': ecosystem_metrics.ecosystem_growth_rate,
                'quality_score': ecosystem_metrics.average_agent_quality,
                'domain_coverage': ecosystem_metrics.domains_covered,
                'coverage_percentage': ecosystem_metrics.coverage_completeness
            },
            'protocol_performance': {
                'success_rate': performance_metrics.success_rate,
                'efficiency_score': performance_metrics.efficiency_score,
                'cycles_completed': performance_metrics.total_cycles,
                'error_rate': performance_metrics.error_rate
            },
            'recent_activity': {
                'agents_today': ecosystem_metrics.agents_created_today,
                'agents_this_week': ecosystem_metrics.agents_created_this_week,
                'cycles_per_day': performance_metrics.cycles_per_day
            }
        }
    
    def _calculate_execution_efficiency(self, cycle_result: Any) -> float:
        """Calculate execution efficiency score."""
        base_score = 1.0
        
        # Penalize for errors
        if cycle_result.errors:
            base_score -= len(cycle_result.errors) * 0.1
        
        # Penalize for long duration
        if cycle_result.duration_minutes > 30:
            base_score -= 0.1
        
        # Bonus for agent creation
        if cycle_result.agent_created:
            base_score += 0.2
        
        return max(0.0, min(1.0, base_score))
    
    def _assess_outcome_quality(self, cycle_result: Any) -> float:
        """Assess quality of cycle outcomes."""
        if cycle_result.agent_created:
            return 1.0  # Successful agent creation
        elif cycle_result.gaps_identified > 0:
            return 0.7  # Gaps identified but no agent created
        else:
            return 0.3  # No significant outcomes
    
    def _assess_strategic_alignment(self, cycle_result: Any) -> float:
        """Assess strategic alignment of cycle focus."""
        # High-value domains get higher scores
        high_value_domains = ['ai', 'healthcare', 'cybersecurity', 'renewable energy', 'quantum']
        
        focus_lower = cycle_result.expansion_focus.lower()
        if any(domain in focus_lower for domain in high_value_domains):
            return 1.0
        else:
            return 0.7
    
    def _estimate_cycles_per_day(self) -> float:
        """Estimate cycles per day based on configuration."""
        interval_hours = self.config.get('autonomous_operation', {}).get('cycle_interval_hours', 1)
        return 24.0 / interval_hours if interval_hours > 0 else 0.0
    
    def _save_report(self, report: Dict[str, Any]):
        """Save report to file."""
        try:
            report_file = self.reports_dir / f"{report['report_id']}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Report saved: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} REPORTING_SYSTEM {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    reporting = ReportingSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            print("Generating status report...")
            report = reporting.generate_status_report()
            
            print("📊 ECOSYSTEM STATUS REPORT")
            print("=" * 50)
            print(f"Total Agents: {report['ecosystem_health']['total_agents']}")
            print(f"Growth Rate: {report['ecosystem_health']['growth_rate']:.2f} agents/day")
            print(f"Quality Score: {report['ecosystem_health']['quality_score']:.3f}")
            print(f"Domain Coverage: {report['ecosystem_health']['domain_coverage']} domains")
            print(f"Coverage: {report['ecosystem_health']['coverage_percentage']:.1f}%")
            print()
            print("📈 PROTOCOL PERFORMANCE")
            print("=" * 50)
            print(f"Success Rate: {report['protocol_performance']['success_rate']:.1f}%")
            print(f"Efficiency Score: {report['protocol_performance']['efficiency_score']:.3f}")
            print(f"Cycles Completed: {report['protocol_performance']['cycles_completed']}")
            print(f"Error Rate: {report['protocol_performance']['error_rate']:.1f}%")
            print()
            print("🕒 RECENT ACTIVITY")
            print("=" * 50)
            print(f"Agents Today: {report['recent_activity']['agents_today']}")
            print(f"Agents This Week: {report['recent_activity']['agents_this_week']}")
            print(f"Cycles Per Day: {report['recent_activity']['cycles_per_day']:.1f}")
        
        elif command == "metrics":
            print("Calculating ecosystem metrics...")
            metrics = reporting._calculate_ecosystem_metrics()
            
            print("🌐 ECOSYSTEM METRICS")
            print("=" * 50)
            print(f"Total Agents: {metrics.total_agents}")
            print(f"Created Today: {metrics.agents_created_today}")
            print(f"Created This Week: {metrics.agents_created_this_week}")
            print(f"Created This Month: {metrics.agents_created_this_month}")
            print(f"Domains Covered: {metrics.domains_covered}")
            print(f"Average Quality: {metrics.average_agent_quality:.3f}")
            print(f"Growth Rate: {metrics.ecosystem_growth_rate:.2f} agents/day")
            print(f"Coverage: {metrics.coverage_completeness:.1f}%")
        
        else:
            print("Usage: python reporting_system.py [status|metrics]")
    else:
        print("Reporting System initialized successfully")
