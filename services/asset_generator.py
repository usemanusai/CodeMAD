#!/usr/bin/env python3
"""
Asset Generation System for Project Chimera
Generates all required assets for new agents including personas, tasks, templates, and memory structures.
Integrates with Agent Synthesis Engine and existing Cipher Architecture.
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class AssetGenerator:
    """
    Comprehensive asset generation system for new agents.
    Creates all necessary files and structures for agent deployment.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.agents_dir = self.workspace_root / "agents"
        self.memory_dir = self.workspace_root / "memory"
        self.ase_dir = self.workspace_root / "architecture" / "ase"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all required directories exist."""
        directories = [
            self.agents_dir / "classes",
            self.agents_dir / "tasks",
            self.agents_dir / "templates", 
            self.agents_dir / "checklists",
            self.memory_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def generate_agent_assets(self, blueprint: Any) -> Dict[str, Any]:
        """
        Generate all assets for an agent from its blueprint.
        
        Args:
            blueprint: AgentBlueprint object
            
        Returns:
            Dictionary with generated asset paths and status
        """
        self.logger.info(f"Generating assets for agent: {blueprint.agent_id}")
        self._log_audit_event("ASSET_GENERATION_STARTED", f"Generating assets for {blueprint.agent_id}")
        
        generation_result = {
            'success': False,
            'generated_assets': {},
            'errors': [],
            'warnings': []
        }
        
        try:
            # Generate persona file
            persona_result = self._generate_persona_file(blueprint)
            generation_result['generated_assets']['persona'] = persona_result
            
            # Generate task files
            tasks_result = self._generate_task_files(blueprint)
            generation_result['generated_assets']['tasks'] = tasks_result
            
            # Generate template files
            templates_result = self._generate_template_files(blueprint)
            generation_result['generated_assets']['templates'] = templates_result
            
            # Generate checklist files
            checklists_result = self._generate_checklist_files(blueprint)
            generation_result['generated_assets']['checklists'] = checklists_result
            
            # Generate memory structure
            memory_result = self._generate_memory_structure(blueprint)
            generation_result['generated_assets']['memory'] = memory_result
            
            # Generate agent configuration entry
            config_result = self._generate_agent_config_entry(blueprint)
            generation_result['generated_assets']['config'] = config_result
            
            generation_result['success'] = True
            self._log_audit_event("ASSET_GENERATION_COMPLETED", f"Successfully generated assets for {blueprint.agent_id}")
            
        except Exception as e:
            self.logger.error(f"Error generating assets: {e}")
            generation_result['errors'].append(str(e))
            self._log_audit_event("ASSET_GENERATION_ERROR", f"Error generating assets for {blueprint.agent_id}: {str(e)}")
        
        return generation_result
    
    def _generate_persona_file(self, blueprint: Any) -> Dict[str, Any]:
        """Generate persona file for the agent."""
        result = {'success': False, 'path': None, 'error': None}
        
        try:
            # Create persona file path
            persona_file = self.agents_dir / "classes" / f"{blueprint.agent_id}.md"
            
            # Write persona content
            with open(persona_file, 'w', encoding='utf-8') as f:
                f.write(blueprint.persona_content)
            
            result['success'] = True
            result['path'] = str(persona_file)
            self.logger.info(f"Generated persona file: {persona_file}")
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Error generating persona file: {e}")
        
        return result
    
    def _generate_task_files(self, blueprint: Any) -> Dict[str, Any]:
        """Generate task files for the agent."""
        result = {'success': False, 'paths': [], 'errors': []}
        
        try:
            for task in blueprint.tasks:
                task_name = task.get('name', 'Unknown Task')
                task_filename = self._sanitize_filename(task_name)
                task_file = self.agents_dir / "tasks" / f"{task_filename}.md"
                
                # Generate task content
                task_content = self._generate_task_content(task, blueprint)
                
                # Write task file
                with open(task_file, 'w', encoding='utf-8') as f:
                    f.write(task_content)
                
                result['paths'].append(str(task_file))
                self.logger.info(f"Generated task file: {task_file}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(str(e))
            self.logger.error(f"Error generating task files: {e}")
        
        return result
    
    def _generate_template_files(self, blueprint: Any) -> Dict[str, Any]:
        """Generate template files for the agent."""
        result = {'success': False, 'paths': [], 'errors': []}
        
        try:
            for template in blueprint.templates:
                template_name = template.get('name', 'Unknown Template')
                template_filename = self._sanitize_filename(template_name)
                template_file = self.agents_dir / "templates" / f"{template_filename}.md"
                
                # Generate template content
                template_content = self._generate_template_content(template, blueprint)
                
                # Write template file
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                
                result['paths'].append(str(template_file))
                self.logger.info(f"Generated template file: {template_file}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(str(e))
            self.logger.error(f"Error generating template files: {e}")
        
        return result
    
    def _generate_checklist_files(self, blueprint: Any) -> Dict[str, Any]:
        """Generate checklist files for the agent."""
        result = {'success': False, 'paths': [], 'errors': []}
        
        try:
            for checklist in blueprint.checklists:
                checklist_name = checklist.get('name', 'Unknown Checklist')
                checklist_filename = self._sanitize_filename(checklist_name)
                checklist_file = self.agents_dir / "checklists" / f"{checklist_filename}.md"
                
                # Generate checklist content
                checklist_content = self._generate_checklist_content(checklist, blueprint)
                
                # Write checklist file
                with open(checklist_file, 'w', encoding='utf-8') as f:
                    f.write(checklist_content)
                
                result['paths'].append(str(checklist_file))
                self.logger.info(f"Generated checklist file: {checklist_file}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(str(e))
            self.logger.error(f"Error generating checklist files: {e}")
        
        return result
    
    def _generate_memory_structure(self, blueprint: Any) -> Dict[str, Any]:
        """Generate memory structure for the agent."""
        result = {'success': False, 'path': None, 'error': None}
        
        try:
            # Create agent memory directory
            agent_memory_dir = self.memory_dir / blueprint.agent_id
            agent_memory_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate memory files
            memory_files = {
                'knowledge_graph.json': blueprint.memory_structure.get('knowledge_graph', {}),
                'episodic_memory.json': blueprint.memory_structure.get('episodic_memory', {}),
                'working_memory.json': blueprint.memory_structure.get('working_memory', {})
            }
            
            for filename, content in memory_files.items():
                memory_file = agent_memory_dir / filename
                with open(memory_file, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
            
            result['success'] = True
            result['path'] = str(agent_memory_dir)
            self.logger.info(f"Generated memory structure: {agent_memory_dir}")
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Error generating memory structure: {e}")
        
        return result
    
    def _generate_agent_config_entry(self, blueprint: Any) -> Dict[str, Any]:
        """Generate agent configuration entry."""
        result = {'success': False, 'config_entry': None, 'error': None}
        
        try:
            # Generate configuration entry
            config_entry = {
                'title': blueprint.title,
                'name': blueprint.name,
                'description': blueprint.description,
                'persona': f"agents/classes/{blueprint.agent_id}.md",
                'specializations': blueprint.specializations,
                'domain': blueprint.domain,
                'tasks': [task.get('name') for task in blueprint.tasks],
                'templates': [template.get('name') for template in blueprint.templates],
                'checklists': [checklist.get('name') for checklist in blueprint.checklists],
                'created_date': datetime.now().isoformat(),
                'creation_method': 'autonomous_synthesis',
                'quality_score': blueprint.quality_score
            }
            
            result['success'] = True
            result['config_entry'] = config_entry
            self.logger.info(f"Generated config entry for: {blueprint.agent_id}")
            
        except Exception as e:
            result['error'] = str(e)
            self.logger.error(f"Error generating config entry: {e}")
        
        return result
    
    def _generate_task_content(self, task: Dict[str, Any], blueprint: Any) -> str:
        """Generate content for a task file."""
        task_name = task.get('name', 'Unknown Task')
        task_description = task.get('description', 'Task description not provided')
        task_type = task.get('type', 'general')
        complexity = task.get('complexity', 'medium')
        
        content = f"""# Task: {task_name}

