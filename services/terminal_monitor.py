#!/usr/bin/env python3
"""
Terminal Monitor Service for Autonomous Expansion Protocol
Provides real-time monitoring, logging, and system resource tracking.
"""

import os
import sys
import time
import json
import psutil
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import deque
import curses
import signal

@dataclass
class SystemMetrics:
    """System resource metrics."""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    disk_percent: float
    disk_used_mb: float
    network_io_kb: float
    process_count: int

@dataclass
class LogEntry:
    """Log entry structure."""
    timestamp: str
    level: str
    component: str
    message: str
    details: Optional[Dict[str, Any]] = None

class TerminalMonitor:
    """Terminal-based monitoring system with real-time updates."""
    
    def __init__(self, data_dir: str = "services/data"):
        self.data_dir = data_dir
        self.log_file = os.path.join(data_dir, "terminal_monitor.log")
        self.metrics_file = os.path.join(data_dir, "system_metrics.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize monitoring state
        self.is_running = False
        self.is_paused = False
        self.auto_scroll = True
        self.refresh_rate = 1.0  # seconds
        
        # Data storage
        self.log_entries = deque(maxlen=1000)  # Last 1000 log entries
        self.metrics_history = deque(maxlen=100)  # Last 100 metric snapshots
        
        # Threading
        self.monitor_thread = None
        self.metrics_thread = None
        self.stop_event = threading.Event()
        
        # Terminal state
        self.screen = None
        self.current_view = "overview"  # overview, logs, metrics, processes
        self.scroll_position = 0
        self.selected_line = 0
        
        # Component status tracking
        self.component_status = {
            "scheduler": "unknown",
            "research_engine": "unknown",
            "quality_assurance": "unknown",
            "agent_directory": "unknown",
            "analytics_engine": "unknown",
            "configuration_manager": "unknown"
        }
        
        # Load existing data
        self._load_existing_data()
    
    def _load_existing_data(self) -> None:
        """Load existing log and metrics data."""
        # Load log entries
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            try:
                                entry_data = json.loads(line.strip())
                                entry = LogEntry(**entry_data)
                                self.log_entries.append(entry)
                            except json.JSONDecodeError:
                                # Handle plain text log entries
                                timestamp = datetime.now().isoformat()
                                entry = LogEntry(
                                    timestamp=timestamp,
                                    level="INFO",
                                    component="system",
                                    message=line.strip()
                                )
                                self.log_entries.append(entry)
            except Exception as e:
                self.add_log_entry("ERROR", "terminal_monitor", f"Error loading log file: {e}")
        
        # Load metrics history
        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    data = json.load(f)
                    for metric_data in data:
                        metric = SystemMetrics(**metric_data)
                        self.metrics_history.append(metric)
            except Exception as e:
                self.add_log_entry("ERROR", "terminal_monitor", f"Error loading metrics file: {e}")
    
    def add_log_entry(self, level: str, component: str, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Add a new log entry."""
        entry = LogEntry(
            timestamp=datetime.now().isoformat(),
            level=level.upper(),
            component=component,
            message=message,
            details=details
        )
        
        self.log_entries.append(entry)
        
        # Write to log file
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(asdict(entry)) + '\n')
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_used_mb = memory.used / (1024 * 1024)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_used_mb = disk.used / (1024 * 1024)
            
            # Network I/O (simplified)
            network = psutil.net_io_counters()
            network_io_kb = (network.bytes_sent + network.bytes_recv) / 1024
            
            # Process count
            process_count = len(psutil.pids())
            
            metrics = SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_used_mb=memory_used_mb,
                disk_percent=disk_percent,
                disk_used_mb=disk_used_mb,
                network_io_kb=network_io_kb,
                process_count=process_count
            )
            
            self.metrics_history.append(metrics)
            return metrics
            
        except Exception as e:
            self.add_log_entry("ERROR", "terminal_monitor", f"Error collecting metrics: {e}")
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=0.0,
                memory_percent=0.0,
                memory_used_mb=0.0,
                disk_percent=0.0,
                disk_used_mb=0.0,
                network_io_kb=0.0,
                process_count=0
            )
    
    def save_metrics_to_file(self) -> None:
        """Save metrics history to file."""
        try:
            metrics_data = [asdict(metric) for metric in self.metrics_history]
            with open(self.metrics_file, 'w') as f:
                json.dump(metrics_data, f, indent=2)
        except Exception as e:
            self.add_log_entry("ERROR", "terminal_monitor", f"Error saving metrics: {e}")
    
    def start_monitoring(self) -> None:
        """Start the monitoring system."""
        if self.is_running:
            return
        
        self.is_running = True
        self.stop_event.clear()
        
        # Start metrics collection thread
        self.metrics_thread = threading.Thread(target=self._metrics_loop, daemon=True)
        self.metrics_thread.start()
        
        self.add_log_entry("INFO", "terminal_monitor", "Terminal monitoring started")
    
    def stop_monitoring(self) -> None:
        """Stop the monitoring system."""
        self.is_running = False
        self.stop_event.set()
        
        if self.metrics_thread and self.metrics_thread.is_alive():
            self.metrics_thread.join(timeout=5)
        
        # Save final metrics
        self.save_metrics_to_file()
        
        self.add_log_entry("INFO", "terminal_monitor", "Terminal monitoring stopped")
    
    def _metrics_loop(self) -> None:
        """Background thread for collecting metrics."""
        while not self.stop_event.is_set() and self.is_running:
            try:
                if not self.is_paused:
                    metrics = self.collect_system_metrics()
                    
                    # Save metrics periodically
                    if len(self.metrics_history) % 10 == 0:
                        self.save_metrics_to_file()
                
                time.sleep(self.refresh_rate)
                
            except Exception as e:
                self.add_log_entry("ERROR", "terminal_monitor", f"Error in metrics loop: {e}")
                time.sleep(5)  # Wait longer on error
    
    def start_terminal_interface(self) -> None:
        """Start the curses-based terminal interface."""
        try:
            # Initialize curses
            self.screen = curses.initscr()
            curses.noecho()
            curses.cbreak()
            self.screen.keypad(True)
            curses.curs_set(0)  # Hide cursor
            
            # Initialize colors if available
            if curses.has_colors():
                curses.start_color()
                curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Success
                curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Warning
                curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Error
                curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Info
                curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Header
            
            # Start monitoring
            self.start_monitoring()
            
            # Main interface loop
            self._interface_loop()
            
        except Exception as e:
            self.add_log_entry("ERROR", "terminal_monitor", f"Terminal interface error: {e}")
        finally:
            self._cleanup_terminal()
    
    def _interface_loop(self) -> None:
        """Main terminal interface loop."""
        while self.is_running:
            try:
                # Clear screen
                self.screen.clear()
                
                # Draw interface based on current view
                if self.current_view == "overview":
                    self._draw_overview()
                elif self.current_view == "logs":
                    self._draw_logs()
                elif self.current_view == "metrics":
                    self._draw_metrics()
                elif self.current_view == "processes":
                    self._draw_processes()
                
                # Draw header and footer
                self._draw_header()
                self._draw_footer()
                
                # Refresh screen
                self.screen.refresh()
                
                # Handle input
                self._handle_input()
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.add_log_entry("ERROR", "terminal_monitor", f"Interface loop error: {e}")
                time.sleep(1)
    
    def _draw_header(self) -> None:
        """Draw the header bar."""
        height, width = self.screen.getmaxyx()
        
        # Header text
        header_text = "🤖 Autonomous AI Ecosystem - Terminal Monitor"
        status_text = f"Status: {'RUNNING' if self.is_running and not self.is_paused else 'PAUSED'}"
        time_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Draw header background
        if curses.has_colors():
            self.screen.attron(curses.color_pair(5))
        
        self.screen.addstr(0, 0, " " * width)
        self.screen.addstr(0, 2, header_text[:width-4])
        self.screen.addstr(0, width - len(status_text) - len(time_text) - 4, status_text)
        self.screen.addstr(0, width - len(time_text) - 2, time_text)
        
        if curses.has_colors():
            self.screen.attroff(curses.color_pair(5))
    
    def _draw_footer(self) -> None:
        """Draw the footer with keyboard shortcuts."""
        height, width = self.screen.getmaxyx()
        
        shortcuts = "F1:Overview F2:Logs F3:Metrics F4:Processes P:Pause Q:Quit"
        
        if curses.has_colors():
            self.screen.attron(curses.color_pair(5))
        
        self.screen.addstr(height - 1, 0, " " * width)
        self.screen.addstr(height - 1, 2, shortcuts[:width-4])
        
        if curses.has_colors():
            self.screen.attroff(curses.color_pair(5))
    
    def _draw_overview(self) -> None:
        """Draw the overview screen."""
        height, width = self.screen.getmaxyx()
        start_row = 2
        
        # System status
        self.screen.addstr(start_row, 2, "SYSTEM STATUS", curses.A_BOLD)
        start_row += 2
        
        # Get latest metrics
        if self.metrics_history:
            latest_metrics = self.metrics_history[-1]
            
            self.screen.addstr(start_row, 4, f"CPU Usage:    {latest_metrics.cpu_percent:5.1f}%")
            start_row += 1
            self.screen.addstr(start_row, 4, f"Memory Usage: {latest_metrics.memory_percent:5.1f}% ({latest_metrics.memory_used_mb:6.1f} MB)")
            start_row += 1
            self.screen.addstr(start_row, 4, f"Disk Usage:   {latest_metrics.disk_percent:5.1f}% ({latest_metrics.disk_used_mb:6.1f} MB)")
            start_row += 1
            self.screen.addstr(start_row, 4, f"Processes:    {latest_metrics.process_count}")
            start_row += 2
        
        # Component status
        self.screen.addstr(start_row, 2, "COMPONENT STATUS", curses.A_BOLD)
        start_row += 2
        
        for component, status in self.component_status.items():
            color = curses.color_pair(1) if status == "running" else curses.color_pair(3) if status == "error" else curses.color_pair(2)
            self.screen.addstr(start_row, 4, f"{component.replace('_', ' ').title():20} ", curses.A_NORMAL)
            if curses.has_colors():
                self.screen.addstr(f"[{status.upper()}]", color)
            else:
                self.screen.addstr(f"[{status.upper()}]")
            start_row += 1
        
        start_row += 1
        
        # Recent log entries
        self.screen.addstr(start_row, 2, "RECENT LOG ENTRIES", curses.A_BOLD)
        start_row += 2
        
        recent_logs = list(self.log_entries)[-10:]  # Last 10 entries
        for entry in recent_logs:
            if start_row >= height - 3:
                break
            
            timestamp = entry.timestamp.split('T')[1][:8]  # HH:MM:SS
            level_color = self._get_level_color(entry.level)
            
            log_line = f"{timestamp} [{entry.level:5}] {entry.component}: {entry.message}"
            if len(log_line) > width - 6:
                log_line = log_line[:width-9] + "..."
            
            self.screen.addstr(start_row, 4, timestamp)
            self.screen.addstr(start_row, 13, f"[{entry.level:5}]", level_color)
            self.screen.addstr(start_row, 21, f"{entry.component}: {entry.message}"[:width-25])
            start_row += 1
    
    def _draw_logs(self) -> None:
        """Draw the logs screen."""
        height, width = self.screen.getmaxyx()
        start_row = 2
        
        self.screen.addstr(start_row, 2, f"LOG ENTRIES (Total: {len(self.log_entries)})", curses.A_BOLD)
        start_row += 2
        
        # Calculate visible range
        visible_lines = height - 6  # Account for header, footer, and title
        start_index = max(0, len(self.log_entries) - visible_lines + self.scroll_position)
        end_index = min(len(self.log_entries), start_index + visible_lines)
        
        # Display log entries
        for i in range(start_index, end_index):
            if start_row >= height - 2:
                break
            
            entry = self.log_entries[i]
            timestamp = entry.timestamp.split('T')[1][:8]  # HH:MM:SS
            level_color = self._get_level_color(entry.level)
            
            # Highlight selected line
            attr = curses.A_REVERSE if i == self.selected_line else curses.A_NORMAL
            
            log_line = f"{timestamp} [{entry.level:5}] {entry.component}: {entry.message}"
            if len(log_line) > width - 6:
                log_line = log_line[:width-9] + "..."
            
            self.screen.addstr(start_row, 4, log_line, attr)
            start_row += 1
    
    def _draw_metrics(self) -> None:
        """Draw the metrics screen."""
        height, width = self.screen.getmaxyx()
        start_row = 2
        
        self.screen.addstr(start_row, 2, "SYSTEM METRICS", curses.A_BOLD)
        start_row += 2
        
        if not self.metrics_history:
            self.screen.addstr(start_row, 4, "No metrics data available")
            return
        
        # Show latest metrics
        latest = self.metrics_history[-1]
        self.screen.addstr(start_row, 4, f"Timestamp: {latest.timestamp}")
        start_row += 2
        
        # CPU usage bar
        self._draw_progress_bar(start_row, 4, "CPU", latest.cpu_percent, width - 20)
        start_row += 2
        
        # Memory usage bar
        self._draw_progress_bar(start_row, 4, "Memory", latest.memory_percent, width - 20)
        start_row += 2
        
        # Disk usage bar
        self._draw_progress_bar(start_row, 4, "Disk", latest.disk_percent, width - 20)
        start_row += 2
        
        # Historical data (simple text-based chart)
        if len(self.metrics_history) > 1:
            start_row += 1
            self.screen.addstr(start_row, 4, "CPU Usage History (last 20 samples):")
            start_row += 1
            
            recent_metrics = list(self.metrics_history)[-20:]
            chart_width = min(60, width - 10)
            
            # Simple ASCII chart
            chart_line = ""
            for metric in recent_metrics:
                if metric.cpu_percent < 25:
                    chart_line += "▁"
                elif metric.cpu_percent < 50:
                    chart_line += "▃"
                elif metric.cpu_percent < 75:
                    chart_line += "▅"
                else:
                    chart_line += "█"
            
            self.screen.addstr(start_row, 6, chart_line[:chart_width])
    
    def _draw_processes(self) -> None:
        """Draw the processes screen."""
        height, width = self.screen.getmaxyx()
        start_row = 2
        
        self.screen.addstr(start_row, 2, "SYSTEM PROCESSES", curses.A_BOLD)
        start_row += 2
        
        try:
            # Get process information
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            # Header
            self.screen.addstr(start_row, 4, "PID     NAME                     CPU%    MEM%")
            start_row += 1
            self.screen.addstr(start_row, 4, "-" * 50)
            start_row += 1
            
            # Show top processes
            for proc in processes[:height-8]:
                if start_row >= height - 2:
                    break
                
                pid = proc['pid']
                name = (proc['name'] or 'Unknown')[:20]
                cpu = proc['cpu_percent'] or 0
                mem = proc['memory_percent'] or 0
                
                proc_line = f"{pid:7} {name:20} {cpu:6.1f}  {mem:6.1f}"
                self.screen.addstr(start_row, 4, proc_line)
                start_row += 1
                
        except Exception as e:
            self.screen.addstr(start_row, 4, f"Error getting process info: {e}")
    
    def _draw_progress_bar(self, row: int, col: int, label: str, percentage: float, width: int) -> None:
        """Draw a progress bar."""
        bar_width = width - len(label) - 10
        filled_width = int((percentage / 100) * bar_width)
        
        self.screen.addstr(row, col, f"{label:8}")
        self.screen.addstr(row, col + 9, "[")
        
        # Filled portion
        if curses.has_colors():
            color = curses.color_pair(1) if percentage < 70 else curses.color_pair(2) if percentage < 90 else curses.color_pair(3)
            self.screen.addstr("█" * filled_width, color)
        else:
            self.screen.addstr("█" * filled_width)
        
        # Empty portion
        self.screen.addstr("░" * (bar_width - filled_width))
        self.screen.addstr(f"] {percentage:5.1f}%")
    
    def _get_level_color(self, level: str) -> int:
        """Get color for log level."""
        if not curses.has_colors():
            return curses.A_NORMAL
        
        color_map = {
            "ERROR": curses.color_pair(3),
            "WARNING": curses.color_pair(2),
            "INFO": curses.color_pair(4),
            "DEBUG": curses.color_pair(1)
        }
        return color_map.get(level, curses.color_pair(4))
    
    def _handle_input(self) -> None:
        """Handle keyboard input."""
        self.screen.timeout(100)  # Non-blocking input with 100ms timeout
        
        try:
            key = self.screen.getch()
            
            if key == ord('q') or key == ord('Q'):
                self.is_running = False
            elif key == ord('p') or key == ord('P'):
                self.is_paused = not self.is_paused
                status = "paused" if self.is_paused else "resumed"
                self.add_log_entry("INFO", "terminal_monitor", f"Monitoring {status}")
            elif key == curses.KEY_F1:
                self.current_view = "overview"
            elif key == curses.KEY_F2:
                self.current_view = "logs"
            elif key == curses.KEY_F3:
                self.current_view = "metrics"
            elif key == curses.KEY_F4:
                self.current_view = "processes"
            elif key == curses.KEY_UP:
                if self.current_view == "logs":
                    self.selected_line = max(0, self.selected_line - 1)
            elif key == curses.KEY_DOWN:
                if self.current_view == "logs":
                    self.selected_line = min(len(self.log_entries) - 1, self.selected_line + 1)
            elif key == curses.KEY_PPAGE:  # Page Up
                self.scroll_position = max(self.scroll_position - 10, -len(self.log_entries))
            elif key == curses.KEY_NPAGE:  # Page Down
                self.scroll_position = min(self.scroll_position + 10, 0)
                
        except curses.error:
            pass  # No input available
    
    def _cleanup_terminal(self) -> None:
        """Clean up terminal settings."""
        if self.screen:
            curses.nocbreak()
            self.screen.keypad(False)
            curses.echo()
            curses.endwin()
        
        self.stop_monitoring()
    
    def update_component_status(self, component: str, status: str) -> None:
        """Update the status of a system component."""
        if component in self.component_status:
            old_status = self.component_status[component]
            self.component_status[component] = status
            
            if old_status != status:
                self.add_log_entry("INFO", "terminal_monitor", f"Component {component} status changed: {old_status} -> {status}")
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get a summary of system status."""
        latest_metrics = self.metrics_history[-1] if self.metrics_history else None
        recent_errors = [entry for entry in self.log_entries if entry.level == "ERROR"][-10:]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "latest_metrics": asdict(latest_metrics) if latest_metrics else None,
            "component_status": self.component_status.copy(),
            "recent_errors": [asdict(entry) for entry in recent_errors],
            "total_log_entries": len(self.log_entries),
            "metrics_collected": len(self.metrics_history)
        }

# Signal handler for graceful shutdown
def signal_handler(signum, frame, monitor):
    monitor.stop_monitoring()
    sys.exit(0)

# Main execution
if __name__ == "__main__":
    monitor = TerminalMonitor()
    
    # Set up signal handler
    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, monitor))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, monitor))
    
    try:
        # Add some test log entries
        monitor.add_log_entry("INFO", "system", "Terminal monitor starting up")
        monitor.add_log_entry("INFO", "scheduler", "Scheduler initialized")
        monitor.add_log_entry("INFO", "research_engine", "Research engine ready")
        monitor.add_log_entry("WARNING", "quality_assurance", "Quality threshold adjusted")
        
        # Update component statuses
        monitor.update_component_status("scheduler", "running")
        monitor.update_component_status("research_engine", "running")
        monitor.update_component_status("quality_assurance", "running")
        
        # Start terminal interface
        print("Starting Terminal Monitor...")
        print("Press F1-F4 to switch views, P to pause, Q to quit")
        time.sleep(2)
        
        monitor.start_terminal_interface()
        
    except Exception as e:
        print(f"Error running terminal monitor: {e}")
    finally:
        monitor.stop_monitoring()
        print("Terminal monitor stopped.")
