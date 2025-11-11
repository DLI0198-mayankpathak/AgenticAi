# API Reference

## JiraAnalysisAgent

Main agent class that orchestrates the analysis workflow.

### Constructor

```python
JiraAnalysisAgent(config: AgentConfig)
```

**Parameters**:
- `config` (AgentConfig): Configuration object

**Example**:
```python
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig

config = AgentConfig(language="java", max_days=2.0)
agent = JiraAnalysisAgent(config)
```

### Methods

#### analyze_issue()

```python
analyze_issue(
    issue_id: str,
    repository_name: Optional[str] = None,
    repository_organization: Optional[str] = None,
    azure_organization: Optional[str] = None,
    azure_project: Optional[str] = None
) -> AnalysisResult
```

Analyzes a Jira issue and generates all artifacts.

**Parameters**:
- `issue_id` (str): Jira issue ID (e.g., "DL-123")
- `repository_name` (Optional[str]): Repository name
- `repository_organization` (Optional[str]): Organization name
- `azure_organization` (Optional[str]): Azure DevOps organization
- `azure_project` (Optional[str]): Azure DevOps project

**Returns**: `AnalysisResult` object containing all generated artifacts

**Example**:
```python
result = agent.analyze_issue(
    issue_id="DL-123",
    repository_name="backend-api",
    repository_organization="mycompany"
)
```

#### generate_report()

```python
generate_report(
    result: AnalysisResult,
    output_filename: Optional[str] = None
) -> str
```

Generates a Markdown report from analysis result.

**Parameters**:
- `result` (AnalysisResult): Analysis result to format
- `output_filename` (Optional[str]): Filename to save report

**Returns**: Markdown formatted report as string

**Example**:
```python
report = agent.generate_report(
    result,
    output_filename="analysis_report.md"
)
```

#### print_effort_table()

```python
print_effort_table(result: AnalysisResult) -> None
```

Prints effort estimation table to console.

**Parameters**:
- `result` (AnalysisResult): Analysis result

**Example**:
```python
agent.print_effort_table(result)
```

---

## AgentConfig

Configuration dataclass for the agent.

### Attributes

```python
@dataclass
class AgentConfig:
    language: Literal["java", "angular"] = "java"
    max_days: float = 2.0
    jira_provider: str = "jira"
    bitbucket_provider: str = "bitbucket"
    output_format: Literal["markdown", "json"] = "markdown"
    output_dir: str = "output"
    model: str = "gpt-4"
    temperature: float = 0.7
```

**Example**:
```python
config = AgentConfig(
    language="angular",
    max_days=1.5,
    output_dir="reports"
)
```

---

## Data Models

### JiraIssue

```python
@dataclass
class JiraIssue:
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
```

### PseudoCode

```python
@dataclass
class PseudoCode:
    sections: List[Dict[str, str]]
    complexity: ComplexityLevel
    notes: List[str] = field(default_factory=list)
```

### SourceCode

```python
@dataclass
class SourceCode:
    language: str
    files: List[Dict[str, str]]
    dependencies: List[str] = field(default_factory=list)
    setup_instructions: List[str] = field(default_factory=list)
```

### EffortEstimate

```python
@dataclass
class EffortEstimate:
    task_name: str
    complexity: ComplexityLevel
    estimated_hours: float
    estimated_days: float
    risk_factors: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
```

### TaskBreakdown

```python
@dataclass
class TaskBreakdown:
    tasks: List[EffortEstimate]
    total_hours: float
    total_days: float
    buffer_percentage: float = 20.0
    
    @property
    def total_with_buffer(self) -> float:
        return self.total_days * (1 + self.buffer_percentage / 100)
```

### AnalysisResult

```python
@dataclass
class AnalysisResult:
    issue: JiraIssue
    pseudo_code: PseudoCode
    source_code: SourceCode
    effort_estimate: TaskBreakdown
    recommendations: List[str] = field(default_factory=list)
```

---

## Enums

### ComplexityLevel

```python
class ComplexityLevel(str, Enum):
    SIMPLE = "Simple"
    MODERATE = "Moderate"
    COMPLEX = "Complex"
```

