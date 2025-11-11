"""
Configuration module for Agentic AI system
"""
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class AgentConfig:
    """Configuration for the agentic AI system"""
    
    # Language configuration
    language: Literal["java", "angular", "fullstack", "BE", "UI"] = "java"
    backend_language: Optional[str] = None  # Deprecated
    frontend_language: Optional[str] = None  # Deprecated
    
    # Effort estimation configuration
    max_hours: float = 4.0  # Maximum hours for effort estimation (default: 4 hours)
    
    # Jira configuration
    jira_provider: str = "jira"  # Provider type for MCP
    pseudo_code_field: str = "Pseudo Code"  # Jira field name for pseudo code (can be custom field ID like "customfield_10XXX")
    source_code_field: str = "Source Code"  # Jira field name for source code (optional)
    original_estimate_field: str = ""  # Standard Jira time tracking field (optional - set to "originalEstimate" to enable)
    
    # Bitbucket configuration
    bitbucket_provider: str = "bitbucket"
    
    # Output configuration (deprecated - reports no longer saved to files)
    output_format: Literal["markdown", "json"] = "markdown"
    
    # AI Model configuration (for future OpenAI integration)
    model: str = "gpt-4"
    temperature: float = 0.7
