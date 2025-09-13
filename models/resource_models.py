"""
Pydantic models for Resource Discovery Agent output.
Ensures consistent, structured output every time.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DatasetResource(BaseModel):
    """Model for a dataset resource."""
    title: str = Field(..., description="Title of the dataset")
    description: str = Field(..., description="Description of the dataset")
    url: str = Field(..., description="URL to the dataset")
    source: str = Field(..., description="Source platform (Kaggle, HuggingFace, etc.)")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score 0-1")
    size: Optional[str] = Field(None, description="Dataset size if available")
    format: Optional[str] = Field(None, description="Dataset format (CSV, JSON, etc.)")
    tags: List[str] = Field(default_factory=list, description="Dataset tags/categories")

class UseCaseResources(BaseModel):
    """Model for resources discovered for a single use case."""
    use_case_title: str = Field(..., description="Title of the use case")
    use_case_description: str = Field(..., description="Description of the use case")
    datasets: List[DatasetResource] = Field(default_factory=list, description="List of discovered datasets")
    total_datasets: int = Field(..., description="Total number of datasets found")

class ResourceDiscoveryResult(BaseModel):
    """Model for complete resource discovery result."""
    status: str = Field(..., description="Status of the discovery process")
    total_use_cases: int = Field(..., description="Total number of use cases processed")
    total_datasets_found: int = Field(..., description="Total datasets discovered across all use cases")
    use_case_resources: List[UseCaseResources] = Field(default_factory=list, description="Resources for each use case")
    discovery_timestamp: datetime = Field(default_factory=datetime.now, description="When discovery was performed")
    search_sources_used: List[str] = Field(default_factory=list, description="Sources used for discovery")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