### IssueType

```python
class IssueType(str, Enum):
    BUG = "Bug"
    FEATURE = "Feature"
    TASK = "Task"
    STORY = "Story"
    IMPROVEMENT = "Improvement"
```

### Priority

```python
class Priority(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
```

---

## MCP Client Classes

### MCPJiraClient

```python
class MCPJiraClient:
    def __init__(self, provider: str = "jira")
    
    def get_issue_detail(
        issue_id: str,
        azure_organization: Optional[str] = None,
        azure_project: Optional[str] = None,
        repository_name: Optional[str] = None,
        repository_organization: Optional[str] = None
    ) -> Dict[str, Any]
    
    def parse_issue_response(response: Dict[str, Any]) -> JiraIssue
    
    def add_comment(
        issue_id: str,
        comment: str,
        ...
    ) -> bool
```

### MCPBitbucketClient

```python
class MCPBitbucketClient:
    def __init__(self, provider: str = "bitbucket")
    
    def get_file_content(
        repository_name: str,
        repository_organization: str,
        file_path: str,
        ref: str = "main",
        azure_project: Optional[str] = None
    ) -> str
    
    def create_pull_request(
        repository_name: str,
        repository_organization: str,
        title: str,
        source_branch: str,
        target_branch: str,
        body: str,
        is_draft: bool = False,
        azure_project: Optional[str] = None
    ) -> Dict[str, Any]
```

---

## Code Generator Classes

### PseudoCodeGenerator

```python
class PseudoCodeGenerator:
    def __init__(self, language: str)
    
    def generate(self, issue: JiraIssue) -> PseudoCode
```

### SourceCodeGenerator

```python
class SourceCodeGenerator:
    def __init__(self, language: str)
    
    def generate(
        self,
        issue: JiraIssue,
        pseudo_code: PseudoCode
    ) -> SourceCode
```

---

## EffortEstimator

```python
class EffortEstimator:
    def __init__(
        self,
        max_days: float = 2.0,
        hours_per_day: float = 8.0
    )
    
    def estimate(
        self,
        issue: JiraIssue,
        pseudo_code: PseudoCode,
        language: str
    ) -> TaskBreakdown
    
    def generate_effort_table(
        self,
        breakdown: TaskBreakdown
    ) -> Dict[str, Any]
```

---

## Formatter Classes

### MarkdownFormatter

```python
class MarkdownFormatter:
    def format(self, result: AnalysisResult) -> str
```

### TableFormatter

```python
class TableFormatter:
    @staticmethod
    def format_simple_table(breakdown: TaskBreakdown) -> str
```

---

## Usage Examples

### Complete Workflow

```python
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig

# 1. Configure
config = AgentConfig(
    language="java",
    max_days=2.0,
    output_dir="output"
)

# 2. Create agent
agent = JiraAnalysisAgent(config)

# 3. Analyze
result = agent.analyze_issue(
    issue_id="DL-123",
    repository_name="api-service",
    repository_organization="company"
)

# 4. Display results
agent.print_effort_table(result)

# 5. Generate report
report = agent.generate_report(
    result,
    output_filename="analysis.md"
)

# 6. Access individual components
print(f"Complexity: {result.pseudo_code.complexity.value}")
print(f"Total Days: {result.effort_estimate.total_days}")
print(f"Files Generated: {len(result.source_code.files)}")
```

### Custom Configuration

```python
# Angular with 1.5 day limit
config = AgentConfig(
    language="angular",
    max_days=1.5,
    output_dir="angular_reports",
    output_format="markdown"
)

agent = JiraAnalysisAgent(config)
result = agent.analyze_issue("PROJ-456")
```

### Accessing Analysis Components

```python
# Pseudo code sections
for section in result.pseudo_code.sections:
    print(f"{section['title']}")
    print(section['steps'])

# Generated source files
for file_info in result.source_code.files:
    print(f"File: {file_info['filename']}")
    print(f"Description: {file_info['description']}")

# Effort breakdown
for task in result.effort_estimate.tasks:
    print(f"{task.task_name}: {task.estimated_days} days")
```
