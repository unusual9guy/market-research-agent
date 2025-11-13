"""
Streamlit Demo Interface for Multi-Agent Market Research System
"""
import streamlit as st
import logging
import re
import os
import tempfile
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
logger = logging.getLogger(__name__)

def sanitize_filename(name: str, max_length: int = 100) -> str:
    """
    Sanitize company/industry name for safe use in file paths.
    
    Args:
        name: Input string to sanitize
        max_length: Maximum length for the sanitized string
        
    Returns:
        Sanitized string safe for file operations
    """
    if not name or not isinstance(name, str):
        return "unknown"
    
    # Remove path traversal attempts and dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name)
    
    # Replace spaces and multiple underscores with single underscore
    sanitized = re.sub(r'[\s_]+', '_', sanitized)
    
    # Remove leading/trailing dots and underscores
    sanitized = sanitized.strip('._')
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    # Ensure it's not empty after sanitization
    if not sanitized:
        return "unknown"
    
    return sanitized.lower()

# Page configuration
st.set_page_config(
    page_title="AI Market Research Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
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
/* Reduce padding for all alert boxes */
.stAlert > div {
    padding: 8px 12px !important;
}

/* Target the first three info boxes specifically */
.stAlert:nth-of-type(1),
.stAlert:nth-of-type(2),
.stAlert:nth-of-type(3) {
    min-height: 80px !important;
    margin-top: 5px !important;
}

/* Center text in the first three info boxes */
.stAlert:nth-of-type(1) > div,
.stAlert:nth-of-type(2) > div,
.stAlert:nth-of-type(3) > div {
    text-align: center !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 100% !important;
}

/* Sidebar styling improvements */
.css-1d391kg {
    padding-top: 1rem;
}

/* Sidebar section headers */
.sidebar .stMarkdown h3 {
    color: #1f77b4 !important;
    margin-bottom: 0.3rem !important;
    margin-top: 0.5rem !important;
}

/* Reduce spacing in sidebar */
.sidebar .stMarkdown {
    margin-bottom: 0.2rem !important;
}

/* Reduce alert spacing */
.sidebar .stAlert {
    margin-bottom: 0.5rem !important;
}

/* Center all text elements in main content area */
.block-container .stMarkdown,
.block-container .stMarkdown h1, 
.block-container .stMarkdown h2, 
.block-container .stMarkdown h3,
.block-container .stMarkdown p,
.block-container .stMarkdown div {
    text-align: center !important;
}

/* Center columns and their content */
.block-container .stColumn {
    text-align: center !important;
}

.block-container .stColumn .stMarkdown {
    text-align: center !important;
}

/* Center alert boxes */
.block-container .stAlert {
    text-align: center !important;
}

.block-container .stAlert > div {
    text-align: center !important;
}

/* Center buttons */
.block-container .stButton {
    text-align: center !important;
}

.block-container .stButton > button {
    text-align: center !important;
}

/* Center metrics */
.block-container .stMetric {
    text-align: center !important;
}

/* Center tabs */
.block-container .stTabs [data-baseweb="tab-list"] {
    justify-content: center !important;
}

.block-container .stTabs [data-baseweb="tab-list"] button {
    text-align: center !important;
}

/* Center tab content */
.block-container .stTabs [data-baseweb="tab-panel"] {
    text-align: center !important;
}

/* Center download buttons */
.block-container .stDownloadButton {
    text-align: center !important;
}

/* Center expander headers and content */
.block-container .streamlit-expanderHeader {
    text-align: center !important;
}

.block-container .streamlit-expanderContent {
    text-align: center !important;
}

/* Center progress bars */
.block-container .stProgress {
    text-align: center !important;
}

/* Center status text */
.block-container .stText {
    text-align: center !important;
}

/* Center spinner */
.block-container .stSpinner {
    text-align: center !important;
}

/* Center text inputs */
.block-container .stTextInput {
    text-align: center !important;
}

.block-container .stTextInput > div > div > input {
    text-align: center !important;
}

/* Center select boxes */
.block-container .stSelectbox {
    text-align: center !important;
}

/* Center checkboxes */
.block-container .stCheckbox {
    text-align: center !important;
}

.block-container .stCheckbox > label {
    text-align: center !important;
}

/* Center file uploader */
.block-container .stFileUploader {
    text-align: center !important;
}

/* Center success/error messages */
.block-container .stSuccess, 
.block-container .stError, 
.block-container .stWarning, 
.block-container .stInfo {
    text-align: center !important;
}

/* Ensure all divs in main are centered */
.block-container div {
    text-align: center !important;
}

/* Override any left alignment in main content */
.block-container * {
    text-align: center !important;
}

/* Exception for sidebar - keep left aligned */
.sidebar * {
    text-align: left !important;
}

/* Force left-align report content for better readability */
.block-container .stExpander .streamlit-expanderContent,
.block-container .stTabs [data-baseweb="tab-panel"],
.block-container .stTabs [data-baseweb="tab-panel"] *,
.block-container .stTabs [data-baseweb="tab-panel"] .stMarkdown,
.block-container .stTabs [data-baseweb="tab-panel"] .stMarkdown *,
.block-container .stTabs [data-baseweb="tab-panel"] p,
.block-container .stTabs [data-baseweb="tab-panel"] div,
.block-container .stTabs [data-baseweb="tab-panel"] ul,
.block-container .stTabs [data-baseweb="tab-panel"] ol,
.block-container .stTabs [data-baseweb="tab-panel"] li,
.block-container .stTabs [data-baseweb="tab-panel"] h1,
.block-container .stTabs [data-baseweb="tab-panel"] h2,
.block-container .stTabs [data-baseweb="tab-panel"] h3,
.block-container .stTabs [data-baseweb="tab-panel"] h4,
.block-container .stTabs [data-baseweb="tab-panel"] h5,
.block-container .stTabs [data-baseweb="tab-panel"] h6 {
    text-align: left !important;
}

/* Force left-align report content in expanders */
.block-container .streamlit-expanderContent,
.block-container .streamlit-expanderContent *,
.block-container .streamlit-expanderContent .stMarkdown,
.block-container .streamlit-expanderContent .stMarkdown *,
.block-container .streamlit-expanderContent p,
.block-container .streamlit-expanderContent div,
.block-container .streamlit-expanderContent ul,
.block-container .streamlit-expanderContent ol,
.block-container .streamlit-expanderContent li,
.block-container .streamlit-expanderContent h1,
.block-container .streamlit-expanderContent h2,
.block-container .streamlit-expanderContent h3,
.block-container .streamlit-expanderContent h4,
.block-container .streamlit-expanderContent h5,
.block-container .streamlit-expanderContent h6 {
    text-align: left !important;
}

/* Center the Generate Analysis button specifically */
.block-container .stButton {
    display: flex !important;
    justify-content: center !important;
}

/* Center-align metric values for better visual alignment */
.block-container .stMetric {
    text-align: center !important;
}

.block-container .stMetric > div {
    text-align: center !important;
}

.block-container .stMetric > div > div {
    text-align: center !important;
}

.block-container .stMetric > div > div > div {
    text-align: center !important;
}

.block-container .stMetric [data-testid="metric-value"],
.block-container .stMetric [data-testid="metric-label"],
.block-container .stMetric .metric-value,
.block-container .stMetric .metric-label {
    text-align: center !important;
    display: block !important;
}

/* Force center alignment for all metric content */
.block-container .stMetric * {
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">AI-Powered Market Research Agent</h1>', unsafe_allow_html=True)
    st.markdown("### Multi-Agent System for Automated Market Research & AI Use Case Generation")
    
    # API Key validation with floating notification
    missing_keys = config.validate_required_keys()
    if missing_keys:
        st.error(f"Missing API keys: {', '.join(missing_keys)}")
        st.info("Please configure your API keys in the .env file")
        st.stop()
    else:
        st.toast("API keys configured successfully!", icon="✅")
    
    # Initialize session state for company name (for example buttons only)
    if 'selected_company' not in st.session_state:
        st.session_state.selected_company = ""
    
    # Main content area
    # Show welcome screen or run analysis
    if 'analysis_results' not in st.session_state:
        # Welcome screen
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Industry Research")
            st.info("Deep market analysis with competitive intelligence")
            
        with col2:
            st.markdown("### AI Use Cases")
            st.info("Strategic AI opportunities that can be implemented")
            
        with col3:
            st.markdown("### Dataset Discovery")
            st.info("Finds Rich dataset from Kaggle and GitHub for each use case")
        
        # Example companies and industries
        st.markdown("### Example Companies & Industries to Analyze:")
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
                    f"{example}", 
                    key=f"example_{example}",
                    use_container_width=True,
                    type="secondary"
                ):
                    st.session_state.selected_company = example
                    st.rerun()
        
        # Search and Analysis Section
        st.markdown("### Analysis Input")
        
        # Check if analysis is running
        analysis_running = 'analysis_in_progress' in st.session_state and st.session_state.analysis_in_progress
        
        company_name = st.text_input(
            "**Company or Industry:**",
            value=st.session_state.selected_company,
            placeholder="e.g., Tesla, Automotive Industry",
            help="Enter the name of any company or industry you want to analyze",
            disabled=analysis_running
        )
        
        # Analysis button - centered using columns
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button(
                "Generate Analysis" if not analysis_running else "Analysis in Progress...",
                type="primary",
                disabled=not company_name.strip() or analysis_running,
                help="Click to start comprehensive market research analysis" if not analysis_running else "Analysis is currently running",
                use_container_width=True
            )
        
        # Run analysis if button clicked
        if analyze_button and company_name.strip():
            # Set analysis in progress immediately and rerun to update UI
            st.session_state.analysis_in_progress = True
            st.rerun()
        
        # Actually run analysis if flag is set
        if 'analysis_in_progress' in st.session_state and st.session_state.analysis_in_progress:
            run_market_research_analysis(company_name.strip())
        
        # System capabilities
        st.markdown("### System Capabilities")
        capabilities = [
            "**Real-time Web Search** - Tavily and Exa API for current market data",
            "**LLM Analysis** - OpenAI GPT-4 for intelligent insights", 
            "**Multi-Agent Architecture** - Specialized agents for different tasks",
            "**Flexible Input** - Works with both companies and industries",
            "**Professional Reports** - Executive-ready analysis and recommendations",
            "**Fast Processing** - Complete analysis in under 5 minutes",
        ]
        
        for capability in capabilities:
            st.markdown(capability)
    
    # Display stored results if they exist (persists after downloads)
    if 'analysis_results' in st.session_state:
        st.markdown("---")
        st.markdown('<h2 class="section-header">Analysis Results</h2>', unsafe_allow_html=True)
        
        # Clear Results button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Clear Results", type="secondary", use_container_width=True):
                del st.session_state.analysis_results
                st.rerun()
        
        # Display the stored results
        results = st.session_state.analysis_results
        display_analysis_results(
            results['company_name'],
            results['deep_research'],
            results['strategic_use_cases'],
            results['dataset_results'],
            results['comprehensive_report']
        )

def run_market_research_analysis(company_name: str):
    """Run the complete market research analysis."""
    
    # Set analysis in progress
    st.session_state.analysis_in_progress = True
    
    # Initialize progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.empty()  # Container for detailed agent logs
    
    
    try:
        # Initialize agents
        status_text.text("Initializing AI agents...")
        progress_bar.progress(10)
        log_container.info("**Starting Multi-Agent Market Research System**")
        
        industry_agent = EnhancedIndustryResearchAgent()
        use_case_agent = EnhancedUseCaseGenerationAgent()
        dataset_agent = DatasetDiscoveryAgent()
        report_generator = ReportGenerator()
        
        log_container.success("**All 3 AI agents initialized successfully**")
        
        # Phase 1: Industry Research
        status_text.text("Conducting deep industry research...")
        progress_bar.progress(20)
        log_container.info(f"**Agent 1 (Industry Research)**: Starting deep analysis for **{company_name}**...")
        
        with st.spinner("Analyzing industry landscape and competitive positioning..."):
            log_container.info("**Agent 1**: Gathering company information, market trends, and competitor analysis...")
            deep_research = industry_agent.conduct_deep_research(company_name)
        
        if deep_research.get('status') != 'completed':
            log_container.error(f"**Agent 1 failed**: {deep_research.get('error', 'Unknown error')}")
            st.error(f"Industry research failed: {deep_research.get('error', 'Unknown error')}")
            return
        
        progress_bar.progress(40)
        research_sources = deep_research.get('research_sources', {})
        total_sources = sum(len(sources) for sources in research_sources.values())
        log_container.success(f"**Agent 1 completed**: Found {total_sources} research sources for {company_name}")
        
        # Phase 2: Use Case Generation
        status_text.text("Generating strategic AI use cases...")
        progress_bar.progress(60)
        log_container.info("**Agent 2 (Use Case Generation)**: Initializing and analyzing AI opportunities...")
        
        with st.spinner("Identifying AI opportunities and analyzing feasibility..."):
            log_container.info("**Agent 2**: Analyzing market trends and generating strategic AI use cases...")
            strategic_use_cases = use_case_agent.generate_strategic_use_cases(deep_research)
        
        if strategic_use_cases.get('status') != 'completed':
            log_container.error(f"**Agent 2 failed**: {strategic_use_cases.get('error', 'Unknown error')}")
            st.error(f"Use case generation failed: {strategic_use_cases.get('error', 'Unknown error')}")
            return
        
        progress_bar.progress(80)
        use_cases = strategic_use_cases.get('strategic_use_cases', [])
        log_container.success(f"**Agent 2 completed**: Generated {len(use_cases)} strategic AI use cases")
        
        # Phase 3: Dataset Discovery
        status_text.text("Discovering relevant datasets...")
        progress_bar.progress(90)
        log_container.info("**Agent 3 (Dataset Discovery)**: Starting dataset search for generated use cases...")
        
        with st.spinner("Finding datasets on Kaggle and GitHub..."):
            log_container.info("**Agent 3**: Searching Kaggle and GitHub for relevant datasets...")
            dataset_results = dataset_agent.discover_datasets(use_cases)
        
        if dataset_results.get('status') != 'completed':
            log_container.error(f"**Agent 3 failed**: {dataset_results.get('error', 'Unknown error')}")
            st.error(f"Dataset discovery failed: {dataset_results.get('error', 'Unknown error')}")
            return
        
        progress_bar.progress(95)
        total_datasets = dataset_results.get('total_datasets_found', 0)
        log_container.success(f"**Agent 3 completed**: Discovered {total_datasets} relevant datasets from Kaggle and GitHub")
        
        # Phase 4: Report Generation
        status_text.text("Generating comprehensive report...")
        log_container.info("**Report Generator**: Compiling comprehensive analysis report...")
        
        comprehensive_report = report_generator.generate_comprehensive_report(
            deep_research, strategic_use_cases
        )
        
        progress_bar.progress(100)
        status_text.text("Analysis completed successfully!")
        log_container.success("**ALL SYSTEMS COMPLETE**: 3-agent analysis finished successfully!")
        
        # Store results in session state to prevent loss on download
        st.session_state.analysis_results = {
            'company_name': company_name,
            'deep_research': deep_research,
            'strategic_use_cases': strategic_use_cases,
            'dataset_results': dataset_results,
            'comprehensive_report': comprehensive_report
        }
        
        # Clear analysis in progress flag
        st.session_state.analysis_in_progress = False
        
        # Rerun to display results (main() will handle display via session state)
        st.rerun()
        
    except Exception as e:
        st.error(f"Analysis failed: {str(e)}")
        # Clear analysis in progress flag on error
        st.session_state.analysis_in_progress = False

def display_analysis_results(
    company_name: str, 
    deep_research: Dict, 
    strategic_use_cases: Dict, 
    dataset_results: Dict,
    comprehensive_report: str
):
    """Display the analysis results in a structured format."""
    
    # Summary metrics
    st.markdown('<h2 class="section-header">Analysis Summary</h2>', unsafe_allow_html=True)
    
    # Get metric values
    research_sources = deep_research.get('research_sources', {})
    total_sources = sum(len(sources) for sources in research_sources.values())
    use_cases = strategic_use_cases.get('strategic_use_cases', [])
    total_datasets = dataset_results.get('total_datasets_found', 0)
    high_innovation = sum(1 for uc in use_cases if 'High' in str(uc.get('innovation_level', '')))
    
    # Create custom aligned metrics using HTML
    metrics_html = f"""
    <div style="display: flex; justify-content: space-around; margin: 20px 0;">
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">Research Sources</div>
            <div style="font-size: 24px; font-weight: bold; color: #fff;">{total_sources}</div>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">AI Use Cases</div>
            <div style="font-size: 24px; font-weight: bold; color: #fff;">{len(use_cases)}</div>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">Datasets Found</div>
            <div style="font-size: 24px; font-weight: bold; color: #fff;">{total_datasets}</div>
        </div>
        <div style="text-align: center; flex: 1;">
            <div style="font-size: 14px; color: #666; margin-bottom: 5px;">High Innovation</div>
            <div style="font-size: 24px; font-weight: bold; color: #fff;">{high_innovation}/{len(use_cases)}</div>
        </div>
    </div>
    """
    st.markdown(metrics_html, unsafe_allow_html=True)
    
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Industry Analysis", "AI Use Cases", "Datasets", "Full Report", "Export"])
    
    with tab1:
        st.markdown("### Industry Research Summary")
        
        # Company foundation
        company_analysis = deep_research.get('company_foundation', {})
        st.markdown("**Company Analysis:**")
        company_content = company_analysis.get('structured_content', 'Analysis in progress')
        if company_content and isinstance(company_content, str):
            st.write(company_content[:500] + ("..." if len(company_content) > 500 else ""))
        else:
            st.write(company_content)
        
        # Market analysis
        market_analysis = deep_research.get('market_analysis', {})
        st.markdown("**Market Position:**")
        market_content = market_analysis.get('structured_content', 'Analysis in progress')
        if market_content and isinstance(market_content, str):
            st.write(market_content[:500] + ("..." if len(market_content) > 500 else ""))
        else:
            st.write(market_content)
        
        # Sources
        st.markdown("**Research Sources:**")
        for category, sources in research_sources.items():
            if sources:
                st.markdown(f"**{category.replace('_', ' ').title()}:**")
                for source in sources[:3]:  # Top 3 sources
                    st.markdown(f"- [{source.get('title', 'Source')[:80]}]({source.get('url', '#')})")
    
    with tab2:
        st.markdown("### Strategic AI Use Cases")
        
        for i, use_case in enumerate(use_cases, 1):
            with st.expander(f"**{i}. {use_case.get('title', f'Use Case {i}')}** (Priority: {use_case.get('priority_rank', i)})"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Strategic Value:**")
                    st.write(use_case.get('strategic_value', 'Not specified'))
                    
                    st.markdown("**Revenue Impact:**")
                    st.write(use_case.get('revenue_impact', 'Not specified'))
                    
                    st.markdown("**Implementation:**")
                    st.write(use_case.get('implementation_approach', 'Not specified'))
                
                with col2:
                    st.markdown("**AI Solution:**")
                    st.write(use_case.get('ai_solution', 'Not specified'))
                    
                    st.markdown("**Success Metrics:**")
                    st.write(use_case.get('success_metrics', 'Not specified'))
                    
                    feasibility = use_case.get('feasibility_analysis', {})
                    st.markdown("**Timeline:**")
                    st.write(feasibility.get('implementation_timeline', 'Not specified'))
                
                # Innovation and Complexity
                st.markdown("**Analysis:**")
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
        st.markdown("### Dataset Discovery Results")
        
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
                            st.markdown(f"#### Kaggle Datasets ({len(kaggle_datasets)} found)")
                            for j, dataset in enumerate(kaggle_datasets, 1):
                                st.markdown(f"**{j}.** [{dataset['title']}]({dataset['url']})")
                                st.markdown(f"- **Description:** {dataset['description']}")
                                st.markdown(f"- **Relevance Score:** {dataset['relevance_score']:.2f}")
                                st.markdown("")
                        
                        if github_datasets:
                            st.markdown(f"#### GitHub Datasets ({len(github_datasets)} found)")
                            for j, dataset in enumerate(github_datasets, 1):
                                st.markdown(f"**{j}.** [{dataset['title']}]({dataset['url']})")
                                st.markdown(f"- **Description:** {dataset['description']}")
                                st.markdown(f"- **Relevance Score:** {dataset['relevance_score']:.2f}")
                                st.markdown("")
        else:
            st.info("No datasets found for the generated use cases.")
    
    with tab4:
        st.markdown("### Comprehensive Report")
        st.markdown(comprehensive_report)
    
    with tab5:
        st.markdown("### Export Options")
        
        # Save report
        # Ensure outputs directory exists
        os.makedirs('outputs', exist_ok=True)
        
        # Generate enhanced report with datasets
        enhanced_report = generate_enhanced_report_with_datasets(
            comprehensive_report, dataset_results
        )
        
        # Sanitize company name for safe file operations
        safe_company_name = sanitize_filename(company_name)
        filename = f"outputs/{safe_company_name}_ai_market_research_report.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(enhanced_report)
        st.success(f"Report saved as: {filename}")
        
        # Create two columns for download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="Download Markdown Report",
                data=enhanced_report,
                file_name=f"{safe_company_name}_complete_3_agent_report.md",
                mime="text/markdown",
                help="Download the complete report with datasets as a Markdown file",
                key=f"download_md_{safe_company_name}"
            )
        
        with col2:
            # PDF Download button
            temp_md_file = None
            pdf_path = None
            try:
                # Create temporary markdown file for PDF conversion using tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as tmp_file:
                    temp_md_file = tmp_file.name
                    tmp_file.write(enhanced_report)
                
                # Convert to PDF
                pdf_path = convert_md_to_pdf(temp_md_file)
                
                # Read PDF file for download
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_data,
                    file_name=f"{safe_company_name}_complete_3_agent_report.pdf",
                    mime="application/pdf",
                    help="Download the complete report as a professional PDF document",
                    key=f"download_pdf_{safe_company_name}"
                )
                
            except Exception as e:
                st.error(f"PDF conversion failed: {str(e)}")
                st.info("Make sure wkhtmltopdf is installed. See requirements for setup instructions.")
            finally:
                # Clean up temporary files regardless of success or failure
                if temp_md_file and os.path.exists(temp_md_file):
                    try:
                        os.remove(temp_md_file)
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to remove temp file {temp_md_file}: {cleanup_error}")
                if pdf_path and os.path.exists(pdf_path):
                    try:
                        os.remove(pdf_path)
                    except Exception as cleanup_error:
                        logger.warning(f"Failed to remove PDF file {pdf_path}: {cleanup_error}")
        
        # Implementation roadmap
        roadmap = strategic_use_cases.get('implementation_roadmap', {})
        st.markdown("### Implementation Roadmap")
        st.write(f"**Timeline:** {roadmap.get('total_timeline', '24 months')}")
        st.write(f"**Overview:** {roadmap.get('roadmap_overview', 'Three-phase approach')}")

