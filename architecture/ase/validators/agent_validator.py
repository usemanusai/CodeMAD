#!/usr/bin/env python3
"""
Agent Validator for Project Chimera ASE
Validates agent blueprints for quality, completeness, and constitutional compliance.
"""

import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

class AgentValidator:
    """
    Comprehensive validator for agent blueprints.
    Ensures quality, completeness, and compliance with Cipher Architecture standards.
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
        
        # Validation thresholds
        self.quality_thresholds = self.config.get('quality_thresholds', {}).get('agent_creation', {})
    
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
    
    def validate_blueprint(self, blueprint: Any) -> Dict[str, Any]:
        """
        Comprehensive validation of agent blueprint.
        
        Args:
            blueprint: AgentBlueprint object to validate
            
        Returns:
            Validation result with quality score and errors
        """
        self.logger.info(f"Validating agent blueprint: {blueprint.agent_id}")
        
        validation_result = {
            'is_valid': False,
            'quality_score': 0.0,
            'errors': [],
            'warnings': [],
            'recommendations': [],
            'validation_details': {}
        }
        
        try:
            # Phase 1: Basic structure validation
            structure_result = self._validate_structure(blueprint)
            validation_result['validation_details']['structure'] = structure_result
            
            # Phase 2: Content quality validation
            content_result = self._validate_content_quality(blueprint)
            validation_result['validation_details']['content'] = content_result
            
            # Phase 3: Constitutional compliance validation
            compliance_result = self._validate_constitutional_compliance(blueprint)
            validation_result['validation_details']['compliance'] = compliance_result
            
            # Phase 4: Integration validation
            integration_result = self._validate_integration_readiness(blueprint)
            validation_result['validation_details']['integration'] = integration_result
            
            # Calculate overall quality score
            quality_score = self._calculate_quality_score(
                structure_result, content_result, compliance_result, integration_result
            )
            validation_result['quality_score'] = quality_score
            
            # Collect all errors and warnings
            all_results = [structure_result, content_result, compliance_result, integration_result]
            for result in all_results:
                validation_result['errors'].extend(result.get('errors', []))
                validation_result['warnings'].extend(result.get('warnings', []))
                validation_result['recommendations'].extend(result.get('recommendations', []))
            
            # Determine if valid based on thresholds
            min_quality = self.quality_thresholds.get('validation_score_threshold', 0.85)
            validation_result['is_valid'] = (
                quality_score >= min_quality and 
                len(validation_result['errors']) == 0
            )
            
            self._log_validation_result(blueprint, validation_result)
            
        except Exception as e:
            self.logger.error(f"Error during validation: {e}")
            validation_result['errors'].append(f"Validation error: {str(e)}")
        
        return validation_result
    
    def _validate_structure(self, blueprint: Any) -> Dict[str, Any]:
        """Validate basic structure and required fields."""
        result = {
            'score': 0.0,
            'errors': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Required fields validation
        required_fields = [
            'agent_id', 'title', 'name', 'description', 'domain',
            'specializations', 'key_responsibilities', 'required_skills'
        ]
        
        missing_fields = []
        for field in required_fields:
            if not hasattr(blueprint, field) or not getattr(blueprint, field):
                missing_fields.append(field)
        
        if missing_fields:
            result['errors'].append(f"Missing required fields: {', '.join(missing_fields)}")
        else:
            result['score'] += 0.3
        
        # Agent ID validation
        if hasattr(blueprint, 'agent_id'):
            if not re.match(r'^[a-z0-9_]+$', blueprint.agent_id):
                result['errors'].append("Agent ID must contain only lowercase letters, numbers, and underscores")
            elif len(blueprint.agent_id) < 3 or len(blueprint.agent_id) > 50:
                result['errors'].append("Agent ID must be between 3 and 50 characters")
            else:
                result['score'] += 0.2
        
        # Title validation
        if hasattr(blueprint, 'title'):
            if len(blueprint.title) < 5 or len(blueprint.title) > 100:
                result['warnings'].append("Title should be between 5 and 100 characters")
            else:
                result['score'] += 0.2
        
        # Description validation
        if hasattr(blueprint, 'description'):
            if len(blueprint.description) < 20 or len(blueprint.description) > 500:
                result['warnings'].append("Description should be between 20 and 500 characters")
            else:
                result['score'] += 0.3
        
        return result
    
    def _validate_content_quality(self, blueprint: Any) -> Dict[str, Any]:
        """Validate content quality and completeness."""
        result = {
            'score': 0.0,
            'errors': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Specializations validation
        if hasattr(blueprint, 'specializations'):
            if len(blueprint.specializations) < 3:
                result['warnings'].append("Consider adding more specializations (minimum 3 recommended)")
            elif len(blueprint.specializations) > 10:
                result['warnings'].append("Too many specializations may dilute focus (maximum 10 recommended)")
            else:
                result['score'] += 0.2
        
        # Responsibilities validation
        if hasattr(blueprint, 'key_responsibilities'):
            if len(blueprint.key_responsibilities) < 3:
                result['errors'].append("Minimum 3 key responsibilities required")
            elif len(blueprint.key_responsibilities) > 8:
                result['warnings'].append("Too many responsibilities may be overwhelming (maximum 8 recommended)")
            else:
                result['score'] += 0.2
        
        # Skills validation
        if hasattr(blueprint, 'required_skills'):
            if len(blueprint.required_skills) < 4:
                result['warnings'].append("Consider adding more required skills (minimum 4 recommended)")
            elif len(blueprint.required_skills) > 12:
                result['warnings'].append("Too many skills may be unrealistic (maximum 12 recommended)")
            else:
                result['score'] += 0.2
        
        # Persona content validation
        if hasattr(blueprint, 'persona_content'):
            if len(blueprint.persona_content) < 500:
                result['errors'].append("Persona content too short (minimum 500 characters)")
            elif len(blueprint.persona_content) > 5000:
                result['warnings'].append("Persona content very long (consider condensing)")
            else:
                result['score'] += 0.2
        
        # Tasks validation
        if hasattr(blueprint, 'tasks'):
            if len(blueprint.tasks) < 2:
                result['warnings'].append("Consider adding more tasks (minimum 2 recommended)")
            elif len(blueprint.tasks) > 6:
                result['warnings'].append("Too many tasks may be overwhelming (maximum 6 recommended)")
            else:
                result['score'] += 0.2
        
        return result
    
    def _validate_constitutional_compliance(self, blueprint: Any) -> Dict[str, Any]:
        """Validate compliance with constitutional requirements."""
        result = {
            'score': 0.0,
            'errors': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Check agent lifecycle compliance
        lifecycle_requirements = self.constitution.get('operational_requirements', {}).get('agent_lifecycle', {})
        
        # School validation requirement
        if lifecycle_requirements.get('creation') == 'must_pass_school_validation':
            result['recommendations'].append("Agent must pass school validation before deployment")
            result['score'] += 0.3
        
        # Orchestrator approval requirement
        if lifecycle_requirements.get('deployment') == 'requires_orchestrator_approval':
            result['recommendations'].append("Agent requires orchestrator approval for deployment")
            result['score'] += 0.3
        
        # Agent class compliance
        agent_classes = self.constitution.get('governance_structure', {}).get('agent_classes', {})
        
        # Assume this is a specialist agent
        if 'specialist_agents' in agent_classes:
            permissions = agent_classes['specialist_agents'].get('permissions')
            if permissions == 'domain_specific_operations':
                result['score'] += 0.4
                result['recommendations'].append("Agent classified as Specialist Agent with domain-specific permissions")
        
        return result
    
    def _validate_integration_readiness(self, blueprint: Any) -> Dict[str, Any]:
        """Validate readiness for integration with existing systems."""
        result = {
            'score': 0.0,
            'errors': [],
            'warnings': [],
            'recommendations': []
        }
        
        # Memory structure validation
        if hasattr(blueprint, 'memory_structure'):
            if not blueprint.memory_structure:
                result['errors'].append("Memory structure is required for integration")
            else:
                required_memory_components = ['knowledge_graph', 'episodic_memory', 'working_memory']
                missing_components = []
                
                for component in required_memory_components:
                    if component not in blueprint.memory_structure:
                        missing_components.append(component)
                
                if missing_components:
                    result['warnings'].append(f"Missing memory components: {', '.join(missing_components)}")
                else:
                    result['score'] += 0.4
        
        # Domain alignment validation
        if hasattr(blueprint, 'domain'):
            # Check if domain is reasonable
            if len(blueprint.domain.split()) > 5:
                result['warnings'].append("Domain name is very long - consider simplifying")
            else:
                result['score'] += 0.2
        
        # Uniqueness validation (basic check)
        if hasattr(blueprint, 'agent_id') and hasattr(blueprint, 'title'):
            # This would ideally check against existing agents
            # For now, just validate the ID format suggests uniqueness
            if '_' in blueprint.agent_id or len(blueprint.agent_id) > 10:
                result['score'] += 0.2
            else:
                result['recommendations'].append("Consider making agent ID more specific for uniqueness")
        
        # Template and checklist validation
        if hasattr(blueprint, 'templates') and hasattr(blueprint, 'checklists'):
            if blueprint.templates and blueprint.checklists:
                result['score'] += 0.2
            else:
                result['warnings'].append("Templates and checklists enhance agent capabilities")
        
        return result
    
    def _calculate_quality_score(self, structure_result: Dict, content_result: Dict, 
                                compliance_result: Dict, integration_result: Dict) -> float:
        """Calculate overall quality score."""
        
        # Weighted combination of scores
        weights = {
            'structure': 0.3,
            'content': 0.3,
            'compliance': 0.2,
            'integration': 0.2
        }
        
        total_score = (
            structure_result['score'] * weights['structure'] +
            content_result['score'] * weights['content'] +
            compliance_result['score'] * weights['compliance'] +
            integration_result['score'] * weights['integration']
        )
        
        return min(1.0, total_score)
    
    def _log_validation_result(self, blueprint: Any, result: Dict[str, Any]):
        """Log validation result to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            
            status = "PASSED" if result['is_valid'] else "FAILED"
            score = result['quality_score']
            errors = len(result['errors'])
            
            details = f"Agent {blueprint.agent_id} validation {status} (Score: {score:.3f}, Errors: {errors})"
            log_entry = f"[{timestamp}] AGENT_VALIDATION AGENT_VALIDATOR {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging validation result: {e}")
    
    def validate_agent_name_uniqueness(self, agent_id: str, existing_agents: List[Dict]) -> bool:
        """Validate that agent ID is unique."""
        return not any(agent.get('id') == agent_id for agent in existing_agents)
    
    def suggest_improvements(self, blueprint: Any, validation_result: Dict[str, Any]) -> List[str]:
        """Suggest improvements based on validation results."""
        suggestions = []
        
        # Add suggestions based on warnings and recommendations
        suggestions.extend(validation_result.get('recommendations', []))
        
        # Add specific suggestions based on quality score
        quality_score = validation_result.get('quality_score', 0.0)
        
        if quality_score < 0.7:
            suggestions.append("Consider enhancing agent description and specializations")
        
        if quality_score < 0.8:
            suggestions.append("Add more detailed responsibilities and required skills")
        
        if quality_score < 0.9:
            suggestions.append("Enhance persona content with more specific guidelines")
        
        return suggestions

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    # Mock blueprint for testing
    class MockBlueprint:
        def __init__(self):
            self.agent_id = "ai_ethics_specialist"
            self.title = "AI Ethics Specialist"
            self.name = "Dr. Ethics"
            self.description = "Specialist in AI ethics and governance within the AI sector"
            self.domain = "AI Governance"
            self.specializations = ["AI Ethics", "Policy Development", "Governance"]
            self.key_responsibilities = ["Develop ethical guidelines", "Review AI systems", "Provide guidance"]
            self.required_skills = ["Ethics", "AI", "Policy", "Communication"]
            self.persona_content = "A" * 600  # Mock content
            self.tasks = [{"name": "Review Ethics", "type": "analysis"}]
            self.templates = [{"name": "Ethics Template"}]
            self.checklists = [{"name": "Ethics Checklist"}]
            self.memory_structure = {
                "knowledge_graph": {},
                "episodic_memory": {},
                "working_memory": {}
            }
    
    validator = AgentValidator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            print("Testing Agent Validator...")
            mock_blueprint = MockBlueprint()
            result = validator.validate_blueprint(mock_blueprint)
            
            print(f"✅ Validation completed")
            print(f"   Valid: {result['is_valid']}")
            print(f"   Quality Score: {result['quality_score']:.3f}")
            print(f"   Errors: {len(result['errors'])}")
            print(f"   Warnings: {len(result['warnings'])}")
            
            if result['errors']:
                print("   Errors:")
                for error in result['errors']:
                    print(f"     - {error}")
        
        else:
            print("Usage: python agent_validator.py [test]")
    else:
        print("Agent Validator initialized successfully")
