#!/usr/bin/env python3
"""
Gap Analysis System for Project Chimera
Intelligent system for identifying missing agent specializations and prioritizing creation opportunities.
Integrates with Agent Directory Service and Domain Research Engine.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass
import re
from difflib import SequenceMatcher

@dataclass
class AgentGap:
    """Data structure for identified agent gaps."""
    occupation_title: str
    domain: str
    priority_score: float
    market_demand_score: float
    strategic_value_score: float
    similarity_to_existing: float
    gap_rationale: str
    required_capabilities: List[str]
    estimated_effort: str
    business_impact: str
    sources: List[str]
    related_existing_agents: List[str]

class GapAnalyzer:
    """
    Intelligent gap analysis system for identifying missing agent specializations.
    Cross-references discovered occupations with existing agent directory.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.config_file = self.workspace_root / "services" / "config" / "expansion_config.json"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize Agent Directory Service
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
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
    
    def analyze_gaps(self, domain: str, discovered_occupations: List[Any]) -> List[AgentGap]:
        """
        Analyze gaps between discovered occupations and existing agents.
        
        Args:
            domain: The domain being analyzed
            discovered_occupations: List of occupation profiles from domain research
            
        Returns:
            List of prioritized agent gaps
        """
        self.logger.info(f"Starting gap analysis for domain: {domain}")
        self._log_audit_event("GAP_ANALYSIS_STARTED", f"Analyzing gaps in domain: {domain}")
        
        try:
            # Phase 1: Get existing agents in domain
            existing_agents = self._get_existing_agents_in_domain(domain)
            
            # Phase 2: Identify gaps
            gaps = self._identify_gaps(domain, discovered_occupations, existing_agents)
            
            # Phase 3: Score and prioritize gaps
            scored_gaps = self._score_and_prioritize_gaps(gaps, domain)
            
            # Phase 4: Filter by quality thresholds
            filtered_gaps = self._filter_gaps_by_quality(scored_gaps)
            
            self._log_audit_event("GAP_ANALYSIS_COMPLETED", f"Found {len(filtered_gaps)} priority gaps in {domain}")
            self.logger.info(f"Gap analysis completed. Found {len(filtered_gaps)} priority gaps.")
            
            return filtered_gaps
            
        except Exception as e:
            self.logger.error(f"Error in gap analysis: {e}")
            self._log_audit_event("GAP_ANALYSIS_ERROR", f"Error analyzing gaps in {domain}: {str(e)}")
            return []
    
    def _get_existing_agents_in_domain(self, domain: str) -> List[Dict[str, Any]]:
        """Get existing agents that might overlap with the domain."""
        self.logger.info(f"Retrieving existing agents for domain: {domain}")
        
        # Query agents by domain keywords
        domain_keywords = self._extract_domain_keywords(domain)
        existing_agents = []
        
        for keyword in domain_keywords:
            agents = self.agent_directory.query_agents(domain=keyword)
            existing_agents.extend(agents)
        
        # Also get agents by specialization
        for keyword in domain_keywords:
            agents = self.agent_directory.query_agents(specialization=keyword)
            existing_agents.extend(agents)
        
        # Deduplicate agents
        unique_agents = {}
        for agent in existing_agents:
            agent_id = agent.get('id')
            if agent_id and agent_id not in unique_agents:
                unique_agents[agent_id] = agent
        
        self.logger.info(f"Found {len(unique_agents)} existing agents related to {domain}")
        return list(unique_agents.values())
    
    def _extract_domain_keywords(self, domain: str) -> List[str]:
        """Extract keywords from domain for searching."""
        # Split domain into words and clean
        words = re.findall(r'\b\w+\b', domain.lower())
        
        # Filter out common words
        stop_words = {'and', 'or', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def _identify_gaps(self, domain: str, discovered_occupations: List[Any], existing_agents: List[Dict]) -> List[AgentGap]:
        """Identify gaps between discovered occupations and existing agents."""
        self.logger.info(f"Identifying gaps between {len(discovered_occupations)} occupations and {len(existing_agents)} existing agents")
        
        gaps = []
        
        for occupation in discovered_occupations:
            # Get occupation details
            if hasattr(occupation, 'title'):
                occupation_title = occupation.title
                occupation_desc = getattr(occupation, 'description', '')
                occupation_skills = getattr(occupation, 'required_skills', [])
            else:
                # Handle string occupations
                occupation_title = str(occupation)
                occupation_desc = ''
                occupation_skills = []
            
            # Check similarity to existing agents
            similarity_results = self._calculate_similarity_to_existing(
                occupation_title, occupation_desc, occupation_skills, existing_agents
            )
            
            max_similarity = similarity_results['max_similarity']
            similar_agents = similarity_results['similar_agents']
            
            # Determine if this is a gap
            similarity_threshold = self.config.get('quality_thresholds', {}).get('gap_analysis', {}).get('duplicate_similarity_threshold', 0.8)
            
            if max_similarity < similarity_threshold:
                # This is a gap - create gap record
                gap = self._create_gap_record(
                    occupation_title, domain, occupation, 
                    max_similarity, similar_agents
                )
                gaps.append(gap)
            else:
                self.logger.debug(f"Skipping {occupation_title} - too similar to existing agents (similarity: {max_similarity:.3f})")
        
        self.logger.info(f"Identified {len(gaps)} potential gaps")
        return gaps
    
    def _calculate_similarity_to_existing(self, occupation_title: str, occupation_desc: str, 
                                        occupation_skills: List[str], existing_agents: List[Dict]) -> Dict[str, Any]:
        """Calculate similarity between occupation and existing agents."""
        max_similarity = 0.0
        similar_agents = []
        
        for agent in existing_agents:
            similarity = self._calculate_occupation_agent_similarity(
                occupation_title, occupation_desc, occupation_skills, agent
            )
            
            if similarity > max_similarity:
                max_similarity = similarity
            
            if similarity > 0.5:  # Threshold for considering "similar"
                similar_agents.append({
                    'agent_id': agent.get('id'),
                    'agent_title': agent.get('title'),
                    'similarity': similarity
                })
        
        # Sort similar agents by similarity
        similar_agents.sort(key=lambda x: x['similarity'], reverse=True)
        
        return {
            'max_similarity': max_similarity,
            'similar_agents': similar_agents[:5]  # Top 5 similar agents
        }
    
    def _calculate_occupation_agent_similarity(self, occupation_title: str, occupation_desc: str,
                                             occupation_skills: List[str], agent: Dict[str, Any]) -> float:
        """Calculate similarity between an occupation and an existing agent."""
        
        # Get agent details
        agent_title = agent.get('title', '')
        agent_desc = agent.get('description', '')
        agent_specializations = agent.get('specializations', [])
        
        # Calculate title similarity
        title_similarity = SequenceMatcher(None, occupation_title.lower(), agent_title.lower()).ratio()
        
        # Calculate description similarity
        desc_similarity = SequenceMatcher(None, occupation_desc.lower(), agent_desc.lower()).ratio()
        
        # Calculate skills/specializations overlap
        skills_similarity = self._calculate_skills_similarity(occupation_skills, agent_specializations)
        
        # Weighted combination
        combined_similarity = (
            title_similarity * 0.5 +
            desc_similarity * 0.3 +
            skills_similarity * 0.2
        )
        
        return combined_similarity
    
    def _calculate_skills_similarity(self, occupation_skills: List[str], agent_specializations: List[str]) -> float:
        """Calculate similarity between skill sets."""
        if not occupation_skills or not agent_specializations:
            return 0.0
        
        # Convert to lowercase for comparison
        occ_skills_lower = [skill.lower() for skill in occupation_skills]
        agent_specs_lower = [spec.lower() for spec in agent_specializations]
        
        # Calculate Jaccard similarity
        intersection = len(set(occ_skills_lower) & set(agent_specs_lower))
        union = len(set(occ_skills_lower) | set(agent_specs_lower))
        
        return intersection / union if union > 0 else 0.0
    
    def _create_gap_record(self, occupation_title: str, domain: str, occupation: Any,
                          similarity_to_existing: float, similar_agents: List[Dict]) -> AgentGap:
        """Create a gap record for an identified gap."""
        
        # Extract occupation details
        if hasattr(occupation, 'required_skills'):
            required_capabilities = occupation.required_skills
        else:
            required_capabilities = self._infer_capabilities(occupation_title, domain)
        
        # Calculate initial scores
        market_demand_score = self._calculate_market_demand_score(occupation_title, domain)
        strategic_value_score = self._calculate_strategic_value_score(occupation_title, domain)
        
        # Calculate priority score
        priority_score = self._calculate_priority_score(
            market_demand_score, strategic_value_score, similarity_to_existing
        )
        
        return AgentGap(
            occupation_title=occupation_title,
            domain=domain,
            priority_score=priority_score,
            market_demand_score=market_demand_score,
            strategic_value_score=strategic_value_score,
            similarity_to_existing=similarity_to_existing,
            gap_rationale=self._generate_gap_rationale(occupation_title, domain, similarity_to_existing),
            required_capabilities=required_capabilities,
            estimated_effort=self._estimate_creation_effort(occupation_title, required_capabilities),
            business_impact=self._estimate_business_impact(occupation_title, domain),
            sources=['Gap Analysis System'],
            related_existing_agents=[agent['agent_title'] for agent in similar_agents[:3]]
        )
    
    def _infer_capabilities(self, occupation_title: str, domain: str) -> List[str]:
        """Infer required capabilities for an occupation."""
        capabilities = []
        
        # Base capabilities
        capabilities.extend(['Problem solving', 'Communication', 'Domain expertise'])
        
        # Title-based capabilities
        title_lower = occupation_title.lower()
        if 'engineer' in title_lower:
            capabilities.extend(['Technical design', 'System analysis', 'Implementation'])
        elif 'analyst' in title_lower:
            capabilities.extend(['Data analysis', 'Research', 'Reporting'])
        elif 'manager' in title_lower:
            capabilities.extend(['Leadership', 'Project management', 'Strategy'])
        elif 'specialist' in title_lower:
            capabilities.extend(['Specialized knowledge', 'Consultation', 'Best practices'])
        
        # Domain-based capabilities
        domain_lower = domain.lower()
        if 'technology' in domain_lower or 'ai' in domain_lower:
            capabilities.extend(['Technical skills', 'Innovation', 'Digital literacy'])
        elif 'healthcare' in domain_lower:
            capabilities.extend(['Medical knowledge', 'Patient care', 'Compliance'])
        elif 'finance' in domain_lower:
            capabilities.extend(['Financial analysis', 'Risk management', 'Regulations'])
        
        return list(set(capabilities))[:8]  # Limit and deduplicate
    
    def _calculate_market_demand_score(self, occupation_title: str, domain: str) -> float:
        """Calculate market demand score for occupation."""
        score = 0.5  # Base score
        
        # High-demand occupation types
        high_demand_types = ['engineer', 'analyst', 'specialist', 'manager', 'consultant']
        if any(demand_type in occupation_title.lower() for demand_type in high_demand_types):
            score += 0.2
        
        # High-demand domains
        high_demand_domains = ['ai', 'cybersecurity', 'healthcare', 'renewable energy', 'data']
        if any(demand_domain in domain.lower() for demand_domain in high_demand_domains):
            score += 0.3
        
        return min(1.0, score)
    
    def _calculate_strategic_value_score(self, occupation_title: str, domain: str) -> float:
        """Calculate strategic value score for occupation."""
        score = 0.5  # Base score
        
        # Strategic occupation types
        strategic_types = ['architect', 'lead', 'principal', 'director', 'strategist']
        if any(strategic_type in occupation_title.lower() for strategic_type in strategic_types):
            score += 0.2
        
        # Strategic domains
        strategic_domains = ['artificial intelligence', 'machine learning', 'blockchain', 'quantum']
        if any(strategic_domain in domain.lower() for strategic_domain in strategic_domains):
            score += 0.3
        
        return min(1.0, score)
    
    def _calculate_priority_score(self, market_demand: float, strategic_value: float, similarity: float) -> float:
        """Calculate overall priority score for gap."""
        # Higher priority for high demand, high value, low similarity
        uniqueness_bonus = 1.0 - similarity  # Bonus for being unique
        
        priority = (
            market_demand * 0.4 +
            strategic_value * 0.4 +
            uniqueness_bonus * 0.2
        )
        
        return priority
    
    def _generate_gap_rationale(self, occupation_title: str, domain: str, similarity: float) -> str:
        """Generate rationale for why this is a gap."""
        return f"No existing agent covers {occupation_title} in {domain}. Similarity to existing agents: {similarity:.1%}. Market demand and strategic value justify creation."
    
    def _estimate_creation_effort(self, occupation_title: str, capabilities: List[str]) -> str:
        """Estimate effort required to create agent."""
        if len(capabilities) <= 4:
            return "Low effort"
        elif len(capabilities) <= 7:
            return "Medium effort"
        else:
            return "High effort"
    
    def _estimate_business_impact(self, occupation_title: str, domain: str) -> str:
        """Estimate business impact of creating this agent."""
        high_impact_types = ['engineer', 'architect', 'strategist', 'director']
        high_impact_domains = ['ai', 'cybersecurity', 'healthcare']
        
        if (any(impact_type in occupation_title.lower() for impact_type in high_impact_types) or
            any(impact_domain in domain.lower() for impact_domain in high_impact_domains)):
            return "High impact"
        else:
            return "Medium impact"
    
    def _score_and_prioritize_gaps(self, gaps: List[AgentGap], domain: str) -> List[AgentGap]:
        """Score and prioritize identified gaps."""
        self.logger.info(f"Scoring and prioritizing {len(gaps)} gaps")
        
        # Sort by priority score
        sorted_gaps = sorted(gaps, key=lambda x: x.priority_score, reverse=True)
        
        return sorted_gaps
    
    def _filter_gaps_by_quality(self, gaps: List[AgentGap]) -> List[AgentGap]:
        """Filter gaps by quality thresholds."""
        thresholds = self.config.get('quality_thresholds', {}).get('gap_analysis', {})
        min_market_demand = thresholds.get('min_market_demand', 0.6)
        min_strategic_value = thresholds.get('min_strategic_value', 0.7)
        
        filtered_gaps = []
        for gap in gaps:
            if (gap.market_demand_score >= min_market_demand and 
                gap.strategic_value_score >= min_strategic_value):
                filtered_gaps.append(gap)
        
        # Limit to max gaps per cycle
        max_gaps = self.config.get('phase_configuration', {}).get('phase_1_strategic_focus', {}).get('gap_identification', {}).get('max_gaps_per_cycle', 10)
        
        return filtered_gaps[:max_gaps]
    
    def select_top_gap(self, gaps: List[AgentGap]) -> Optional[AgentGap]:
        """Select the top priority gap for agent creation."""
        if not gaps:
            return None
        
        # Return highest priority gap
        top_gap = gaps[0]
        
        self._log_audit_event("TOP_GAP_SELECTED", f"Selected {top_gap.occupation_title} in {top_gap.domain} (priority: {top_gap.priority_score:.3f})")
        
        return top_gap
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} GAP_ANALYZER {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    # Mock occupation for testing
    class MockOccupation:
        def __init__(self, title, description="", skills=None):
            self.title = title
            self.description = description
            self.required_skills = skills or []
    
    analyzer = GapAnalyzer()
    
    if len(sys.argv) > 2:
        command = sys.argv[1]
        domain = sys.argv[2]
        
        if command == "analyze":
            # Create mock occupations for testing
            mock_occupations = [
                MockOccupation("AI Ethics Specialist", "Specialist in AI ethics and governance", ["Ethics", "AI", "Policy"]),
                MockOccupation("Renewable Energy Engineer", "Engineer for renewable energy systems", ["Engineering", "Renewable Energy", "Sustainability"]),
                MockOccupation("Cybersecurity Analyst", "Analyst for cybersecurity threats", ["Security", "Analysis", "Risk Management"])
            ]
            
            print(f"Starting gap analysis for domain: {domain}")
            gaps = analyzer.analyze_gaps(domain, mock_occupations)
            
            print(f"\nFound {len(gaps)} priority gaps:")
            for i, gap in enumerate(gaps[:5], 1):
                print(f"{i}. {gap.occupation_title}")
                print(f"   Priority Score: {gap.priority_score:.3f}")
                print(f"   Market Demand: {gap.market_demand_score:.3f}")
                print(f"   Strategic Value: {gap.strategic_value_score:.3f}")
                print(f"   Rationale: {gap.gap_rationale}")
                print()
        
        else:
            print("Usage: python gap_analyzer.py analyze <domain>")
    else:
        print("Usage: python gap_analyzer.py analyze <domain>")
        print("Example: python gap_analyzer.py analyze 'AI Healthcare'")
