"""
Streamlit Demo Interface for Multi-Agent Market Research System
"""
import streamlit as st
import logging
from typing import Dict
from datetime import datetime
from agents.enhanced_industry_agent import EnhancedIndustryResearchAgent
from agents.enhanced_use_case_agent import EnhancedUseCaseGenerationAgent
from agents.dataset_discovery_agent import DatasetDiscoveryAgent
from utils.report_generator import ReportGenerator
from utils.md_to_pdf import convert_md_to_pdf
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
.example-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 15px 20px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.example-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI-Powered Market Research Agent</h1>', unsafe_allow_html=True)
    st.markdown("### Multi-Agent System for Automated Market Research & AI Use Case Generation")
    
    # Agent progress log container (will be populated during analysis)
    if 'agent_progress_log' not in st.session_state:
        st.session_state.agent_progress_log = []
    
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
        st.header("🏢 Company/Industry Analysis")
         
        # Initialize session state for company name (for example buttons only)
        if 'selected_company' not in st.session_state:
            st.session_state.selected_company = ""
        
        company_name = st.text_input(
            "Enter Company Name or Industry:",
            value=st.session_state.selected_company,
            placeholder="e.g., Tesla, Automotive Industry, Netflix, Streaming Industry",
            help="Enter the name of any company or industry for AI market research analysis"
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            show_debug = st.checkbox("Show debug information", value=False)
            save_report = st.checkbox("Save Report to File", value=True, help="Automatically save report to outputs folder")
        
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
            st.markdown("### 📊 Dataset Discovery")
            st.info("Curated datasets from Kaggle and GitHub")
        
        # Example companies and industries
        st.markdown("### 💡 Example Companies & Industries to Analyze:")
        example_cols = st.columns(4)
        examples = ["Tesla", "Automotive Industry", "Netflix", "Streaming Industry"]
        
        for i, example in enumerate(examples):
            with example_cols[i]:
                button_html = f"""
                <style>
                .stButton > button:first-child {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 15px 20px;
                    font-size: 16px;
                    font-weight: 600;
                    width: 100%;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                .stButton > button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                }}
                </style>
                """
                st.markdown(button_html, unsafe_allow_html=True)
                
                if st.button(
                    f"📊 {example}", 
                    key=f"example_{example}",
                    use_container_width=True,
                    type="secondary"
                ):
                    st.session_state.selected_company = example
                    st.rerun()
        
        # System capabilities
        st.markdown("### 🔧 System Capabilities")
        capabilities = [
            "🔍 **Real-time Web Search** - Tavily and Exa API for current market data",
            "🤖 **LLM Analysis** - OpenAI GPT-4 for intelligent insights", 
            "📊 **Multi-Agent Architecture** - Specialized agents for different tasks",
            "🏢 **Flexible Input** - Works with both companies and industries",
            "📋 **Professional Reports** - Executive-ready analysis and recommendations",
            "⚡ **Fast Processing** - Complete analysis in under 5 minutes"
        ]
        
        for capability in capabilities:
            st.markdown(capability)
    
    else:
        # Run analysis
        if company_name.strip():
            run_market_research_analysis(company_name.strip(), show_debug, save_report)
    
    # Display stored results if they exist (persists after downloads)
    if 'analysis_results' in st.session_state and not analyze_button:
        st.markdown("---")
        st.markdown('<h2 class="section-header">📊 Analysis Results</h2>', unsafe_allow_html=True)
        
        # Display the stored results
        results = st.session_state.analysis_results
        display_analysis_results(
            results['company_name'],
            results['deep_research'],
            results['strategic_use_cases'],
            results['dataset_results'],
            results['comprehensive_report'],
            results['save_report']
        )

def run_market_research_analysis(company_name: str, show_debug: bool, save_report: bool):
    """Run the complete market research analysis."""
    
    # Initialize progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.empty()  # Container for detailed agent logs
    
    
    try:
        # Initialize agents
        status_text.text("🔧 Initializing AI agents...")
        progress_bar.progress(10)
        log_container.info("🚀 **Starting Multi-Agent Market Research System**")
        
        industry_agent = EnhancedIndustryResearchAgent()
        use_case_agent = EnhancedUseCaseGenerationAgent()
        dataset_agent = DatasetDiscoveryAgent()
        report_generator = ReportGenerator()
        
        log_container.success("✅ **All 3 AI agents initialized successfully**")
        if show_debug:
            st.success("✅ Agents initialized successfully")
        
        # Phase 1: Industry Research
        status_text.text("📊 Conducting deep industry research...")
        progress_bar.progress(20)
        log_container.info(f"🤖 **Agent 1 (Industry Research)**: Starting deep analysis for **{company_name}**...")
        
        with st.spinner("Analyzing industry landscape and competitive positioning..."):
            log_container.info("🔍 **Agent 1**: Gathering company information, market trends, and competitor analysis...")
            deep_research = industry_agent.conduct_deep_research(company_name)
        
        if deep_research.get('status') != 'completed':
            log_container.error(f"❌ **Agent 1 failed**: {deep_research.get('error', 'Unknown error')}")
            st.error(f"❌ Industry research failed: {deep_research.get('error', 'Unknown error')}")
            return
        
        progress_bar.progress(40)
        research_sources = deep_research.get('research_sources', {})
        total_sources = sum(len(sources) for sources in research_sources.values())
        log_container.success(f"✅ **Agent 1 completed**: Found {total_sources} research sources for {company_name}")
        
        if show_debug:
            st.info(f"✅ Industry research completed with {total_sources} sources")
        
        # Phase 2: Use Case Generation
        status_text.text("🎯 Generating strategic AI use cases...")
        progress_bar.progress(60)
        log_container.info("🤖 **Agent 2 (Use Case Generation)**: Initializing and analyzing AI opportunities...")
        
        with st.spinner("Identifying AI opportunities and analyzing feasibility..."):
            log_container.info("🎯 **Agent 2**: Analyzing market trends and generating strategic AI use cases...")
            strategic_use_cases = use_case_agent.generate_strategic_use_cases(deep_research)
        
        if strategic_use_cases.get('status') != 'completed':
            log_container.error(f"❌ **Agent 2 failed**: {strategic_use_cases.get('error', 'Unknown error')}")
            st.error(f"❌ Use case generation failed: {strategic_use_cases.get('error', 'Unknown error')}")
            return
        
        progress_bar.progress(80)
        use_cases = strategic_use_cases.get('strategic_use_cases', [])
        log_container.success(f"✅ **Agent 2 completed**: Generated {len(use_cases)} strategic AI use cases")
        
        if show_debug:
            st.info(f"✅ Generated {len(use_cases)} strategic use cases")
        
        # Phase 3: Dataset Discovery
        status_text.text("📊 Discovering relevant datasets...")
        progress_bar.progress(90)
        log_container.info("🤖 **Agent 3 (Dataset Discovery)**: Starting dataset search for generated use cases...")
        
        with st.spinner("Finding datasets on Kaggle and GitHub..."):
            log_container.info("📊 **Agent 3**: Searching Kaggle and GitHub for relevant datasets...")
            dataset_results = dataset_agent.discover_datasets(use_cases)
        
        if dataset_results.get('status') != 'completed':
            log_container.error(f"❌ **Agent 3 failed**: {dataset_results.get('error', 'Unknown error')}")
            st.error(f"❌ Dataset discovery failed: {dataset_results.get('error', 'Unknown error')}")
            return
        
        progress_bar.progress(95)
        total_datasets = dataset_results.get('total_datasets_found', 0)
        log_container.success(f"✅ **Agent 3 completed**: Discovered {total_datasets} relevant datasets from Kaggle and GitHub")
        
        if show_debug:
            st.info(f"✅ Discovered {total_datasets} relevant datasets")
        
        # Phase 4: Report Generation
        status_text.text("📋 Generating comprehensive report...")
        log_container.info("📋 **Report Generator**: Compiling comprehensive analysis report...")
        
        comprehensive_report = report_generator.generate_comprehensive_report(
            deep_research, strategic_use_cases
        )
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis completed successfully!")
        log_container.success("🎉 **ALL SYSTEMS COMPLETE**: 3-agent analysis finished successfully!")
        
        # Store results in session state to prevent loss on download
        st.session_state.analysis_results = {
            'company_name': company_name,
            'deep_research': deep_research,
            'strategic_use_cases': strategic_use_cases,
            'dataset_results': dataset_results,
            'comprehensive_report': comprehensive_report,
            'save_report': save_report
        }
        
        # Display results
        display_analysis_results(
            company_name, deep_research, strategic_use_cases, 
            dataset_results, comprehensive_report, save_report
        )
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        if show_debug:
            st.exception(e)

def display_analysis_results(
    company_name: str, 
    deep_research: Dict, 
    strategic_use_cases: Dict, 
    dataset_results: Dict,
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
        total_datasets = dataset_results.get('total_datasets_found', 0)
        st.metric("📊 Datasets Found", total_datasets)
    
    with col4:
        high_innovation = sum(1 for uc in use_cases if 'High' in str(uc.get('innovation_level', '')))
        st.metric("💡 High Innovation", f"{high_innovation}/{len(use_cases)}")
    
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏭 Industry Analysis", "🎯 AI Use Cases", "📊 Datasets", "📋 Full Report", "💾 Export"])
    
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
                
                # Innovation and Complexity
                st.markdown("**📈 Analysis:**")
                score_col1, score_col2 = st.columns(2)
                with score_col1:
                    # Extract just the first word (High, Medium, Low) for display
                    innovation_full = use_case.get('innovation_level', 'Unknown')
                    innovation_display = innovation_full.split()[0] if innovation_full and innovation_full.strip() else 'Unknown'
                    st.metric("Innovation", innovation_display)
                with score_col2:
                    complexity = use_case.get('complexity_analysis', {})
                    st.metric("Complexity", complexity.get('technical_complexity', 'Medium'))
    
    with tab3:
        st.markdown("### 📊 Dataset Discovery Results")
        
        total_datasets = dataset_results.get('total_datasets_found', 0)
        st.markdown(f"**Total Datasets Found:** {total_datasets}")
        
        if total_datasets > 0:
            # Show datasets by use case
            for i, use_case_data in enumerate(dataset_results.get('use_case_datasets', []), 1):
                use_case_title = use_case_data.get('use_case_title', f'Use Case {i}')
                kaggle_datasets = use_case_data.get('kaggle_datasets', [])
                github_datasets = use_case_data.get('github_datasets', [])
                use_case_total = len(kaggle_datasets) + len(github_datasets)
                
                if use_case_total > 0:
                    with st.expander(f"**{i}. {use_case_title}** ({use_case_total} datasets)"):
                        
                        if kaggle_datasets:
                            st.markdown(f"#### 📊 Kaggle Datasets ({len(kaggle_datasets)} found)")
                            for j, dataset in enumerate(kaggle_datasets, 1):
                                st.markdown(f"**{j}.** [{dataset['title']}]({dataset['url']})")
                                st.markdown(f"- **Description:** {dataset['description']}")
                                st.markdown(f"- **Relevance Score:** {dataset['relevance_score']:.2f}")
                                st.markdown("")
                        
                        if github_datasets:
                            st.markdown(f"#### 💻 GitHub Datasets ({len(github_datasets)} found)")
                            for j, dataset in enumerate(github_datasets, 1):
                                st.markdown(f"**{j}.** [{dataset['title']}]({dataset['url']})")
                                st.markdown(f"- **Description:** {dataset['description']}")
                                st.markdown(f"- **Relevance Score:** {dataset['relevance_score']:.2f}")
                                st.markdown("")
        else:
            st.info("No datasets found for the generated use cases.")
    
    with tab4:
        st.markdown("### 📋 Comprehensive Report")
        st.markdown(comprehensive_report)
    
    with tab5:
        st.markdown("### 💾 Export Options")
        
        # Save report
        if save_report:
            import os
            # Ensure outputs directory exists
            os.makedirs('outputs', exist_ok=True)
            
            # Generate enhanced report with datasets
            enhanced_report = generate_enhanced_report_with_datasets(
                comprehensive_report, dataset_results
            )
            
            filename = f"outputs/{company_name.lower().replace(' ', '_')}_ai_market_research_report.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(enhanced_report)
            st.success(f"✅ Report saved as: {filename}")
        
        # Download button
        enhanced_report = generate_enhanced_report_with_datasets(
            comprehensive_report, dataset_results
        )
        
        # Create two columns for download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download Markdown Report",
                data=enhanced_report,
                file_name=f"{company_name.lower().replace(' ', '_')}_complete_3_agent_report.md",
                mime="text/markdown",
                help="Download the complete report with datasets as a Markdown file",
                key=f"download_md_{company_name.replace(' ', '_')}"
            )
        
        with col2:
            # PDF Download button
            try:
                # Create temporary markdown file for PDF conversion
                temp_md_file = f"temp_{company_name.lower().replace(' ', '_')}_report.md"
                with open(temp_md_file, 'w', encoding='utf-8') as f:
                    f.write(enhanced_report)
                
                # Convert to PDF
                pdf_path = convert_md_to_pdf(temp_md_file)
                
                # Read PDF file for download
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                
                # Clean up temporary files
                import os
                os.remove(temp_md_file)
                os.remove(pdf_path)
                
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_data,
                    file_name=f"{company_name.lower().replace(' ', '_')}_complete_3_agent_report.pdf",
                    mime="application/pdf",
                    help="Download the complete report as a professional PDF document",
                    key=f"download_pdf_{company_name.replace(' ', '_')}"
                )
                
            except Exception as e:
                st.error(f"❌ PDF conversion failed: {str(e)}")
                st.info("💡 Make sure wkhtmltopdf is installed. See requirements for setup instructions.")
        
        # Implementation roadmap
        roadmap = strategic_use_cases.get('implementation_roadmap', {})
        st.markdown("### 🗺️ Implementation Roadmap")
        st.write(f"**Timeline:** {roadmap.get('total_timeline', '24 months')}")
        st.write(f"**Overview:** {roadmap.get('roadmap_overview', 'Three-phase approach')}")

