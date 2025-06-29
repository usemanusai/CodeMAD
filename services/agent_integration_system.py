#!/usr/bin/env python3
"""
Agent Integration System for Project Chimera
Handles integration of newly synthesized agents with existing Cipher Architecture.
Manages school validation, orchestrator approval, and system registration.
"""

import json
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add services directory to path for imports
sys.path.append(os.path.dirname(__file__))

class AgentIntegrationSystem:
    """
    Comprehensive integration system for newly synthesized agents.
    Handles validation, approval, and registration with existing systems.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.config_file = self.workspace_root / "services" / "config" / "expansion_config.json"
        self.constitution_file = self.workspace_root / "governance" / "constitution.json"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load configurations
        self.config = self._load_config()
        self.constitution = self._load_constitution()
        
        # Initialize subsystems
        from agent_directory_service import AgentDirectoryService
        from asset_generator import AssetGenerator
        
        self.agent_directory = AgentDirectoryService(workspace_root)
        self.asset_generator = AssetGenerator(workspace_root)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load expansion configuration."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def _load_constitution(self) -> Dict[str, Any]:
        """Load constitutional requirements."""
        try:
            with open(self.constitution_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading constitution: {e}")
            return {}
    
    def integrate_agent(self, blueprint: Any) -> Dict[str, Any]:
        """
        Integrate a new agent into the Cipher Architecture.
        
        Args:
            blueprint: AgentBlueprint object from synthesis
            
        Returns:
            Integration result with status and details
        """
        self.logger.info(f"Starting integration for agent: {blueprint.agent_id}")
        self._log_audit_event("AGENT_INTEGRATION_STARTED", f"Integrating agent: {blueprint.agent_id}")
        
        integration_result = {
            'success': False,
            'agent_id': blueprint.agent_id,
            'integration_steps': {},
            'errors': [],
            'warnings': []
        }
        
        try:
            # Phase 1: Pre-integration validation
            validation_result = self._pre_integration_validation(blueprint)
            integration_result['integration_steps']['validation'] = validation_result
            
            if not validation_result['success']:
                integration_result['errors'].extend(validation_result['errors'])
                return integration_result
            
            # Phase 2: Generate assets
            asset_result = self._generate_agent_assets(blueprint)
            integration_result['integration_steps']['asset_generation'] = asset_result
            
            if not asset_result['success']:
                integration_result['errors'].extend(asset_result['errors'])
                return integration_result
            
            # Phase 3: School validation (simulated)
            school_result = self._school_validation(blueprint)
            integration_result['integration_steps']['school_validation'] = school_result
            
            if not school_result['success']:
                integration_result['errors'].extend(school_result['errors'])
                return integration_result
            
            # Phase 4: Orchestrator approval (simulated)
            approval_result = self._orchestrator_approval(blueprint)
            integration_result['integration_steps']['orchestrator_approval'] = approval_result
            
            if not approval_result['success']:
                integration_result['errors'].extend(approval_result['errors'])
                return integration_result
            
            # Phase 5: System registration
            registration_result = self._system_registration(blueprint)
            integration_result['integration_steps']['system_registration'] = registration_result
            
            if not registration_result['success']:
                integration_result['errors'].extend(registration_result['errors'])
                return integration_result
            
            # Phase 6: Final validation and activation
            activation_result = self._agent_activation(blueprint)
            integration_result['integration_steps']['activation'] = activation_result
            
            integration_result['success'] = activation_result['success']
            
            if integration_result['success']:
                self._log_audit_event("AGENT_INTEGRATION_COMPLETED", f"Successfully integrated agent: {blueprint.agent_id}")
                self.logger.info(f"Agent integration completed successfully: {blueprint.agent_id}")
            else:
                integration_result['errors'].extend(activation_result['errors'])
                
        except Exception as e:
            self.logger.error(f"Error during integration: {e}")
            integration_result['errors'].append(f"Integration error: {str(e)}")
            self._log_audit_event("AGENT_INTEGRATION_ERROR", f"Error integrating {blueprint.agent_id}: {str(e)}")
        
        return integration_result
    
    def _pre_integration_validation(self, blueprint: Any) -> Dict[str, Any]:
        """Perform pre-integration validation checks."""
        result = {'success': False, 'errors': [], 'warnings': []}
        
        try:
            # Check agent ID uniqueness
            existing_agent = self.agent_directory.get_agent_by_id(blueprint.agent_id)
            if existing_agent:
                result['errors'].append(f"Agent ID {blueprint.agent_id} already exists")
                return result
            
            # Check constitutional compliance requirements
            lifecycle_config = self.constitution.get('operational_requirements', {}).get('agent_lifecycle', {})
            
            if lifecycle_config.get('creation') == 'must_pass_school_validation':
                result['warnings'].append("Agent must pass school validation")
            
            if lifecycle_config.get('deployment') == 'requires_orchestrator_approval':
                result['warnings'].append("Agent requires orchestrator approval")
            
            # Validate blueprint quality
            if blueprint.quality_score < 0.7:
                result['errors'].append(f"Blueprint quality score too low: {blueprint.quality_score}")
                return result
            
            result['success'] = True
            self.logger.info(f"Pre-integration validation passed for: {blueprint.agent_id}")
            
        except Exception as e:
            result['errors'].append(f"Validation error: {str(e)}")
        
        return result
    
    def _generate_agent_assets(self, blueprint: Any) -> Dict[str, Any]:
        """Generate all required assets for the agent."""
        result = {'success': False, 'errors': [], 'generated_assets': {}}
        
        try:
            asset_result = self.asset_generator.generate_agent_assets(blueprint)
            
            if asset_result['success']:
                result['success'] = True
                result['generated_assets'] = asset_result['generated_assets']
                self.logger.info(f"Assets generated successfully for: {blueprint.agent_id}")
            else:
                result['errors'].extend(asset_result['errors'])
                
        except Exception as e:
            result['errors'].append(f"Asset generation error: {str(e)}")
        
        return result
    
    def _school_validation(self, blueprint: Any) -> Dict[str, Any]:
        """Simulate school validation process."""
        result = {'success': False, 'errors': [], 'validation_score': 0.0}
        
        try:
            # Simulate school validation criteria
            validation_criteria = {
                'persona_quality': self._evaluate_persona_quality(blueprint),
                'task_completeness': self._evaluate_task_completeness(blueprint),
                'domain_expertise': self._evaluate_domain_expertise(blueprint),
                'integration_readiness': self._evaluate_integration_readiness(blueprint)
            }
            
            # Calculate overall validation score
            validation_score = sum(validation_criteria.values()) / len(validation_criteria)
            result['validation_score'] = validation_score
            
            # School validation threshold
            school_threshold = 0.75
            
            if validation_score >= school_threshold:
                result['success'] = True
                self.logger.info(f"School validation passed for: {blueprint.agent_id} (Score: {validation_score:.3f})")
            else:
                result['errors'].append(f"School validation failed: Score {validation_score:.3f} below threshold {school_threshold}")
            
            # Log validation details
            self._log_audit_event("SCHOOL_VALIDATION", f"Agent {blueprint.agent_id} validation score: {validation_score:.3f}")
            
        except Exception as e:
            result['errors'].append(f"School validation error: {str(e)}")
        
        return result
    
    def _orchestrator_approval(self, blueprint: Any) -> Dict[str, Any]:
        """Simulate orchestrator approval process."""
        result = {'success': False, 'errors': [], 'approval_rationale': ''}
        
        try:
            # Simulate orchestrator approval criteria
            approval_criteria = {
                'strategic_alignment': self._evaluate_strategic_alignment(blueprint),
                'resource_requirements': self._evaluate_resource_requirements(blueprint),
                'risk_assessment': self._evaluate_risk_level(blueprint),
                'business_value': self._evaluate_business_value(blueprint)
            }
            
            # Calculate approval score
            approval_score = sum(approval_criteria.values()) / len(approval_criteria)
            
            # Orchestrator approval threshold
            approval_threshold = 0.70
            
            if approval_score >= approval_threshold:
                result['success'] = True
                result['approval_rationale'] = f"Agent approved with score {approval_score:.3f}. Meets strategic and operational requirements."
                self.logger.info(f"Orchestrator approval granted for: {blueprint.agent_id}")
            else:
                result['errors'].append(f"Orchestrator approval denied: Score {approval_score:.3f} below threshold {approval_threshold}")
                result['approval_rationale'] = "Agent does not meet strategic or operational requirements."
            
            # Log approval decision
            self._log_audit_event("ORCHESTRATOR_APPROVAL", f"Agent {blueprint.agent_id} approval score: {approval_score:.3f}")
            
        except Exception as e:
            result['errors'].append(f"Orchestrator approval error: {str(e)}")
        
        return result
    
    def _system_registration(self, blueprint: Any) -> Dict[str, Any]:
        """Register agent with system directories and services."""
        result = {'success': False, 'errors': [], 'registration_id': None}
        
        try:
            # Create agent data for registration
            agent_data = {
                'id': blueprint.agent_id,
                'title': blueprint.title,
                'name': blueprint.name,
                'description': blueprint.description,
                'persona': f"agents/classes/{blueprint.agent_id}.md",
                'specializations': blueprint.specializations,
                'domain': blueprint.domain,
                'status': 'active',
                'source': 'autonomous_synthesis',
                'quality_score': blueprint.quality_score,
                'creation_rationale': blueprint.creation_rationale
            }
            
            # Register with Agent Directory Service
            registration_id = self.agent_directory.register_new_agent(agent_data)
            
            result['success'] = True
            result['registration_id'] = registration_id
            self.logger.info(f"Agent registered successfully: {registration_id}")
            
        except Exception as e:
            result['errors'].append(f"Registration error: {str(e)}")
        
        return result
    
    def _agent_activation(self, blueprint: Any) -> Dict[str, Any]:
        """Activate agent and finalize integration."""
        result = {'success': False, 'errors': [], 'activation_timestamp': None}
        
        try:
            # Final validation checks
            if not self._verify_asset_integrity(blueprint):
                result['errors'].append("Asset integrity verification failed")
                return result
            
            # Set activation timestamp
            activation_timestamp = datetime.now().isoformat()
            result['activation_timestamp'] = activation_timestamp
            
            # Mark as successfully activated
            result['success'] = True
            
            self.logger.info(f"Agent activated successfully: {blueprint.agent_id}")
            self._log_audit_event("AGENT_ACTIVATED", f"Agent {blueprint.agent_id} activated at {activation_timestamp}")
            
        except Exception as e:
            result['errors'].append(f"Activation error: {str(e)}")
        
        return result
    
    def _evaluate_persona_quality(self, blueprint: Any) -> float:
        """Evaluate persona quality."""
        score = 0.5  # Base score
        
        if len(blueprint.persona_content) > 500:
            score += 0.2
        
        if len(blueprint.specializations) >= 3:
            score += 0.2
        
        if len(blueprint.key_responsibilities) >= 3:
            score += 0.1
        
        return min(1.0, score)
    
    def _evaluate_task_completeness(self, blueprint: Any) -> float:
        """Evaluate task completeness."""
        score = 0.5  # Base score
        
        if len(blueprint.tasks) >= 2:
            score += 0.3
        
        if len(blueprint.templates) >= 1:
            score += 0.1
        
        if len(blueprint.checklists) >= 1:
            score += 0.1
        
        return min(1.0, score)
    
    def _evaluate_domain_expertise(self, blueprint: Any) -> float:
        """Evaluate domain expertise."""
        score = 0.6  # Base score
        
        # High-value domains
        high_value_domains = ['ai', 'healthcare', 'cybersecurity', 'renewable energy']
        if any(domain in blueprint.domain.lower() for domain in high_value_domains):
            score += 0.3
        
        if len(blueprint.required_skills) >= 5:
            score += 0.1
        
        return min(1.0, score)
    
    def _evaluate_integration_readiness(self, blueprint: Any) -> float:
        """Evaluate integration readiness."""
        score = 0.5  # Base score
        
        if blueprint.memory_structure:
            score += 0.3
        
        if blueprint.quality_score > 0.8:
            score += 0.2
        
        return min(1.0, score)
    
    def _evaluate_strategic_alignment(self, blueprint: Any) -> float:
        """Evaluate strategic alignment."""
        return 0.8  # Assume good alignment for autonomous synthesis
    
    def _evaluate_resource_requirements(self, blueprint: Any) -> float:
        """Evaluate resource requirements."""
        return 0.9  # Assume low resource requirements for knowledge agents
    
    def _evaluate_risk_level(self, blueprint: Any) -> float:
        """Evaluate risk level (higher score = lower risk)."""
        return 0.85  # Assume low risk for specialist agents
    
    def _evaluate_business_value(self, blueprint: Any) -> float:
        """Evaluate business value."""
        return 0.8  # Assume good business value for identified gaps
    
    def _verify_asset_integrity(self, blueprint: Any) -> bool:
        """Verify that all assets were created successfully."""
        try:
            # Check persona file
            persona_file = self.workspace_root / "agents" / "classes" / f"{blueprint.agent_id}.md"
            if not persona_file.exists():
                return False
            
            # Check memory directory
            memory_dir = self.workspace_root / "memory" / blueprint.agent_id
            if not memory_dir.exists():
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Asset integrity verification error: {e}")
            return False
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} AGENT_INTEGRATION_SYSTEM {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    # Mock blueprint for testing
    class MockBlueprint:
        def __init__(self):
            self.agent_id = "integration_test_agent"
            self.title = "Integration Test Specialist"
            self.name = "Test Agent"
            self.description = "Agent for testing integration system"
            self.domain = "Testing"
            self.specializations = ["Integration Testing", "System Validation", "Quality Assurance"]
            self.key_responsibilities = ["Test integrations", "Validate systems", "Ensure quality"]
            self.required_skills = ["Testing", "Integration", "Validation", "Quality Assurance", "Documentation"]
            self.persona_content = "# Integration Test Specialist\n\n" + "A" * 600
            self.tasks = [
                {"name": "Integration Testing", "description": "Test system integrations", "type": "testing"},
                {"name": "Validation", "description": "Validate system functionality", "type": "validation"}
            ]
            self.templates = [{"name": "Test Report Template", "description": "Template for test reports"}]
            self.checklists = [{"name": "Integration Checklist", "description": "Checklist for integrations"}]
            self.memory_structure = {
                "knowledge_graph": {"domain": "Testing"},
                "episodic_memory": {"creation": "test"},
                "working_memory": {}
            }
            self.quality_score = 0.85
            self.creation_rationale = "Created for testing integration system"
    
    integration_system = AgentIntegrationSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            print("Testing Agent Integration System...")
            mock_blueprint = MockBlueprint()
            result = integration_system.integrate_agent(mock_blueprint)
            
            print(f"✅ Integration completed")
            print(f"   Success: {result['success']}")
            print(f"   Agent ID: {result['agent_id']}")
            print(f"   Integration steps: {len(result['integration_steps'])}")
            
            for step_name, step_result in result['integration_steps'].items():
                status = "✅" if step_result.get('success', False) else "❌"
                print(f"   {status} {step_name}: {'Passed' if step_result.get('success', False) else 'Failed'}")
            
            if result['errors']:
                print("   Errors:")
                for error in result['errors']:
                    print(f"     - {error}")
        
        else:
            print("Usage: python agent_integration_system.py [test]")
    else:
        print("Agent Integration System initialized successfully")
