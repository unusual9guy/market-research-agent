"""
Web Search Utility using Tavily API for market research.
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from tavily import TavilyClient
from config import config

logger = logging.getLogger(__name__)

class WebSearcher:
    """Web searcher utility using Tavily API."""
    
    def __init__(self):
        """Initialize the web searcher with Tavily client."""
        if not config.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is required")
        
        self.client = TavilyClient(api_key=config.TAVILY_API_KEY)
        self.max_results = config.MAX_SEARCH_RESULTS
    
    def search_company_info(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Search for basic company information.
        
        Args:
            company_name: Name of the company to research
            
        Returns:
            List of search results with title, content, and url
        """
        query = f"{company_name} company overview business model industry"
        
        try:
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=self.max_results
            )
            
            return self._format_results(response.get('results', []))
            
        except Exception as e:
            logger.error(f"Error searching company info for {company_name}: {e}")
            return []
    
    def search_competitors(self, company_name: str, industry: str = "") -> List[Dict[str, Any]]:
        """
        Search for company competitors.
        
        Args:
            company_name: Name of the company
            industry: Industry context (optional)
            
        Returns:
            List of search results about competitors
        """
        query = f"{company_name} competitors {industry} market leaders alternatives"
        
        try:
            response = self.client.search(
                query=query,
                search_depth="basic", 
                max_results=self.max_results
            )
            
            return self._format_results(response.get('results', []))
            
        except Exception as e:
            logger.error(f"Error searching competitors for {company_name}: {e}")
            return []
    
    def search_industry_trends(self, industry: str) -> List[Dict[str, Any]]:
        """
        Search for AI/ML trends in a specific industry.
        
        Args:
            industry: Industry to research
            
        Returns:
            List of search results about AI trends
        """
        query = f"{industry} AI artificial intelligence machine learning trends 2024 applications use cases"
        
        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=self.max_results
            )
            
            return self._format_results(response.get('results', []))
            
        except Exception as e:
            logger.error(f"Error searching AI trends for {industry}: {e}")
            return []
    
    def search_ai_use_cases(self, industry: str, company_context: str = "") -> List[Dict[str, Any]]:
        """
        Search for specific AI use cases in an industry.
        
        Args:
            industry: Industry to research
            company_context: Additional company context
            
        Returns:
            List of search results about AI use cases
        """
        query = f"{industry} AI use cases machine learning applications {company_context} examples implementation"
        
        try:
            response = self.client.search(
                query=query,
                search_depth="advanced",
                max_results=self.max_results
            )
            
            return self._format_results(response.get('results', []))
            
        except Exception as e:
            logger.error(f"Error searching AI use cases for {industry}: {e}")
            return []
    
    def search_datasets(self, domain: str, use_case: str = "") -> List[Dict[str, Any]]:
        """
        Search for relevant datasets for a specific domain/use case.
        
        Args:
            domain: Domain or industry
            use_case: Specific use case context
            
        Returns:
            List of search results about datasets
        """
        query = f"{domain} {use_case} dataset kaggle github data machine learning training"
        
        try:
            response = self.client.search(
                query=query,
                search_depth="basic",
                max_results=self.max_results
            )
            
            return self._format_results(response.get('results', []))
            
        except Exception as e:
            logger.error(f"Error searching datasets for {domain}: {e}")
            return []
    
    def _format_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format search results into a consistent structure.
        
        Args:
            results: Raw results from Tavily
            
        Returns:
            Formatted results with title, content, url, and score
        """
        formatted_results = []
        
        for result in results:
            formatted_result = {
                'title': result.get('title', 'No Title'),
                'content': result.get('content', 'No Content'),
                'url': result.get('url', ''),
                'score': result.get('score', 0.0),
                'published_date': result.get('published_date', None)
            }
            formatted_results.append(formatted_result)
        
        # Sort by score (highest first)
        formatted_results.sort(key=lambda x: x['score'], reverse=True)
        
        return formatted_results
    
    def get_search_summary(self, results: List[Dict[str, Any]]) -> str:
        """
        Create a summary of search results for LLM processing.
        
        Args:
            results: Formatted search results
            
        Returns:
            Combined text summary of all results
        """
        if not results:
            return "No search results found."
        
        summary_parts = []
        for i, result in enumerate(results[:5], 1):  # Limit to top 5 results
            summary_parts.append(f"""
Result {i}:
Title: {result['title']}
Content: {result['content'][:500]}...
URL: {result['url']}
""")
        
        return "\n".join(summary_parts)
