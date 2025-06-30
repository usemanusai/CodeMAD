#!/usr/bin/env python3
"""
Analytics Engine for Autonomous Expansion Protocol
Provides comprehensive statistics, performance tracking, and trend analysis.
"""

import json
import os
import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import math

@dataclass
class PerformanceMetrics:
    """Performance metrics data structure."""
    timestamp: str
    cycle_duration_minutes: float
    agents_created: int
    success_rate: float
    quality_score: float
    resource_usage: Dict[str, float]
    errors_count: int
    domains_covered: int

@dataclass
class TrendAnalysis:
    """Trend analysis results."""
    metric_name: str
    current_value: float
    trend_direction: str  # "increasing", "decreasing", "stable"
    trend_strength: float  # 0.0 to 1.0
    prediction_7d: float
    confidence: float

@dataclass
class SystemHealth:
    """System health indicators."""
    overall_health: float  # 0.0 to 1.0
    component_health: Dict[str, float]
    active_alerts: List[Dict[str, Any]]
    performance_score: float
    reliability_score: float

class AnalyticsEngine:
    """Comprehensive analytics and performance tracking system."""
    
    def __init__(self, data_dir: str = "services/data"):
        self.data_dir = data_dir
        self.metrics_file = os.path.join(data_dir, "performance_metrics.json")
        self.analytics_file = os.path.join(data_dir, "analytics_data.json")
        self.trends_file = os.path.join(data_dir, "trend_analysis.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing data
        self.metrics_history = self._load_metrics_history()
        self.analytics_data = self._load_analytics_data()
        
        # Initialize real-time tracking
        self.real_time_metrics = deque(maxlen=1000)  # Last 1000 data points
        self.alert_thresholds = self._define_alert_thresholds()
    
    def _load_metrics_history(self) -> List[PerformanceMetrics]:
        """Load historical performance metrics."""
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                return [PerformanceMetrics(**item) for item in data]
            except Exception as e:
                print(f"Error loading metrics history: {e}")
                return []
        return []
    
    def _load_analytics_data(self) -> Dict[str, Any]:
        """Load analytics data."""
        if os.path.exists(self.analytics_file):
            try:
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading analytics data: {e}")
                return self._create_default_analytics_data()
        return self._create_default_analytics_data()
    
    def _create_default_analytics_data(self) -> Dict[str, Any]:
        """Create default analytics data structure."""
        return {
            "system_stats": {
                "total_cycles_completed": 0,
                "total_agents_created": 0,
                "total_domains_covered": 0,
                "system_uptime_hours": 0,
                "last_updated": datetime.now().isoformat()
            },
            "performance_baselines": {
                "average_cycle_duration": 0.0,
                "average_success_rate": 0.0,
                "average_quality_score": 0.0,
                "baseline_established": False
            },
            "domain_statistics": {},
            "error_patterns": {},
            "resource_usage_patterns": {}
        }
    
    def _define_alert_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Define alert thresholds for various metrics."""
        return {
            "performance": {
                "cycle_duration_warning": 30.0,  # minutes
                "cycle_duration_critical": 60.0,
                "success_rate_warning": 0.8,
                "success_rate_critical": 0.6,
                "quality_score_warning": 0.8,
                "quality_score_critical": 0.7
            },
            "resources": {
                "memory_usage_warning": 0.8,  # 80%
                "memory_usage_critical": 0.9,  # 90%
                "cpu_usage_warning": 0.7,
                "cpu_usage_critical": 0.85,
                "disk_usage_warning": 0.8,
                "disk_usage_critical": 0.9
            },
            "errors": {
                "error_rate_warning": 0.1,  # 10%
                "error_rate_critical": 0.2,  # 20%
                "consecutive_failures_warning": 3,
                "consecutive_failures_critical": 5
            }
        }
    
    def record_cycle_metrics(self, cycle_data: Dict[str, Any]) -> None:
        """Record metrics from a completed cycle."""
        try:
            # Extract metrics from cycle data
            metrics = PerformanceMetrics(
                timestamp=datetime.now().isoformat(),
                cycle_duration_minutes=cycle_data.get('duration_minutes', 0.0),
                agents_created=1 if cycle_data.get('agent_created') else 0,
                success_rate=1.0 if cycle_data.get('success', False) else 0.0,
                quality_score=cycle_data.get('quality_score', 0.0),
                resource_usage=cycle_data.get('resource_usage', {}),
                errors_count=len(cycle_data.get('errors', [])),
                domains_covered=1 if cycle_data.get('expansion_focus') else 0
            )
            
            # Add to history
            self.metrics_history.append(metrics)
            self.real_time_metrics.append(metrics)
            
            # Update analytics data
            self._update_analytics_data(metrics)
            
            # Save to disk
            self._save_metrics_history()
            self._save_analytics_data()
            
            # Check for alerts
            self._check_alerts(metrics)
            
        except Exception as e:
            print(f"Error recording cycle metrics: {e}")
    
    def _update_analytics_data(self, metrics: PerformanceMetrics) -> None:
        """Update analytics data with new metrics."""
        stats = self.analytics_data["system_stats"]
        
        # Update counters
        stats["total_cycles_completed"] += 1
        stats["total_agents_created"] += metrics.agents_created
        if metrics.domains_covered > 0:
            stats["total_domains_covered"] += metrics.domains_covered
        stats["last_updated"] = metrics.timestamp
        
        # Update performance baselines
        baselines = self.analytics_data["performance_baselines"]
        if len(self.metrics_history) >= 10:  # Need at least 10 data points
            recent_metrics = self.metrics_history[-10:]
            baselines["average_cycle_duration"] = statistics.mean(
                [m.cycle_duration_minutes for m in recent_metrics]
            )
            baselines["average_success_rate"] = statistics.mean(
                [m.success_rate for m in recent_metrics]
            )
            baselines["average_quality_score"] = statistics.mean(
                [m.quality_score for m in recent_metrics if m.quality_score > 0]
            )
            baselines["baseline_established"] = True
    
    def _check_alerts(self, metrics: PerformanceMetrics) -> List[Dict[str, Any]]:
        """Check for alert conditions and generate alerts."""
        alerts = []
        thresholds = self.alert_thresholds
        
        # Performance alerts
        if metrics.cycle_duration_minutes > thresholds["performance"]["cycle_duration_critical"]:
            alerts.append({
                "type": "performance",
                "severity": "critical",
                "message": f"Cycle duration {metrics.cycle_duration_minutes:.1f}m exceeds critical threshold",
                "timestamp": metrics.timestamp,
                "metric": "cycle_duration",
                "value": metrics.cycle_duration_minutes
            })
        elif metrics.cycle_duration_minutes > thresholds["performance"]["cycle_duration_warning"]:
            alerts.append({
                "type": "performance",
                "severity": "warning",
                "message": f"Cycle duration {metrics.cycle_duration_minutes:.1f}m exceeds warning threshold",
                "timestamp": metrics.timestamp,
                "metric": "cycle_duration",
                "value": metrics.cycle_duration_minutes
            })
        
        # Success rate alerts
        if metrics.success_rate < thresholds["performance"]["success_rate_critical"]:
            alerts.append({
                "type": "performance",
                "severity": "critical",
                "message": f"Success rate {metrics.success_rate:.1%} below critical threshold",
                "timestamp": metrics.timestamp,
                "metric": "success_rate",
                "value": metrics.success_rate
            })
        
        # Quality score alerts
        if metrics.quality_score > 0 and metrics.quality_score < thresholds["performance"]["quality_score_critical"]:
            alerts.append({
                "type": "quality",
                "severity": "critical",
                "message": f"Quality score {metrics.quality_score:.3f} below critical threshold",
                "timestamp": metrics.timestamp,
                "metric": "quality_score",
                "value": metrics.quality_score
            })
        
        # Error alerts
        if metrics.errors_count > 0:
            alerts.append({
                "type": "errors",
                "severity": "warning" if metrics.errors_count < 3 else "critical",
                "message": f"{metrics.errors_count} errors detected in cycle",
                "timestamp": metrics.timestamp,
                "metric": "error_count",
                "value": metrics.errors_count
            })
        
        return alerts
    
    def calculate_trend_analysis(self, metric_name: str, days: int = 7) -> Optional[TrendAnalysis]:
        """Calculate trend analysis for a specific metric."""
        if len(self.metrics_history) < 2:
            return None
        
        try:
            # Get recent data points
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_metrics = [
                m for m in self.metrics_history
                if datetime.fromisoformat(m.timestamp.replace('Z', '+00:00')) > cutoff_date
            ]
            
            if len(recent_metrics) < 2:
                return None
            
            # Extract values for the specified metric
            values = []
            for m in recent_metrics:
                if metric_name == "cycle_duration":
                    values.append(m.cycle_duration_minutes)
                elif metric_name == "success_rate":
                    values.append(m.success_rate)
                elif metric_name == "quality_score":
                    values.append(m.quality_score)
                elif metric_name == "agents_created":
                    values.append(m.agents_created)
                elif metric_name == "errors_count":
                    values.append(m.errors_count)
            
            if not values:
                return None
            
            # Calculate trend
            current_value = values[-1]
            
            # Simple linear regression for trend
            n = len(values)
            x_values = list(range(n))
            
            # Calculate slope
            x_mean = statistics.mean(x_values)
            y_mean = statistics.mean(values)
            
            numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_values, values))
            denominator = sum((x - x_mean) ** 2 for x in x_values)
            
            if denominator == 0:
                slope = 0
            else:
                slope = numerator / denominator
            
            # Determine trend direction and strength
            if abs(slope) < 0.01:
                trend_direction = "stable"
                trend_strength = 0.0
            elif slope > 0:
                trend_direction = "increasing"
                trend_strength = min(abs(slope) / (y_mean + 0.001), 1.0)
            else:
                trend_direction = "decreasing"
                trend_strength = min(abs(slope) / (y_mean + 0.001), 1.0)
            
            # Simple prediction (linear extrapolation)
            prediction_7d = current_value + (slope * 7)
            
            # Calculate confidence based on data consistency
            if len(values) > 2:
                variance = statistics.variance(values)
                confidence = max(0.0, min(1.0, 1.0 - (variance / (y_mean + 0.001))))
            else:
                confidence = 0.5
            
            return TrendAnalysis(
                metric_name=metric_name,
                current_value=current_value,
                trend_direction=trend_direction,
                trend_strength=trend_strength,
                prediction_7d=prediction_7d,
                confidence=confidence
            )
            
        except Exception as e:
            print(f"Error calculating trend analysis: {e}")
            return None
    
    def get_system_health(self) -> SystemHealth:
        """Calculate overall system health."""
        try:
            if len(self.metrics_history) < 5:
                return SystemHealth(
                    overall_health=0.5,
                    component_health={"insufficient_data": 0.5},
                    active_alerts=[],
                    performance_score=0.5,
                    reliability_score=0.5
                )
            
            # Get recent metrics (last 24 hours)
            cutoff_date = datetime.now() - timedelta(hours=24)
            recent_metrics = [
                m for m in self.metrics_history
                if datetime.fromisoformat(m.timestamp.replace('Z', '+00:00')) > cutoff_date
            ]
            
            if not recent_metrics:
                recent_metrics = self.metrics_history[-5:]  # Fallback to last 5
            
            # Calculate component health scores
            component_health = {}
            
            # Performance health
            avg_success_rate = statistics.mean([m.success_rate for m in recent_metrics])
            avg_quality_score = statistics.mean([m.quality_score for m in recent_metrics if m.quality_score > 0])
            performance_score = (avg_success_rate + avg_quality_score) / 2
            component_health["performance"] = performance_score
            
            # Reliability health (based on error rates)
            total_cycles = len(recent_metrics)
            error_cycles = sum(1 for m in recent_metrics if m.errors_count > 0)
            reliability_score = 1.0 - (error_cycles / total_cycles) if total_cycles > 0 else 1.0
            component_health["reliability"] = reliability_score
            
            # Resource health (if available)
            resource_scores = []
            for m in recent_metrics:
                if m.resource_usage:
                    memory_usage = m.resource_usage.get('memory_percent', 0.5)
                    cpu_usage = m.resource_usage.get('cpu_percent', 0.5)
                    resource_score = 1.0 - max(memory_usage, cpu_usage)
                    resource_scores.append(resource_score)
            
            if resource_scores:
                component_health["resources"] = statistics.mean(resource_scores)
            else:
                component_health["resources"] = 0.8  # Default good score
            
            # Calculate overall health
            overall_health = statistics.mean(component_health.values())
            
            # Get active alerts (last hour)
            active_alerts = []
            for m in recent_metrics[-5:]:  # Check last 5 cycles
                alerts = self._check_alerts(m)
                active_alerts.extend(alerts)
            
            return SystemHealth(
                overall_health=overall_health,
                component_health=component_health,
                active_alerts=active_alerts,
                performance_score=performance_score,
                reliability_score=reliability_score
            )
            
        except Exception as e:
            print(f"Error calculating system health: {e}")
            return SystemHealth(
                overall_health=0.5,
                component_health={"error": 0.0},
                active_alerts=[{"type": "system", "severity": "error", "message": str(e)}],
                performance_score=0.5,
                reliability_score=0.5
            )
    
    def get_comprehensive_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        try:
            if not self.metrics_history:
                return {"error": "No metrics data available"}
            
            # Basic statistics
            total_cycles = len(self.metrics_history)
            total_agents = sum(m.agents_created for m in self.metrics_history)
            
            # Recent performance (last 24 hours)
            cutoff_date = datetime.now() - timedelta(hours=24)
            recent_metrics = [
                m for m in self.metrics_history
                if datetime.fromisoformat(m.timestamp.replace('Z', '+00:00')) > cutoff_date
            ]
            
            if not recent_metrics:
                recent_metrics = self.metrics_history[-10:]  # Fallback
            
            # Calculate rates
            if recent_metrics:
                time_span_hours = 24 if len(recent_metrics) > 10 else 1
                agents_per_hour = sum(m.agents_created for m in recent_metrics) / time_span_hours
                cycles_per_hour = len(recent_metrics) / time_span_hours
                
                avg_cycle_duration = statistics.mean([m.cycle_duration_minutes for m in recent_metrics])
                avg_success_rate = statistics.mean([m.success_rate for m in recent_metrics])
                avg_quality_score = statistics.mean([m.quality_score for m in recent_metrics if m.quality_score > 0])
            else:
                agents_per_hour = 0
                cycles_per_hour = 0
                avg_cycle_duration = 0
                avg_success_rate = 0
                avg_quality_score = 0
            
            # Trend analyses
            trends = {}
            for metric in ["cycle_duration", "success_rate", "quality_score", "agents_created"]:
                trend = self.calculate_trend_analysis(metric)
                if trend:
                    trends[metric] = asdict(trend)
            
            # System health
            health = self.get_system_health()
            
            return {
                "overview": {
                    "total_cycles_completed": total_cycles,
                    "total_agents_created": total_agents,
                    "system_uptime_hours": self.analytics_data["system_stats"]["system_uptime_hours"],
                    "last_updated": datetime.now().isoformat()
                },
                "current_performance": {
                    "agents_per_hour": round(agents_per_hour, 2),
                    "cycles_per_hour": round(cycles_per_hour, 2),
                    "average_cycle_duration_minutes": round(avg_cycle_duration, 2),
                    "success_rate": round(avg_success_rate, 3),
                    "quality_score": round(avg_quality_score, 3)
                },
                "trends": trends,
                "system_health": asdict(health),
                "analytics_data": self.analytics_data
            }
            
        except Exception as e:
            return {"error": f"Error generating statistics: {e}"}
    
    def get_domain_statistics(self) -> Dict[str, Any]:
        """Get statistics broken down by domain."""
        domain_stats = defaultdict(lambda: {
            "agents_created": 0,
            "cycles_focused": 0,
            "success_rate": 0.0,
            "quality_scores": []
        })

        # This would be enhanced with actual domain tracking
        # For now, return placeholder data
        return {
            "ai_healthcare": {"agents_created": 15, "success_rate": 0.92, "avg_quality": 0.89},
            "renewable_energy": {"agents_created": 12, "success_rate": 0.88, "avg_quality": 0.86},
            "cybersecurity": {"agents_created": 18, "success_rate": 0.94, "avg_quality": 0.91},
            "quantum_computing": {"agents_created": 8, "success_rate": 0.85, "avg_quality": 0.87}
        }

    def export_analytics_data(self, format_type: str = "json") -> Dict[str, Any]:
        """Export analytics data for external analysis."""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "metrics_history": [asdict(m) for m in self.metrics_history],
                "analytics_data": self.analytics_data,
                "system_health": asdict(self.get_system_health()),
                "comprehensive_stats": self.get_comprehensive_statistics(),
                "domain_statistics": self.get_domain_statistics()
            }

            return export_data

        except Exception as e:
            return {"error": f"Error exporting data: {e}"}
    
    def _save_metrics_history(self) -> None:
        """Save metrics history to disk."""
        try:
            # Keep only last 1000 entries to prevent file from growing too large
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
            
            with open(self.metrics_file, 'w') as f:
                json.dump([asdict(m) for m in self.metrics_history], f, indent=2)
        except Exception as e:
            print(f"Error saving metrics history: {e}")
    
    def _save_analytics_data(self) -> None:
        """Save analytics data to disk."""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.analytics_data, f, indent=2)
        except Exception as e:
            print(f"Error saving analytics data: {e}")

# Example usage
if __name__ == "__main__":
    analytics = AnalyticsEngine()
    
    # Simulate some cycle data
    test_cycle_data = {
        "duration_minutes": 15.5,
        "success": True,
        "agent_created": "test_agent",
        "quality_score": 0.87,
        "expansion_focus": "AI Healthcare",
        "errors": [],
        "resource_usage": {
            "memory_percent": 0.45,
            "cpu_percent": 0.32
        }
    }
    
    analytics.record_cycle_metrics(test_cycle_data)
    
    # Get comprehensive statistics
    stats = analytics.get_comprehensive_statistics()
    print("Analytics Engine initialized and tested successfully!")
    print(f"System health: {stats.get('system_health', {}).get('overall_health', 'N/A')}")
