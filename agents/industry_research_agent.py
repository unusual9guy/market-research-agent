"""
Industry Research Agent - Gathers company and industry background information.
"""
import logging
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from utils.web_searcher import WebSearcher
from config import config

logger = logging.getLogger(__name__)

class IndustryResearchAgent:
    """Agent responsible for gathering company and industry background data."""
    
    def __init__(self):
        """Initialize the Industry Research Agent."""
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        
        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            api_key=config.OPENAI_API_KEY,
            temperature=0.3
        )
        self.web_searcher = WebSearcher()
        
    def research_company(self, company_name: str) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a company.
        
        Args:
            company_name: Name of the company to research
            
        Returns:
            Dictionary containing company research results
        """
        logger.info(f"Starting research for company: {company_name}")
        
        try:
            # Step 1: Search for company information
            company_results = self.web_searcher.search_company_info(company_name)
            
            # Step 2: Extract key information using LLM
            company_analysis = self._analyze_company_info(company_name, company_results)
            
            # Step 3: Search for competitors
            industry = company_analysis.get('industry', '')
            competitor_results = self.web_searcher.search_competitors(company_name, industry)
            
            # Step 4: Analyze competitors
            competitor_analysis = self._analyze_competitors(company_name, competitor_results)
            
            # Step 5: Compile final report
            research_report = {
                'company_name': company_name,
                'company_analysis': company_analysis,
                'competitor_analysis': competitor_analysis,
                'raw_sources': {
                    'company_sources': company_results[:3],  # Top 3 sources
                    'competitor_sources': competitor_results[:3]
                },
                'agent': 'IndustryResearchAgent',
                'status': 'completed'
            }
            
            logger.info(f"Research completed for {company_name}")
            return research_report
            
        except Exception as e:
            logger.error(f"Error in company research for {company_name}: {e}")
            return {
                'company_name': company_name,
                'error': str(e),
                'agent': 'IndustryResearchAgent',
                'status': 'failed'
            }
    
    def _analyze_company_info(self, company_name: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze company information using LLM.
        
        Args:
            company_name: Name of the company
            search_results: Raw search results from web search
            
        Returns:
            Structured analysis of company information
        """
        search_summary = self.web_searcher.get_search_summary(search_results)
        
        system_prompt = """You are an expert business analyst. Analyze the provided search results about a company and extract key information in a structured format.

Focus on:
1. Company description and core business
2. Industry classification
3. Key products/services
4. Market position and size
5. Recent developments or news
6. Geographic presence

Provide a JSON-like response with clear, concise information. Be factual and cite specific details from the sources."""

        user_prompt = f"""
Analyze the following search results for {company_name}:

{search_summary}

Provide a structured analysis covering:
- company_description (2-3 sentences)
- industry (primary industry)
- key_products_services (list of main offerings)
- market_position (brief description of market standing)
- recent_developments (any notable recent news)
- geographic_presence (main markets/regions)
- key_facts (3-5 important facts about the company)
"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse the response and structure it
            analysis = self._parse_company_analysis(response.content)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing company info: {e}")
            return {
                'company_description': f"Analysis unavailable for {company_name}",
                'industry': 'Unknown',
                'error': str(e)
            }
    
    def _analyze_competitors(self, company_name: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze competitor information using LLM.
        
        Args:
            company_name: Name of the target company
            search_results: Raw search results about competitors
            
        Returns:
            Structured analysis of competitors
        """
        search_summary = self.web_searcher.get_search_summary(search_results)
        
        system_prompt = """You are an expert competitive intelligence analyst. Analyze the provided search results to identify and describe the main competitors of the target company.

Focus on:
1. Direct competitors (similar products/services)
2. Market leaders in the industry
3. Emerging competitors or disruptors
4. Brief description of each competitor's strengths

Provide clear, factual information based only on the search results provided."""

        user_prompt = f"""
Based on the following search results, identify the top 3-5 competitors for {company_name}:

{search_summary}

Provide:
- competitors (list of company names with brief descriptions)
- market_leaders (who are the established leaders)
- competitive_landscape (brief overview of the competitive environment)
- key_differentiators (what makes {company_name} different, if mentioned)
"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse the response and structure it
            analysis = self._parse_competitor_analysis(response.content)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing competitors: {e}")
            return {
                'competitors': [],
                'error': str(e)
            }
    
    def _parse_company_analysis(self, response_content: str) -> Dict[str, Any]:
        """
        Parse LLM response for company analysis.
        
        Args:
            response_content: Raw response from LLM
            
        Returns:
            Structured dictionary with company information
        """
        # Simple parsing - in a production system, you'd want more robust parsing
        try:
            # For now, we'll structure the response as-is
            # In a real implementation, you might use structured output or JSON parsing
            return {
                'company_description': self._extract_section(response_content, 'company_description'),
                'industry': self._extract_section(response_content, 'industry'),
                'key_products_services': self._extract_section(response_content, 'key_products_services'),
                'market_position': self._extract_section(response_content, 'market_position'),
                'recent_developments': self._extract_section(response_content, 'recent_developments'),
                'geographic_presence': self._extract_section(response_content, 'geographic_presence'),
                'key_facts': self._extract_section(response_content, 'key_facts'),
                'raw_analysis': response_content
            }
        except Exception as e:
            logger.error(f"Error parsing company analysis: {e}")
            return {
                'raw_analysis': response_content,
                'parse_error': str(e)
            }
    
    def _parse_competitor_analysis(self, response_content: str) -> Dict[str, Any]:
        """
        Parse LLM response for competitor analysis.
        
        Args:
            response_content: Raw response from LLM
            
        Returns:
            Structured dictionary with competitor information
        """
        try:
            return {
                'competitors': self._extract_section(response_content, 'competitors'),
                'market_leaders': self._extract_section(response_content, 'market_leaders'),
                'competitive_landscape': self._extract_section(response_content, 'competitive_landscape'),
                'key_differentiators': self._extract_section(response_content, 'key_differentiators'),
                'raw_analysis': response_content
            }
        except Exception as e:
            logger.error(f"Error parsing competitor analysis: {e}")
            return {
                'raw_analysis': response_content,
                'parse_error': str(e)
            }
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """
        Extract a specific section from the LLM response.
        
        Args:
            text: Full response text
            section_name: Name of section to extract
            
        Returns:
            Extracted section content or the full text if section not found
        """
        # Simple section extraction - look for section_name followed by content
        lines = text.split('\n')
        section_content = []
        in_section = False
        
        for line in lines:
            if section_name.lower() in line.lower() and ':' in line:
                in_section = True
                # Add the content after the colon
                content_after_colon = line.split(':', 1)[1].strip()
                if content_after_colon:
                    section_content.append(content_after_colon)
            elif in_section and line.strip():
                if any(keyword in line.lower() for keyword in ['company_description', 'industry', 'key_products', 'market_position', 'recent_developments', 'geographic_presence', 'key_facts', 'competitors', 'market_leaders', 'competitive_landscape', 'key_differentiators']):
                    break
                section_content.append(line.strip())
            elif in_section and not line.strip():
                # Empty line might indicate end of section
                continue
        
        return ' '.join(section_content) if section_content else text.strip()
    
    def get_summary(self, research_report: Dict[str, Any]) -> str:
        """
        Generate a concise summary of the research report.
        
        Args:
            research_report: Complete research report
            
        Returns:
            Text summary of key findings
        """
        if research_report.get('status') == 'failed':
            return f"Research failed for {research_report.get('company_name', 'Unknown')}: {research_report.get('error', 'Unknown error')}"
        
        company_name = research_report.get('company_name', 'Unknown Company')
        company_analysis = research_report.get('company_analysis', {})
        competitor_analysis = research_report.get('competitor_analysis', {})
        
        summary = f"""
**Industry Research Summary for {company_name}**

**Company Overview:**
{company_analysis.get('company_description', 'No description available')}

**Industry:** {company_analysis.get('industry', 'Unknown')}

**Key Products/Services:**
{company_analysis.get('key_products_services', 'Not specified')}

**Market Position:**
{company_analysis.get('market_position', 'Not specified')}

**Main Competitors:**
{competitor_analysis.get('competitors', 'Not identified')}

**Sources:** {len(research_report.get('raw_sources', {}).get('company_sources', []))} company sources, {len(research_report.get('raw_sources', {}).get('competitor_sources', []))} competitor sources
"""
        
        return summary.strip()
