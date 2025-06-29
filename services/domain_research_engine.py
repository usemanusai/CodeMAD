#!/usr/bin/env python3
"""
Domain Research Engine for Project Chimera
Deep-dive research system for selected expansion focus domains.
Discovers specific occupations, specializations, and knowledge requirements.
"""

import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
import re
from dataclasses import dataclass
from urllib.parse import urljoin
import hashlib

@dataclass
class OccupationProfile:
    """Data structure for occupation analysis."""
    title: str
    description: str
    key_responsibilities: List[str]
    required_skills: List[str]
    education_requirements: List[str]
    industry_context: str
    growth_outlook: str
    salary_range: str
    specializations: List[str]
    related_occupations: List[str]
    sources: List[str]
    quality_score: float

class DomainResearchEngine:
    """
    Deep research engine for analyzing specific domains and discovering occupations.
    Performs comprehensive research on selected expansion focus areas.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.config_file = self.workspace_root / "services" / "config" / "expansion_config.json"
        self.sources_file = self.workspace_root / "services" / "config" / "research_sources.json"
        self.cache_dir = self.workspace_root / "services" / "data" / "research_cache"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load configurations
        self.config = self._load_config()
        self.research_sources = self._load_research_sources()
        
        # Request session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ChimeraResearchBot/1.0; +https://github.com/usemanusai/CodeMAD)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
    
    def _load_config(self) -> Dict[str, Any]:
        """Load expansion configuration."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def _load_research_sources(self) -> Dict[str, Any]:
        """Load research sources configuration."""
        try:
            with open(self.sources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading research sources: {e}")
            return {}
    
    def research_domain(self, domain: str) -> List[OccupationProfile]:
        """
        Perform deep research on a specific domain.
        
        Args:
            domain: The domain to research (e.g., "Renewable Energy", "AI Healthcare")
            
        Returns:
            List of discovered occupation profiles
        """
        self.logger.info(f"Starting deep research on domain: {domain}")
        self._log_audit_event("DOMAIN_RESEARCH_STARTED", f"Researching domain: {domain}")
        
        try:
            # Phase 1: Gather domain-specific data
            domain_data = self._gather_domain_data(domain)
            
            # Phase 2: Extract occupation information
            occupations = self._extract_occupations(domain, domain_data)
            
            # Phase 3: Enrich occupation profiles
            enriched_profiles = self._enrich_occupation_profiles(occupations, domain)
            
            # Phase 4: Validate and score profiles
            validated_profiles = self._validate_and_score_profiles(enriched_profiles)
            
            self._log_audit_event("DOMAIN_RESEARCH_COMPLETED", f"Found {len(validated_profiles)} occupations in {domain}")
            self.logger.info(f"Domain research completed. Found {len(validated_profiles)} occupation profiles.")
            
            return validated_profiles
            
        except Exception as e:
            self.logger.error(f"Error in domain research: {e}")
            self._log_audit_event("DOMAIN_RESEARCH_ERROR", f"Error researching {domain}: {str(e)}")
            return []
    
    def _gather_domain_data(self, domain: str) -> Dict[str, Any]:
        """Gather comprehensive data about the domain."""
        self.logger.info(f"Gathering data for domain: {domain}")
        domain_data = {}
        
        # Map domain to relevant source categories
        source_mapping = self._map_domain_to_sources(domain)
        
        for category, sources in source_mapping.items():
            category_data = {}
            
            for source in sources:
                try:
                    source_data = self._research_domain_source(source, domain)
                    if source_data:
                        category_data[source['name']] = source_data
                        
                except Exception as e:
                    self.logger.warning(f"Error researching {source.get('name', 'unknown')}: {e}")
            
            if category_data:
                domain_data[category] = category_data
        
        return domain_data
    
    def _map_domain_to_sources(self, domain: str) -> Dict[str, List[Dict]]:
        """Map domain to relevant research sources."""
        domain_lower = domain.lower()
        source_mapping = {}
        
        # Always include labor market data
        source_mapping['labor_market'] = (
            self.research_sources.get('labor_market_data', {}).get('government_sources', []) +
            self.research_sources.get('labor_market_data', {}).get('industry_reports', [])
        )
        
        # Add job market platforms
        source_mapping['job_market'] = self.research_sources.get('job_market_platforms', {}).get('job_boards', [])
        
        # Add domain-specific sources
        if any(tech_term in domain_lower for tech_term in ['ai', 'technology', 'software', 'data', 'cyber']):
            source_mapping['technology'] = self.research_sources.get('technology_trends', {}).get('tech_platforms', [])
        
        if 'healthcare' in domain_lower or 'medical' in domain_lower:
            source_mapping['healthcare'] = self.research_sources.get('industry_specific', {}).get('healthcare', [])
        
        if 'finance' in domain_lower or 'fintech' in domain_lower:
            source_mapping['finance'] = self.research_sources.get('industry_specific', {}).get('finance', [])
        
        if 'education' in domain_lower or 'learning' in domain_lower:
            source_mapping['education'] = self.research_sources.get('industry_specific', {}).get('education', [])
        
        # Add emerging sector sources
        emerging_sectors = self.research_sources.get('emerging_sectors', {})
        for sector_name, sources in emerging_sectors.items():
            if any(term in domain_lower for term in sector_name.split('_')):
                source_mapping[f'emerging_{sector_name}'] = sources
        
        return source_mapping
    
    def _research_domain_source(self, source: Dict[str, Any], domain: str) -> Optional[Dict[str, Any]]:
        """Research a specific source for domain information."""
        source_name = source.get('name', 'unknown')
        
        # Check cache first
        cache_key = self._generate_cache_key(f"{source_name}_{domain}")
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            return cached_data
        
        # Perform research
        source_data = {
            'name': source_name,
            'domain': domain,
            'researched_at': datetime.now().isoformat(),
            'occupations': [],
            'skills': [],
            'trends': [],
            'content_quality': 0.0
        }
        
        # Research specific endpoints
        endpoints = source.get('endpoints', [])
        for endpoint in endpoints[:2]:  # Limit endpoints
            try:
                url = urljoin(source.get('url', ''), endpoint)
                content = self._fetch_url_content(url)
                
                if content:
                    extracted_data = self._extract_domain_info(content, domain)
                    
                    source_data['occupations'].extend(extracted_data['occupations'])
                    source_data['skills'].extend(extracted_data['skills'])
                    source_data['trends'].extend(extracted_data['trends'])
                    source_data['content_quality'] = max(source_data['content_quality'], extracted_data['quality'])
                    
            except Exception as e:
                self.logger.warning(f"Error fetching {url}: {e}")
        
        # Deduplicate and limit data
        source_data['occupations'] = list(set(source_data['occupations']))[:20]
        source_data['skills'] = list(set(source_data['skills']))[:30]
        source_data['trends'] = list(set(source_data['trends']))[:15]
        
        # Cache if quality is sufficient
        if source_data['content_quality'] > 0.3:
            self._cache_data(cache_key, source_data)
            return source_data
        
        return None
    
    def _extract_domain_info(self, content: str, domain: str) -> Dict[str, Any]:
        """Extract domain-specific information from content."""
        domain_lower = domain.lower()
        content_lower = content.lower()
        
        # Extract occupations/job titles
        occupation_patterns = [
            r'\b([A-Z][a-z]+ (?:Engineer|Analyst|Manager|Specialist|Coordinator|Developer|Designer|Consultant|Advisor|Director|Lead))\b',
            r'\b([A-Z][a-z]+ [A-Z][a-z]+(?:ist|er|or|ian))\b',
            r'\b((?:Senior|Junior|Lead|Principal) [A-Z][a-z]+ [A-Z][a-z]+)\b'
        ]
        
        occupations = []
        for pattern in occupation_patterns:
            matches = re.findall(pattern, content)
            occupations.extend(matches)
        
        # Filter occupations related to domain
        relevant_occupations = []
        for occupation in occupations:
            if any(domain_term in occupation.lower() for domain_term in domain_lower.split()):
                relevant_occupations.append(occupation)
            elif self._is_occupation_relevant(occupation, domain):
                relevant_occupations.append(occupation)
        
        # Extract skills
        skill_patterns = [
            r'\b(programming|coding|development|analysis|management|leadership|communication|design|research|strategy)\b',
            r'\b([A-Z][a-z]+ (?:skills|knowledge|experience|expertise))\b',
            r'\b(proficiency in [A-Za-z ]+)\b'
        ]
        
        skills = []
        for pattern in skill_patterns:
            matches = re.findall(pattern, content_lower)
            skills.extend(matches)
        
        # Extract trends
        trend_patterns = [
            r'\b(emerging|growing|increasing|trending|future|next-generation|innovative|cutting-edge)\s+([A-Za-z ]+)\b',
            r'\b([A-Za-z ]+)\s+(?:is|are)\s+(?:becoming|growing|emerging)\b'
        ]
        
        trends = []
        for pattern in trend_patterns:
            matches = re.findall(pattern, content_lower)
            trends.extend([match[1] if isinstance(match, tuple) else match for match in matches])
        
        # Calculate quality score
        quality_score = self._calculate_content_quality(content, domain, relevant_occupations, skills, trends)
        
        return {
            'occupations': relevant_occupations,
            'skills': skills,
            'trends': trends,
            'quality': quality_score
        }
    
    def _is_occupation_relevant(self, occupation: str, domain: str) -> bool:
        """Check if occupation is relevant to domain."""
        occupation_lower = occupation.lower()
        domain_lower = domain.lower()
        
        # Domain-specific relevance rules
        if 'healthcare' in domain_lower:
            return any(term in occupation_lower for term in ['health', 'medical', 'clinical', 'nurse', 'therapy'])
        
        if 'technology' in domain_lower or 'ai' in domain_lower:
            return any(term in occupation_lower for term in ['tech', 'software', 'data', 'ai', 'machine', 'cyber'])
        
        if 'renewable' in domain_lower or 'energy' in domain_lower:
            return any(term in occupation_lower for term in ['energy', 'renewable', 'solar', 'wind', 'environmental'])
        
        if 'finance' in domain_lower:
            return any(term in occupation_lower for term in ['financial', 'finance', 'banking', 'investment', 'risk'])
        
        return False
    
    def _calculate_content_quality(self, content: str, domain: str, occupations: List, skills: List, trends: List) -> float:
        """Calculate quality score for extracted content."""
        score = 0.0
        
        # Base score for content length
        if len(content) > 500:
            score += 0.2
        
        # Score for relevant occupations found
        score += min(0.4, len(occupations) * 0.05)
        
        # Score for skills found
        score += min(0.2, len(skills) * 0.02)
        
        # Score for trends found
        score += min(0.2, len(trends) * 0.03)
        
        return min(1.0, score)
    
    def _extract_occupations(self, domain: str, domain_data: Dict[str, Any]) -> List[str]:
        """Extract unique occupations from domain data."""
        all_occupations = set()
        
        for category_data in domain_data.values():
            for source_data in category_data.values():
                if isinstance(source_data, dict) and 'occupations' in source_data:
                    all_occupations.update(source_data['occupations'])
        
        # Filter and clean occupations
        cleaned_occupations = []
        for occupation in all_occupations:
            if len(occupation) > 5 and len(occupation) < 100:  # Reasonable length
                cleaned_occupations.append(occupation.strip())
        
        return list(set(cleaned_occupations))[:50]  # Limit to top 50
    
    def _enrich_occupation_profiles(self, occupations: List[str], domain: str) -> List[OccupationProfile]:
        """Enrich occupation data with detailed profiles."""
        self.logger.info(f"Enriching {len(occupations)} occupation profiles...")
        
        profiles = []
        for occupation in occupations:
            try:
                profile = self._create_occupation_profile(occupation, domain)
                if profile:
                    profiles.append(profile)
                    
            except Exception as e:
                self.logger.warning(f"Error creating profile for {occupation}: {e}")
        
        return profiles
    
    def _create_occupation_profile(self, occupation: str, domain: str) -> Optional[OccupationProfile]:
        """Create detailed profile for an occupation."""
        
        # Generate profile based on occupation title and domain
        profile = OccupationProfile(
            title=occupation,
            description=self._generate_description(occupation, domain),
            key_responsibilities=self._generate_responsibilities(occupation, domain),
            required_skills=self._generate_skills(occupation, domain),
            education_requirements=self._generate_education_requirements(occupation),
            industry_context=domain,
            growth_outlook=self._estimate_growth_outlook(occupation, domain),
            salary_range=self._estimate_salary_range(occupation),
            specializations=self._identify_specializations(occupation, domain),
            related_occupations=self._find_related_occupations(occupation),
            sources=['Domain Research Engine'],
            quality_score=self._calculate_profile_quality(occupation, domain)
        )
        
        return profile if profile.quality_score > 0.5 else None
    
    def _generate_description(self, occupation: str, domain: str) -> str:
        """Generate description for occupation."""
        return f"Professional specializing in {occupation.lower()} within the {domain} sector. Responsible for applying domain expertise to solve complex challenges and drive innovation."
    
    def _generate_responsibilities(self, occupation: str, domain: str) -> List[str]:
        """Generate key responsibilities for occupation."""
        base_responsibilities = [
            f"Apply {occupation.lower()} expertise to {domain.lower()} challenges",
            "Collaborate with cross-functional teams",
            "Stay current with industry trends and best practices",
            "Contribute to strategic planning and decision-making"
        ]
        
        # Add occupation-specific responsibilities
        if 'engineer' in occupation.lower():
            base_responsibilities.extend([
                "Design and implement technical solutions",
                "Conduct system analysis and optimization"
            ])
        elif 'analyst' in occupation.lower():
            base_responsibilities.extend([
                "Analyze data and generate insights",
                "Prepare reports and recommendations"
            ])
        elif 'manager' in occupation.lower():
            base_responsibilities.extend([
                "Lead and manage team members",
                "Oversee project execution and delivery"
            ])
        
        return base_responsibilities[:5]
    
    def _generate_skills(self, occupation: str, domain: str) -> List[str]:
        """Generate required skills for occupation."""
        base_skills = [
            "Problem-solving",
            "Communication",
            "Critical thinking",
            "Project management"
        ]
        
        # Add domain-specific skills
        domain_lower = domain.lower()
        if 'technology' in domain_lower or 'ai' in domain_lower:
            base_skills.extend(["Programming", "Data analysis", "Technical documentation"])
        elif 'healthcare' in domain_lower:
            base_skills.extend(["Medical knowledge", "Patient care", "Regulatory compliance"])
        elif 'finance' in domain_lower:
            base_skills.extend(["Financial analysis", "Risk assessment", "Regulatory knowledge"])
        
        # Add occupation-specific skills
        if 'engineer' in occupation.lower():
            base_skills.extend(["Technical design", "System architecture"])
        elif 'analyst' in occupation.lower():
            base_skills.extend(["Data analysis", "Research methodology"])
        
        return list(set(base_skills))[:8]
    
    def _generate_education_requirements(self, occupation: str) -> List[str]:
        """Generate education requirements for occupation."""
        if any(term in occupation.lower() for term in ['engineer', 'scientist', 'analyst']):
            return ["Bachelor's degree in relevant field", "Professional certifications preferred"]
        elif 'manager' in occupation.lower():
            return ["Bachelor's degree", "Management experience", "Leadership training"]
        else:
            return ["Relevant education or experience", "Professional development"]
    
    def _estimate_growth_outlook(self, occupation: str, domain: str) -> str:
        """Estimate growth outlook for occupation."""
        # High-growth domains
        high_growth_domains = ['ai', 'renewable energy', 'cybersecurity', 'healthcare technology']
        if any(term in domain.lower() for term in high_growth_domains):
            return "High growth expected"
        else:
            return "Moderate growth expected"
    
    def _estimate_salary_range(self, occupation: str) -> str:
        """Estimate salary range for occupation."""
        if any(term in occupation.lower() for term in ['engineer', 'manager', 'director']):
            return "$70,000 - $150,000+"
        elif any(term in occupation.lower() for term in ['analyst', 'specialist']):
            return "$50,000 - $100,000"
        else:
            return "$40,000 - $80,000"
    
    def _identify_specializations(self, occupation: str, domain: str) -> List[str]:
        """Identify potential specializations for occupation."""
        specializations = []
        
        if 'engineer' in occupation.lower():
            specializations = ["Senior Engineer", "Lead Engineer", "Principal Engineer", "Architect"]
        elif 'analyst' in occupation.lower():
            specializations = ["Senior Analyst", "Lead Analyst", "Principal Analyst", "Consultant"]
        elif 'manager' in occupation.lower():
            specializations = ["Senior Manager", "Director", "VP", "Executive"]
        
        return specializations[:3]
    
    def _find_related_occupations(self, occupation: str) -> List[str]:
        """Find related occupations."""
        # Simple related occupation generation
        base = occupation.split()[0] if occupation.split() else occupation
        
        related = [
            f"Senior {occupation}",
            f"{base} Consultant",
            f"{base} Coordinator"
        ]
        
        return [r for r in related if r != occupation][:3]
    
    def _calculate_profile_quality(self, occupation: str, domain: str) -> float:
        """Calculate quality score for occupation profile."""
        score = 0.5  # Base score
        
        # Higher score for well-defined occupations
        if len(occupation.split()) >= 2:
            score += 0.2
        
        # Higher score for common occupation types
        if any(term in occupation.lower() for term in ['engineer', 'analyst', 'manager', 'specialist']):
            score += 0.2
        
        # Higher score for high-demand domains
        if any(term in domain.lower() for term in ['ai', 'healthcare', 'renewable', 'cyber']):
            score += 0.1
        
        return min(1.0, score)
    
    def _validate_and_score_profiles(self, profiles: List[OccupationProfile]) -> List[OccupationProfile]:
        """Validate and score occupation profiles."""
        validated = []
        
        for profile in profiles:
            # Quality threshold
            if profile.quality_score >= 0.5:
                validated.append(profile)
        
        # Sort by quality score
        validated.sort(key=lambda x: x.quality_score, reverse=True)
        
        return validated[:30]  # Return top 30 profiles
    
    def _fetch_url_content(self, url: str) -> Optional[str]:
        """Fetch content from URL with error handling."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
            
        except Exception as e:
            self.logger.warning(f"Error fetching {url}: {e}")
            return None
    
    def _generate_cache_key(self, key_data: str) -> str:
        """Generate cache key."""
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached data if still valid."""
        cache_file = self.cache_dir / f"domain_{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                # Check if cache is still valid (6 hours for domain research)
                cached_time = datetime.fromisoformat(cached_data.get('cached_at', ''))
                if datetime.now() - cached_time < timedelta(hours=6):
                    return cached_data.get('data')
                    
            except Exception as e:
                self.logger.warning(f"Error reading cache {cache_key}: {e}")
        
        return None
    
    def _cache_data(self, cache_key: str, data: Dict[str, Any]):
        """Cache data for future use."""
        cache_file = self.cache_dir / f"domain_{cache_key}.json"
        
        try:
            cache_entry = {
                'cached_at': datetime.now().isoformat(),
                'cache_key': cache_key,
                'data': data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_entry, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.warning(f"Error caching data {cache_key}: {e}")
    
    def _log_audit_event(self, event_type: str, details: str):
        """Log event to audit ledger."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            log_entry = f"[{timestamp}] {event_type} DOMAIN_RESEARCH_ENGINE {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    engine = DomainResearchEngine()
    
    if len(sys.argv) > 2:
        command = sys.argv[1]
        domain = sys.argv[2]
        
        if command == "research":
            print(f"Starting domain research for: {domain}")
            profiles = engine.research_domain(domain)
            
            print(f"\nFound {len(profiles)} occupation profiles:")
            for i, profile in enumerate(profiles[:5], 1):
                print(f"{i}. {profile.title}")
                print(f"   Quality Score: {profile.quality_score:.3f}")
                print(f"   Description: {profile.description[:100]}...")
                print(f"   Key Skills: {', '.join(profile.required_skills[:3])}")
                print()
        
        else:
            print("Usage: python domain_research_engine.py research <domain>")
    else:
        print("Usage: python domain_research_engine.py research <domain>")
        print("Example: python domain_research_engine.py research 'AI Healthcare'")
