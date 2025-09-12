"""
Compare Tavily vs Exa search results side by side.
"""
import logging
from utils.web_searcher import WebSearcher
from utils.exa_searcher import ExaSearcher
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compare_search_results():
    """Compare Tavily and Exa search results for the same queries."""
    
    print("🔍 SEARCH ENGINE COMPARISON: Tavily vs Exa")
    print("=" * 60)
    
    # Initialize searchers
    tavily_searcher = WebSearcher()
    exa_searcher = ExaSearcher()
    
    # Check availability
    tavily_available = config.TAVILY_API_KEY is not None
    exa_available = exa_searcher.is_available()
    
    print(f"Tavily Status: {'✅ Available' if tavily_available else '❌ Not configured'}")
    print(f"Exa Status: {'✅ Available' if exa_available else '❌ Not configured'}")
    
    if not tavily_available:
        print("❌ Tavily API key not found in .env file")
        return
    
    if not exa_available:
        print("⚠️ Exa API key not found or invalid - proceeding with Tavily only")
    
    # Test queries
    test_queries = [
        {
            "company": "Netflix",
            "description": "Current AI capabilities and tech stack"
        },
        {
            "company": "Tesla", 
            "description": "Recent AI innovations and developments"
        }
    ]
    
    for query_info in test_queries:
        company = query_info["company"]
        description = query_info["description"]
        
        print(f"\n{'='*60}")
        print(f"🎯 TESTING: {company} - {description}")
        print(f"{'='*60}")
        
        # Test current capabilities search
        print(f"\n🔍 Query: {company} current AI capabilities 2024")
        print("-" * 50)
        
        # Tavily results
        print("\n📊 TAVILY RESULTS:")
        try:
            tavily_results = tavily_searcher.search_company_info(company)
            display_search_results(tavily_results, "Tavily", max_results=3)
        except Exception as e:
            print(f"❌ Tavily error: {e}")
        
        # Exa results
        if exa_available:
            print("\n🚀 EXA RESULTS:")
            try:
                exa_results = exa_searcher.search_current_capabilities(company, "AI machine learning")
                display_search_results(exa_results, "Exa", max_results=3)
            except Exception as e:
                print(f"❌ Exa error: {e}")
        
        # Compare industry trends
        print(f"\n🔍 Query: {company} industry AI trends 2024")
        print("-" * 50)
        
        # Tavily trends
        print("\n📊 TAVILY AI TRENDS:")
        try:
            industry = "streaming" if company == "Netflix" else "automotive"
            tavily_trends = tavily_searcher.search_industry_trends(industry)
            display_search_results(tavily_trends, "Tavily", max_results=2)
        except Exception as e:
            print(f"❌ Tavily trends error: {e}")
        
        # Exa trends
        if exa_available:
            print("\n🚀 EXA AI TRENDS:")
            try:
                exa_trends = exa_searcher.search_industry_trends(industry)
                display_search_results(exa_trends, "Exa", max_results=2)
            except Exception as e:
                print(f"❌ Exa trends error: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 COMPARISON SUMMARY")
    print(f"{'='*60}")
    print("""
Key Differences to Look For:

1. **Content Freshness**: Exa should have more recent content (2024)
2. **Content Quality**: Exa focuses on high-quality, authoritative sources  
3. **Specificity**: Exa should be better at finding specific technical details
4. **Current State**: Exa should better identify what companies ALREADY have
5. **Source Authority**: Exa tends to find more authoritative sources

For Netflix Use Cases:
- Look for content about their CURRENT recommendation systems
- Check for recent AI initiatives they've already implemented
- Find gaps they haven't addressed yet

This comparison will help us choose the best search engine for each type of query.
""")

def display_search_results(results: list, source_name: str, max_results: int = 3):
    """Display formatted search results."""
    
    if not results:
        print(f"   ❌ No results from {source_name}")
        return
    
    print(f"   📈 Found {len(results)} results from {source_name}")
    
    for i, result in enumerate(results[:max_results], 1):
        title = result.get('title', 'No Title')
        content = result.get('content', 'No Content')
        url = result.get('url', 'No URL')
        published_date = result.get('published_date', 'Date unknown')
        score = result.get('score', 0.0)
        
        print(f"\n   🔸 Result {i}:")
        print(f"      Title: {title[:80]}{'...' if len(title) > 80 else ''}")
        print(f"      Published: {published_date}")
        print(f"      Score: {score:.2f}")
        print(f"      Content: {content[:200]}{'...' if len(content) > 200 else ''}")
        print(f"      URL: {url}")

if __name__ == "__main__":
    compare_search_results()
