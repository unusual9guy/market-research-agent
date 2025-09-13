"""
Pydantic models for the Market Research Agent system.
"""

from .resource_models import (
    DatasetResource,
    UseCaseResources, 
    ResourceDiscoveryResult
)

__all__ = [
    "DatasetResource",
    "UseCaseResources",
    "ResourceDiscoveryResult"
]