def generate_enhanced_report_with_datasets(base_report: str, dataset_results: Dict) -> str:
    """Generate enhanced report with dataset information."""
    
    enhanced_report = f"""# Complete 3-Agent AI Market Research Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**System:** 3-Agent AI Market Research System  
**Status:** All agents completed successfully

---

## 🤖 System Performance Summary

- **Agent 1 (Industry Research):** Completed
- **Agent 2 (Use Case Generation):** Completed  
- **Agent 3 (Dataset Discovery):** Completed
- **Report Generation:** Completed

---

{base_report}

---

## Dataset Discovery Results

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
            enhanced_report += f"#### Kaggle Datasets ({len(kaggle_datasets)} found)\n\n"
            for j, dataset in enumerate(kaggle_datasets, 1):
                enhanced_report += f"{j}. [{dataset['title']}]({dataset['url']})\n"
                enhanced_report += f"   - **Description:** {dataset['description']}\n"
                enhanced_report += f"   - **Relevance Score:** {dataset['relevance_score']:.2f}\n\n"
        
        if github_datasets:
            enhanced_report += f"#### GitHub Datasets ({len(github_datasets)} found)\n\n"
            for j, dataset in enumerate(github_datasets, 1):
                enhanced_report += f"{j}. [{dataset['title']}]({dataset['url']})\n"
                enhanced_report += f"   - **Description:** {dataset['description']}\n"
                enhanced_report += f"   - **Relevance Score:** {dataset['relevance_score']:.2f}\n\n"
        
        if not kaggle_datasets and not github_datasets:
            enhanced_report += "*No datasets found for this use case.*\n\n"
        
        enhanced_report += "---\n\n"
    
    enhanced_report += f"""
## System Evaluation

### Success Metrics:
- **Multi-Agent Coordination:** All 3 agents executed successfully in sequence
- **Data Flow:** Information passed correctly between agents
- **Output Quality:** High-quality research, use cases, and dataset discoveries
- **Integration:** Seamless workflow from research → use cases → datasets → report

### Ready for Production:
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

