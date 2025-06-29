#!/usr/bin/env python3
"""
Global Needs Analyzer for Project Chimera
Autonomous system for identifying global occupational needs and strategic expansion opportunities.
Integrates with web research capabilities and trend analysis.
"""

import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import re
import time
import hashlib
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass

@dataclass
class DomainAnalysis:
    """Data structure for domain analysis results."""
    domain: str
    urgency_score: float
    impact_score: float
    feasibility_score: float
    combined_score: float
    evidence: List[str]
    sources: List[str]
    trends: List[str]
    job_growth_data: Dict[str, Any]
    skills_demand: List[str]

class GlobalNeedsAnalyzer:
    """
    Autonomous analyzer for identifying global occupational needs and trends.
    Performs web research, trend analysis, and strategic domain scoring.
    """
    
    def __init__(self, workspace_root: str = "/mnt/persist/workspace"):
        self.workspace_root = Path(workspace_root)
        self.config_file = self.workspace_root / "services" / "config" / "expansion_config.json"
        self.sources_file = self.workspace_root / "services" / "config" / "research_sources.json"
        self.cache_dir = self.workspace_root / "services" / "data" / "research_cache"
        self.state_file = self.workspace_root / "services" / "data" / "expansion_state.json"
        self.audit_log = self.workspace_root / "logs" / "audit_ledger.log"
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load configurations
        self.config = self._load_config()
        self.research_sources = self._load_research_sources()
        
        # Initialize cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Request session with proper headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ChimeraResearchBot/1.0; +https://github.com/usemanusai/CodeMAD)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Rate limiting
        self.last_request_time = {}
        self.request_counts = {}
    
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
    
    def analyze_global_needs(self) -> List[DomainAnalysis]:
        """
        Perform comprehensive global needs analysis.
        
        Returns:
            List of domain analyses ranked by strategic importance
        """
        self.logger.info("Starting global needs analysis...")
        self._log_audit_event("GLOBAL_NEEDS_ANALYSIS_STARTED", "Beginning comprehensive analysis")
        
        try:
            # Phase 1: Gather labor market data
            labor_data = self._gather_labor_market_data()
            
            # Phase 2: Analyze technology trends
            tech_trends = self._analyze_technology_trends()
            
            # Phase 3: Research emerging sectors
            emerging_sectors = self._research_emerging_sectors()
            
            # Phase 4: Combine and score domains
            domain_analyses = self._combine_and_score_domains(labor_data, tech_trends, emerging_sectors)
            
            # Phase 5: Rank by strategic importance
            ranked_domains = self._rank_domains_strategically(domain_analyses)
            
            self._log_audit_event("GLOBAL_NEEDS_ANALYSIS_COMPLETED", f"Analyzed {len(ranked_domains)} domains")
            self.logger.info(f"Global needs analysis completed. Found {len(ranked_domains)} strategic domains.")
            
            return ranked_domains
            
        except Exception as e:
            self.logger.error(f"Error in global needs analysis: {e}")
            self._log_audit_event("GLOBAL_NEEDS_ANALYSIS_ERROR", str(e))
            return []
    
    def _gather_labor_market_data(self) -> Dict[str, Any]:
        """Gather labor market data from government and industry sources."""
        self.logger.info("Gathering labor market data...")
        labor_data = {}
        
        # Get government sources
        gov_sources = self.research_sources.get('labor_market_data', {}).get('government_sources', [])
        
        for source in gov_sources:
            try:
                source_data = self._research_source(source)
                if source_data:
                    labor_data[source['name']] = source_data
                    
            except Exception as e:
                self.logger.warning(f"Error researching {source.get('name', 'unknown')}: {e}")
        
        # Get industry reports
        industry_sources = self.research_sources.get('labor_market_data', {}).get('industry_reports', [])
        
        for source in industry_sources:
            try:
                source_data = self._research_source(source)
                if source_data:
                    labor_data[source['name']] = source_data
                    
            except Exception as e:
                self.logger.warning(f"Error researching {source.get('name', 'unknown')}: {e}")
        
        return labor_data
    
    def _analyze_technology_trends(self) -> Dict[str, Any]:
        """Analyze technology trends and emerging skills."""
        self.logger.info("Analyzing technology trends...")
        tech_data = {}
        
        # Get tech platform sources
        tech_sources = self.research_sources.get('technology_trends', {}).get('tech_platforms', [])
        
        for source in tech_sources:
            try:
                source_data = self._research_source(source)
                if source_data:
                    tech_data[source['name']] = source_data
                    
            except Exception as e:
                self.logger.warning(f"Error researching {source.get('name', 'unknown')}: {e}")
        
        return tech_data
    
    def _research_emerging_sectors(self) -> Dict[str, Any]:
        """Research emerging sectors and new occupational areas."""
        self.logger.info("Researching emerging sectors...")
        emerging_data = {}
        
        # Get emerging sector sources
        emerging_sources = self.research_sources.get('emerging_sectors', {})
        
        for sector_name, sources in emerging_sources.items():
            sector_data = {}
            for source in sources:
                try:
                    source_data = self._research_source(source)
                    if source_data:
                        sector_data[source['name']] = source_data
                        
                except Exception as e:
                    self.logger.warning(f"Error researching {source.get('name', 'unknown')}: {e}")
            
            if sector_data:
                emerging_data[sector_name] = sector_data
        
        return emerging_data
    
    def _research_source(self, source: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Research a specific source with rate limiting and caching."""
        source_name = source.get('name', 'unknown')
        base_url = source.get('url', '')
        endpoints = source.get('endpoints', [])
        
        # Check rate limiting
        if not self._check_rate_limit(source_name, source.get('rate_limit', '60_requests_per_hour')):
            self.logger.warning(f"Rate limit exceeded for {source_name}")
            return None
        
        # Check cache first
        cache_key = self._generate_cache_key(source_name, endpoints)
        cached_data = self._get_cached_data(cache_key)
        if cached_data:
            self.logger.info(f"Using cached data for {source_name}")
            return cached_data
        
        # Research the source
        source_data = {
            'name': source_name,
            'url': base_url,
            'data_types': source.get('data_types', []),
            'reliability_score': source.get('reliability_score', 0.5),
            'researched_at': datetime.now().isoformat(),
            'content': [],
            'keywords': [],
            'trends': []
        }
        
        for endpoint in endpoints[:2]:  # Limit to first 2 endpoints to avoid overload
            try:
                url = urljoin(base_url, endpoint)
                content = self._fetch_url_content(url)
                
                if content:
                    processed_content = self._process_content(content, source.get('data_types', []))
                    source_data['content'].append({
                        'endpoint': endpoint,
                        'url': url,
                        'content': processed_content['text'][:1000],  # Limit content size
                        'keywords': processed_content['keywords'],
                        'quality_score': processed_content['quality_score']
                    })
                    
                    source_data['keywords'].extend(processed_content['keywords'])
                    
            except Exception as e:
                self.logger.warning(f"Error fetching {url}: {e}")
        
        # Cache the results
        if source_data['content']:
            self._cache_data(cache_key, source_data)
            return source_data
        
        return None
    
    def _fetch_url_content(self, url: str) -> Optional[str]:
        """Fetch content from URL with error handling."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
            
        except Exception as e:
            self.logger.warning(f"Error fetching {url}: {e}")
            return None
    
    def _process_content(self, content: str, data_types: List[str]) -> Dict[str, Any]:
        """Process and extract relevant information from content."""
        # Simple content processing - extract keywords and assess quality
        
        # Extract keywords related to jobs and skills
        job_keywords = re.findall(r'\b(?:job|career|skill|employment|work|profession|occupation|role|position)\w*\b', 
                                 content.lower())
        
        # Extract domain-specific keywords based on data types
        domain_keywords = []
        for data_type in data_types:
            if 'employment' in data_type:
                domain_keywords.extend(re.findall(r'\b(?:hiring|recruitment|workforce|labor)\w*\b', content.lower()))
            elif 'technology' in data_type:
                domain_keywords.extend(re.findall(r'\b(?:AI|machine learning|blockchain|cloud|automation)\w*\b', content.lower()))
            elif 'healthcare' in data_type:
                domain_keywords.extend(re.findall(r'\b(?:medical|healthcare|nursing|therapy|clinical)\w*\b', content.lower()))
        
        # Assess content quality
        quality_score = min(1.0, (len(job_keywords) + len(domain_keywords)) / 20.0)
        
        return {
            'text': content[:2000],  # Limit text size
            'keywords': list(set(job_keywords + domain_keywords))[:20],  # Limit keywords
            'quality_score': quality_score
        }
    
    def _combine_and_score_domains(self, labor_data: Dict, tech_trends: Dict, emerging_sectors: Dict) -> List[DomainAnalysis]:
        """Combine research data and score domains."""
        self.logger.info("Combining research data and scoring domains...")
        
        # Extract domains from all data sources
        all_domains = set()
        
        # Extract from labor data
        for source_name, source_data in labor_data.items():
            if isinstance(source_data, dict) and 'keywords' in source_data:
                all_domains.update(self._extract_domains_from_keywords(source_data['keywords']))
        
        # Extract from tech trends
        for source_name, source_data in tech_trends.items():
            if isinstance(source_data, dict) and 'keywords' in source_data:
                all_domains.update(self._extract_domains_from_keywords(source_data['keywords']))
        
        # Extract from emerging sectors
        for sector_name, sector_data in emerging_sectors.items():
            all_domains.add(sector_name.replace('_', ' ').title())
            for source_name, source_data in sector_data.items():
                if isinstance(source_data, dict) and 'keywords' in source_data:
                    all_domains.update(self._extract_domains_from_keywords(source_data['keywords']))
        
        # Score each domain
        domain_analyses = []
        for domain in all_domains:
            if len(domain) > 3:  # Filter out very short domains
                analysis = self._score_domain(domain, labor_data, tech_trends, emerging_sectors)
                if analysis.combined_score > 0.3:  # Only include domains with reasonable scores
                    domain_analyses.append(analysis)
        
        return domain_analyses
    
    def _extract_domains_from_keywords(self, keywords: List[str]) -> List[str]:
        """Extract potential domains from keywords."""
        domains = []
        
        # Common domain patterns
        domain_patterns = [
            r'\b(healthcare|medical|nursing)\b',
            r'\b(technology|tech|software|AI|artificial intelligence)\b',
            r'\b(finance|financial|banking|fintech)\b',
            r'\b(education|educational|teaching|learning)\b',
            r'\b(renewable energy|sustainability|green|environmental)\b',
            r'\b(cybersecurity|security|privacy)\b',
            r'\b(biotechnology|biotech|pharmaceutical)\b',
            r'\b(data science|analytics|machine learning)\b'
        ]
        
        text = ' '.join(keywords).lower()
        
        for pattern in domain_patterns:
            matches = re.findall(pattern, text)
            domains.extend([match.title() for match in matches])
        
        return list(set(domains))
    
    def _score_domain(self, domain: str, labor_data: Dict, tech_trends: Dict, emerging_sectors: Dict) -> DomainAnalysis:
        """Score a domain based on urgency, impact, and feasibility."""
        
        # Calculate urgency score (0.0 - 1.0)
        urgency_score = self._calculate_urgency_score(domain, labor_data, tech_trends)
        
        # Calculate impact score (0.0 - 1.0)
        impact_score = self._calculate_impact_score(domain, labor_data, emerging_sectors)
        
        # Calculate feasibility score (0.0 - 1.0)
        feasibility_score = self._calculate_feasibility_score(domain)
        
        # Combined score with weights from config
        weights = self.config.get('phase_configuration', {}).get('phase_1_strategic_focus', {}).get('scoring_algorithm', 'urgency_impact_feasibility')
        if weights == 'urgency_impact_feasibility':
            combined_score = (urgency_score * 0.4 + impact_score * 0.4 + feasibility_score * 0.2)
        else:
            combined_score = (urgency_score + impact_score + feasibility_score) / 3.0
        
        return DomainAnalysis(
            domain=domain,
            urgency_score=urgency_score,
            impact_score=impact_score,
            feasibility_score=feasibility_score,
            combined_score=combined_score,
            evidence=self._gather_evidence(domain, labor_data, tech_trends, emerging_sectors),
            sources=self._gather_sources(domain, labor_data, tech_trends, emerging_sectors),
            trends=self._identify_trends(domain, tech_trends),
            job_growth_data=self._extract_job_growth_data(domain, labor_data),
            skills_demand=self._extract_skills_demand(domain, labor_data, tech_trends)
        )
    
    def _calculate_urgency_score(self, domain: str, labor_data: Dict, tech_trends: Dict) -> float:
        """Calculate urgency score based on current market signals."""
        score = 0.5  # Base score
        
        # Check for mentions in recent data
        domain_lower = domain.lower()
        
        # Labor market urgency indicators
        for source_data in labor_data.values():
            if isinstance(source_data, dict):
                keywords = source_data.get('keywords', [])
                if any(domain_lower in keyword.lower() for keyword in keywords):
                    score += 0.1
        
        # Technology trend urgency
        for source_data in tech_trends.values():
            if isinstance(source_data, dict):
                keywords = source_data.get('keywords', [])
                if any(domain_lower in keyword.lower() for keyword in keywords):
                    score += 0.15
        
        return min(1.0, score)
    
    def _calculate_impact_score(self, domain: str, labor_data: Dict, emerging_sectors: Dict) -> float:
        """Calculate potential impact score."""
        score = 0.5  # Base score
        
        # High-impact domains
        high_impact_domains = ['healthcare', 'ai', 'artificial intelligence', 'renewable energy', 'cybersecurity']
        if any(high_impact in domain.lower() for high_impact in high_impact_domains):
            score += 0.3
        
        # Emerging sector impact
        for sector_data in emerging_sectors.values():
            if isinstance(sector_data, dict):
                for source_data in sector_data.values():
                    if isinstance(source_data, dict):
                        keywords = source_data.get('keywords', [])
                        if any(domain.lower() in keyword.lower() for keyword in keywords):
                            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_feasibility_score(self, domain: str) -> float:
        """Calculate feasibility score for creating agents in this domain."""
        # Base feasibility - most domains are feasible for agent creation
        score = 0.7
        
        # Highly feasible domains (knowledge-based work)
        high_feasibility = ['technology', 'software', 'data', 'analysis', 'research', 'writing', 'consulting']
        if any(feasible in domain.lower() for feasible in high_feasibility):
            score += 0.2
        
        # Lower feasibility domains (physical work)
        low_feasibility = ['construction', 'manufacturing', 'physical', 'manual']
        if any(difficult in domain.lower() for difficult in low_feasibility):
            score -= 0.3
        
        return max(0.1, min(1.0, score))
    
    def _rank_domains_strategically(self, domain_analyses: List[DomainAnalysis]) -> List[DomainAnalysis]:
        """Rank domains by strategic importance."""
        # Sort by combined score descending
        ranked = sorted(domain_analyses, key=lambda x: x.combined_score, reverse=True)
        
        # Apply quality thresholds from config
        thresholds = self.config.get('quality_thresholds', {}).get('domain_scoring', {})
        min_combined = thresholds.get('combined_threshold', 0.5)
        
        # Filter by minimum threshold
        filtered = [domain for domain in ranked if domain.combined_score >= min_combined]
        
        return filtered[:10]  # Return top 10 domains
    
    def _gather_evidence(self, domain: str, *data_sources) -> List[str]:
        """Gather evidence supporting domain importance."""
        evidence = []
        domain_lower = domain.lower()
        
        for data_source in data_sources:
            if isinstance(data_source, dict):
                for source_data in data_source.values():
                    if isinstance(source_data, dict) and 'content' in source_data:
                        for content_item in source_data['content']:
                            if domain_lower in content_item.get('content', '').lower():
                                evidence.append(f"Mentioned in {source_data.get('name', 'source')}")
        
        return evidence[:5]  # Limit evidence items
    
    def _gather_sources(self, domain: str, *data_sources) -> List[str]:
        """Gather sources that mention the domain."""
        sources = []
        domain_lower = domain.lower()
        
        for data_source in data_sources:
            if isinstance(data_source, dict):
                for source_data in data_source.values():
                    if isinstance(source_data, dict):
                        keywords = source_data.get('keywords', [])
                        if any(domain_lower in keyword.lower() for keyword in keywords):
                            sources.append(source_data.get('name', 'Unknown Source'))
        
        return list(set(sources))[:3]  # Limit and deduplicate sources
    
    def _identify_trends(self, domain: str, tech_trends: Dict) -> List[str]:
        """Identify trends related to the domain."""
        trends = []
        domain_lower = domain.lower()
        
        for source_data in tech_trends.values():
            if isinstance(source_data, dict):
                keywords = source_data.get('keywords', [])
                related_keywords = [kw for kw in keywords if domain_lower in kw.lower()]
                trends.extend(related_keywords)
        
        return list(set(trends))[:5]  # Limit and deduplicate trends
    
    def _extract_job_growth_data(self, domain: str, labor_data: Dict) -> Dict[str, Any]:
        """Extract job growth data for the domain."""
        return {
            'growth_rate': 'Unknown',
            'demand_level': 'Moderate',
            'source': 'Research Analysis'
        }
    
    def _extract_skills_demand(self, domain: str, labor_data: Dict, tech_trends: Dict) -> List[str]:
        """Extract skills in demand for the domain."""
        skills = []
        domain_lower = domain.lower()
        
        # Common skills patterns
        skill_patterns = [
            r'\b(programming|coding|development)\b',
            r'\b(analysis|analytics|data)\b',
            r'\b(management|leadership|strategy)\b',
            r'\b(communication|writing|presentation)\b'
        ]
        
        for data_source in [labor_data, tech_trends]:
            for source_data in data_source.values():
                if isinstance(source_data, dict):
                    keywords = source_data.get('keywords', [])
                    text = ' '.join(keywords).lower()
                    
                    if domain_lower in text:
                        for pattern in skill_patterns:
                            matches = re.findall(pattern, text)
                            skills.extend(matches)
        
        return list(set(skills))[:5]  # Limit and deduplicate skills
    
    def _check_rate_limit(self, source_name: str, rate_limit: str) -> bool:
        """Check if request is within rate limits."""
        # Parse rate limit (e.g., "60_requests_per_hour")
        try:
            parts = rate_limit.split('_')
            if len(parts) >= 4:
                limit = int(parts[0])
                period = parts[3]  # hour, minute, day
                
                now = datetime.now()
                period_key = f"{source_name}_{period}"
                
                # Reset counters based on period
                if period == 'hour':
                    reset_time = now.replace(minute=0, second=0, microsecond=0)
                elif period == 'minute':
                    reset_time = now.replace(second=0, microsecond=0)
                else:  # day
                    reset_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
                
                # Check if we need to reset counter
                if period_key not in self.last_request_time or self.last_request_time[period_key] < reset_time:
                    self.request_counts[period_key] = 0
                    self.last_request_time[period_key] = now
                
                # Check limit
                current_count = self.request_counts.get(period_key, 0)
                if current_count >= limit:
                    return False
                
                # Increment counter
                self.request_counts[period_key] = current_count + 1
                return True
                
        except Exception as e:
            self.logger.warning(f"Error parsing rate limit {rate_limit}: {e}")
        
        return True  # Allow if can't parse
    
    def _generate_cache_key(self, source_name: str, endpoints: List[str]) -> str:
        """Generate cache key for source data."""
        key_data = f"{source_name}_{','.join(endpoints)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached data if still valid."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                # Check if cache is still valid (24 hours)
                cached_time = datetime.fromisoformat(cached_data.get('cached_at', ''))
                if datetime.now() - cached_time < timedelta(hours=24):
                    return cached_data.get('data')
                    
            except Exception as e:
                self.logger.warning(f"Error reading cache {cache_key}: {e}")
        
        return None
    
    def _cache_data(self, cache_key: str, data: Dict[str, Any]):
        """Cache data for future use."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
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
            log_entry = f"[{timestamp}] {event_type} GLOBAL_NEEDS_ANALYZER {details}\n"
            
            with open(self.audit_log, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                
        except Exception as e:
            self.logger.error(f"Error logging audit event: {e}")

# CLI interface for testing
if __name__ == "__main__":
    import sys
    
    analyzer = GlobalNeedsAnalyzer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analyze":
            print("Starting global needs analysis...")
            results = analyzer.analyze_global_needs()
            
            print(f"\nFound {len(results)} strategic domains:")
            for i, domain in enumerate(results[:5], 1):
                print(f"{i}. {domain.domain}")
                print(f"   Combined Score: {domain.combined_score:.3f}")
                print(f"   Urgency: {domain.urgency_score:.3f}, Impact: {domain.impact_score:.3f}, Feasibility: {domain.feasibility_score:.3f}")
                print(f"   Evidence: {', '.join(domain.evidence[:2])}")
                print()
        
        else:
            print("Usage: python global_needs_analyzer.py [analyze]")
    else:
        print("Global Needs Analyzer initialized. Use 'analyze' command to start analysis.")
