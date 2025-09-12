"""
Simple test script for Industry Research Agent.
"""
import logging
from agents.industry_research_agent import IndustryResearchAgent
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_industry_research_agent():
    """Test the Industry Research Agent with a sample company."""
    
    # Check if required API keys are configured
    missing_keys = config.validate_required_keys()
    if missing_keys:
        print(f"❌ Missing required API keys: {', '.join(missing_keys)}")
        print("Please check your .env file.")
        return
    
    print("✅ API keys configured. Testing Industry Research Agent...")
    
    # Initialize the agent
    try:
        agent = IndustryResearchAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return
    
    # Test with a well-known company
    test_company = "Tesla"
    print(f"\n🔍 Researching: {test_company}")
    
    try:
        # Run the research
        research_result = agent.research_company(test_company)
        
        if research_result.get('status') == 'completed':
            print("✅ Research completed successfully!")
            
            # Display summary
            summary = agent.get_summary(research_result)
            print("\n📋 Research Summary:")
            print("=" * 50)
            print(summary)
            print("=" * 50)
            
            # Display some raw data
            company_analysis = research_result.get('company_analysis', {})
            print(f"\n📊 Industry: {company_analysis.get('industry', 'N/A')}")
            
            sources = research_result.get('raw_sources', {})
            company_sources = sources.get('company_sources', [])
            print(f"📚 Sources found: {len(company_sources)} company sources")
            
            if company_sources:
                print("\n🔗 Top source:")
                top_source = company_sources[0]
                print(f"   Title: {top_source.get('title', 'N/A')}")
                print(f"   URL: {top_source.get('url', 'N/A')}")
        
        else:
            print(f"❌ Research failed: {research_result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during research: {e}")

if __name__ == "__main__":
    test_industry_research_agent()
