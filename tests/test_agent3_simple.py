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
        discovery_result = resource_agent.discover_resources_for_use_cases([test_use_case])
        
        if discovery_result.status == 'completed':
            print("✅ Dataset discovery completed!")
            
            # Show results
            for use_case_resource in discovery_result.use_case_resources:
                print(f"\n📋 Datasets for: {use_case_resource.use_case_title}")
                print(f"   📊 Total datasets found: {use_case_resource.total_datasets}")
                
                if use_case_resource.datasets:
                    for i, dataset in enumerate(use_case_resource.datasets[:3], 1):  # Show first 3
                        print(f"\n   {i}. {dataset.title[:60]}...")
                        print(f"      Source: {dataset.source}")
                        print(f"      Score: {dataset.relevance_score:.2f}")
                        print(f"      🔗 {dataset.url}")
                        
                        if dataset.size:
                            print(f"      Size: {dataset.size}")
                        if dataset.format:
                            print(f"      Format: {dataset.format}")
                        if dataset.tags:
                            print(f"      Tags: {', '.join(dataset.tags[:3])}")
                else:
                    print("   No datasets found for this use case.")
            
            # Show summary
            print(f"\n📊 SUMMARY:")
            print(f"   Total use cases: {discovery_result.total_use_cases}")
            print(f"   Total datasets found: {discovery_result.total_datasets_found}")
            print(f"   Sources used: {', '.join(discovery_result.search_sources_used)}")
            
            # Show saved file info
            print(f"\n💾 Report saved to: agent3_output/ folder")
            
        else:
            print(f"❌ Discovery failed: {discovery_result.status}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_resource_discovery()
