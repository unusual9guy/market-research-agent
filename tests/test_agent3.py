"""
Test Script for Agent 3: Resource Discovery Agent

This script tests the Resource Discovery Agent with sample use cases.
You can copy-paste use cases from Agent 2 output to test resource discovery.
"""

import logging
from agents.resource_discovery_agent import ResourceDiscoveryAgent
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_resource_discovery_agent():
    """Test the Resource Discovery Agent with sample use cases."""
    
    print("🔍 Testing Agent 3: Resource Discovery Agent")
    print("=" * 60)
    
    # Check API keys
    missing_keys = config.validate_required_keys()
    if missing_keys:
        print(f"❌ Missing API keys: {', '.join(missing_keys)}")
        print("Please configure your API keys in the .env file")
        return
    
    print("✅ API keys configured")
    
    # Initialize Agent 3
    try:
        resource_agent = ResourceDiscoveryAgent()
        print("✅ Resource Discovery Agent initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Resource Discovery Agent: {e}")
        return
    
    # Sample use cases for testing (you can replace these with real ones)
    sample_use_cases = [
        {
            "title": "AI-Powered Content Recommendation System",
            "ai_solution": "Machine learning algorithms to analyze user preferences and viewing history to recommend personalized content",
            "strategic_value": "Increase user engagement and retention by 25% through personalized recommendations",
            "implementation_approach": "Implement collaborative filtering and content-based filtering algorithms",
            "revenue_impact": "Potential 15-20% increase in subscription retention and ad revenue",
            "complexity_analysis": {"technical_complexity": "Medium"},
            "innovation_level": "High - Advanced recommendation algorithms",
            "overall_score": 0.85
        },
        {
            "title": "Automated Content Generation and Editing",
            "ai_solution": "Generative AI models to create and edit video content, thumbnails, and promotional materials",
            "strategic_value": "Reduce content production costs by 40% and accelerate time-to-market",
            "implementation_approach": "Deploy transformer-based models for video generation and editing",
            "revenue_impact": "Cost savings of $2-3M annually in content production",
            "complexity_analysis": {"technical_complexity": "High"},
            "innovation_level": "Very High - Cutting-edge generative AI",
            "overall_score": 0.90
        },
        {
            "title": "Predictive Analytics for Viewer Behavior",
            "ai_solution": "Time series analysis and machine learning to predict viewer preferences and churn probability",
            "strategic_value": "Improve content strategy and reduce subscriber churn by 20%",
            "implementation_approach": "Implement LSTM networks and ensemble methods for prediction",
            "revenue_impact": "Maintain 20% more subscribers through predictive retention",
            "complexity_analysis": {"technical_complexity": "Medium-High"},
            "innovation_level": "High - Advanced predictive modeling",
            "overall_score": 0.80
        }
    ]
    
    print(f"\n📋 Testing with {len(sample_use_cases)} sample use cases:")
    for i, use_case in enumerate(sample_use_cases, 1):
        print(f"   {i}. {use_case['title']}")
    
    # Test resource discovery
    print(f"\n🔍 Starting resource discovery...")
    try:
        discovery_results = resource_agent.discover_resources_for_use_cases(sample_use_cases)
        
        if discovery_results.get('status') == 'completed':
            print("✅ Resource discovery completed successfully!")
            
            # Show summary
            summary = discovery_results.get('discovery_summary', {})
            print(f"\n📊 DISCOVERY SUMMARY:")
            print(f"   Total Resources Found: {summary.get('total_resources_discovered', 0)}")
            print(f"   Average per Use Case: {summary.get('average_resources_per_use_case', 0):.1f}")
            
            category_breakdown = summary.get('category_breakdown', {})
            print(f"   📊 Datasets: {category_breakdown.get('datasets', 0)}")
            print(f"   💻 Code Repositories: {category_breakdown.get('code_repositories', 0)}")
            print(f"   📚 Papers & Docs: {category_breakdown.get('papers_and_docs', 0)}")
            print(f"   🛠️ Tools & Frameworks: {category_breakdown.get('tools_and_frameworks', 0)}")
            
            top_sources = summary.get('top_sources', [])
            if top_sources:
                print(f"\n🏆 TOP SOURCES:")
                for source_info in top_sources[:3]:
                    print(f"   {source_info['source']}: {source_info['count']} resources")
            
            # Show detailed results for each use case
            resources_by_use_case = discovery_results.get('resources_by_use_case', {})
            print(f"\n📋 DETAILED RESULTS:")
            
            for use_case_title, use_case_resources in resources_by_use_case.items():
                print(f"\n🎯 {use_case_title}:")
                
                for category, resources in use_case_resources.items():
                    if resources:
                        print(f"\n   📁 {category.replace('_', ' ').title()}:")
                        for resource in resources[:3]:  # Show top 3 per category
                            title = resource.get('title', 'No title')[:60]
                            url = resource.get('url', '')
                            source = resource.get('source', 'Unknown')
                            score = resource.get('relevance_score', 0)
                            print(f"      • {title}... [{source}] (Score: {score:.2f})")
                            print(f"        🔗 {url}")
                
                # Show total resources for this use case
                total_resources = sum(len(resources) for resources in use_case_resources.values())
                print(f"   📊 Total: {total_resources} resources")
        
        else:
            print(f"❌ Resource discovery failed: {discovery_results.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Error during resource discovery: {e}")
        import traceback
        traceback.print_exc()

def test_with_custom_use_cases():
    """Test with custom use cases that you can paste from Agent 2 output."""
    
    print("\n" + "=" * 60)
    print("🎯 CUSTOM USE CASE TESTING")
    print("=" * 60)
    print("You can copy-paste use cases from Agent 2 output here to test!")
    print("Example format:")
    print("""
    custom_use_cases = [
        {
            "title": "Your Use Case Title",
            "ai_solution": "Description of AI solution",
            "strategic_value": "Business value",
            "implementation_approach": "How to implement",
            "revenue_impact": "Financial impact",
            "complexity_analysis": {"technical_complexity": "Medium"},
            "innovation_level": "High - Description",
            "overall_score": 0.80
        }
    ]
    """)
    
    # Initialize agent
    try:
        resource_agent = ResourceDiscoveryAgent()
        print("✅ Agent 3 ready for custom testing")
        print("💡 Replace the sample_use_cases in this script with your own use cases from Agent 2")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")

if __name__ == "__main__":
    test_resource_discovery_agent()
    test_with_custom_use_cases()
