"""
Exa Search Utility for high-quality, recent web content.
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from exa_py import Exa
from config import config

logger = logging.getLogger(__name__)

class ExaSearcher:
    """Exa searcher utility for high-quality, recent content."""
    
    def __init__(self):
        """Initialize the Exa searcher."""
        # Get API key from config properly
        exa_api_key = config.EXA_API_KEY
        
        if not exa_api_key:
            logger.warning("EXA_API_KEY not found in environment variables")
            self.client = None
            self.max_results = config.MAX_SEARCH_RESULTS
            return
        
        try:
            self.client = Exa(api_key=exa_api_key)
            self.max_results = config.MAX_SEARCH_RESULTS
            logger.info("Exa client initialized successfully")
        except Exception as e:
            logger.error(f"Exa client initialization failed: {e}")
            self.client = None
    
    def search_company_info(self, company_name: str) -> List[Dict[str, Any]]:
        """
        Search for recent company information using Exa.
        
        Args:
            company_name: Name of the company to research
            
        Returns:
            List of search results with title, content, and url
        """
        if not self.client:
            return []
        
        query = f"{company_name} company business model recent developments 2024"
        
        try:
            # Search for recent, high-quality content
            response = self.client.search_and_contents(
                query=query,
                num_results=self.max_results,
                text=True,
                start_published_date=(datetime.now() - timedelta(days=365)).isoformat(),  # Last year
                use_autoprompt=True,  # Let Exa optimize the query
                type="neural"  # Use neural search for better relevance
            )
            
            return self._format_exa_results(response.results)
            
        except Exception as e:
            logger.error(f"Error searching company info with Exa for {company_name}: {e}")
            return []
    
    def search_competitors(self, company_name: str, industry: str = "") -> List[Dict[str, Any]]:
        """
        Search for company competitors using Exa.
        
        Args:
            company_name: Name of the company
            industry: Industry context (optional)
            
        Returns:
            List of search results about competitors
        """
        if not self.client:
            return []
        
        query = f"{company_name} competitors {industry} market analysis competitive landscape 2024"
        
        try:
            response = self.client.search_and_contents(
                query=query,
                num_results=self.max_results,
                text=True,
                start_published_date=(datetime.now() - timedelta(days=365)).isoformat(),
                use_autoprompt=True,
                type="neural"
            )
            
            return self._format_exa_results(response.results)
            
        except Exception as e:
            logger.error(f"Error searching competitors with Exa for {company_name}: {e}")
            return []
    
    def search_industry_trends(self, industry: str) -> List[Dict[str, Any]]:
        """
        Search for recent AI/ML trends in a specific industry.
        
        Args:
            industry: Industry to research
            
        Returns:
            List of search results about AI trends
        """
        if not self.client:
            return []
        
        query = f"{industry} artificial intelligence machine learning trends 2024 latest developments applications"
        
        try:
            response = self.client.search_and_contents(
                query=query,
                num_results=self.max_results,
                text=True,
                start_published_date=(datetime.now() - timedelta(days=180)).isoformat(),  # Last 6 months
                use_autoprompt=True,
                type="neural"
            )
            
            return self._format_exa_results(response.results)
            
        except Exception as e:
            logger.error(f"Error searching AI trends with Exa for {industry}: {e}")
            return []
    
    def search_ai_use_cases(self, industry: str, company_context: str = "") -> List[Dict[str, Any]]:
        """
        Search for specific, recent AI use cases in an industry.
        
        Args:
            industry: Industry to research
            company_context: Additional company context
            
        Returns:
            List of search results about AI use cases
        """
        if not self.client:
            return []
        
        query = f"{industry} AI use cases 2024 machine learning applications {company_context} implementation examples"
        
        try:
            response = self.client.search_and_contents(
                query=query,
                num_results=self.max_results,
                text=True,
                start_published_date=(datetime.now() - timedelta(days=365)).isoformat(),
                use_autoprompt=True,
                type="neural"
            )
            
            return self._format_exa_results(response.results)
            
        except Exception as e:
            logger.error(f"Error searching AI use cases with Exa for {industry}: {e}")
            return []
    
    def search_current_capabilities(self, company_name: str, domain: str = "") -> List[Dict[str, Any]]:
        """
        Search for a company's current AI/tech capabilities to avoid suggesting existing solutions.
        
        Args:
            company_name: Name of the company
            domain: Specific domain (e.g., "AI", "machine learning", "recommendation systems")
            
        Returns:
            List of search results about current capabilities
        """
        if not self.client:
            return []
        
        query = f"{company_name} current {domain} technology capabilities AI systems 2024 what they already have"
        
        try:
            response = self.client.search_and_contents(
                query=query,
                num_results=self.max_results,
                text=True,
                start_published_date=(datetime.now() - timedelta(days=365)).isoformat(),
                use_autoprompt=True,
                type="neural"
            )
            
            return self._format_exa_results(response.results)
            
        except Exception as e:
            logger.error(f"Error searching current capabilities with Exa for {company_name}: {e}")
            return []
    
    def search_innovation_opportunities(self, industry: str, company_name: str = "") -> List[Dict[str, Any]]:
        """
        Search for emerging technologies and innovation opportunities.
        
        Args:
            industry: Industry to research
            company_name: Company context (optional)
            
        Returns:
            List of search results about innovation opportunities
        """
        if not self.client:
            return []
        
        query = f"{industry} emerging AI technologies 2024 innovation opportunities {company_name} future trends"
        
        try:
            response = self.client.search_and_contents(
                query=query,
                num_results=self.max_results,
                text=True,
                start_published_date=(datetime.now() - timedelta(days=180)).isoformat(),
                use_autoprompt=True,
                type="neural"
            )
            
            return self._format_exa_results(response.results)
            
        except Exception as e:
            logger.error(f"Error searching innovation opportunities with Exa: {e}")
            return []
    
    def _format_exa_results(self, results) -> List[Dict[str, Any]]:
        """
        Format Exa search results into a consistent structure.
        
        Args:
            results: Raw results from Exa
            
        Returns:
            Formatted results with title, content, url, and metadata
        """
        formatted_results = []
        
        for result in results:
            formatted_result = {
                'title': getattr(result, 'title', 'No Title'),
                'content': getattr(result, 'text', 'No Content'),
                'url': getattr(result, 'url', ''),
                'score': getattr(result, 'score', 0.0),
                'published_date': getattr(result, 'published_date', None),
                'author': getattr(result, 'author', None),
                'source': 'Exa'
            }
            formatted_results.append(formatted_result)
        
        # Results from Exa are already ranked by relevance
        return formatted_results
    
    def get_search_summary(self, results: List[Dict[str, Any]]) -> str:
        """
        Create a summary of Exa search results for LLM processing.
        
        Args:
            results: Formatted search results
            
        Returns:
            Combined text summary of all results
        """
        if not results:
            return "No search results found from Exa."
        
        summary_parts = []
        for i, result in enumerate(results[:5], 1):  # Limit to top 5 results
            published_date = result.get('published_date', 'Date unknown')
            author = result.get('author', 'Author unknown')
            
            summary_parts.append(f"""
Result {i} (Exa):
Title: {result['title']}
Author: {author}
Published: {published_date}
Content: {result['content'][:600]}...
URL: {result['url']}
""")
        
        return "\n".join(summary_parts)
    
    def is_available(self) -> bool:
        """Check if Exa client is available."""
        return self.client is not None