## Overview

**Objective:** {task_description}

**Domain:** {blueprint.domain}

**Agent:** {blueprint.title}

**Complexity Level:** {complexity.title()}

**Task Type:** {task_type.title()}

## Task Specification

### Primary Goals
- Apply {blueprint.title.lower()} expertise to accomplish task objectives
- Deliver high-quality results that meet stakeholder requirements
- Ensure compliance with relevant standards and best practices

### Success Criteria
- Task objectives are fully achieved
- Deliverables meet quality standards
- Stakeholder requirements are satisfied
- Timeline and resource constraints are respected

### Key Deliverables
- Comprehensive analysis and recommendations
- Detailed documentation and reports
- Implementation guidance and next steps

## Methodology

### Phase 1: Analysis & Planning
1. **Requirement Analysis**
   - Gather and analyze all relevant requirements
   - Identify key stakeholders and their needs
   - Document constraints and assumptions

2. **Approach Planning**
   - Develop comprehensive approach and methodology
   - Create detailed timeline and milestones
   - Identify required resources and dependencies

### Phase 2: Execution
1. **Core Work**
   - Execute planned approach systematically
   - Apply {blueprint.title.lower()} expertise and best practices
   - Monitor progress and adjust as needed

2. **Quality Assurance**
   - Validate results against requirements
   - Ensure compliance with standards
   - Conduct thorough review and testing