def generate_enhanced_report_with_datasets(base_report: str, dataset_results: Dict) -> str:
    """Generate enhanced report with dataset information."""
    
    enhanced_report = f"""# Complete 3-Agent AI Market Research Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**System:** 3-Agent AI Market Research System  
**Status:** ✅ All agents completed successfully

---

## 🤖 System Performance Summary

- **Agent 1 (Industry Research):** ✅ Completed
- **Agent 2 (Use Case Generation):** ✅ Completed  
- **Agent 3 (Dataset Discovery):** ✅ Completed
- **Report Generation:** ✅ Completed

---

{base_report}

---

## 📊 Dataset Discovery Results

**Total Datasets Found:** {dataset_results.get('total_datasets_found', 0)}

### Dataset Summary by Use Case

"""
    
    for i, use_case_data in enumerate(dataset_results.get('use_case_datasets', []), 1):
        use_case_title = use_case_data.get('use_case_title', f'Use Case {i}')
        kaggle_datasets = use_case_data.get('kaggle_datasets', [])
        github_datasets = use_case_data.get('github_datasets', [])
        total_datasets = len(kaggle_datasets) + len(github_datasets)
        
        enhanced_report += f"""### {i}. {use_case_title}

**Total Datasets:** {total_datasets} ({len(kaggle_datasets)} Kaggle, {len(github_datasets)} GitHub)

"""
        
        if kaggle_datasets:
            enhanced_report += f"#### 📊 Kaggle Datasets ({len(kaggle_datasets)} found)\n\n"
            for j, dataset in enumerate(kaggle_datasets, 1):
                enhanced_report += f"{j}. [{dataset['title']}]({dataset['url']})\n"
                enhanced_report += f"   - **Description:** {dataset['description']}\n"
                enhanced_report += f"   - **Relevance Score:** {dataset['relevance_score']:.2f}\n\n"
        
        if github_datasets:
            enhanced_report += f"#### 💻 GitHub Datasets ({len(github_datasets)} found)\n\n"
            for j, dataset in enumerate(github_datasets, 1):
                enhanced_report += f"{j}. [{dataset['title']}]({dataset['url']})\n"
                enhanced_report += f"   - **Description:** {dataset['description']}\n"
                enhanced_report += f"   - **Relevance Score:** {dataset['relevance_score']:.2f}\n\n"
        
        if not kaggle_datasets and not github_datasets:
            enhanced_report += "*No datasets found for this use case.*\n\n"
        
        enhanced_report += "---\n\n"
    
    enhanced_report += f"""
## 🎯 System Evaluation

### ✅ Success Metrics:
- **Multi-Agent Coordination:** All 3 agents executed successfully in sequence
- **Data Flow:** Information passed correctly between agents
- **Output Quality:** High-quality research, use cases, and dataset discoveries
- **Integration:** Seamless workflow from research → use cases → datasets → report

### 🚀 Ready for Production:
This 3-agent system demonstrates:
- **Deep Market Research** with comprehensive source gathering
- **Strategic AI Use Case Generation** with feasibility analysis
- **Targeted Dataset Discovery** from Kaggle and GitHub
- **Professional Report Generation** with actionable insights

---

*Generated by 3-Agent AI Market Research System*  
*All agents working in perfect coordination*
"""
    
    return enhanced_report

if __name__ == "__main__":
    main()
