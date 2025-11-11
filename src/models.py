"""
Data models for Jira issues, code generation, and effort estimation
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class IssueType(str, Enum):
    """Jira issue types"""
    BUG = "Bug"
    FEATURE = "Feature"
    TASK = "Task"
    STORY = "Story"
    IMPROVEMENT = "Improvement"


class Priority(str, Enum):
    """Issue priority levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class ComplexityLevel(str, Enum):
    """Code complexity levels"""
    SIMPLE = "Simple"
    MODERATE = "Moderate"
    COMPLEX = "Complex"


@dataclass
class JiraIssue:
    """Represents a Jira issue"""
    issue_id: str
    title: str
    description: str
    issue_type: str
    priority: str
    assignee: Optional[str] = None
    status: str = "Open"
    labels: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PseudoCode:
    """Represents generated pseudo code"""
    sections: List[Dict[str, str]]  # [{title: str, steps: str}]
    complexity: ComplexityLevel
    notes: List[str] = field(default_factory=list)


@dataclass
class SourceCode:
    """Represents generated source code"""
    language: str
    files: List[Dict[str, str]]  # [{filename: str, code: str, description: str}]
    dependencies: List[str] = field(default_factory=list)
    setup_instructions: List[str] = field(default_factory=list)


@dataclass
class EffortEstimate:
    """Represents effort estimation"""
    task_name: str
    complexity: ComplexityLevel
    estimated_hours: float
    estimated_days: float
    risk_factors: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)


@dataclass
class TaskBreakdown:
    """Breakdown of tasks with effort estimates"""
    tasks: List[EffortEstimate]
    total_hours: float
    total_days: float
    buffer_percentage: float = 20.0
    
    @property
    def total_with_buffer(self) -> float:
        """Calculate total days with buffer"""
        return self.total_days * (1 + self.buffer_percentage / 100)


@dataclass
class AnalysisResult:
    """Complete analysis result for a Jira issue"""
    issue: JiraIssue
    pseudo_code: PseudoCode
    source_code: SourceCode
    effort_estimate: TaskBreakdown
    recommendations: List[str] = field(default_factory=list)
