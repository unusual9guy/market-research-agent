"""
Streamlit Demo Interface for Multi-Agent Market Research System
"""
import streamlit as st
import logging
from typing import Dict
from agents.enhanced_industry_agent import EnhancedIndustryResearchAgent
from agents.enhanced_use_case_agent import EnhancedUseCaseGenerationAgent
from utils.report_generator import ReportGenerator
from config import config

# Set up logging
logging.basicConfig(level=logging.WARNING)  # Reduce log noise in demo

# Page configuration
st.set_page_config(
    page_title="AI Market Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.section-header {
    font-size: 1.5rem;
    color: #ff7f0e;
    margin-top: 2rem;
    margin-bottom: 1rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI-Powered Market Research Agent</h1>', unsafe_allow_html=True)
    st.markdown("### Multi-Agent System for Automated Market Research & AI Use Case Generation")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key validation
        missing_keys = config.validate_required_keys()
        if missing_keys:
            st.error(f"❌ Missing API keys: {', '.join(missing_keys)}")
            st.info("Please configure your API keys in the .env file")
            st.stop()
        else:
            st.success("✅ API keys configured")
        
        # Company input
        st.header("🏢 Company Analysis")
        company_name = st.text_input(
            "Enter Company Name:",
            placeholder="e.g., Tesla, Netflix, Amazon",
            help="Enter the name of any company for AI market research analysis"
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            show_debug = st.checkbox("Show debug information", value=False)
            save_report = st.checkbox("Save report to file", value=True)
        
        # Analysis button
        analyze_button = st.button(
            "🚀 Generate Analysis",
            type="primary",
            disabled=not company_name.strip(),
            help="Click to start comprehensive market research analysis"
        )
    
    # Main content area
    if not analyze_button:
        # Welcome screen
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Industry Research")
            st.info("Deep market analysis with competitive intelligence")
            
        with col2:
            st.markdown("### 🎯 AI Use Cases")
            st.info("Strategic AI opportunities with feasibility analysis")
            
        with col3:
            st.markdown("### 📋 Implementation")
            st.info("Executive recommendations with actionable roadmaps")
        
        # Example companies
        st.markdown("### 💡 Example Companies to Analyze:")
        example_cols = st.columns(4)
        examples = ["Tesla", "Netflix", "Spotify", "Airbnb"]
        
        for i, example in enumerate(examples):
            with example_cols[i]:
                if st.button(f"📊 {example}", key=f"example_{example}"):
                    st.rerun()
        
        # System capabilities
        st.markdown("### 🔧 System Capabilities")
        capabilities = [
            "🔍 **Real-time Web Search** - Tavily API for current market data",
            "🤖 **LLM Analysis** - OpenAI GPT-4 for intelligent insights", 
            "📊 **Multi-Agent Architecture** - Specialized agents for different tasks",
            "📋 **Professional Reports** - Executive-ready analysis and recommendations",
            "⚡ **Fast Processing** - Complete analysis in under 5 minutes"
        ]
        
        for capability in capabilities:
            st.markdown(capability)
    
    else:
        # Run analysis
        if company_name.strip():
            run_market_research_analysis(company_name.strip(), show_debug, save_report)

def run_market_research_analysis(company_name: str, show_debug: bool, save_report: bool):
    """Run the complete market research analysis."""
    
    # Initialize progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Initialize agents
        status_text.text("🔧 Initializing AI agents...")
        progress_bar.progress(10)
        
        industry_agent = EnhancedIndustryResearchAgent()
        use_case_agent = EnhancedUseCaseGenerationAgent()
        report_generator = ReportGenerator()
        
        if show_debug:
            st.success("✅ Agents initialized successfully")
        
        # Phase 1: Industry Research
        status_text.text("📊 Conducting deep industry research...")
        progress_bar.progress(25)
        
        with st.spinner("Analyzing industry landscape and competitive positioning..."):
            deep_research = industry_agent.conduct_deep_research(company_name)
        
        if deep_research.get('status') != 'completed':
            st.error(f"❌ Industry research failed: {deep_research.get('error', 'Unknown error')}")
            return
        
        progress_bar.progress(50)
        
        if show_debug:
            research_sources = deep_research.get('research_sources', {})
            total_sources = sum(len(sources) for sources in research_sources.values())
            st.info(f"✅ Industry research completed with {total_sources} sources")
        
        # Phase 2: Use Case Generation
        status_text.text("🎯 Generating strategic AI use cases...")
        progress_bar.progress(75)
        
        with st.spinner("Identifying AI opportunities and analyzing feasibility..."):
            strategic_use_cases = use_case_agent.generate_strategic_use_cases(deep_research)
        
        if strategic_use_cases.get('status') != 'completed':
            st.error(f"❌ Use case generation failed: {strategic_use_cases.get('error', 'Unknown error')}")
            return
        
        progress_bar.progress(90)
        
        if show_debug:
            use_cases = strategic_use_cases.get('strategic_use_cases', [])
            st.info(f"✅ Generated {len(use_cases)} strategic use cases")
        
        # Phase 3: Report Generation
        status_text.text("📋 Generating comprehensive report...")
        
        comprehensive_report = report_generator.generate_comprehensive_report(
            deep_research, strategic_use_cases
        )
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis completed successfully!")
        
        # Display results
        display_analysis_results(
            company_name, deep_research, strategic_use_cases, 
            comprehensive_report, save_report
        )
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        if show_debug:
            st.exception(e)

def display_analysis_results(
    company_name: str, 
    deep_research: Dict, 
    strategic_use_cases: Dict, 
    comprehensive_report: str, 
    save_report: bool
):
    """Display the analysis results in a structured format."""
    
    # Summary metrics
    st.markdown('<h2 class="section-header">📊 Analysis Summary</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        research_sources = deep_research.get('research_sources', {})
        total_sources = sum(len(sources) for sources in research_sources.values())
        st.metric("📚 Research Sources", total_sources)
    
    with col2:
        use_cases = strategic_use_cases.get('strategic_use_cases', [])
        st.metric("🎯 AI Use Cases", len(use_cases))
    
    with col3:
        high_innovation = sum(1 for uc in use_cases if 'High' in str(uc.get('innovation_level', '')))
        st.metric("💡 High Innovation", f"{high_innovation}/{len(use_cases)}")
    
    with col4:
        avg_score = sum(uc.get('overall_score', 0) for uc in use_cases) / len(use_cases) if use_cases else 0
        st.metric("📈 Avg Quality Score", f"{avg_score:.1%}")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["🏭 Industry Analysis", "🎯 AI Use Cases", "📋 Full Report", "💾 Export"])
    
    with tab1:
        st.markdown("### 🔍 Industry Research Summary")
        
        # Company foundation
        company_analysis = deep_research.get('company_foundation', {})
        st.markdown("**Company Analysis:**")
        st.write(company_analysis.get('structured_content', 'Analysis in progress')[:500] + "...")
        
        # Market analysis
        market_analysis = deep_research.get('market_analysis', {})
        st.markdown("**Market Position:**")
        st.write(market_analysis.get('structured_content', 'Analysis in progress')[:500] + "...")
        
        # Sources
        st.markdown("**Research Sources:**")
        for category, sources in research_sources.items():
            if sources:
                st.markdown(f"**{category.replace('_', ' ').title()}:**")
                for source in sources[:3]:  # Top 3 sources
                    st.markdown(f"- [{source.get('title', 'Source')[:80]}]({source.get('url', '#')})")
    
    with tab2:
        st.markdown("### 🎯 Strategic AI Use Cases")
        
        for i, use_case in enumerate(use_cases, 1):
            with st.expander(f"**{i}. {use_case.get('title', f'Use Case {i}')}** (Priority: {use_case.get('priority_rank', i)})"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🎯 Strategic Value:**")
                    st.write(use_case.get('strategic_value', 'Not specified'))
                    
                    st.markdown("**💰 Revenue Impact:**")
                    st.write(use_case.get('revenue_impact', 'Not specified'))
                    
                    st.markdown("**⚙️ Implementation:**")
                    st.write(use_case.get('implementation_approach', 'Not specified'))
                
                with col2:
                    st.markdown("**🤖 AI Solution:**")
                    st.write(use_case.get('ai_solution', 'Not specified'))
                    
                    st.markdown("**📊 Success Metrics:**")
                    st.write(use_case.get('success_metrics', 'Not specified'))
                    
                    feasibility = use_case.get('feasibility_analysis', {})
                    st.markdown("**⏱️ Timeline:**")
                    st.write(feasibility.get('implementation_timeline', 'Not specified'))
                
                # Scores
                st.markdown("**📈 Scores:**")
                score_col1, score_col2, score_col3 = st.columns(3)
                with score_col1:
                    # Extract just the first word (High, Medium, Low) for display
                    innovation_full = use_case.get('innovation_level', 'Unknown')
                    innovation_display = innovation_full.split(' - ')[0] if ' - ' in innovation_full else innovation_full.split()[0] if innovation_full else 'Unknown'
                    st.metric("Innovation", innovation_display)
                with score_col2:
                    st.metric("Overall Score", f"{use_case.get('overall_score', 0):.1%}")
                with score_col3:
                    complexity = use_case.get('complexity_analysis', {})
                    st.metric("Complexity", complexity.get('technical_complexity', 'Medium'))
    
    with tab3:
        st.markdown("### 📋 Comprehensive Report")
        st.markdown(comprehensive_report)
    
    with tab4:
        st.markdown("### 💾 Export Options")
        
        # Save report
        if save_report:
            import os
            # Ensure outputs directory exists
            os.makedirs('outputs', exist_ok=True)
            filename = f"outputs/{company_name.lower().replace(' ', '_')}_ai_market_research_report.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(comprehensive_report)
            st.success(f"✅ Report saved as: {filename}")
        
        # Download button
        st.download_button(
            label="📥 Download Report",
            data=comprehensive_report,
            file_name=f"{company_name.lower().replace(' ', '_')}_ai_market_research_report.md",
            mime="text/markdown",
            help="Download the complete report as a Markdown file"
        )
        
        # Implementation roadmap
        roadmap = strategic_use_cases.get('implementation_roadmap', {})
        st.markdown("### 🗺️ Implementation Roadmap")
        st.write(f"**Timeline:** {roadmap.get('total_timeline', '24 months')}")
        st.write(f"**Overview:** {roadmap.get('roadmap_overview', 'Three-phase approach')}")

if __name__ == "__main__":
    main()
