#!/usr/bin/env python3
"""
Agent Synthesis Engine (ASE) for Project Chimera
Autonomous system for creating new specialist agents based on identified gaps.
Integrates with existing Cipher Architecture and constitutional governance.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass
import hashlib
import re

@dataclass
class AgentBlueprint:
    """Data structure for agent creation blueprint."""
    agent_id: str
    title: str
    name: str
    description: str
    domain: str
    specializations: List[str]
    key_responsibilities: List[str]
    required_skills: List[str]
    persona_content: str
    tasks: List[Dict[str, Any]]
    templates: List[Dict[str, Any]]
    checklists: List[Dict[str, Any]]
    memory_structure: Dict[str, Any]
    quality_score: float
    creation_rationale: str

class AgentSynthesisEngine:
    """
    Core Agent Synthesis Engine for autonomous agent creation.
    Transforms gap analysis results into fully functional agent specifications.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.config_file = self.workspace_root / "services" / "config" / "expansion_config.json"
        self.ase_dir = self.workspace_root / "architecture" / "ase"
        self.agents_dir = self.workspace_root / "agents"
        self.memory_dir = self.workspace_root / "memory"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize template system
        self.templates = self._load_templates()
        
        # Initialize validators
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'validators'))
        from agent_validator import AgentValidator
        self.validator = AgentValidator(workspace_root)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load expansion configuration."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def _load_templates(self) -> Dict[str, str]:
        """Load agent creation templates."""
        templates = {}
        templates_dir = self.ase_dir / "templates"
        
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.md"):
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        templates[template_file.stem] = f.read()
                except Exception as e:
                    self.logger.warning(f"Error loading template {template_file}: {e}")
        
        return templates
    
    def synthesize_agent(self, gap_data: Any) -> Optional[AgentBlueprint]:
        """
        Synthesize a new agent from gap analysis data.
        
        Args:
            gap_data: AgentGap object from gap analysis
            
        Returns:
            AgentBlueprint for the new agent or None if synthesis fails
        """
        self.logger.info(f"Starting agent synthesis for: {gap_data.occupation_title}")
        self._log_audit_event("AGENT_SYNTHESIS_STARTED", f"Synthesizing agent: {gap_data.occupation_title}")
        
        try:
            # Phase 1: Generate agent blueprint
            blueprint = self._generate_agent_blueprint(gap_data)
            
            # Phase 2: Create persona content
            blueprint.persona_content = self._generate_persona_content(blueprint)
            
            # Phase 3: Generate tasks and capabilities
            blueprint.tasks = self._generate_agent_tasks(blueprint)
            blueprint.templates = self._generate_agent_templates(blueprint)
            blueprint.checklists = self._generate_agent_checklists(blueprint)
            
            # Phase 4: Create memory structure
            blueprint.memory_structure = self._generate_memory_structure(blueprint)
            
            # Phase 5: Validate blueprint
            validation_result = self.validator.validate_blueprint(blueprint)
            blueprint.quality_score = validation_result['quality_score']
            
            if validation_result['is_valid']:
                self._log_audit_event("AGENT_SYNTHESIS_COMPLETED", f"Successfully synthesized: {blueprint.agent_id}")
                self.logger.info(f"Agent synthesis completed successfully: {blueprint.agent_id}")
                return blueprint
            else:
                self._log_audit_event("AGENT_SYNTHESIS_FAILED", f"Validation failed for: {blueprint.agent_id}")
                self.logger.warning(f"Agent synthesis validation failed: {validation_result['errors']}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in agent synthesis: {e}")
            self._log_audit_event("AGENT_SYNTHESIS_ERROR", f"Error synthesizing {gap_data.occupation_title}: {str(e)}")
            return None
    
    def _generate_agent_blueprint(self, gap_data: Any) -> AgentBlueprint:
        """Generate basic agent blueprint from gap data."""
        
        # Generate unique agent ID
        agent_id = self._generate_agent_id(gap_data.occupation_title, gap_data.domain)
        
        # Generate agent name
        agent_name = self._generate_agent_name(gap_data.occupation_title)
        
        # Generate description
        description = self._generate_agent_description(gap_data)
        
        # Extract specializations
        specializations = self._extract_specializations(gap_data)
        
        # Generate responsibilities
        responsibilities = self._generate_responsibilities(gap_data)
        
        # Extract skills
        skills = self._extract_skills(gap_data)
        
        return AgentBlueprint(
            agent_id=agent_id,
            title=gap_data.occupation_title,
            name=agent_name,
            description=description,
            domain=gap_data.domain,
            specializations=specializations,
            key_responsibilities=responsibilities,
            required_skills=skills,
            persona_content="",  # Will be generated later
            tasks=[],  # Will be generated later
            templates=[],  # Will be generated later
            checklists=[],  # Will be generated later
            memory_structure={},  # Will be generated later
            quality_score=0.0,  # Will be calculated later
            creation_rationale=gap_data.gap_rationale
        )
    
    def _generate_agent_id(self, occupation_title: str, domain: str) -> str:
        """Generate unique agent ID."""
        # Clean and format title
        clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', occupation_title)
        words = clean_title.lower().split()
        
        # Take first 3 words or all if less
        id_words = words[:3]
        agent_id = '_'.join(id_words)
        
        # Add domain suffix if needed for uniqueness
        if len(agent_id) < 5:
            domain_suffix = re.sub(r'[^a-zA-Z0-9]', '', domain.lower())[:3]
            agent_id = f"{agent_id}_{domain_suffix}"
        
        return agent_id
    
    def _generate_agent_name(self, occupation_title: str) -> str:
        """Generate agent name from occupation title."""
        # Use title as base, clean it up
        name = occupation_title.replace('Specialist', '').replace('Engineer', '').strip()
        
        # If too long, use initials + last word
        if len(name) > 20:
            words = name.split()
            if len(words) > 1:
                initials = ''.join([w[0].upper() for w in words[:-1]])
                name = f"{initials}. {words[-1]}"
        
        return name
    
    def _generate_agent_description(self, gap_data: Any) -> str:
        """Generate agent description."""
        return f"Specialist in {gap_data.occupation_title.lower()} within the {gap_data.domain} sector. {gap_data.gap_rationale}"
    
    def _extract_specializations(self, gap_data: Any) -> List[str]:
        """Extract specializations from gap data."""
        specializations = []
        
        # Use required capabilities as base
        if hasattr(gap_data, 'required_capabilities'):
            specializations.extend(gap_data.required_capabilities[:5])
        
        # Add domain-specific specializations
        domain_lower = gap_data.domain.lower()
        if 'ai' in domain_lower or 'artificial intelligence' in domain_lower:
            specializations.extend(['Machine Learning', 'AI Ethics', 'Data Analysis'])
        elif 'healthcare' in domain_lower:
            specializations.extend(['Medical Knowledge', 'Patient Care', 'Healthcare Technology'])
        elif 'renewable' in domain_lower or 'energy' in domain_lower:
            specializations.extend(['Sustainability', 'Energy Systems', 'Environmental Impact'])
        elif 'cybersecurity' in domain_lower:
            specializations.extend(['Security Analysis', 'Risk Assessment', 'Threat Detection'])
        
        # Add occupation-specific specializations
        title_lower = gap_data.occupation_title.lower()
        if 'engineer' in title_lower:
            specializations.extend(['System Design', 'Technical Implementation'])
        elif 'analyst' in title_lower:
            specializations.extend(['Data Analysis', 'Research Methodology'])
        elif 'manager' in title_lower:
            specializations.extend(['Project Management', 'Team Leadership'])
        
        return list(set(specializations))[:8]  # Limit and deduplicate
    
    def _generate_responsibilities(self, gap_data: Any) -> List[str]:
        """Generate key responsibilities."""
        responsibilities = [
            f"Apply {gap_data.occupation_title.lower()} expertise to solve complex challenges",
            f"Stay current with {gap_data.domain.lower()} industry trends and best practices",
            "Collaborate with cross-functional teams and stakeholders",
            "Contribute to strategic planning and decision-making processes"
        ]
        
        # Add occupation-specific responsibilities
        title_lower = gap_data.occupation_title.lower()
        if 'engineer' in title_lower:
            responsibilities.extend([
                "Design and implement technical solutions",
                "Conduct system analysis and optimization",
                "Ensure compliance with technical standards"
            ])
        elif 'analyst' in title_lower:
            responsibilities.extend([
                "Analyze data and generate actionable insights",
                "Prepare comprehensive reports and recommendations",
                "Monitor key performance indicators and metrics"
            ])
        elif 'manager' in title_lower:
            responsibilities.extend([
                "Lead and manage team members effectively",
                "Oversee project execution and delivery",
                "Develop and implement strategic initiatives"
            ])
        elif 'specialist' in title_lower:
            responsibilities.extend([
                "Provide expert consultation and guidance",
                "Develop specialized methodologies and frameworks",
                "Train and mentor team members"
            ])
        
        return responsibilities[:6]  # Limit to 6 responsibilities
    
    def _extract_skills(self, gap_data: Any) -> List[str]:
        """Extract required skills."""
        skills = ['Problem-solving', 'Communication', 'Critical thinking']
        
        # Add capabilities as skills
        if hasattr(gap_data, 'required_capabilities'):
            skills.extend(gap_data.required_capabilities)
        
        # Add domain-specific skills
        domain_lower = gap_data.domain.lower()
        if 'technology' in domain_lower or 'ai' in domain_lower:
            skills.extend(['Technical expertise', 'Innovation', 'Digital literacy'])
        elif 'healthcare' in domain_lower:
            skills.extend(['Medical knowledge', 'Patient care', 'Regulatory compliance'])
        elif 'finance' in domain_lower:
            skills.extend(['Financial analysis', 'Risk management', 'Regulatory knowledge'])
        
        return list(set(skills))[:10]  # Limit and deduplicate
    
    def _generate_persona_content(self, blueprint: AgentBlueprint) -> str:
        """Generate persona content for the agent."""
        template = self.templates.get('agent_persona_template', self._get_default_persona_template())
        
        # Replace template variables
        persona_content = template.format(
            title=blueprint.title,
            name=blueprint.name,
            description=blueprint.description,
            domain=blueprint.domain,
            specializations=', '.join(blueprint.specializations[:5]),
            responsibilities='\n'.join([f"- {resp}" for resp in blueprint.key_responsibilities]),
            skills=', '.join(blueprint.required_skills[:8])
        )
        
        return persona_content
    
    def _get_default_persona_template(self) -> str:
        """Get default persona template if none loaded."""
        return """# Role: {title}

## Persona

- **Role:** {title} & {domain} Expert
- **Style:** Professional, knowledgeable, analytical, and results-oriented. Focuses on applying specialized expertise to solve complex challenges in the {domain} sector.
- **Core Strength:** Deep understanding of {title} principles, methodologies, and best practices. Excels at {specializations} and delivering high-quality solutions.

## Domain Expertise

### Core Specializations
{specializations}

### Key Responsibilities
{responsibilities}

### Required Skills
{skills}

## Operational Guidelines

### Communication Style
- Clear, professional, and technically accurate
- Adapts communication to audience expertise level
- Provides actionable recommendations and insights
- Maintains focus on practical solutions

### Quality Standards
- Ensures all deliverables meet industry standards
- Validates solutions against best practices
- Considers regulatory and compliance requirements
- Prioritizes safety and ethical considerations

### Collaboration Approach
- Works effectively with cross-functional teams
- Shares knowledge and mentors team members
- Seeks input from relevant stakeholders
- Maintains professional relationships
"""
    
    def _generate_agent_tasks(self, blueprint: AgentBlueprint) -> List[Dict[str, Any]]:
        """Generate tasks for the agent."""
        tasks = []
        
        # Core analysis task
        tasks.append({
            'name': f'Analyze {blueprint.domain} Requirements',
            'description': f'Analyze and assess requirements in the {blueprint.domain} domain',
            'type': 'analysis',
            'complexity': 'medium'
        })
        
        # Domain-specific tasks based on occupation type
        title_lower = blueprint.title.lower()
        if 'engineer' in title_lower:
            tasks.extend([
                {
                    'name': 'Design Technical Solution',
                    'description': 'Design comprehensive technical solutions for complex challenges',
                    'type': 'design',
                    'complexity': 'high'
                },
                {
                    'name': 'Conduct System Analysis',
                    'description': 'Perform detailed system analysis and optimization',
                    'type': 'analysis',
                    'complexity': 'medium'
                }
            ])
        elif 'analyst' in title_lower:
            tasks.extend([
                {
                    'name': 'Generate Insights Report',
                    'description': 'Analyze data and generate actionable insights',
                    'type': 'reporting',
                    'complexity': 'medium'
                },
                {
                    'name': 'Conduct Research Analysis',
                    'description': 'Perform comprehensive research and analysis',
                    'type': 'research',
                    'complexity': 'medium'
                }
            ])
        elif 'manager' in title_lower:
            tasks.extend([
                {
                    'name': 'Develop Strategic Plan',
                    'description': 'Create comprehensive strategic plans and roadmaps',
                    'type': 'planning',
                    'complexity': 'high'
                },
                {
                    'name': 'Coordinate Team Activities',
                    'description': 'Coordinate and manage team activities and deliverables',
                    'type': 'management',
                    'complexity': 'medium'
                }
            ])
        
        # Add consultation task for all agents
        tasks.append({
            'name': 'Provide Expert Consultation',
            'description': f'Provide expert consultation on {blueprint.domain} matters',
            'type': 'consultation',
            'complexity': 'medium'
        })
        
        return tasks[:4]  # Limit to 4 tasks
    
    def _generate_agent_templates(self, blueprint: AgentBlueprint) -> List[Dict[str, Any]]:
        """Generate templates for the agent."""
        templates = []
        
        # Analysis template
        templates.append({
            'name': f'{blueprint.domain} Analysis Template',
            'description': f'Template for analyzing {blueprint.domain} requirements and challenges',
            'type': 'analysis'
        })
        
        # Report template
        templates.append({
            'name': f'{blueprint.title} Report Template',
            'description': f'Template for {blueprint.title} reports and recommendations',
            'type': 'report'
        })
        
        return templates
    
    def _generate_agent_checklists(self, blueprint: AgentBlueprint) -> List[Dict[str, Any]]:
        """Generate checklists for the agent."""
        checklists = []
        
        # Quality checklist
        checklists.append({
            'name': f'{blueprint.title} Quality Checklist',
            'description': f'Quality assurance checklist for {blueprint.title} deliverables',
            'type': 'quality'
        })
        
        # Compliance checklist if applicable
        if any(term in blueprint.domain.lower() for term in ['healthcare', 'finance', 'legal']):
            checklists.append({
                'name': f'{blueprint.domain} Compliance Checklist',
                'description': f'Compliance checklist for {blueprint.domain} requirements',
                'type': 'compliance'
            })
        
        return checklists
    
    def _generate_memory_structure(self, blueprint: AgentBlueprint) -> Dict[str, Any]:
        """Generate memory structure for the agent."""
        return {
            'knowledge_graph': {
                'domain_knowledge': blueprint.domain,
                'specializations': blueprint.specializations,
                'skills': blueprint.required_skills
            },
            'episodic_memory': {
                'creation_context': {
                    'created_from_gap': True,
                    'gap_rationale': blueprint.creation_rationale,
                    'creation_date': datetime.now().isoformat()
                }
            },
            'working_memory': {
                'active_tasks': [],
                'current_context': {}
            }
        }
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} AGENT_SYNTHESIS_ENGINE {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    # Mock gap data for testing
    class MockGap:
        def __init__(self):
            self.occupation_title = "AI Ethics Specialist"
            self.domain = "AI Governance"
            self.gap_rationale = "No existing agent covers AI ethics and governance"
            self.required_capabilities = ["Ethics", "AI", "Policy", "Governance"]
    
    engine = AgentSynthesisEngine()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            print("Testing Agent Synthesis Engine...")
            mock_gap = MockGap()
            blueprint = engine.synthesize_agent(mock_gap)
            
            if blueprint:
                print(f"✅ Successfully synthesized agent: {blueprint.agent_id}")
                print(f"   Title: {blueprint.title}")
                print(f"   Name: {blueprint.name}")
                print(f"   Quality Score: {blueprint.quality_score}")
                print(f"   Specializations: {', '.join(blueprint.specializations[:3])}")
            else:
                print("❌ Agent synthesis failed")
        
        else:
            print("Usage: python agent_synthesis_engine.py [test]")
    else:
        print("Agent Synthesis Engine initialized successfully")
