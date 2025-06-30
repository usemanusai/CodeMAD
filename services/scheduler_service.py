#!/usr/bin/env python3
"""
Advanced Scheduler Service for Autonomous Expansion Protocol
Provides timer management, scheduling, and cycle control functionality.
"""

import json
import os
import time
import threading
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import pytz

class SchedulerState(Enum):
    """Scheduler state enumeration."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    COOLDOWN = "cooldown"
    ERROR = "error"

@dataclass
class ScheduleInfo:
    """Schedule information structure."""
    next_run_time: str
    time_until_next_run: str
    cycle_interval_minutes: int
    timezone: str
    is_manual_trigger_available: bool
    cooldown_remaining_seconds: int

@dataclass
class CycleHistory:
    """Cycle execution history."""
    cycle_id: str
    start_time: str
    end_time: str
    duration_minutes: float
    success: bool
    trigger_type: str  # "scheduled", "manual", "retry"
    result_summary: str

class AdvancedScheduler:
    """Advanced scheduling system with timer management and cycle control."""
    
    def __init__(self, config_manager=None):
        self.config_manager = config_manager
        self.state = SchedulerState.STOPPED
        self.data_dir = "services/data"
        self.schedule_file = os.path.join(self.data_dir, "scheduler_state.json")
        self.history_file = os.path.join(self.data_dir, "cycle_history.json")
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize state
        self.current_schedule = self._load_schedule_state()
        self.cycle_history = self._load_cycle_history()
        
        # Threading for background operations
        self.scheduler_thread = None
        self.stop_event = threading.Event()
        
        # Cooldown management
        self.last_manual_trigger = None
        self.manual_cooldown_minutes = 5
        
        # Callbacks
        self.cycle_callback = None
        self.status_callback = None
        
        # Performance tracking
        self.performance_stats = {
            "total_cycles": 0,
            "successful_cycles": 0,
            "failed_cycles": 0,
            "average_duration": 0.0,
            "last_success_time": None,
            "consecutive_failures": 0
        }
    
    def _load_schedule_state(self) -> Dict[str, Any]:
        """Load scheduler state from disk."""
        if os.path.exists(self.schedule_file):
            try:
                with open(self.schedule_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading schedule state: {e}")
                return self._create_default_schedule_state()
        return self._create_default_schedule_state()
    
    def _create_default_schedule_state(self) -> Dict[str, Any]:
        """Create default schedule state."""
        return {
            "state": SchedulerState.STOPPED.value,
            "cycle_interval_minutes": 120,
            "timezone": "UTC",
            "next_scheduled_run": None,
            "last_run_time": None,
            "pause_until": None,
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
    
    def _load_cycle_history(self) -> List[CycleHistory]:
        """Load cycle execution history."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                return [CycleHistory(**item) for item in data]
            except Exception as e:
                print(f"Error loading cycle history: {e}")
                return []
        return []
    
    def _save_schedule_state(self) -> None:
        """Save scheduler state to disk."""
        try:
            self.current_schedule["last_updated"] = datetime.now().isoformat()
            with open(self.schedule_file, 'w') as f:
                json.dump(self.current_schedule, f, indent=2)
        except Exception as e:
            print(f"Error saving schedule state: {e}")
    
    def _save_cycle_history(self) -> None:
        """Save cycle history to disk."""
        try:
            # Keep only last 100 entries
            if len(self.cycle_history) > 100:
                self.cycle_history = self.cycle_history[-100:]
            
            with open(self.history_file, 'w') as f:
                json.dump([asdict(cycle) for cycle in self.cycle_history], f, indent=2)
        except Exception as e:
            print(f"Error saving cycle history: {e}")
    
    def set_cycle_callback(self, callback: Callable) -> None:
        """Set callback function for cycle execution."""
        self.cycle_callback = callback
    
    def set_status_callback(self, callback: Callable) -> None:
        """Set callback function for status updates."""
        self.status_callback = callback
    
    def start_scheduler(self, cycle_interval_minutes: int = None) -> bool:
        """Start the scheduler."""
        try:
            if self.state == SchedulerState.RUNNING:
                return True
            
            # Update interval if provided
            if cycle_interval_minutes:
                self.current_schedule["cycle_interval_minutes"] = cycle_interval_minutes
            
            # Calculate next run time
            interval = self.current_schedule["cycle_interval_minutes"]
            next_run = datetime.now() + timedelta(minutes=interval)
            self.current_schedule["next_scheduled_run"] = next_run.isoformat()
            
            # Update state
            self.state = SchedulerState.RUNNING
            self.current_schedule["state"] = self.state.value
            self._save_schedule_state()
            
            # Start scheduler thread
            self.stop_event.clear()
            self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
            self.scheduler_thread.start()
            
            if self.status_callback:
                self.status_callback("Scheduler started successfully")
            
            return True
            
        except Exception as e:
            print(f"Error starting scheduler: {e}")
            self.state = SchedulerState.ERROR
            return False
    
    def stop_scheduler(self) -> bool:
        """Stop the scheduler."""
        try:
            self.state = SchedulerState.STOPPED
            self.current_schedule["state"] = self.state.value
            self.current_schedule["next_scheduled_run"] = None
            self._save_schedule_state()
            
            # Stop scheduler thread
            self.stop_event.set()
            if self.scheduler_thread and self.scheduler_thread.is_alive():
                self.scheduler_thread.join(timeout=5)
            
            if self.status_callback:
                self.status_callback("Scheduler stopped")
            
            return True
            
        except Exception as e:
            print(f"Error stopping scheduler: {e}")
            return False
    
    def pause_scheduler(self, duration_minutes: int = None) -> bool:
        """Pause the scheduler for a specified duration."""
        try:
            if self.state != SchedulerState.RUNNING:
                return False
            
            self.state = SchedulerState.PAUSED
            self.current_schedule["state"] = self.state.value
            
            if duration_minutes:
                pause_until = datetime.now() + timedelta(minutes=duration_minutes)
                self.current_schedule["pause_until"] = pause_until.isoformat()
            else:
                self.current_schedule["pause_until"] = None
            
            self._save_schedule_state()
            
            if self.status_callback:
                self.status_callback(f"Scheduler paused for {duration_minutes} minutes" if duration_minutes else "Scheduler paused indefinitely")
            
            return True
            
        except Exception as e:
            print(f"Error pausing scheduler: {e}")
            return False
    
    def resume_scheduler(self) -> bool:
        """Resume the paused scheduler."""
        try:
            if self.state != SchedulerState.PAUSED:
                return False
            
            self.state = SchedulerState.RUNNING
            self.current_schedule["state"] = self.state.value
            self.current_schedule["pause_until"] = None
            
            # Recalculate next run time
            interval = self.current_schedule["cycle_interval_minutes"]
            next_run = datetime.now() + timedelta(minutes=interval)
            self.current_schedule["next_scheduled_run"] = next_run.isoformat()
            
            self._save_schedule_state()
            
            if self.status_callback:
                self.status_callback("Scheduler resumed")
            
            return True
            
        except Exception as e:
            print(f"Error resuming scheduler: {e}")
            return False
    
    def trigger_manual_cycle(self) -> Tuple[bool, str]:
        """Trigger a manual cycle execution."""
        try:
            # Check cooldown
            if self.last_manual_trigger:
                time_since_last = datetime.now() - self.last_manual_trigger
                if time_since_last.total_seconds() < (self.manual_cooldown_minutes * 60):
                    remaining = (self.manual_cooldown_minutes * 60) - time_since_last.total_seconds()
                    return False, f"Manual trigger on cooldown. {remaining:.0f} seconds remaining."
            
            # Execute cycle
            if self.cycle_callback:
                cycle_id = f"manual_{int(time.time())}"
                start_time = datetime.now()
                
                try:
                    result = self.cycle_callback()
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds() / 60
                    
                    # Record in history
                    cycle_history = CycleHistory(
                        cycle_id=cycle_id,
                        start_time=start_time.isoformat(),
                        end_time=end_time.isoformat(),
                        duration_minutes=duration,
                        success=result.get('success', False) if isinstance(result, dict) else bool(result),
                        trigger_type="manual",
                        result_summary=str(result)[:200] if result else "No result"
                    )
                    
                    self.cycle_history.append(cycle_history)
                    self._save_cycle_history()
                    
                    # Update performance stats
                    self._update_performance_stats(cycle_history)
                    
                    # Set cooldown
                    self.last_manual_trigger = datetime.now()
                    
                    return True, f"Manual cycle completed successfully in {duration:.1f} minutes"
                    
                except Exception as e:
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds() / 60
                    
                    cycle_history = CycleHistory(
                        cycle_id=cycle_id,
                        start_time=start_time.isoformat(),
                        end_time=end_time.isoformat(),
                        duration_minutes=duration,
                        success=False,
                        trigger_type="manual",
                        result_summary=f"Error: {str(e)}"
                    )
                    
                    self.cycle_history.append(cycle_history)
                    self._save_cycle_history()
                    self._update_performance_stats(cycle_history)
                    
                    return False, f"Manual cycle failed: {str(e)}"
            else:
                return False, "No cycle callback configured"
                
        except Exception as e:
            return False, f"Error triggering manual cycle: {str(e)}"
    
    def _scheduler_loop(self) -> None:
        """Main scheduler loop running in background thread."""
        while not self.stop_event.is_set():
            try:
                # Check if paused
                if self.state == SchedulerState.PAUSED:
                    # Check if pause duration has expired
                    if self.current_schedule.get("pause_until"):
                        pause_until = datetime.fromisoformat(self.current_schedule["pause_until"])
                        if datetime.now() > pause_until:
                            self.resume_scheduler()
                    
                    time.sleep(10)  # Check every 10 seconds
                    continue
                
                # Check if it's time for next cycle
                if self.current_schedule.get("next_scheduled_run"):
                    next_run = datetime.fromisoformat(self.current_schedule["next_scheduled_run"])
                    if datetime.now() >= next_run:
                        self._execute_scheduled_cycle()
                
                # Sleep for 30 seconds before next check
                time.sleep(30)
                
            except Exception as e:
                print(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _execute_scheduled_cycle(self) -> None:
        """Execute a scheduled cycle."""
        if not self.cycle_callback:
            return
        
        cycle_id = f"scheduled_{int(time.time())}"
        start_time = datetime.now()
        
        try:
            result = self.cycle_callback()
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 60
            
            # Record in history
            cycle_history = CycleHistory(
                cycle_id=cycle_id,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration_minutes=duration,
                success=result.get('success', False) if isinstance(result, dict) else bool(result),
                trigger_type="scheduled",
                result_summary=str(result)[:200] if result else "No result"
            )
            
            self.cycle_history.append(cycle_history)
            self._save_cycle_history()
            self._update_performance_stats(cycle_history)
            
            # Schedule next run
            interval = self.current_schedule["cycle_interval_minutes"]
            next_run = datetime.now() + timedelta(minutes=interval)
            self.current_schedule["next_scheduled_run"] = next_run.isoformat()
            self.current_schedule["last_run_time"] = start_time.isoformat()
            self._save_schedule_state()
            
            if self.status_callback:
                self.status_callback(f"Scheduled cycle completed in {duration:.1f} minutes")
                
        except Exception as e:
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds() / 60
            
            cycle_history = CycleHistory(
                cycle_id=cycle_id,
                start_time=start_time.isoformat(),
                end_time=end_time.isoformat(),
                duration_minutes=duration,
                success=False,
                trigger_type="scheduled",
                result_summary=f"Error: {str(e)}"
            )
            
            self.cycle_history.append(cycle_history)
            self._save_cycle_history()
            self._update_performance_stats(cycle_history)
            
            # Still schedule next run even on failure
            interval = self.current_schedule["cycle_interval_minutes"]
            next_run = datetime.now() + timedelta(minutes=interval)
            self.current_schedule["next_scheduled_run"] = next_run.isoformat()
            self._save_schedule_state()
            
            if self.status_callback:
                self.status_callback(f"Scheduled cycle failed: {str(e)}")
    
    def _update_performance_stats(self, cycle: CycleHistory) -> None:
        """Update performance statistics."""
        self.performance_stats["total_cycles"] += 1
        
        if cycle.success:
            self.performance_stats["successful_cycles"] += 1
            self.performance_stats["last_success_time"] = cycle.end_time
            self.performance_stats["consecutive_failures"] = 0
        else:
            self.performance_stats["failed_cycles"] += 1
            self.performance_stats["consecutive_failures"] += 1
        
        # Update average duration
        total_duration = sum(c.duration_minutes for c in self.cycle_history)
        self.performance_stats["average_duration"] = total_duration / len(self.cycle_history)
    
    def get_schedule_info(self) -> ScheduleInfo:
        """Get current schedule information."""
        try:
            next_run_str = "Not scheduled"
            time_until_str = "N/A"
            cooldown_remaining = 0
            
            if self.current_schedule.get("next_scheduled_run"):
                next_run = datetime.fromisoformat(self.current_schedule["next_scheduled_run"])
                next_run_str = next_run.strftime("%Y-%m-%d %H:%M:%S UTC")
                
                time_until = next_run - datetime.now()
                if time_until.total_seconds() > 0:
                    hours, remainder = divmod(int(time_until.total_seconds()), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    time_until_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    time_until_str = "Overdue"
            
            # Check manual trigger cooldown
            is_manual_available = True
            if self.last_manual_trigger:
                time_since_last = datetime.now() - self.last_manual_trigger
                cooldown_remaining = max(0, (self.manual_cooldown_minutes * 60) - time_since_last.total_seconds())
                is_manual_available = cooldown_remaining == 0
            
            return ScheduleInfo(
                next_run_time=next_run_str,
                time_until_next_run=time_until_str,
                cycle_interval_minutes=self.current_schedule["cycle_interval_minutes"],
                timezone=self.current_schedule["timezone"],
                is_manual_trigger_available=is_manual_available,
                cooldown_remaining_seconds=int(cooldown_remaining)
            )
            
        except Exception as e:
            print(f"Error getting schedule info: {e}")
            return ScheduleInfo(
                next_run_time="Error",
                time_until_next_run="Error",
                cycle_interval_minutes=120,
                timezone="UTC",
                is_manual_trigger_available=False,
                cooldown_remaining_seconds=0
            )
    
    def get_cycle_history(self, limit: int = 20) -> List[CycleHistory]:
        """Get recent cycle history."""
        return self.cycle_history[-limit:] if self.cycle_history else []
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics."""
        stats = self.performance_stats.copy()
        
        # Calculate success rate
        if stats["total_cycles"] > 0:
            stats["success_rate"] = stats["successful_cycles"] / stats["total_cycles"]
        else:
            stats["success_rate"] = 0.0
        
        # Add recent performance (last 10 cycles)
        recent_cycles = self.cycle_history[-10:] if len(self.cycle_history) >= 10 else self.cycle_history
        if recent_cycles:
            recent_success = sum(1 for c in recent_cycles if c.success)
            stats["recent_success_rate"] = recent_success / len(recent_cycles)
            stats["recent_average_duration"] = sum(c.duration_minutes for c in recent_cycles) / len(recent_cycles)
        else:
            stats["recent_success_rate"] = 0.0
            stats["recent_average_duration"] = 0.0
        
        return stats
    
    def update_schedule_interval(self, new_interval_minutes: int) -> bool:
        """Update the cycle interval."""
        try:
            if not 30 <= new_interval_minutes <= 1440:  # 30 minutes to 24 hours
                return False
            
            self.current_schedule["cycle_interval_minutes"] = new_interval_minutes
            
            # Recalculate next run time if scheduler is running
            if self.state == SchedulerState.RUNNING:
                next_run = datetime.now() + timedelta(minutes=new_interval_minutes)
                self.current_schedule["next_scheduled_run"] = next_run.isoformat()
            
            self._save_schedule_state()
            return True
            
        except Exception as e:
            print(f"Error updating schedule interval: {e}")
            return False

# Example usage
if __name__ == "__main__":
    def test_cycle_callback():
        """Test cycle callback function."""
        print("Executing test cycle...")
        time.sleep(2)  # Simulate work
        return {"success": True, "message": "Test cycle completed"}
    
    scheduler = AdvancedScheduler()
    scheduler.set_cycle_callback(test_cycle_callback)
    
    # Test scheduler functionality
    print("Testing Advanced Scheduler...")
    
    # Start scheduler
    success = scheduler.start_scheduler(cycle_interval_minutes=1)  # 1 minute for testing
    print(f"Start scheduler: {success}")
    
    # Get schedule info
    info = scheduler.get_schedule_info()
    print(f"Next run: {info.next_run_time}")
    print(f"Time until next: {info.time_until_next_run}")
    
    # Test manual trigger
    success, message = scheduler.trigger_manual_cycle()
    print(f"Manual trigger: {success} - {message}")
    
    print("Advanced Scheduler initialized successfully!")