### Phase 3: Delivery
1. **Documentation**
   - Prepare comprehensive documentation
   - Create executive summaries and reports
   - Develop implementation guides

2. **Handover**
   - Present results to stakeholders
   - Provide training and knowledge transfer
   - Establish ongoing support arrangements

## Quality Standards

- Adherence to {blueprint.domain} industry standards
- Compliance with relevant regulations and guidelines
- Integration with existing systems and processes
- Scalability and maintainability considerations

## Required Skills

{chr(10).join([f"- {skill}" for skill in blueprint.required_skills[:5]])}

## Success Metrics

- Quality of deliverables and solutions
- Stakeholder satisfaction and feedback
- Adherence to timelines and budgets
- Innovation and effectiveness of approach
"""
        
        return content
    
    def _generate_template_content(self, template: Dict[str, Any], blueprint: Any) -> str:
        """Generate content for a template file."""
        template_name = template.get('name', 'Unknown Template')
        template_description = template.get('description', 'Template description not provided')
        template_type = template.get('type', 'general')
        
        content = f"""# Template: {template_name}

## Overview

**Purpose:** {template_description}

**Domain:** {blueprint.domain}

**Agent:** {blueprint.title}

**Template Type:** {template_type.title()}

## Template Structure

### Header Section
- **Project/Task Name:** [Enter name]
- **Date:** [Enter date]
- **Prepared By:** {blueprint.title}
- **Version:** [Enter version]

### Executive Summary
[Provide high-level overview and key findings]

### Detailed Analysis
[Provide comprehensive analysis and findings]

### Recommendations
[List specific, actionable recommendations]

### Implementation Plan
[Outline steps for implementation]

### Appendices
[Include supporting documentation and references]

## Usage Guidelines

1. **Customization:** Adapt sections based on specific requirements
2. **Quality Review:** Ensure all sections are complete and accurate
3. **Stakeholder Review:** Obtain feedback from relevant stakeholders
4. **Version Control:** Maintain proper version control and documentation

## Quality Checklist

