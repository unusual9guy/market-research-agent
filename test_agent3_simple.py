"""
Simple Test for Agent 3: Resource Discovery Agent

This is a simplified test to verify Agent 3 works with Exa search.
"""

import logging
from agents.resource_discovery_agent import ResourceDiscoveryAgent
from config import config

# Set up logging
logging.basicConfig(level=logging.WARNING)  # Reduce noise

def test_simple_resource_discovery():
    """Simple test with one use case."""
    
    print("🔍 Simple Agent 3 Test")
    print("=" * 40)
    
    # Check API keys
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY required")
        return
    
    if not config.EXA_API_KEY:
        print("❌ EXA_API_KEY required")
        return
    
    print("✅ Required API keys configured")
    
    # Initialize Agent 3
    try:
        resource_agent = ResourceDiscoveryAgent()
        print("✅ Resource Discovery Agent initialized")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Single simple use case
    test_use_case = {
        "title": "Machine Learning Recommendation System",
        "ai_solution": "Build a recommendation system using collaborative filtering",
        "strategic_value": "Improve user engagement through personalized recommendations",
        "implementation_approach": "Python with scikit-learn and pandas",
        "revenue_impact": "Increase user retention by 20%",
        "complexity_analysis": {"technical_complexity": "Medium"},
        "innovation_level": "Medium",
        "overall_score": 0.75
    }
    
    print(f"\n🎯 Testing with: {test_use_case['title']}")
    
    # Test resource discovery
    try:
        discovery_results = resource_agent.discover_resources_for_use_cases([test_use_case])
        
        if discovery_results.get('status') == 'completed':
            print("✅ Resource discovery completed!")
            
            # Show results
            resources_by_use_case = discovery_results.get('resources_by_use_case', {})
            
            for use_case_title, use_case_resources in resources_by_use_case.items():
                print(f"\n📋 Resources for: {use_case_title}")
                
                for category, resources in use_case_resources.items():
                    if resources:
                        print(f"\n   📁 {category.replace('_', ' ').title()}: {len(resources)} found")
                        for i, resource in enumerate(resources[:2], 1):  # Show first 2
                            title = resource.get('title', 'No title')[:50]
                            source = resource.get('source', 'Unknown')
                            print(f"      {i}. {title}... [{source}]")
                            print(f"         🔗 {resource.get('url', 'No URL')}")
            
            # Show summary
            summary = discovery_results.get('discovery_summary', {})
            total = summary.get('total_resources_discovered', 0)
            print(f"\n📊 Total resources found: {total}")
            
        else:
            print(f"❌ Discovery failed: {discovery_results.get('error', 'Unknown')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_resource_discovery()
