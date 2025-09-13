"""
Enhanced Industry Research Agent with deeper market analysis.
"""
import logging
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages import HumanMessage, SystemMessage
from utils.web_searcher import WebSearcher  # Back to Tavily for better sources
from config import config
import json

logger = logging.getLogger(__name__)

class EnhancedIndustryResearchAgent:
    """Agent for comprehensive industry and competitive analysis."""
    
    def __init__(self):

        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        # setting the model 
        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            api_key=config.OPENAI_API_KEY,
            temperature=0.2  # More focused for research
        )
        self.web_searcher = WebSearcher()  # Using Tavily for better source quality
        
    def conduct_deep_research(self, company_name: str) -> Dict[str, Any]:
        """
        Conduct comprehensive, evaluation-ready research.
        
        Args:
            company_name: Name of the company to research
            
        Returns:
            Deep research report with competitive analysis
        """
        logger.info(f"Starting deep research for: {company_name}")
        
        try:
            # Phase 1: Company Foundation Research
            company_results = self.web_searcher.search_company_info(company_name)
            company_analysis = self._analyze_company_foundation(company_name, company_results)
            
            # Phase 2: Market Position & Size Analysis
            market_results = self._search_market_data(company_name, company_analysis.get('industry', ''))
            market_analysis = self._analyze_market_position(company_name, market_results)
            
            # Phase 3: Deep Competitive Intelligence
            competitor_results = self._search_competitive_landscape(company_name, company_analysis.get('industry', ''))
            competitive_analysis = self._analyze_competitive_landscape(company_name, competitor_results)
            
            # Phase 4: Innovation & Technology Analysis
            tech_results = self._search_technology_landscape(company_name, company_analysis.get('industry', ''))
            tech_analysis = self._analyze_technology_position(company_name, tech_results)
            
            # Phase 5: Strategic Analysis
            strategic_analysis = self._conduct_strategic_analysis(
                company_analysis, market_analysis, competitive_analysis, tech_analysis
            )
            
            # Compile comprehensive report
            deep_research_report = {
                'company_name': company_name,
                'research_depth': 'comprehensive',
                'company_foundation': company_analysis,
                'market_analysis': market_analysis,
                'competitive_intelligence': competitive_analysis,
                'technology_landscape': tech_analysis,
                'strategic_insights': strategic_analysis,
                'research_sources': {
                    'company_sources': company_results[:5],
                    'market_sources': market_results[:5],
                    'competitive_sources': competitor_results[:5],
                    'technology_sources': tech_results[:5]
                },
                'agent': 'EnhancedIndustryResearchAgent',
                'status': 'completed'
            }
            
            logger.info(f"Deep research completed for {company_name}")
            return deep_research_report
            
        except Exception as e:
            logger.error(f"Error in deep research for {company_name}: {e}")
            return {
                'company_name': company_name,
                'error': str(e),
                'agent': 'EnhancedIndustryResearchAgent',
                'status': 'failed'
            }
    
    def _search_market_data(self, company_name: str, industry: str) -> List[Dict[str, Any]]:
        """Search for market size, trends, and positioning data."""
        queries = [
            f"{industry} market size revenue growth 2024 trends",
            f"{company_name} market share position revenue competitors",
            f"{industry} industry analysis competitive landscape 2024"
        ]
        
        all_results = []
        for query in queries:
            try:
                response = self.web_searcher.client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=5
                )
                results = self.web_searcher._format_results(response.get('results', []))
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Error searching market data: {e}")
        
        return all_results[:15]  # Top 15 market results
    
    def _search_competitive_landscape(self, company_name: str, industry: str) -> List[Dict[str, Any]]:
        """Search for detailed competitive intelligence."""
        queries = [
            f"{company_name} vs competitors comparison analysis 2024",
            f"{industry} competitive analysis market leaders",
            f"{company_name} competitive advantages differentiators",
            f"{industry} emerging competitors disruptors new entrants"
        ]
        
        all_results = []
        for query in queries:
            try:
                response = self.web_searcher.client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=4
                )
                results = self.web_searcher._format_results(response.get('results', []))
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Error searching competitive landscape: {e}")
        
        return all_results[:16]  # Top 16 competitive results
    
    def _search_technology_landscape(self, company_name: str, industry: str) -> List[Dict[str, Any]]:
        """Search for technology adoption and innovation trends."""
        queries = [
            f"{company_name} technology stack innovation AI adoption",
            f"{industry} digital transformation technology trends 2024",
            f"{company_name} research development innovation investments",
            f"{industry} emerging technologies AI machine learning adoption"
        ]
        
        all_results = []
        for query in queries:
            try:
                response = self.web_searcher.client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=4
                )
                results = self.web_searcher._format_results(response.get('results', []))
                all_results.extend(results)
            except Exception as e:
                logger.error(f"Error searching technology landscape: {e}")
        
        return all_results[:16]  # Top 16 technology results
    
    def _analyze_company_foundation(self, company_name: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Deep analysis of company fundamentals."""
        search_summary = self.web_searcher.get_search_summary(search_results)
        
        system_prompt = """You are a senior business analyst conducting deep company research. 
        
        Analyze the company comprehensively, focusing on:
        1. Business model and revenue streams
        2. Core value propositions and competitive advantages  
        3. Market position and customer segments
        4. Financial performance and growth trajectory
        5. Geographic presence and expansion strategy
        6. Recent strategic initiatives and partnerships
        
        Provide detailed, insightful analysis that demonstrates deep market understanding."""
        
        user_prompt = f"""
        Conduct comprehensive analysis of {company_name} based on this research:
        
        {search_summary}
        
        Provide detailed analysis covering:
        - **Business Model**: Revenue streams, cost structure, key partnerships
        - **Value Proposition**: Core offerings and competitive advantages
        - **Market Position**: Size, growth, customer segments served
        - **Financial Health**: Revenue trends, profitability, key metrics
        - **Geographic Footprint**: Markets served and expansion plans
        - **Strategic Direction**: Recent initiatives, investments, partnerships
        - **Key Success Factors**: What drives their competitive advantage
        """
        
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = self.llm.invoke(messages)
            return self._parse_structured_analysis(response.content, "company_foundation")
        except Exception as e:
            logger.error(f"Error analyzing company foundation: {e}")
            return {'error': str(e), 'raw_analysis': search_summary}
    
    def _analyze_market_position(self, company_name: str, market_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze market dynamics and positioning."""
        market_summary = self.web_searcher.get_search_summary(market_results)
        
        system_prompt = """You are a market research expert analyzing industry dynamics and competitive positioning.
        
        Focus on quantitative and qualitative market insights including:
        1. Market size, growth rates, and trends
        2. Market segmentation and customer behavior
        3. Competitive positioning and market share
        4. Industry drivers and challenges
        5. Regulatory environment and barriers to entry
        6. Future market projections and opportunities"""
        
        user_prompt = f"""
        Analyze the market position of {company_name} based on this market research:
        
        {market_summary}
        
        Provide detailed market analysis covering:
        - **Market Size & Growth**: Current size, growth rate, projected trends
        - **Market Segments**: Key customer segments and their characteristics
        - **Competitive Position**: Market share, ranking vs competitors
        - **Market Drivers**: Key factors driving industry growth
        - **Industry Challenges**: Headwinds and potential disruptions
        - **Regulatory Environment**: Compliance requirements and policy impacts
        - **Market Opportunities**: Untapped segments and growth vectors
        """
        
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = self.llm.invoke(messages)
            return self._parse_structured_analysis(response.content, "market_analysis")
        except Exception as e:
            logger.error(f"Error analyzing market position: {e}")
            return {'error': str(e), 'raw_analysis': market_summary}
    
    def _analyze_competitive_landscape(self, company_name: str, competitive_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Deep competitive intelligence analysis."""
        competitive_summary = self.web_searcher.get_search_summary(competitive_results)
        
        system_prompt = """You are a competitive intelligence analyst providing strategic insights.
        
        Conduct thorough competitive analysis including:
        1. Direct and indirect competitor identification
        2. Competitive positioning and differentiation
        3. Competitive advantages and vulnerabilities
        4. Strategic moves and competitive responses
        5. Emerging threats and disruptors
        6. Competitive dynamics and market share shifts"""
        
        user_prompt = f"""
        Analyze the competitive landscape for {company_name} based on this intelligence:
        
        {competitive_summary}
        
        Provide comprehensive competitive analysis covering:
        - **Direct Competitors**: Main competitors with business model overlap
        - **Indirect Competitors**: Alternative solutions and substitutes
        - **Competitive Positioning**: How {company_name} differentiates itself
        - **Competitive Advantages**: Sustainable competitive moats
        - **Competitive Vulnerabilities**: Areas where competitors excel
        - **Emerging Threats**: New entrants and disruptive technologies
        - **Competitive Dynamics**: Recent strategic moves and market reactions
        - **Market Share Trends**: Share gains/losses and underlying drivers
        """
        
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = self.llm.invoke(messages)
            return self._parse_structured_analysis(response.content, "competitive_analysis")
        except Exception as e:
            logger.error(f"Error analyzing competitive landscape: {e}")
            return {'error': str(e), 'raw_analysis': competitive_summary}
    
    def _analyze_technology_position(self, company_name: str, tech_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze technology adoption and innovation capabilities."""
        tech_summary = self.web_searcher.get_search_summary(tech_results)
        
        system_prompt = """You are a technology analyst specializing in digital transformation and innovation.
        
        Evaluate technology capabilities and innovation potential including:
        1. Current technology stack and digital maturity
        2. Innovation investments and R&D capabilities
        3. Technology partnerships and ecosystem
        4. Digital transformation initiatives
        5. Emerging technology adoption readiness
        6. Technology-driven competitive advantages"""
        
        user_prompt = f"""
        Analyze the technology landscape and innovation position of {company_name}:
        
        {tech_summary}
        
        Provide technology analysis covering:
        - **Technology Stack**: Current systems, platforms, and capabilities
        - **Digital Maturity**: Level of digital transformation and sophistication
        - **Innovation Capabilities**: R&D investments, innovation processes
        - **Technology Partnerships**: Key tech alliances and ecosystem relationships
        - **Emerging Tech Adoption**: AI, ML, cloud, automation adoption status
        - **Technology Competitive Advantages**: Tech-driven differentiation
        - **Innovation Gaps**: Areas lacking technological advancement
        - **Future Technology Roadmap**: Planned technology investments and initiatives
        """
        
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = self.llm.invoke(messages)
            return self._parse_structured_analysis(response.content, "technology_analysis")
        except Exception as e:
            logger.error(f"Error analyzing technology position: {e}")
            return {'error': str(e), 'raw_analysis': tech_summary}
    
    def _conduct_strategic_analysis(
        self, 
        company_analysis: Dict[str, Any], 
        market_analysis: Dict[str, Any], 
        competitive_analysis: Dict[str, Any], 
        tech_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize insights into strategic recommendations."""
        
        system_prompt = """You are a senior strategy consultant providing executive-level insights.
        
        Synthesize the research into strategic insights including:
        1. SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
        2. Strategic priorities and recommendations
        3. Growth opportunities and expansion vectors
        4. Risk assessment and mitigation strategies
        5. Innovation imperatives and technology roadmap
        6. Competitive response strategies"""
        
        combined_analysis = f"""
        COMPANY FOUNDATION:
        {str(company_analysis)}
        
        MARKET ANALYSIS:
        {str(market_analysis)}
        
        COMPETITIVE ANALYSIS:
        {str(competitive_analysis)}
        
        TECHNOLOGY ANALYSIS:
        {str(tech_analysis)}
        """
        
        user_prompt = f"""
        Based on the comprehensive research above, provide strategic insights covering:
        
        - **SWOT Analysis**: Strengths, Weaknesses, Opportunities, Threats
        - **Strategic Priorities**: Top 3-5 strategic imperatives for the next 2-3 years
        - **Growth Opportunities**: Specific expansion vectors and market opportunities
        - **Risk Assessment**: Key risks and mitigation strategies
        - **Innovation Roadmap**: Technology and innovation investment priorities
        - **Competitive Strategy**: How to maintain and strengthen competitive position
        - **Success Metrics**: Key performance indicators to track strategic progress
        """
        
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = self.llm.invoke(messages)
            return self._parse_structured_analysis(response.content, "strategic_analysis")
        except Exception as e:
            logger.error(f"Error conducting strategic analysis: {e}")
            return {'error': str(e)}
    
    def _parse_structured_analysis(self, response_content: str, analysis_type: str) -> Dict[str, Any]:
        """Parse LLM response into structured analysis."""
        try:
            # For now, return structured content with raw analysis
            # In production, you'd implement more sophisticated parsing
            return {
                'analysis_type': analysis_type,
                'structured_content': response_content,
                'key_insights': self._extract_key_insights(response_content),
                'confidence_score': 0.85  # Placeholder - could implement confidence scoring
            }
        except Exception as e:
            logger.error(f"Error parsing {analysis_type}: {e}")
            return {
                'analysis_type': analysis_type,
                'raw_content': response_content,
                'parse_error': str(e)
            }
    
    def _extract_key_insights(self, content: str) -> List[str]:
        """Extract key insights from analysis content."""
        # Simple extraction - look for bullet points and key phrases
        insights = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if (line.startswith('-') or line.startswith('•') or 
                'key' in line.lower() or 'important' in line.lower() or
                'critical' in line.lower() or 'significant' in line.lower()):
                if len(line) > 20:  # Filter out short lines
                    insights.append(line)
        
        return insights[:10]  # Top 10 insights
    
    def get_executive_summary(self, research_report: Dict[str, Any]) -> str:
        """Generate executive summary of deep research."""
        if research_report.get('status') == 'failed':
            return f"Research failed for {research_report.get('company_name', 'Unknown')}: {research_report.get('error', 'Unknown error')}"
        
        company_name = research_report.get('company_name', 'Unknown Company')
        
        summary = f"""
# Executive Summary: {company_name} Market Research

## Company Foundation
{research_report.get('company_foundation', {}).get('structured_content', 'Analysis pending')[:300]}...

## Market Position  
{research_report.get('market_analysis', {}).get('structured_content', 'Analysis pending')[:300]}...

## Competitive Landscape
{research_report.get('competitive_intelligence', {}).get('structured_content', 'Analysis pending')[:300]}...

## Technology Position
{research_report.get('technology_landscape', {}).get('structured_content', 'Analysis pending')[:300]}...

## Strategic Insights
{research_report.get('strategic_insights', {}).get('structured_content', 'Analysis pending')[:300]}...

## Research Sources
- Company Sources: {len(research_report.get('research_sources', {}).get('company_sources', []))}
- Market Sources: {len(research_report.get('research_sources', {}).get('market_sources', []))}
- Competitive Sources: {len(research_report.get('research_sources', {}).get('competitive_sources', []))}
- Technology Sources: {len(research_report.get('research_sources', {}).get('technology_sources', []))}
"""
        
        return summary.strip()
