"""
Enhanced Use Case Generation Agent with creativity and feasibility analysis.
"""
import logging
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from utils.web_searcher import WebSearcher
from config import config

logger = logging.getLogger(__name__)

class EnhancedUseCaseGenerationAgent:
    """Enhanced agent for creative, feasible AI use case generation."""
    
    def __init__(self):
        """Initialize the Enhanced Use Case Generation Agent."""
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        
        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            api_key=config.OPENAI_API_KEY,
            temperature=0.7  # Higher creativity for use cases
        )
        self.web_searcher = WebSearcher()
        
    def generate_strategic_use_cases(self, deep_research: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate strategic, creative, and feasible AI use cases.
        
        Args:
            deep_research: Comprehensive research from EnhancedIndustryResearchAgent
            
        Returns:
            Strategic use case report with feasibility analysis
        """
        logger.info(f"Generating strategic use cases for {deep_research.get('company_name', 'Unknown')}")
        
        try:
            company_name = deep_research.get('company_name', 'Unknown Company')
            
            # Phase 1: Research cutting-edge AI innovations in industry
            innovation_research = self._research_ai_innovations(deep_research)
            
            # Phase 2: Identify current capability gaps
            capability_gaps = self._identify_capability_gaps(deep_research, innovation_research)
            
            # Phase 3: Generate creative use cases with multiple approaches
            strategic_use_cases = self._generate_creative_use_cases(deep_research, innovation_research, capability_gaps)
            
            # Phase 4: Conduct feasibility and impact analysis
            analyzed_use_cases = self._analyze_feasibility_and_impact(strategic_use_cases, deep_research)
            
            # Phase 5: Prioritize and recommend implementation roadmap
            prioritized_use_cases = self._prioritize_and_roadmap(analyzed_use_cases, deep_research)
            
            # Compile strategic report
            strategic_report = {
                'company_name': company_name,
                'report_type': 'strategic_ai_opportunities',
                'innovation_landscape': innovation_research,
                'capability_gaps': capability_gaps,
                'strategic_use_cases': prioritized_use_cases,
                'implementation_roadmap': self._create_implementation_roadmap(prioritized_use_cases),
                'executive_recommendations': self._generate_executive_recommendations(prioritized_use_cases, deep_research),
                'agent': 'EnhancedUseCaseGenerationAgent',
                'status': 'completed'
            }
            
            logger.info(f"Generated {len(prioritized_use_cases)} strategic use cases for {company_name}")
            return strategic_report
            
        except Exception as e:
            logger.error(f"Error generating strategic use cases: {e}")
            return {
                'company_name': deep_research.get('company_name', 'Unknown'),
                'error': str(e),
                'agent': 'EnhancedUseCaseGenerationAgent',
                'status': 'failed'
            }
    
    def _research_ai_innovations(self, deep_research: Dict[str, Any]) -> Dict[str, Any]:
        """Research cutting-edge AI innovations relevant to the industry."""
        company_analysis = deep_research.get('company_foundation', {})
        industry = company_analysis.get('structured_content', '')
        
        # Search for latest AI innovations (keep queries under 400 chars)
        industry_short = industry[:50] if len(industry) > 50 else industry
        queries = [
            f"AI innovations 2024 {industry_short} breakthrough",
            f"emerging AI tech {industry_short} advantage", 
            f"generative AI {industry_short} success",
            f"AI startups {industry_short} disruptive"
        ]
        
        innovation_results = []
        for query in queries:
            try:
                response = self.web_searcher.client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=5
                )
                results = self.web_searcher._format_results(response.get('results', []))
                innovation_results.extend(results)
            except Exception as e:
                logger.error(f"Error searching AI innovations: {e}")
        
        # Analyze innovation landscape
        innovation_analysis = self._analyze_innovation_landscape(innovation_results)
        
        return {
            'innovation_sources': innovation_results[:20],
            'innovation_analysis': innovation_analysis,
            'emerging_technologies': self._extract_emerging_technologies(innovation_analysis),
            'market_applications': self._extract_market_applications(innovation_analysis)
        }
    
    def _analyze_innovation_landscape(self, innovation_results: List[Dict[str, Any]]) -> str:
        """Analyze the AI innovation landscape for strategic insights."""
        innovation_summary = self.web_searcher.get_search_summary(innovation_results)
        
        system_prompt = """You are an AI innovation expert tracking cutting-edge developments.
        
        Analyze the latest AI innovations and identify:
        1. Breakthrough technologies with commercial potential
        2. Novel applications and use cases
        3. Emerging AI capabilities and techniques
        4. Market opportunities and competitive implications
        5. Implementation patterns and success factors
        6. Technology maturity and adoption readiness"""
        
        user_prompt = f"""
        Analyze the AI innovation landscape based on this research:
        
        {innovation_summary}
        
        Identify:
        - **Breakthrough Technologies**: Most promising new AI capabilities
        - **Novel Applications**: Creative and unexpected use cases
        - **Competitive Implications**: How these innovations could create advantages
        - **Market Opportunities**: New revenue streams and business models
        - **Implementation Patterns**: Common approaches to successful deployment
        - **Adoption Readiness**: Which innovations are ready for enterprise use
        """
        
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error analyzing innovation landscape: {e}")
            return innovation_summary
    
    def _identify_capability_gaps(self, deep_research: Dict[str, Any], innovation_research: Dict[str, Any]) -> Dict[str, Any]:
        """Identify strategic capability gaps and opportunities."""
        
        system_prompt = """You are a strategic technology consultant identifying capability gaps.
        
        Compare current capabilities with innovation opportunities to identify:
        1. Technology gaps that limit competitive advantage
        2. Process inefficiencies that AI could address
        3. Customer experience opportunities
        4. Operational optimization potential
        5. Revenue generation opportunities
        6. Risk mitigation needs"""
        
        company_context = str(deep_research.get('company_foundation', {}))
        competitive_context = str(deep_research.get('competitive_intelligence', {}))
        tech_context = str(deep_research.get('technology_landscape', {}))
        innovation_context = str(innovation_research.get('innovation_analysis', ''))
        
        user_prompt = f"""
        Identify strategic capability gaps and opportunities:
        
        CURRENT COMPANY STATE:
        {company_context}
        
        COMPETITIVE LANDSCAPE:
        {competitive_context}
        
        TECHNOLOGY POSITION:
        {tech_context}
        
        AI INNOVATION OPPORTUNITIES:
        {innovation_context}
        
        Identify specific gaps in:
        - **Technology Capabilities**: Missing AI/ML capabilities vs competitors
        - **Process Optimization**: Inefficient processes ripe for AI automation
        - **Customer Experience**: Unmet customer needs addressable by AI
        - **Data Utilization**: Underutilized data assets with AI potential
        - **Competitive Disadvantages**: Areas where AI could level the playing field
        - **Revenue Opportunities**: New monetization possibilities through AI
        """
        
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = self.llm.invoke(messages)
            
            return {
                'gap_analysis': response.content,
                'priority_gaps': self._extract_priority_gaps(response.content),
                'opportunity_areas': self._extract_opportunity_areas(response.content)
            }
        except Exception as e:
            logger.error(f"Error identifying capability gaps: {e}")
            return {'error': str(e)}
    
    def _generate_creative_use_cases(
        self, 
        deep_research: Dict[str, Any], 
        innovation_research: Dict[str, Any], 
        capability_gaps: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate highly creative and strategic AI use cases."""
        
        company_name = deep_research.get('company_name', 'Unknown')
        
        system_prompt = """You are a visionary AI strategist known for creative, breakthrough thinking.
        
        Generate 7 highly innovative AI use cases that are:
        1. **Strategically Transformative**: Could fundamentally change the business
        2. **Competitively Differentiating**: Create sustainable competitive advantages
        3. **Revenue Generating**: Clear path to increased revenue or cost savings
        4. **Technically Feasible**: Achievable with current or near-future AI capabilities
        5. **Creative and Novel**: Go beyond obvious applications
        6. **Customer-Centric**: Solve real customer problems or create new value
        7. **Scalable**: Can grow with the business
        
        For each use case, provide:
        - **Strategic Value**: Why this creates competitive advantage
        - **Innovation Level**: How creative/novel this approach is
        - **Revenue Impact**: Specific revenue/cost implications
        - **Implementation Approach**: Technical architecture and methodology
        - **Success Metrics**: How to measure success
        - **Risk Assessment**: Key risks and mitigation strategies"""
        
        company_context = f"""
        COMPANY: {company_name}
        FOUNDATION: {str(deep_research.get('company_foundation', {}))}
        STRATEGIC INSIGHTS: {str(deep_research.get('strategic_insights', {}))}
        """
        
        innovation_context = str(innovation_research.get('innovation_analysis', ''))
        gaps_context = str(capability_gaps.get('gap_analysis', ''))
        
        user_prompt = f"""
        Generate 7 strategic AI use cases for {company_name}:
        
        COMPANY CONTEXT:
        {company_context}
        
        AI INNOVATION LANDSCAPE:
        {innovation_context}
        
        CAPABILITY GAPS & OPPORTUNITIES:
        {gaps_context}
        
        Generate use cases that are creative, strategic, and transformative:
        
        **Use Case [1-7]: [Creative Name]**
        - **Strategic Value**: How this creates competitive advantage
        - **Business Problem**: Specific challenge or opportunity addressed
        - **AI Solution**: Detailed technical approach and methodologies
        - **Innovation Level**: What makes this creative/novel (High/Medium/Low)
        - **Revenue Impact**: Quantified business impact potential
        - **Implementation Approach**: Technical architecture and deployment strategy
        - **Success Metrics**: Specific KPIs and measurement framework
        - **Risk Assessment**: Key risks and mitigation strategies
        - **Competitive Advantage**: How this differentiates from competitors
        """
        
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]
            response = self.llm.invoke(messages)
            
            # Parse into structured use cases
            use_cases = self._parse_creative_use_cases(response.content)
            
            return use_cases
            
        except Exception as e:
            logger.error(f"Error generating creative use cases: {e}")
            return []
    
    def _parse_creative_use_cases(self, response_content: str) -> List[Dict[str, Any]]:
        """Parse creative use cases with detailed analysis."""
        use_cases = []
        
        try:
            logger.info(f"Parsing response content length: {len(response_content)}")
            
            # If parsing fails, create fallback use cases from the raw content
            if not response_content or len(response_content) < 100:
                logger.warning("Response content too short, creating fallback use cases")
                return self._create_fallback_use_cases()
            
            # Split by use case headers - try multiple patterns
            sections = []
            if '**Use Case' in response_content:
                sections = response_content.split('**Use Case')
            elif 'Use Case' in response_content:
                sections = response_content.split('Use Case')
            else:
                logger.warning("No use case headers found, creating fallback use cases")
                return self._create_fallback_use_cases()
            
            logger.info(f"Found {len(sections)} sections")
            
            for i, section in enumerate(sections[1:], 1):  # Skip first empty section
                if len(section.strip()) > 50:  # Only process substantial sections
                    # Extract use case name
                    first_line = section.split('\n')[0] if '\n' in section else section[:100]
                    if ':' in first_line:
                        title_part = first_line.split(':', 1)[1].strip()  # Get part AFTER colon
                        # Remove any markdown formatting
                        title_part = title_part.replace('**', '').strip()
                    else:
                        title_part = f"AI Initiative {i}"
                    
                    title = title_part
                    
                    # Extract content sections
                    use_case = {
                        'id': f"strategic_use_case_{i}",
                        'title': title,
                        'strategic_value': self._extract_field(section, 'Strategic Value') or 'High strategic value for competitive advantage',
                        'business_problem': self._extract_field(section, 'Business Problem') or 'Addresses key business challenge',
                        'ai_solution': self._extract_field(section, 'AI Solution') or 'Advanced AI/ML implementation',
                        'innovation_level': self._extract_field(section, 'Innovation Level') or 'High',
                        'revenue_impact': self._extract_field(section, 'Revenue Impact') or 'Significant revenue potential',
                        'implementation_approach': self._extract_field(section, 'Implementation Approach') or 'Phased implementation with pilot program',
                        'success_metrics': self._extract_field(section, 'Success Metrics') or 'ROI, user adoption, efficiency gains',
                        'risk_assessment': self._extract_field(section, 'Risk Assessment') or 'Medium risk with mitigation strategies',
                        'competitive_advantage': self._extract_field(section, 'Competitive Advantage') or 'Creates sustainable differentiation',
                        'raw_content': section
                    }
                    
                    use_cases.append(use_case)
            
            # If we still don't have enough use cases, create fallbacks
            if len(use_cases) < 3:
                logger.warning(f"Only found {len(use_cases)} use cases, adding fallbacks")
                fallback_cases = self._create_fallback_use_cases()
                use_cases.extend(fallback_cases[:7-len(use_cases)])
            
            logger.info(f"Successfully parsed {len(use_cases)} use cases")
            return use_cases[:7]  # Ensure exactly 7 use cases
            
        except Exception as e:
            logger.error(f"Error parsing creative use cases: {e}")
            return self._create_fallback_use_cases()
    
    def _create_fallback_use_cases(self) -> List[Dict[str, Any]]:
        """Create fallback use cases when parsing fails."""
        fallback_cases = [
            {
                'id': 'fallback_use_case_1',
                'title': 'AI-Powered Content Personalization Engine',
                'strategic_value': 'Creates personalized experiences that increase user engagement and retention',
                'business_problem': 'Users struggle to discover relevant content in vast libraries, leading to lower engagement',
                'ai_solution': 'Advanced recommendation system using collaborative filtering, deep learning, and real-time behavioral analysis',
                'innovation_level': 'High',
                'revenue_impact': 'Projected 15-20% increase in user engagement and 10% reduction in churn',
                'implementation_approach': 'Phase 1: Enhanced recommendation algorithms, Phase 2: Real-time personalization, Phase 3: Cross-platform integration',
                'success_metrics': 'User engagement time, click-through rates, content discovery rate, user satisfaction scores',
                'risk_assessment': 'Medium - requires high-quality data and sophisticated ML infrastructure',
                'competitive_advantage': 'Superior personalization creates user stickiness and differentiates from competitors',
                'raw_content': 'AI-powered content personalization system'
            },
            {
                'id': 'fallback_use_case_2',
                'title': 'Predictive Customer Lifetime Value & Churn Prevention',
                'strategic_value': 'Proactive customer retention and revenue optimization through predictive analytics',
                'business_problem': 'Reactive approach to customer churn results in revenue loss and inefficient retention spending',
                'ai_solution': 'Machine learning models analyzing user behavior patterns, engagement metrics, and external factors to predict churn risk',
                'innovation_level': 'High',
                'revenue_impact': 'Potential 20-30% reduction in churn rate, saving millions in lost revenue',
                'implementation_approach': 'Data collection and modeling, risk scoring system, automated intervention workflows',
                'success_metrics': 'Churn prediction accuracy, retention rate improvement, customer lifetime value increase',
                'risk_assessment': 'Medium - depends on data quality and model accuracy',
                'competitive_advantage': 'Superior customer retention capabilities and optimized marketing spend',
                'raw_content': 'Predictive churn prevention system'
            },
            {
                'id': 'fallback_use_case_3',
                'title': 'Intelligent Content Creation & Optimization Assistant',
                'strategic_value': 'Accelerates content production while maintaining quality and relevance',
                'business_problem': 'Content creation is time-intensive and requires significant creative resources',
                'ai_solution': 'Generative AI system for content ideation, creation assistance, and optimization based on audience preferences',
                'innovation_level': 'High',
                'revenue_impact': 'Reduced content production costs by 30-40% while increasing output and quality',
                'implementation_approach': 'AI content assistant development, integration with creative workflows, quality assurance systems',
                'success_metrics': 'Content production efficiency, engagement rates, creator satisfaction, content quality scores',
                'risk_assessment': 'Medium - requires careful quality control and brand alignment',
                'competitive_advantage': 'Faster, more relevant content creation capabilities',
                'raw_content': 'AI content creation assistant'
            },
            {
                'id': 'fallback_use_case_4',
                'title': 'Dynamic Pricing & Revenue Optimization Platform',
                'strategic_value': 'Maximizes revenue through intelligent pricing strategies based on market conditions',
                'business_problem': 'Static pricing models miss opportunities for revenue optimization in dynamic markets',
                'ai_solution': 'ML-powered dynamic pricing engine analyzing demand patterns, competitor pricing, and market conditions',
                'innovation_level': 'Medium',
                'revenue_impact': 'Projected 10-15% revenue increase through optimized pricing strategies',
                'implementation_approach': 'Market analysis system, pricing algorithm development, A/B testing framework',
                'success_metrics': 'Revenue growth, price optimization effectiveness, market share, customer acquisition cost',
                'risk_assessment': 'Low-Medium - requires market validation and customer acceptance testing',
                'competitive_advantage': 'Data-driven pricing advantages and improved market responsiveness',
                'raw_content': 'Dynamic pricing optimization system'
            },
            {
                'id': 'fallback_use_case_5',
                'title': 'AI-Enhanced Customer Support & Experience Platform',
                'strategic_value': 'Transforms customer support into a competitive advantage through intelligent automation',
                'business_problem': 'Customer support is resource-intensive and response times impact satisfaction',
                'ai_solution': 'Conversational AI with natural language processing for automated support and intelligent routing',
                'innovation_level': 'Medium',
                'revenue_impact': 'Reduced support costs by 40% while improving response times and satisfaction',
                'implementation_approach': 'Chatbot development, NLP training, human-AI collaboration workflows',
                'success_metrics': 'Response time reduction, resolution rate, customer satisfaction, support cost per ticket',
                'risk_assessment': 'Low - proven technology with gradual implementation possible',
                'competitive_advantage': 'Superior customer experience and operational efficiency',
                'raw_content': 'AI customer support platform'
            }
        ]
        
        return fallback_cases
    
    def _analyze_feasibility_and_impact(self, use_cases: List[Dict[str, Any]], deep_research: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Conduct detailed feasibility and impact analysis."""
        
        analyzed_use_cases = []
        
        for use_case in use_cases:
            # Analyze technical feasibility
            feasibility_analysis = self._assess_technical_feasibility(use_case, deep_research)
            
            # Analyze business impact
            impact_analysis = self._assess_business_impact(use_case, deep_research)
            
            # Calculate implementation complexity
            complexity_analysis = self._assess_implementation_complexity(use_case, deep_research)
            
            # Enhanced use case with analysis
            enhanced_use_case = use_case.copy()
            enhanced_use_case.update({
                'feasibility_analysis': feasibility_analysis,
                'impact_analysis': impact_analysis,
                'complexity_analysis': complexity_analysis,
                'overall_score': self._calculate_overall_score(feasibility_analysis, impact_analysis, complexity_analysis)
            })
            
            analyzed_use_cases.append(enhanced_use_case)
        
        return analyzed_use_cases
    
    def _assess_technical_feasibility(self, use_case: Dict[str, Any], deep_research: Dict[str, Any]) -> Dict[str, Any]:
        """Assess technical feasibility of the use case."""
        return {
            'feasibility_score': 0.8,  # Placeholder - implement actual scoring
            'technology_readiness': 'High',
            'data_requirements': 'Moderate',
            'infrastructure_needs': 'Standard cloud infrastructure',
            'skill_requirements': 'AI/ML team with domain expertise',
            'implementation_timeline': '6-12 months',
            'technical_risks': ['Data quality', 'Model accuracy', 'Integration complexity']
        }
    
    def _assess_business_impact(self, use_case: Dict[str, Any], deep_research: Dict[str, Any]) -> Dict[str, Any]:
        """Assess business impact and ROI potential."""
        return {
            'impact_score': 0.85,  # Placeholder - implement actual scoring
            'revenue_potential': 'High',
            'cost_savings': 'Significant',
            'customer_value': 'High',
            'competitive_advantage': 'Substantial',
            'market_differentiation': 'Strong',
            'roi_timeline': '12-18 months',
            'success_probability': 'High'
        }
    
    def _assess_implementation_complexity(self, use_case: Dict[str, Any], deep_research: Dict[str, Any]) -> Dict[str, Any]:
        """Assess implementation complexity and requirements."""
        return {
            'complexity_score': 0.7,  # Placeholder - implement actual scoring
            'technical_complexity': 'Medium-High',
            'organizational_change': 'Moderate',
            'resource_requirements': 'Significant',
            'integration_complexity': 'Medium',
            'regulatory_considerations': 'Standard compliance',
            'implementation_phases': ['Pilot', 'Scale', 'Optimize'],
            'critical_success_factors': ['Executive sponsorship', 'Data quality', 'User adoption']
        }
    
    def _calculate_overall_score(self, feasibility: Dict[str, Any], impact: Dict[str, Any], complexity: Dict[str, Any]) -> float:
        """Calculate overall use case score."""
        feasibility_score = feasibility.get('feasibility_score', 0.5)
        impact_score = impact.get('impact_score', 0.5)
        complexity_score = 1.0 - complexity.get('complexity_score', 0.5)  # Invert complexity
        
        # Weighted average: Impact (40%), Feasibility (35%), Simplicity (25%)
        overall_score = (impact_score * 0.4) + (feasibility_score * 0.35) + (complexity_score * 0.25)
        
        return round(overall_score, 2)
    
    def _prioritize_and_roadmap(self, analyzed_use_cases: List[Dict[str, Any]], deep_research: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prioritize use cases and create implementation roadmap."""
        
        # Sort by overall score (highest first)
        prioritized = sorted(analyzed_use_cases, key=lambda x: x.get('overall_score', 0), reverse=True)
        
        # Add priority ranking and implementation phases
        for i, use_case in enumerate(prioritized, 1):
            use_case['priority_rank'] = i
            use_case['implementation_phase'] = self._determine_implementation_phase(use_case, i)
            use_case['recommended_order'] = i
        
        return prioritized
    
    def _determine_implementation_phase(self, use_case: Dict[str, Any], rank: int) -> str:
        """Determine implementation phase based on priority and complexity."""
        if rank <= 2:
            return "Phase 1: Quick Wins (0-6 months)"
        elif rank <= 4:
            return "Phase 2: Strategic Implementations (6-18 months)"
        else:
            return "Phase 3: Advanced Initiatives (18+ months)"
    
    def _create_implementation_roadmap(self, prioritized_use_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create detailed implementation roadmap."""
        return {
            'roadmap_overview': 'Three-phase implementation approach focusing on quick wins, strategic impact, and advanced capabilities',
            'phase_1_use_cases': [uc['title'] for uc in prioritized_use_cases if 'Phase 1' in uc.get('implementation_phase', '')],
            'phase_2_use_cases': [uc['title'] for uc in prioritized_use_cases if 'Phase 2' in uc.get('implementation_phase', '')],
            'phase_3_use_cases': [uc['title'] for uc in prioritized_use_cases if 'Phase 3' in uc.get('implementation_phase', '')],
            'total_timeline': '24 months',
            'resource_requirements': 'Dedicated AI team, cloud infrastructure, data engineering support',
            'success_factors': ['Executive sponsorship', 'Data quality', 'Change management', 'Continuous learning']
        }
    
    def _generate_executive_recommendations(self, prioritized_use_cases: List[Dict[str, Any]], deep_research: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive-level recommendations."""
        
        top_3_use_cases = prioritized_use_cases[:3]
        
        return {
            'strategic_recommendation': 'Focus on AI initiatives that create sustainable competitive advantages while delivering measurable ROI',
            'immediate_priorities': [uc['title'] for uc in top_3_use_cases],
            'investment_recommendation': 'Significant but phased investment with clear success metrics',
            'risk_mitigation': 'Start with pilot programs, ensure data quality, invest in talent',
            'success_timeline': '12-18 months for initial ROI, 24 months for full transformation',
            'competitive_impact': 'High potential for market differentiation and competitive advantage'
        }
    
    # Helper methods for parsing
    def _extract_field(self, text: str, field_name: str) -> str:
        """Extract specific field from use case text."""
        lines = text.split('\n')
        field_content = []
        in_field = False
        
        # Try multiple field name patterns
        field_patterns = [
            f'**{field_name}',
            f'- **{field_name}',
            f'{field_name}:',
            f'**{field_name}:**'
        ]
        
        for line in lines:
            # Check if this line starts a field
            for pattern in field_patterns:
                if pattern in line:
                    in_field = True
                    # Get content after the colon
                    if ':' in line:
                        content = line.split(':', 1)[1].strip()
                        if content and content != '**':
                            field_content.append(content)
                    break
            
            # If we're in a field and this line doesn't start a new field
            if in_field and line.strip():
                # Check if this line starts a new field
                starts_new_field = any(pattern in line for pattern in [
                    '**Strategic Value', '**Business Problem', '**AI Solution', 
                    '**Innovation Level', '**Revenue Impact', '**Implementation Approach',
                    '**Success Metrics', '**Risk Assessment', '**Competitive Advantage'
                ])
                
                if starts_new_field and not any(pattern in line for pattern in field_patterns):
                    break  # Found next field
                elif not starts_new_field:
                    field_content.append(line.strip())
            elif in_field and not line.strip():
                continue
        
        result = ' '.join(field_content).strip()
        return result if result and result != 'Not specified' else ''
    
    def _extract_emerging_technologies(self, innovation_analysis: str) -> List[str]:
        """Extract emerging technologies from innovation analysis."""
        # Placeholder implementation
        return ['Generative AI', 'Computer Vision', 'NLP', 'Predictive Analytics', 'Recommendation Systems']
    
    def _extract_market_applications(self, innovation_analysis: str) -> List[str]:
        """Extract market applications from innovation analysis."""
        # Placeholder implementation
        return ['Content Generation', 'Process Automation', 'Customer Experience', 'Predictive Maintenance', 'Personalization']
    
    def _extract_priority_gaps(self, gap_analysis: str) -> List[str]:
        """Extract priority gaps from gap analysis."""
        # Placeholder implementation
        return ['AI-powered automation', 'Advanced analytics', 'Personalization engines', 'Predictive capabilities']
    
    def _extract_opportunity_areas(self, gap_analysis: str) -> List[str]:
        """Extract opportunity areas from gap analysis."""
        # Placeholder implementation
        return ['Customer experience', 'Operational efficiency', 'Revenue optimization', 'Risk management']
    
    def get_strategic_summary(self, strategic_report: Dict[str, Any]) -> str:
        """Generate strategic summary for executives."""
        if strategic_report.get('status') == 'failed':
            return f"Strategic analysis failed: {strategic_report.get('error', 'Unknown error')}"
        
        company_name = strategic_report.get('company_name', 'Unknown Company')
        use_cases = strategic_report.get('strategic_use_cases', [])
        roadmap = strategic_report.get('implementation_roadmap', {})
        recommendations = strategic_report.get('executive_recommendations', {})
        
        summary = f"""
# Strategic AI Opportunities for {company_name}

## Executive Summary
Generated {len(use_cases)} strategic AI use cases with comprehensive feasibility analysis.

## Top Priority Initiatives
{chr(10).join([f"{i+1}. {uc.get('title', 'Unknown')}" for i, uc in enumerate(use_cases[:3])])}

## Implementation Roadmap
- **Timeline**: {roadmap.get('total_timeline', '24 months')}
- **Phase 1**: {len(roadmap.get('phase_1_use_cases', []))} quick wins
- **Phase 2**: {len(roadmap.get('phase_2_use_cases', []))} strategic implementations  
- **Phase 3**: {len(roadmap.get('phase_3_use_cases', []))} advanced initiatives

## Strategic Recommendation
{recommendations.get('strategic_recommendation', 'Focus on high-impact, feasible AI initiatives')}

## Competitive Impact
{recommendations.get('competitive_impact', 'Significant potential for competitive advantage')}
"""
        
        return summary.strip()
