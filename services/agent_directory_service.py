#!/usr/bin/env python3
"""
Agent Directory Service for Project Chimera
Provides centralized registry and query capabilities for all agents in the ecosystem.
Integrates with existing Cipher Architecture and constitutional governance.
"""

import json
import os
import re
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from pathlib import Path

class AgentDirectoryService:
    """
    Centralized service for managing and querying the agent ecosystem.
    Maintains real-time registry of all agents with metadata and capabilities.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.data_dir = self.workspace_root / "services" / "data"
        self.agent_directory_file = self.data_dir / "agent_directory.json"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Agent registry
        self.agents = {}
        self.load_agent_directory()
    
    def load_agent_directory(self):
        """Load existing agent directory or create new one."""
        try:
            if self.agent_directory_file.exists():
                with open(self.agent_directory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.agents = data.get('agents', {})
                    self.logger.info(f"Loaded {len(self.agents)} agents from directory")
            else:
                self.logger.info("No existing agent directory found, creating new one")
                self.agents = {}
                self._initialize_from_existing_agents()
        except Exception as e:
            self.logger.error(f"Error loading agent directory: {e}")
            self.agents = {}
    
    def _initialize_from_existing_agents(self):
        """Initialize directory by scanning existing agent configurations."""
        self.logger.info("Scanning existing agent configurations...")
        
        # Scan comprehensive agent config
        self._scan_comprehensive_config()
        
        # Scan agent classes
        self._scan_agent_classes()
        
        # Scan agent instances
        self._scan_agent_instances()
        
        # Save initial directory
        self.save_agent_directory()
        self._log_audit_event("AGENT_DIRECTORY_INITIALIZED", f"Indexed {len(self.agents)} existing agents")
    
    def _scan_comprehensive_config(self):
        """Scan the comprehensive agent configuration file."""
        config_file = self.workspace_root / "architecture" / "comprehensive-agent-config.md"
        if not config_file.exists():
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse agent definitions using regex
            agent_pattern = r'### Title: (.+?)\n\n- Name: (.+?)\n.*?- Description: "(.+?)".*?- Persona: "(.+?)"'
            matches = re.findall(agent_pattern, content, re.DOTALL)
            
            for match in matches:
                title, name, description, persona = match
                agent_id = self._generate_agent_id(title, name)
                
                # Extract specializations if present
                specializations = self._extract_specializations(content, title)
                
                self.agents[agent_id] = {
                    "id": agent_id,
                    "title": title.strip(),
                    "name": name.strip(),
                    "description": description.strip(),
                    "persona": persona.strip(),
                    "specializations": specializations,
                    "source": "comprehensive-config",
                    "status": "active",
                    "created_date": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Error scanning comprehensive config: {e}")
    
    def _scan_agent_classes(self):
        """Scan agent class definitions."""
        classes_dir = self.workspace_root / "agents" / "classes"
        if not classes_dir.exists():
            return
        
        for class_file in classes_dir.glob("*.md"):
            try:
                with open(class_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract role and persona information
                role_match = re.search(r'- \*\*Role:\*\* (.+)', content)
                style_match = re.search(r'- \*\*Style:\*\* (.+)', content)
                
                if role_match:
                    role = role_match.group(1).strip()
                    agent_id = class_file.stem
                    
                    # Only add if not already exists from comprehensive config
                    if agent_id not in self.agents:
                        self.agents[agent_id] = {
                            "id": agent_id,
                            "title": role,
                            "name": agent_id.replace('-', ' ').title(),
                            "description": style_match.group(1).strip() if style_match else role,
                            "persona": f"agents/classes/{class_file.name}",
                            "specializations": [],
                            "source": "agent-classes",
                            "status": "active",
                            "created_date": datetime.now().isoformat(),
                            "last_updated": datetime.now().isoformat()
                        }
                        
            except Exception as e:
                self.logger.error(f"Error scanning agent class {class_file}: {e}")
    
    def _scan_agent_instances(self):
        """Scan agent instance configurations."""
        instances_dir = self.workspace_root / "agents" / "instances"
        if not instances_dir.exists():
            return
        
        for instance_dir in instances_dir.iterdir():
            if instance_dir.is_dir():
                config_file = instance_dir / "agent-config.txt"
                if config_file.exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Parse instance configurations
                        self._parse_instance_config(content, instance_dir.name)
                        
                    except Exception as e:
                        self.logger.error(f"Error scanning instance {instance_dir}: {e}")
    
    def _parse_instance_config(self, content: str, instance_name: str):
        """Parse agent configuration from instance files."""
        # Extract agent definitions
        agent_pattern = r'## Title: (.+?)\n\n- Name: (.+?)\n.*?- Description: "(.+?)".*?- Persona: "(.+?)"'
        matches = re.findall(agent_pattern, content, re.DOTALL)
        
        for match in matches:
            title, name, description, persona = match
            agent_id = f"{instance_name}_{self._generate_agent_id(title, name)}"
            
            if agent_id not in self.agents:
                self.agents[agent_id] = {
                    "id": agent_id,
                    "title": title.strip(),
                    "name": name.strip(),
                    "description": description.strip(),
                    "persona": persona.strip(),
                    "specializations": [],
                    "source": f"instance-{instance_name}",
                    "status": "active",
                    "created_date": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat()
                }
    
    def _extract_specializations(self, content: str, title: str) -> List[str]:
        """Extract specializations for an agent from content."""
        # Look for specializations array after the title
        pattern = rf'### Title: {re.escape(title)}.*?- Specializations: \[(.*?)\]'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            specs_str = match.group(1)
            # Parse the array format
            specs = re.findall(r'"([^"]+)"', specs_str)
            return specs
        
        return []
    
    def _generate_agent_id(self, title: str, name: str) -> str:
        """Generate unique agent ID from title and name."""
        # Create ID from title, fallback to name
        base = title.lower().replace(' ', '_').replace('-', '_')
        base = re.sub(r'[^a-z0-9_]', '', base)
        return base
    
    def save_agent_directory(self):
        """Save agent directory to file."""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            
            directory_data = {
                "metadata": {
                    "version": "1.0.0",
                    "last_updated": datetime.now().isoformat(),
                    "total_agents": len(self.agents),
                    "source": "Agent Directory Service"
                },
                "agents": self.agents
            }
            
            with open(self.agent_directory_file, 'w', encoding='utf-8') as f:
                json.dump(directory_data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved agent directory with {len(self.agents)} agents")
            
        except Exception as e:
            self.logger.error(f"Error saving agent directory: {e}")
    
    def query_agents(self, 
                    domain: Optional[str] = None,
                    specialization: Optional[str] = None,
                    keywords: Optional[List[str]] = None,
                    status: str = "active") -> List[Dict[str, Any]]:
        """
        Query agents based on various criteria.
        
        Args:
            domain: Domain/category to filter by
            specialization: Specific specialization to match
            keywords: Keywords to search in title/description
            status: Agent status filter
            
        Returns:
            List of matching agent records
        """
        results = []
        
        for agent_id, agent in self.agents.items():
            if agent.get('status') != status:
                continue
            
            # Domain filtering (fuzzy match on title/description)
            if domain and not self._matches_domain(agent, domain):
                continue
            
            # Specialization filtering
            if specialization and not self._matches_specialization(agent, specialization):
                continue
            
            # Keywords filtering
            if keywords and not self._matches_keywords(agent, keywords):
                continue
            
            results.append(agent)
        
        return results
    
    def _matches_domain(self, agent: Dict[str, Any], domain: str) -> bool:
        """Check if agent matches domain criteria."""
        domain_lower = domain.lower()
        title_lower = agent.get('title', '').lower()
        desc_lower = agent.get('description', '').lower()
        
        return domain_lower in title_lower or domain_lower in desc_lower
    
    def _matches_specialization(self, agent: Dict[str, Any], specialization: str) -> bool:
        """Check if agent matches specialization criteria."""
        spec_lower = specialization.lower()
        agent_specs = [s.lower() for s in agent.get('specializations', [])]
        
        return any(spec_lower in spec for spec in agent_specs)
    
    def _matches_keywords(self, agent: Dict[str, Any], keywords: List[str]) -> bool:
        """Check if agent matches keyword criteria."""
        text = f"{agent.get('title', '')} {agent.get('description', '')} {' '.join(agent.get('specializations', []))}".lower()
        
        return any(keyword.lower() in text for keyword in keywords)
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent by ID."""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> Dict[str, Any]:
        """Get all agents."""
        return self.agents.copy()
    
    def get_agent_count(self) -> int:
        """Get total number of agents."""
        return len(self.agents)
    
    def get_domains(self) -> Set[str]:
        """Get all unique domains/categories."""
        domains = set()
        for agent in self.agents.values():
            # Extract domain from title/description
            title_words = agent.get('title', '').split()
            if title_words:
                domains.add(title_words[-1])  # Often the domain is the last word
        
        return domains
    
    def register_new_agent(self, agent_data: Dict[str, Any]) -> str:
        """
        Register a new agent in the directory.
        
        Args:
            agent_data: Agent information dictionary
            
        Returns:
            Generated agent ID
        """
        agent_id = self._generate_agent_id(
            agent_data.get('title', ''),
            agent_data.get('name', '')
        )
        
        # Ensure unique ID
        counter = 1
        original_id = agent_id
        while agent_id in self.agents:
            agent_id = f"{original_id}_{counter}"
            counter += 1
        
        # Add metadata
        agent_data.update({
            "id": agent_id,
            "status": "active",
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "source": "autonomous_creation"
        })
        
        self.agents[agent_id] = agent_data
        self.save_agent_directory()
        
        # Log to audit
        self._log_audit_event("AGENT_REGISTERED", f"New agent registered: {agent_id}")
        
        return agent_id
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} AGENT_DIRECTORY_SERVICE {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    service = AgentDirectoryService()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "count":
            print(f"Total agents: {service.get_agent_count()}")
        
        elif command == "domains":
            domains = service.get_domains()
            print(f"Domains: {', '.join(sorted(domains))}")
        
        elif command == "query" and len(sys.argv) > 2:
            domain = sys.argv[2]
            results = service.query_agents(domain=domain)
            print(f"Found {len(results)} agents in domain '{domain}':")
            for agent in results[:5]:  # Show first 5
                print(f"  - {agent['title']} ({agent['name']})")
        
        else:
            print("Usage: python agent_directory_service.py [count|domains|query <domain>]")
    else:
        print(f"Agent Directory Service initialized with {service.get_agent_count()} agents")
