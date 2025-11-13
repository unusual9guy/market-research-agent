"""
Dataset Discovery Agent - FINAL VERSION

This agent ONLY searches for datasets on:
1. Kaggle
2. GitHub 
3. HuggingFace

NO OTHER WEBSITES OR SOURCES!
"""

import logging
import requests
import os
from typing import List, Dict, Any
from datetime import datetime
from utils.web_searcher import WebSearcher
from utils.exa_searcher import ExaSearcher
from config import config

# Set up logging
logging.basicConfig(level=logging.WARNING)  # Reduce noise
logger = logging.getLogger(__name__)

class DatasetDiscoveryAgent:
    """
    Dataset Discovery Agent that ONLY searches:
    - Kaggle datasets
    - GitHub datasets
    """
    
    def __init__(self):
        """Initialize the Dataset Discovery Agent."""
        self.tavily_searcher = WebSearcher()  # Tavily for general search
        self.exa_searcher = ExaSearcher()     # Exa for better content
        self.github_token = config.GITHUB_TOKEN
        
    def discover_datasets(self, use_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Discover datasets for use cases from ONLY Kaggle and GitHub.
        
        Args:
            use_cases: List of use case dictionaries from Agent 2
            
        Returns:
            Dictionary with discovered datasets
        """
        try:
            logger.info(f"Starting dataset discovery for {len(use_cases)} use cases")
            
            all_results = {
                'status': 'completed',
                'total_use_cases': len(use_cases),
                'total_datasets_found': 0,
                'use_case_datasets': [],
                'timestamp': datetime.now().isoformat()
            }
            
            for i, use_case in enumerate(use_cases, 1):
                use_case_title = use_case.get('title', f'Use Case {i}')
                ai_solution = use_case.get('ai_solution', '')
                
                print(f"🔍 Searching datasets for: {use_case_title}")
                
                # Search platforms (Kaggle and GitHub only)
                kaggle_datasets = self._search_kaggle_datasets(use_case_title, ai_solution)
                github_datasets = self._search_github_datasets(use_case_title, ai_solution)
                
                # Combine datasets
                all_datasets = kaggle_datasets + github_datasets
                
                use_case_result = {
                    'use_case_title': use_case_title,
                    'ai_solution': ai_solution,
                    'kaggle_datasets': kaggle_datasets,
                    'github_datasets': github_datasets,
                    'total_datasets': len(all_datasets),
                    'all_datasets': all_datasets
                }
                
                all_results['use_case_datasets'].append(use_case_result)
                all_results['total_datasets_found'] += len(all_datasets)
                
                print(f"✅ Found {len(all_datasets)} datasets ({len(kaggle_datasets)} Kaggle, {len(github_datasets)} GitHub)")
            
            # Save to markdown
            self._save_to_markdown(all_results)
            
            return all_results
            
        except Exception as e:
            logger.error(f"Error during dataset discovery: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'use_case_datasets': [],
                'total_datasets_found': 0
            }
    
    def _search_kaggle_datasets(self, use_case_title: str, ai_solution: str) -> List[Dict[str, Any]]:
        """Search ONLY Kaggle for datasets."""
        print(f"   📊 Searching Kaggle...")
        datasets = []
        
        try:
            # Create specific Kaggle search queries
            search_terms = self._extract_search_terms(use_case_title, ai_solution)
            
            for term in search_terms[:3]:  # Top 3 search terms
                # Search with site:kaggle.com to ONLY get Kaggle results
                kaggle_query = f"site:kaggle.com/datasets {term} dataset"
                
                # Try both Tavily and Exa
                try:
                    # Tavily search
                    tavily_results = self.tavily_searcher.search_ai_use_cases(kaggle_query)
                    for result in tavily_results[:3]:  # Top 3 per search
                        if 'kaggle.com/datasets' in result.get('url', '').lower():
                            dataset = self._format_kaggle_dataset(result)
                            if dataset and dataset not in datasets:
                                datasets.append(dataset)
                except Exception as tavily_error:
                    logger.warning(f"Tavily search failed for Kaggle query '{kaggle_query}': {tavily_error}")
                
                try:
                    # Exa search
                    exa_results = self.exa_searcher.search_ai_use_cases(kaggle_query)
                    for result in exa_results[:3]:  # Top 3 per search
                        if 'kaggle.com/datasets' in result.get('url', '').lower():
                            dataset = self._format_kaggle_dataset(result)
                            if dataset and dataset not in datasets:
                                datasets.append(dataset)
                except Exception as exa_error:
                    logger.warning(f"Exa search failed for Kaggle query '{kaggle_query}': {exa_error}")
        
        except Exception as e:
            logger.error(f"Error searching Kaggle: {e}")
        
        print(f"   📊 Found {len(datasets)} Kaggle datasets")
        return datasets[:5]  # Max 5 Kaggle datasets per use case
    
    def _search_github_datasets(self, use_case_title: str, ai_solution: str) -> List[Dict[str, Any]]:
        """Search ONLY GitHub for datasets."""
        print(f"   💻 Searching GitHub...")
        datasets = []
        
        try:
            # Create specific GitHub search queries
            search_terms = self._extract_search_terms(use_case_title, ai_solution)
            
            for term in search_terms[:2]:  # Top 2 search terms
                # Search with site:github.com to ONLY get GitHub results
                github_query = f"site:github.com {term} dataset"
                
                # Try both Tavily and Exa
                try:
                    # Tavily search
                    tavily_results = self.tavily_searcher.search_ai_use_cases(github_query)
                    for result in tavily_results[:3]:  # Top 3 per search
                        if 'github.com' in result.get('url', '').lower() and 'dataset' in result.get('title', '').lower():
                            dataset = self._format_github_dataset(result)
                            if dataset and dataset not in datasets:
                                datasets.append(dataset)
                except Exception as tavily_error:
                    logger.warning(f"Tavily search failed for GitHub query '{github_query}': {tavily_error}")
                
                try:
                    # Exa search
                    exa_results = self.exa_searcher.search_ai_use_cases(github_query)
                    for result in exa_results[:3]:  # Top 3 per search
                        if 'github.com' in result.get('url', '').lower() and 'dataset' in result.get('title', '').lower():
                            dataset = self._format_github_dataset(result)
                            if dataset and dataset not in datasets:
                                datasets.append(dataset)
                except Exception as exa_error:
                    logger.warning(f"Exa search failed for GitHub query '{github_query}': {exa_error}")
        
        except Exception as e:
            logger.error(f"Error searching GitHub: {e}")
        
        print(f"   💻 Found {len(datasets)} GitHub datasets")
        return datasets[:3]  # Max 3 GitHub datasets per use case
    
    
    def _extract_search_terms(self, use_case_title: str, ai_solution: str) -> List[str]:
        """Extract highly specific search terms from use case."""
        combined_text = f"{use_case_title} {ai_solution}".lower()
        
        # Create highly specific, targeted search terms
        terms = []
        
        # Extract the core domain/application
        if 'recommendation' in combined_text:
            # Only recommendation-specific terms
            terms.extend([
                'recommendation system dataset',
                'collaborative filtering dataset', 
                'user recommendation data'
            ])
        elif 'image' in combined_text or 'vision' in combined_text or 'classification' in combined_text:
            # Only image/vision-specific terms
            terms.extend([
                'image classification dataset',
                'computer vision dataset',
                'image recognition data'
            ])
        elif 'nlp' in combined_text or 'text' in combined_text or 'language' in combined_text:
            # Only NLP-specific terms
            terms.extend([
                'natural language processing dataset',
                'text classification dataset',
                'sentiment analysis data'
            ])
        elif 'prediction' in combined_text or 'forecast' in combined_text:
            # Only prediction-specific terms
            terms.extend([
                'time series dataset',
                'forecasting data',
                'predictive analytics dataset'
            ])
        else:
            # Generic fallback - use the exact title
            terms.append(use_case_title.lower())
        
        return terms[:3]  # Return only top 3 highly specific terms
    
    def _format_kaggle_dataset(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format Kaggle dataset result with relevance filtering."""
        title = result.get('title', 'Untitled Dataset')
        description = result.get('content', '')
        url = result.get('url', '')
        
        # Clean up description (remove random text like "Kind regards, Em...")
        cleaned_description = self._clean_description(description)
        
        # Calculate relevance score based on title and description
        relevance_score = self._calculate_relevance_score(title, cleaned_description)
        
        # Only return if relevance score is above threshold
        if relevance_score < 0.6:
            return None
        
        return {
            'title': title,
            'description': cleaned_description,
            'url': url,
            'source': 'Kaggle',
            'platform': 'Kaggle',
            'relevance_score': relevance_score
        }
    
    def _format_github_dataset(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format GitHub dataset result with relevance filtering."""
        title = result.get('title', 'Untitled Dataset')
        description = result.get('content', '')
        url = result.get('url', '')
        
        # Clean up description
        cleaned_description = self._clean_description(description)
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(title, cleaned_description)
        
        # Only return if relevance score is above threshold
        if relevance_score < 0.6:
            return None
        
        return {
            'title': title,
            'description': cleaned_description,
            'url': url,
            'source': 'GitHub',
            'platform': 'GitHub',
            'relevance_score': relevance_score
        }
    
    
    def _save_to_markdown(self, results: Dict[str, Any]) -> str:
        """Save results to markdown file."""
        try:
            # Create agent3_output directory
            output_dir = "agent3_output"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/dataset_discovery_{timestamp}.md"
            
            # Generate markdown content
            markdown_content = self._generate_markdown_report(results)
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"💾 Dataset discovery report saved to: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving markdown report: {e}")
            return None
    
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Generate markdown content for the dataset discovery report."""
        markdown = f"""# Dataset Discovery Report

**Generated:** {results['timestamp']}  
**Total Use Cases:** {results['total_use_cases']}  
**Total Datasets Found:** {results['total_datasets_found']}  
**Sources:** Kaggle, GitHub ONLY

---

"""
        
        for i, use_case_data in enumerate(results['use_case_datasets'], 1):
            markdown += f"""## {i}. {use_case_data['use_case_title']}

**AI Solution:** {use_case_data['ai_solution']}

**Total Datasets Found:** {use_case_data['total_datasets']}

"""
            
            # Kaggle datasets
            if use_case_data['kaggle_datasets']:
                markdown += f"### 📊 Kaggle Datasets ({len(use_case_data['kaggle_datasets'])} found)\n\n"
                for j, dataset in enumerate(use_case_data['kaggle_datasets'], 1):
                    markdown += f"**{j}.** [{dataset['title']}]({dataset['url']})  \n"
                    markdown += f"- **Source:** {dataset['source']}\n"
                    markdown += f"- **Description:** {dataset['description']}\n\n"
            
            # GitHub datasets
            if use_case_data['github_datasets']:
                markdown += f"### 💻 GitHub Datasets ({len(use_case_data['github_datasets'])} found)\n\n"
                for j, dataset in enumerate(use_case_data['github_datasets'], 1):
                    markdown += f"**{j}.** [{dataset['title']}]({dataset['url']})  \n"
                    markdown += f"- **Source:** {dataset['source']}\n"
                    markdown += f"- **Description:** {dataset['description']}\n\n"
            
            
            if not use_case_data['all_datasets']:
                markdown += "*No datasets found on Kaggle or GitHub for this use case.*\n\n"
            
            markdown += "---\n\n"
        
        return markdown
    
    def _clean_description(self, description: str) -> str:
        """Clean up dataset description by removing irrelevant text."""
        if not description:
            return "No description available"
        
        # Remove common irrelevant patterns
        import re
        
        # Remove email signatures and random text
        description = re.sub(r'Kind regards,.*', '', description, flags=re.IGNORECASE | re.DOTALL)
        description = re.sub(r'Best regards,.*', '', description, flags=re.IGNORECASE | re.DOTALL)
        description = re.sub(r'Regards,.*', '', description, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove expand_more and other UI elements
        description = re.sub(r'expand_more.*', '', description, flags=re.IGNORECASE | re.DOTALL)
        description = re.sub(r'View more.*', '', description, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove license and copyright info
        description = re.sub(r'Data files ©.*', '', description, flags=re.IGNORECASE | re.DOTALL)
        description = re.sub(r'License.*', '', description, flags=re.IGNORECASE | re.DOTALL)
        
        # Remove code blocks and algorithms lists
        description = re.sub(r'Algorithms used in it:.*', '', description, flags=re.IGNORECASE | re.DOTALL)
        description = re.sub(r'```.*?```', '', description, flags=re.DOTALL)
        
        # Remove multiple spaces and newlines
        description = re.sub(r'\s+', ' ', description)
        
        # Truncate to reasonable length
        if len(description) > 200:
            description = description[:200] + '...'
        
        return description.strip()
    
    def _calculate_relevance_score(self, title: str, description: str) -> float:
        """Calculate relevance score based on title and description content."""
        if not title and not description:
            return 0.0
        
        combined_text = f"{title} {description}".lower()
        
        # Penalize irrelevant content
        irrelevant_patterns = [
            'tutorial', 'example', 'learning', 'practice', 'beginner',
            'algorithm', 'method', 'technique', 'approach', 'framework',
            'library', 'tool', 'software', 'platform', 'service',
            'api', 'documentation', 'guide', 'manual', 'reference'
        ]
        
        # Check for irrelevant patterns
        irrelevant_count = sum(1 for pattern in irrelevant_patterns if pattern in combined_text)
        if irrelevant_count >= 2:
            return 0.3  # Low relevance for tutorial/learning content
        
        # Boost relevant content
        relevant_patterns = [
            'dataset', 'data', 'training', 'model', 'prediction',
            'classification', 'recommendation', 'filtering', 'analysis'
        ]
        
        relevant_count = sum(1 for pattern in relevant_patterns if pattern in combined_text)
        
        # Calculate base score
        base_score = 0.5
        
        # Boost for relevant content
        if relevant_count >= 2:
            base_score += 0.3
        elif relevant_count >= 1:
            base_score += 0.2
        
        # Boost for specific dataset indicators
        if 'dataset' in combined_text:
            base_score += 0.2
        
        # Penalize generic titles
        generic_titles = [
            'machine learning', 'artificial intelligence', 'data science',
            'deep learning', 'neural network', 'ai'
        ]
        
        if any(generic in title.lower() for generic in generic_titles) and 'dataset' not in combined_text:
            base_score -= 0.3
        
        return min(max(base_score, 0.0), 1.0)  # Clamp between 0 and 1
