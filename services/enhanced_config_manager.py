#!/usr/bin/env python3
"""
Enhanced Configuration Manager for Autonomous Expansion Protocol
Provides real-time configuration editing, validation, and preset management.
"""

import json
import os
import time
import copy
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class ConfigPreset(Enum):
    """Configuration preset modes."""
    CONSERVATIVE = "conservative"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    CUSTOM = "custom"

@dataclass
class ConfigurationState:
    """Represents the current configuration state."""
    preset_mode: str
    cycle_interval_minutes: int
    quality_threshold: float
    max_failures: int
    max_agents_per_day: int
    research_timeout_seconds: int
    emergency_stop_enabled: bool
    last_modified: str
    modified_by: str
    version: int

@dataclass
class ConfigValidationResult:
    """Result of configuration validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    constitutional_compliance: bool

class EnhancedConfigManager:
    """Enhanced configuration manager with real-time editing and validation."""
    
    def __init__(self, config_dir: str = "services/config"):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "enhanced_expansion_config.json")
        self.backup_dir = os.path.join(config_dir, "backups")
        self.history_file = os.path.join(config_dir, "config_history.json")
        
        # Ensure directories exist
        os.makedirs(config_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Load or create configuration
        self.current_config = self._load_or_create_config()
        self.config_history = self._load_config_history()
        
        # Define preset configurations
        self.presets = self._define_presets()
    
    def _define_presets(self) -> Dict[str, Dict[str, Any]]:
        """Define configuration presets."""
        return {
            ConfigPreset.CONSERVATIVE.value: {
                "cycle_interval_minutes": 240,  # 4 hours
                "quality_threshold": 0.95,
                "max_failures": 2,
                "max_agents_per_day": 3,
                "research_timeout_seconds": 300,
                "emergency_stop_enabled": True,
                "research_source_weights": {
                    "academic": 0.4,
                    "industry": 0.3,
                    "government": 0.2,
                    "news": 0.1
                },
                "safety_limits": {
                    "max_memory_usage_mb": 512,
                    "max_api_calls_per_hour": 100,
                    "max_concurrent_research": 2
                }
            },
            ConfigPreset.BALANCED.value: {
                "cycle_interval_minutes": 120,  # 2 hours
                "quality_threshold": 0.85,
                "max_failures": 5,
                "max_agents_per_day": 8,
                "research_timeout_seconds": 600,
                "emergency_stop_enabled": True,
                "research_source_weights": {
                    "academic": 0.3,
                    "industry": 0.4,
                    "government": 0.2,
                    "news": 0.1
                },
                "safety_limits": {
                    "max_memory_usage_mb": 1024,
                    "max_api_calls_per_hour": 200,
                    "max_concurrent_research": 4
                }
            },
            ConfigPreset.AGGRESSIVE.value: {
                "cycle_interval_minutes": 60,  # 1 hour
                "quality_threshold": 0.75,
                "max_failures": 10,
                "max_agents_per_day": 20,
                "research_timeout_seconds": 900,
                "emergency_stop_enabled": True,
                "research_source_weights": {
                    "academic": 0.2,
                    "industry": 0.5,
                    "government": 0.2,
                    "news": 0.1
                },
                "safety_limits": {
                    "max_memory_usage_mb": 2048,
                    "max_api_calls_per_hour": 500,
                    "max_concurrent_research": 8
                }
            }
        }
    
    def _load_or_create_config(self) -> Dict[str, Any]:
        """Load existing configuration or create default."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._create_default_config()
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration."""
        default_config = {
            "metadata": {
                "version": 1,
                "created": datetime.now().isoformat(),
                "preset_mode": ConfigPreset.BALANCED.value,
                "last_modified": datetime.now().isoformat(),
                "modified_by": "system"
            },
            "autonomous_operation": {
                "enabled": True,
                "cycle_interval_minutes": 120,
                "max_cycles_per_day": 12,
                "auto_start_on_boot": True,
                "require_human_approval": False
            },
            "quality_assurance": {
                "validation_score_threshold": 0.85,
                "duplicate_similarity_threshold": 0.8,
                "multi_tier_validation": True,
                "constitutional_compliance_check": True
            },
            "safety_limits": {
                "error_thresholds": {
                    "max_consecutive_failures": 5,
                    "max_failure_rate_percent": 20,
                    "auto_disable_on_errors": True
                },
                "resource_limits": {
                    "max_memory_usage_mb": 1024,
                    "max_disk_usage_mb": 500,
                    "max_api_calls_per_hour": 200
                },
                "emergency_controls": {
                    "emergency_stop_enabled": True,
                    "human_override_required": False,
                    "cooldown_period_minutes": 30
                }
            },
            "research_configuration": {
                "timeout_seconds": 600,
                "max_concurrent_research": 4,
                "source_priorities": {
                    "academic_papers": 0.3,
                    "industry_reports": 0.4,
                    "government_data": 0.2,
                    "news_sources": 0.1
                },
                "cache_duration_hours": 24
            },
            "agent_creation": {
                "max_agents_per_day": 8,
                "max_agents_per_domain": 5,
                "quality_gate_enabled": True,
                "approval_workflow": "automatic"
            }
        }
        
        # Apply balanced preset
        self._apply_preset_to_config(default_config, ConfigPreset.BALANCED.value)
        self._save_config(default_config)
        return default_config
    
    def _load_config_history(self) -> List[Dict[str, Any]]:
        """Load configuration change history."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def _save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file."""
        try:
            # Create backup first
            self._create_backup()
            
            # Update metadata
            config["metadata"]["last_modified"] = datetime.now().isoformat()
            config["metadata"]["version"] = config["metadata"].get("version", 0) + 1
            
            # Save configuration
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            # Update history
            self._add_to_history(config)
            
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _create_backup(self) -> str:
        """Create a backup of current configuration."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"config_backup_{timestamp}.json")
        
        try:
            with open(backup_file, 'w') as f:
                json.dump(self.current_config, f, indent=2)
            return backup_file
        except Exception as e:
            print(f"Error creating backup: {e}")
            return ""
    
    def _add_to_history(self, config: Dict[str, Any]) -> None:
        """Add configuration change to history."""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "version": config["metadata"]["version"],
            "preset_mode": config["metadata"]["preset_mode"],
            "modified_by": config["metadata"]["modified_by"],
            "changes": self._calculate_changes(self.current_config, config)
        }
        
        self.config_history.append(history_entry)
        
        # Keep only last 100 entries
        if len(self.config_history) > 100:
            self.config_history = self.config_history[-100:]
        
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.config_history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def _calculate_changes(self, old_config: Dict[str, Any], new_config: Dict[str, Any]) -> List[str]:
        """Calculate what changed between configurations."""
        changes = []
        
        def compare_dicts(old_dict, new_dict, path=""):
            for key in set(old_dict.keys()) | set(new_dict.keys()):
                current_path = f"{path}.{key}" if path else key
                
                if key not in old_dict:
                    changes.append(f"Added: {current_path} = {new_dict[key]}")
                elif key not in new_dict:
                    changes.append(f"Removed: {current_path}")
                elif isinstance(old_dict[key], dict) and isinstance(new_dict[key], dict):
                    compare_dicts(old_dict[key], new_dict[key], current_path)
                elif old_dict[key] != new_dict[key]:
                    changes.append(f"Changed: {current_path} from {old_dict[key]} to {new_dict[key]}")
        
        compare_dicts(old_config, new_config)
        return changes
    
    def validate_configuration(self, config: Dict[str, Any]) -> ConfigValidationResult:
        """Validate configuration against rules and constitutional requirements."""
        errors = []
        warnings = []
        
        # Basic validation
        try:
            # Check cycle interval
            interval = config["autonomous_operation"]["cycle_interval_minutes"]
            if not 30 <= interval <= 1440:  # 30 minutes to 24 hours
                errors.append("Cycle interval must be between 30 minutes and 24 hours")
            
            # Check quality threshold
            quality_threshold = config["quality_assurance"]["validation_score_threshold"]
            if not 0.5 <= quality_threshold <= 1.0:
                errors.append("Quality threshold must be between 0.5 and 1.0")
            
            # Check safety limits
            max_failures = config["safety_limits"]["error_thresholds"]["max_consecutive_failures"]
            if max_failures < 1 or max_failures > 20:
                errors.append("Max consecutive failures must be between 1 and 20")
            
            # Check resource limits
            memory_limit = config["safety_limits"]["resource_limits"]["max_memory_usage_mb"]
            if memory_limit < 256 or memory_limit > 4096:
                warnings.append("Memory limit outside recommended range (256-4096 MB)")
            
            # Constitutional compliance checks
            constitutional_compliance = True
            if not config["quality_assurance"]["constitutional_compliance_check"]:
                errors.append("Constitutional compliance check cannot be disabled")
                constitutional_compliance = False
            
            if not config["safety_limits"]["emergency_controls"]["emergency_stop_enabled"]:
                warnings.append("Emergency stop is disabled - this reduces safety")
            
        except KeyError as e:
            errors.append(f"Missing required configuration key: {e}")
            constitutional_compliance = False
        except Exception as e:
            errors.append(f"Configuration validation error: {e}")
            constitutional_compliance = False
        
        return ConfigValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            constitutional_compliance=constitutional_compliance
        )
    
    def apply_preset(self, preset: ConfigPreset, modified_by: str = "user") -> Tuple[bool, str]:
        """Apply a configuration preset."""
        if preset.value not in self.presets:
            return False, f"Unknown preset: {preset.value}"
        
        try:
            # Create new config based on current
            new_config = copy.deepcopy(self.current_config)
            
            # Apply preset
            self._apply_preset_to_config(new_config, preset.value)
            
            # Update metadata
            new_config["metadata"]["preset_mode"] = preset.value
            new_config["metadata"]["modified_by"] = modified_by
            
            # Validate
            validation = self.validate_configuration(new_config)
            if not validation.is_valid:
                return False, f"Preset validation failed: {'; '.join(validation.errors)}"
            
            # Save
            if self._save_config(new_config):
                self.current_config = new_config
                return True, f"Successfully applied {preset.value} preset"
            else:
                return False, "Failed to save configuration"
                
        except Exception as e:
            return False, f"Error applying preset: {e}"
    
    def _apply_preset_to_config(self, config: Dict[str, Any], preset_name: str) -> None:
        """Apply preset values to configuration."""
        preset_values = self.presets[preset_name]
        
        # Apply autonomous operation settings
        config["autonomous_operation"]["cycle_interval_minutes"] = preset_values["cycle_interval_minutes"]
        
        # Apply quality settings
        config["quality_assurance"]["validation_score_threshold"] = preset_values["quality_threshold"]
        
        # Apply safety limits
        config["safety_limits"]["error_thresholds"]["max_consecutive_failures"] = preset_values["max_failures"]
        config["safety_limits"]["emergency_controls"]["emergency_stop_enabled"] = preset_values["emergency_stop_enabled"]
        
        # Apply research settings
        config["research_configuration"]["timeout_seconds"] = preset_values["research_timeout_seconds"]
        config["research_configuration"]["source_priorities"] = preset_values["research_source_weights"]
        
        # Apply agent creation limits
        config["agent_creation"]["max_agents_per_day"] = preset_values["max_agents_per_day"]
        
        # Apply safety limits
        if "safety_limits" in preset_values:
            config["safety_limits"]["resource_limits"].update(preset_values["safety_limits"])
    
    def update_configuration(self, updates: Dict[str, Any], modified_by: str = "user") -> Tuple[bool, str]:
        """Update configuration with new values."""
        try:
            # Create new config with updates
            new_config = copy.deepcopy(self.current_config)
            
            # Apply updates
            self._deep_update(new_config, updates)
            
            # Update metadata
            new_config["metadata"]["modified_by"] = modified_by
            new_config["metadata"]["preset_mode"] = ConfigPreset.CUSTOM.value
            
            # Validate
            validation = self.validate_configuration(new_config)
            if not validation.is_valid:
                return False, f"Configuration validation failed: {'; '.join(validation.errors)}"
            
            # Save
            if self._save_config(new_config):
                self.current_config = new_config
                return True, "Configuration updated successfully"
            else:
                return False, "Failed to save configuration"
                
        except Exception as e:
            return False, f"Error updating configuration: {e}"
    
    def _deep_update(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Deep update dictionary."""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def rollback_to_version(self, version: int) -> Tuple[bool, str]:
        """Rollback to a specific configuration version."""
        try:
            # Find backup file for version
            backup_files = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            backup_files.sort(reverse=True)
            
            if not backup_files:
                return False, "No backup files available for rollback"
            
            # For now, rollback to most recent backup
            # In a full implementation, we'd track versions more precisely
            backup_file = os.path.join(self.backup_dir, backup_files[0])
            
            with open(backup_file, 'r') as f:
                backup_config = json.load(f)
            
            # Validate backup
            validation = self.validate_configuration(backup_config)
            if not validation.is_valid:
                return False, f"Backup configuration is invalid: {'; '.join(validation.errors)}"
            
            # Apply rollback
            backup_config["metadata"]["modified_by"] = "rollback"
            backup_config["metadata"]["last_modified"] = datetime.now().isoformat()
            
            if self._save_config(backup_config):
                self.current_config = backup_config
                return True, f"Successfully rolled back to version {version}"
            else:
                return False, "Failed to save rolled back configuration"
                
        except Exception as e:
            return False, f"Error during rollback: {e}"
    
    def get_current_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        return copy.deepcopy(self.current_config)
    
    def get_config_history(self) -> List[Dict[str, Any]]:
        """Get configuration change history."""
        return copy.deepcopy(self.config_history)
    
    def get_available_presets(self) -> Dict[str, Dict[str, Any]]:
        """Get available configuration presets."""
        return copy.deepcopy(self.presets)
    
    def export_configuration(self, include_history: bool = False) -> Dict[str, Any]:
        """Export configuration for backup or sharing."""
        export_data = {
            "configuration": self.current_config,
            "exported_at": datetime.now().isoformat(),
            "version": self.current_config["metadata"]["version"]
        }
        
        if include_history:
            export_data["history"] = self.config_history
        
        return export_data
    
    def import_configuration(self, config_data: Dict[str, Any], modified_by: str = "import") -> Tuple[bool, str]:
        """Import configuration from backup or external source."""
        try:
            if "configuration" not in config_data:
                return False, "Invalid import data: missing configuration"
            
            imported_config = config_data["configuration"]
            
            # Validate imported configuration
            validation = self.validate_configuration(imported_config)
            if not validation.is_valid:
                return False, f"Imported configuration is invalid: {'; '.join(validation.errors)}"
            
            # Update metadata
            imported_config["metadata"]["modified_by"] = modified_by
            imported_config["metadata"]["last_modified"] = datetime.now().isoformat()
            
            # Save
            if self._save_config(imported_config):
                self.current_config = imported_config
                return True, "Configuration imported successfully"
            else:
                return False, "Failed to save imported configuration"
                
        except Exception as e:
            return False, f"Error importing configuration: {e}"

# Example usage and testing
if __name__ == "__main__":
    config_manager = EnhancedConfigManager()
    
    # Test preset application
    success, message = config_manager.apply_preset(ConfigPreset.AGGRESSIVE)
    print(f"Apply aggressive preset: {success} - {message}")
    
    # Test configuration update
    updates = {
        "autonomous_operation": {
            "cycle_interval_minutes": 90
        }
    }
    success, message = config_manager.update_configuration(updates)
    print(f"Update configuration: {success} - {message}")
    
    # Test validation
    validation = config_manager.validate_configuration(config_manager.current_config)
    print(f"Validation: {validation.is_valid}, Errors: {validation.errors}")
    
    print("Enhanced Configuration Manager initialized successfully!")
