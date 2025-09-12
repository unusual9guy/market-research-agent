"""
Use Case Generation Agent - Generates AI/ML use cases based on industry research.
"""
import logging
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from utils.web_searcher import WebSearcher
from config import config

logger = logging.getLogger(__name__)

class UseCaseGenerationAgent:
    """Agent responsible for generating relevant AI/ML use cases for companies/industries."""
    
    def __init__(self):
        """Initialize the Use Case Generation Agent."""
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        
        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            api_key=config.OPENAI_API_KEY,
            temperature=0.4  # Slightly more creative for use case generation
        )
        self.web_searcher = WebSearcher()
        
    def generate_use_cases(self, company_research: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate AI/ML use cases based on company research data.
        
        Args:
            company_research: Research data from Industry Research Agent
            
        Returns:
            Dictionary containing generated use cases with references
        """
        logger.info(f"Generating AI use cases for {company_research.get('company_name', 'Unknown')}")
        
        try:
            company_name = company_research.get('company_name', 'Unknown Company')
            company_analysis = company_research.get('company_analysis', {})
            industry = company_analysis.get('industry', 'Unknown')
            
            # Step 1: Search for AI trends in the industry
            ai_trends = self.web_searcher.search_industry_trends(industry)
            
            # Step 2: Search for specific AI use cases in the industry
            use_case_research = self.web_searcher.search_ai_use_cases(
                industry, 
                company_analysis.get('company_description', '')
            )
            
            # Step 3: Generate contextual use cases using LLM
            use_cases = self._generate_contextual_use_cases(
                company_research, 
                ai_trends, 
                use_case_research
            )
            
            # Step 4: Add references and validate use cases
            validated_use_cases = self._add_references_and_validate(use_cases, ai_trends, use_case_research)
            
            # Step 5: Compile final report
            use_case_report = {
                'company_name': company_name,
                'industry': industry,
                'use_cases': validated_use_cases,
                'industry_trends': self._summarize_trends(ai_trends),
                'research_sources': {
                    'ai_trends_sources': ai_trends[:3],  # Top 3 trend sources
                    'use_case_sources': use_case_research[:3]  # Top 3 use case sources
                },
                'agent': 'UseCaseGenerationAgent',
                'status': 'completed'
            }
            
            logger.info(f"Generated {len(validated_use_cases)} use cases for {company_name}")
            return use_case_report
            
        except Exception as e:
            logger.error(f"Error generating use cases: {e}")
            return {
                'company_name': company_research.get('company_name', 'Unknown'),
                'error': str(e),
                'agent': 'UseCaseGenerationAgent',
                'status': 'failed'
            }
    
    def _generate_contextual_use_cases(
        self, 
        company_research: Dict[str, Any], 
        ai_trends: List[Dict[str, Any]], 
        use_case_research: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate contextual AI use cases using LLM analysis.
        
        Args:
            company_research: Company background data
            ai_trends: Industry AI trend data
            use_case_research: Existing AI use case examples
            
        Returns:
            List of generated use cases
        """
        company_name = company_research.get('company_name', 'Unknown')
        company_analysis = company_research.get('company_analysis', {})
        industry = company_analysis.get('industry', 'Unknown')
        
        # Prepare context for LLM
        company_context = f"""
Company: {company_name}
Industry: {industry}
Description: {company_analysis.get('company_description', 'N/A')}
Key Products/Services: {company_analysis.get('key_products_services', 'N/A')}
Market Position: {company_analysis.get('market_position', 'N/A')}
"""
        
        trends_summary = self.web_searcher.get_search_summary(ai_trends)
        use_cases_summary = self.web_searcher.get_search_summary(use_case_research)
        
        system_prompt = """You are an expert AI consultant specializing in identifying practical AI/ML applications for businesses. 

Your task is to generate exactly 5 specific, actionable AI/ML use cases that are:
1. Directly relevant to the company's industry and business model
2. Technically feasible with current AI/ML technologies
3. Aligned with industry trends and best practices
4. Focused on solving real business problems or creating value

For each use case, provide:
- Use case name (concise, descriptive)
- Business problem it solves
- AI/ML approach (specific techniques/technologies)
- Expected business impact
- Implementation complexity (Low/Medium/High)

Base your recommendations on the provided company context and industry research."""

        user_prompt = f"""
Generate 5 AI/ML use cases for the following company:

{company_context}

Consider these industry AI trends:
{trends_summary}

And these existing AI use case examples in similar industries:
{use_cases_summary}

Provide 5 specific, actionable AI/ML use cases that would be valuable for {company_name}. 
Each use case should be tailored to their specific business context and industry.

Format each use case as:
**Use Case [Number]: [Name]**
- **Problem:** [Business problem being solved]
- **AI/ML Approach:** [Specific technologies/techniques]
- **Business Impact:** [Expected value/benefits]
- **Complexity:** [Low/Medium/High]
- **Industry Relevance:** [Why this is relevant to their industry]
"""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse the response into structured use cases
            use_cases = self._parse_use_cases(response.content)
            
            return use_cases
            
        except Exception as e:
            logger.error(f"Error generating contextual use cases: {e}")
            return []
    
    def _parse_use_cases(self, response_content: str) -> List[Dict[str, Any]]:
        """
        Parse LLM response into structured use cases.
        
        Args:
            response_content: Raw response from LLM
            
        Returns:
            List of structured use case dictionaries
        """
        use_cases = []
        
        try:
            # Split response by use case headers
            lines = response_content.split('\n')
            current_use_case = {}
            current_field = None
            
            for line in lines:
                line = line.strip()
                
                # Check for use case header
                if line.startswith('**Use Case') and ':' in line:
                    # Save previous use case if exists
                    if current_use_case:
                        use_cases.append(current_use_case)
                    
                    # Start new use case
                    use_case_title = line.replace('**', '').replace('Use Case ', '').strip()
                    current_use_case = {
                        'title': use_case_title,
                        'problem': '',
                        'ai_approach': '',
                        'business_impact': '',
                        'complexity': '',
                        'industry_relevance': '',
                        'raw_content': ''
                    }
                    current_field = None
                
                # Check for field headers
                elif line.startswith('- **') and current_use_case:
                    if 'Problem:' in line:
                        current_field = 'problem'
                        current_use_case['problem'] = line.split(':', 1)[1].strip() if ':' in line else ''
                    elif 'AI/ML Approach:' in line:
                        current_field = 'ai_approach'
                        current_use_case['ai_approach'] = line.split(':', 1)[1].strip() if ':' in line else ''
                    elif 'Business Impact:' in line:
                        current_field = 'business_impact'
                        current_use_case['business_impact'] = line.split(':', 1)[1].strip() if ':' in line else ''
                    elif 'Complexity:' in line:
                        current_field = 'complexity'
                        current_use_case['complexity'] = line.split(':', 1)[1].strip() if ':' in line else ''
                    elif 'Industry Relevance:' in line:
                        current_field = 'industry_relevance'
                        current_use_case['industry_relevance'] = line.split(':', 1)[1].strip() if ':' in line else ''
                    else:
                        current_field = None
                
                # Add content to current field
                elif line and current_field and current_use_case:
                    if current_use_case[current_field]:
                        current_use_case[current_field] += ' ' + line
                    else:
                        current_use_case[current_field] = line
                
                # Add to raw content
                if current_use_case:
                    current_use_case['raw_content'] += line + '\n'
            
            # Add the last use case
            if current_use_case:
                use_cases.append(current_use_case)
            
            # Ensure we have exactly 5 use cases or create fallback
            if len(use_cases) < 5:
                logger.warning(f"Only parsed {len(use_cases)} use cases, expected 5")
                # Add the raw response as fallback
                for i in range(len(use_cases), 5):
                    use_cases.append({
                        'title': f"Use Case {i+1}: Analysis Required",
                        'problem': 'See raw analysis for details',
                        'ai_approach': 'Multiple approaches possible',
                        'business_impact': 'Significant potential impact',
                        'complexity': 'Medium',
                        'industry_relevance': 'Industry-specific application',
                        'raw_content': response_content
                    })
            
            return use_cases[:5]  # Ensure exactly 5 use cases
            
        except Exception as e:
            logger.error(f"Error parsing use cases: {e}")
            # Return fallback structure
            return [{
                'title': f"Use Case {i+1}: Parsing Error",
                'problem': 'Use case parsing failed',
                'ai_approach': 'See raw analysis',
                'business_impact': 'Potential value identified',
                'complexity': 'Medium',
                'industry_relevance': 'Industry-relevant',
                'raw_content': response_content,
                'parse_error': str(e)
            } for i in range(5)]
    
    def _add_references_and_validate(
        self, 
        use_cases: List[Dict[str, Any]], 
        ai_trends: List[Dict[str, Any]], 
        use_case_research: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Add references and validate use cases.
        
        Args:
            use_cases: Generated use cases
            ai_trends: AI trend research results
            use_case_research: Use case research results
            
        Returns:
            Enhanced use cases with references
        """
        enhanced_use_cases = []
        
        for i, use_case in enumerate(use_cases):
            enhanced_use_case = use_case.copy()
            
            # Add references from research
            references = []
            
            # Add relevant trend sources
            if i < len(ai_trends):
                trend_source = ai_trends[i]
                references.append({
                    'type': 'industry_trend',
                    'title': trend_source.get('title', 'Industry Trend Analysis'),
                    'url': trend_source.get('url', ''),
                    'relevance': 'Industry AI trends and applications'
                })
            
            # Add relevant use case sources
            if i < len(use_case_research):
                case_source = use_case_research[i]
                references.append({
                    'type': 'use_case_example',
                    'title': case_source.get('title', 'AI Use Case Example'),
                    'url': case_source.get('url', ''),
                    'relevance': 'Similar industry implementation'
                })
            
            # Add fallback reference if no specific sources
            if not references and (ai_trends or use_case_research):
                fallback_source = (ai_trends + use_case_research)[0]
                references.append({
                    'type': 'general_research',
                    'title': fallback_source.get('title', 'Industry Research'),
                    'url': fallback_source.get('url', ''),
                    'relevance': 'Supporting industry research'
                })
            
            enhanced_use_case['references'] = references
            enhanced_use_case['validation_score'] = self._calculate_validation_score(use_case)
            
            enhanced_use_cases.append(enhanced_use_case)
        
        return enhanced_use_cases
    
    def _calculate_validation_score(self, use_case: Dict[str, Any]) -> float:
        """
        Calculate a simple validation score for the use case.
        
        Args:
            use_case: Use case data
            
        Returns:
            Validation score between 0.0 and 1.0
        """
        score = 0.0
        
        # Check completeness of fields
        required_fields = ['title', 'problem', 'ai_approach', 'business_impact']
        completed_fields = sum(1 for field in required_fields if use_case.get(field, '').strip())
        score += (completed_fields / len(required_fields)) * 0.5
        
        # Check content quality (basic length check)
        if len(use_case.get('problem', '')) > 50:
            score += 0.2
        if len(use_case.get('ai_approach', '')) > 30:
            score += 0.2
        if len(use_case.get('business_impact', '')) > 30:
            score += 0.1
        
        return min(score, 1.0)
    
    def _summarize_trends(self, ai_trends: List[Dict[str, Any]]) -> str:
        """
        Summarize AI trends for the report.
        
        Args:
            ai_trends: AI trend research results
            
        Returns:
            Summary of key AI trends
        """
        if not ai_trends:
            return "No specific AI trends identified for this industry."
        
        trend_summary = "Key AI trends in this industry:\n"
        for i, trend in enumerate(ai_trends[:3], 1):
            trend_summary += f"{i}. {trend.get('title', 'Trend Analysis')}\n"
            trend_summary += f"   {trend.get('content', 'No details available')[:200]}...\n\n"
        
        return trend_summary.strip()
    
    def get_summary(self, use_case_report: Dict[str, Any]) -> str:
        """
        Generate a concise summary of the use case report.
        
        Args:
            use_case_report: Complete use case report
            
        Returns:
            Text summary of generated use cases
        """
        if use_case_report.get('status') == 'failed':
            return f"Use case generation failed for {use_case_report.get('company_name', 'Unknown')}: {use_case_report.get('error', 'Unknown error')}"
        
        company_name = use_case_report.get('company_name', 'Unknown Company')
        industry = use_case_report.get('industry', 'Unknown')
        use_cases = use_case_report.get('use_cases', [])
        
        summary = f"""
**AI/ML Use Cases for {company_name}**

**Industry:** {industry}
**Generated Use Cases:** {len(use_cases)}

"""
        
        for i, use_case in enumerate(use_cases, 1):
            summary += f"""
**{i}. {use_case.get('title', f'Use Case {i}')}**
Problem: {use_case.get('problem', 'Not specified')[:100]}...
Approach: {use_case.get('ai_approach', 'Not specified')[:100]}...
Impact: {use_case.get('business_impact', 'Not specified')[:100]}...
Complexity: {use_case.get('complexity', 'Unknown')}
References: {len(use_case.get('references', []))} sources

"""
        
        return summary.strip()