- [ ] All required sections completed
- [ ] Content is accurate and up-to-date
- [ ] Recommendations are specific and actionable
- [ ] Documentation follows {blueprint.domain} standards
- [ ] Stakeholder requirements are addressed
- [ ] Quality review completed
"""
        
        return content
    
    def _generate_checklist_content(self, checklist: Dict[str, Any], blueprint: Any) -> str:
        """Generate content for a checklist file."""
        checklist_name = checklist.get('name', 'Unknown Checklist')
        checklist_description = checklist.get('description', 'Checklist description not provided')
        checklist_type = checklist.get('type', 'general')
        
        content = f"""# Checklist: {checklist_name}

## Overview

**Purpose:** {checklist_description}

**Domain:** {blueprint.domain}

**Agent:** {blueprint.title}

**Checklist Type:** {checklist_type.title()}

## Pre-Work Checklist

- [ ] Requirements clearly defined and documented
- [ ] Stakeholders identified and engaged
- [ ] Resources and timeline confirmed
- [ ] Approach and methodology planned
- [ ] Quality standards established

## Execution Checklist

- [ ] Work executed according to plan
- [ ] {blueprint.title.lower()} best practices applied
- [ ] Progress monitored and documented
- [ ] Issues identified and addressed
- [ ] Quality checkpoints completed

## Quality Assurance Checklist

- [ ] Deliverables meet requirements
- [ ] {blueprint.domain} standards followed
- [ ] Compliance requirements satisfied
- [ ] Stakeholder feedback incorporated
- [ ] Documentation complete and accurate

## Completion Checklist

- [ ] All objectives achieved
- [ ] Final quality review completed
- [ ] Stakeholder approval obtained
- [ ] Documentation finalized
- [ ] Knowledge transfer completed
- [ ] Lessons learned documented

## Domain-Specific Checks

{chr(10).join([f"- [ ] {spec} considerations addressed" for spec in blueprint.specializations[:5]])}

## Final Validation

- [ ] All checklist items completed
- [ ] Quality standards met
- [ ] Stakeholder satisfaction confirmed
- [ ] Project officially closed
"""
        
        return content
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize name for use as filename."""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9\s]', '', name)
        sanitized = re.sub(r'\s+', '_', sanitized.strip())
        return sanitized.lower()
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} ASSET_GENERATOR {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing
if __name__ == "__main__":
    import sys
    import re
    
    # Mock blueprint for testing
    class MockBlueprint:
        def __init__(self):
            self.agent_id = "test_agent"
            self.title = "Test Specialist"
            self.name = "Test Agent"
            self.description = "Test agent for validation"
            self.domain = "Testing"
            self.specializations = ["Testing", "Validation", "Quality Assurance"]
            self.key_responsibilities = ["Test systems", "Validate results", "Ensure quality"]
            self.required_skills = ["Testing", "Analysis", "Communication"]
            self.persona_content = "# Test Agent Persona\n\nThis is a test agent."
            self.tasks = [{"name": "Run Tests", "description": "Execute test procedures", "type": "testing", "complexity": "medium"}]
            self.templates = [{"name": "Test Report Template", "description": "Template for test reports", "type": "report"}]
            self.checklists = [{"name": "Test Quality Checklist", "description": "Quality checklist for testing", "type": "quality"}]
            self.memory_structure = {
                "knowledge_graph": {"domain": "Testing"},
                "episodic_memory": {"creation": "test"},
                "working_memory": {}
            }
            self.quality_score = 0.85
    
    generator = AssetGenerator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            print("Testing Asset Generator...")
            mock_blueprint = MockBlueprint()
            result = generator.generate_agent_assets(mock_blueprint)
            
            print(f"✅ Asset generation completed")
            print(f"   Success: {result['success']}")
            print(f"   Generated assets: {len(result['generated_assets'])}")
            
            for asset_type, asset_result in result['generated_assets'].items():
                if isinstance(asset_result, dict) and asset_result.get('success'):
                    print(f"   ✅ {asset_type}: Generated successfully")
                else:
                    print(f"   ❌ {asset_type}: Generation failed")
        
        else:
            print("Usage: python asset_generator.py [test]")
    else:
        print("Asset Generator initialized successfully")
