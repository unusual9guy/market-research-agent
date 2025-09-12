"""
Test script for Use Case Generation Agent.
"""
import logging
from agents.industry_research_agent import IndustryResearchAgent
from agents.use_case_generation_agent import UseCaseGenerationAgent
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_use_case_generation_agent():
    """Test the Use Case Generation Agent with real data from Agent 1."""
    
    # Check if required API keys are configured
    missing_keys = config.validate_required_keys()
    if missing_keys:
        print(f"❌ Missing required API keys: {', '.join(missing_keys)}")
        print("Please check your .env file.")
        return
    
    print("✅ API keys configured. Testing Agent 1 → Agent 2 workflow...")
    
    # Initialize both agents
    try:
        agent1 = IndustryResearchAgent()
        agent2 = UseCaseGenerationAgent()
        print("✅ Both agents initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agents: {e}")
        return
    
    # Test with a well-known company
    test_company = "Netflix"
    print(f"\n🔍 Testing workflow with: {test_company}")
    
    try:
        # Step 1: Run Agent 1 (Industry Research)
        print("📊 Step 1: Running Industry Research Agent...")
        research_result = agent1.research_company(test_company)
        
        if research_result.get('status') != 'completed':
            print(f"❌ Agent 1 failed: {research_result.get('error', 'Unknown error')}")
            return
        
        print("✅ Agent 1 completed successfully!")
        
        # Step 2: Run Agent 2 (Use Case Generation)
        print("🤖 Step 2: Running Use Case Generation Agent...")
        use_case_result = agent2.generate_use_cases(research_result)
        
        if use_case_result.get('status') != 'completed':
            print(f"❌ Agent 2 failed: {use_case_result.get('error', 'Unknown error')}")
            return
        
        print("✅ Agent 2 completed successfully!")
        
        # Step 3: Display results
        print("\n" + "="*60)
        print("🎯 AGENT 2 RESULTS: AI/ML USE CASES")
        print("="*60)
        
        # Show summary
        summary = agent2.get_summary(use_case_result)
        print(summary)
        
        # Show individual use cases
        use_cases = use_case_result.get('use_cases', [])
        print(f"\n📋 Detailed Use Cases ({len(use_cases)} generated):")
        print("-" * 50)
        
        for i, use_case in enumerate(use_cases, 1):
            print(f"\n🔸 {use_case.get('title', f'Use Case {i}')}")
            print(f"   Problem: {use_case.get('problem', 'N/A')[:150]}...")
            print(f"   AI Approach: {use_case.get('ai_approach', 'N/A')[:100]}...")
            print(f"   Business Impact: {use_case.get('business_impact', 'N/A')[:100]}...")
            print(f"   Complexity: {use_case.get('complexity', 'N/A')}")
            
            references = use_case.get('references', [])
            if references:
                print(f"   References: {len(references)} sources")
                for ref in references[:1]:  # Show first reference
                    print(f"     - {ref.get('title', 'N/A')[:60]}...")
            else:
                print("   References: None")
        
        # Show industry trends
        trends = use_case_result.get('industry_trends', 'No trends available')
        print(f"\n🌟 Industry AI Trends:")
        print("-" * 30)
        print(trends[:500] + "..." if len(trends) > 500 else trends)
        
        # Show sources
        sources = use_case_result.get('research_sources', {})
        trend_sources = sources.get('ai_trends_sources', [])
        case_sources = sources.get('use_case_sources', [])
        
        print(f"\n📚 Research Sources:")
        print(f"   AI Trends: {len(trend_sources)} sources")
        print(f"   Use Cases: {len(case_sources)} sources")
        
        if trend_sources:
            print(f"\n🔗 Top AI Trend Source:")
            top_source = trend_sources[0]
            print(f"   Title: {top_source.get('title', 'N/A')}")
            print(f"   URL: {top_source.get('url', 'N/A')}")
        
        print("\n✅ Agent 1 → Agent 2 workflow completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during workflow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_use_case_generation_agent()
