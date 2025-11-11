# Architecture Documentation

## System Overview

The Agentic AI system is designed as a modular pipeline that processes Jira issues and generates comprehensive technical artifacts.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        JiraAnalysisAgent                        │
│                     (Main Orchestrator)                         │
└───────────┬─────────────────────────────────────────────────────┘
            │
            ├──► MCPJiraClient ──────► Fetch Jira Issue Details
            │
            ├──► PseudoCodeGenerator ──► Generate Algorithm
            │
            ├──► SourceCodeGenerator ──► Generate Code Files
            │
            ├──► EffortEstimator ────► Calculate Time Estimates
            │
            └──► MarkdownFormatter ──► Generate Report
```

## Module Responsibilities

### 1. Agent Module (`agent.py`)
**Responsibility**: Main orchestrator that coordinates the entire workflow

**Key Methods**:
- `analyze_issue()` - Main entry point for analysis
- `generate_report()` - Creates markdown output
- `print_effort_table()` - Console output

**Dependencies**: All other modules

### 2. MCP Client Module (`mcp_client.py`)
**Responsibility**: Interface with Model Context Protocol for Jira/Bitbucket

**Key Classes**:
- `MCPJiraClient` - Jira integration
- `MCPBitbucketClient` - Bitbucket integration

**MCP Tools Used**:
- `mcp_gitkraken_issues_get_detail`
- `mcp_gitkraken_issues_add_comment`
- `mcp_gitkraken_repository_get_file_content`
- `mcp_gitkraken_pull_request_create`

### 3. Code Generator Module (`code_generator.py`)
**Responsibility**: Generate pseudo code and source code

**Key Classes**:
- `PseudoCodeGenerator` - Creates implementation algorithms
- `SourceCodeGenerator` - Generates language-specific code

**Supported Languages**:
- Java/Spring Boot
- Angular/TypeScript

### 4. Effort Estimator Module (`effort_estimator.py`)
**Responsibility**: Calculate development effort estimates

**Key Features**:
- Complexity-based estimation (Simple, Moderate, Complex)
- Task breakdown with assumptions and risks
- Configurable max days constraint
- Buffer percentage calculation

**Estimation Formula**:
```
Base Hours (by complexity) → Tasks → Total Hours → Total Days → With Buffer
```

### 5. Formatter Module (`formatter.py`)
**Responsibility**: Format output as Markdown reports

**Key Classes**:
- `MarkdownFormatter` - Rich markdown reports
- `TableFormatter` - Simple console tables

### 6. Models Module (`models.py`)
**Responsibility**: Data structures and type definitions

**Key Models**:
- `JiraIssue` - Issue representation
- `PseudoCode` - Algorithm structure
- `SourceCode` - Generated code files
- `EffortEstimate` - Task estimation
- `TaskBreakdown` - Complete effort breakdown
- `AnalysisResult` - Final output container

### 7. Config Module (`config.py`)
**Responsibility**: Configuration and settings

**Key Parameters**:
- Language selection
- Max days constraint
- Output directory
- MCP provider settings

## Data Flow

```
1. User Input (Issue ID, Language, Max Days)
   ↓
2. MCP Client Fetches Jira Issue
   ↓
3. Pseudo Code Generator Analyzes & Creates Algorithm
   ↓
4. Source Code Generator Produces Code Files
   ↓
5. Effort Estimator Calculates Time Breakdown
   ↓
6. Formatter Creates Markdown Report
   ↓
7. Output (Report File + Console Display)
```

## Complexity Analysis Algorithm

The system determines complexity based on:

1. **Issue Type**:
   - Bug/Task → Simple bias
   - Feature/Story → Complex bias

2. **Description Length**:
   - < 200 chars → Simple
   - 200-500 chars → Moderate
   - > 500 chars → Complex

3. **Keywords**:
   - "integration", "performance" → Increase complexity
   - "calculate", "transform" → Business logic indicators

## Code Generation Strategy

### Java/Spring Boot
Generates layered architecture:
1. **Controller Layer** - REST endpoints
2. **Service Layer** - Business logic
3. **Repository Layer** - Data access
4. **DTO Layer** - Data transfer objects
5. **Entity Layer** - JPA entities

### Angular
Generates component-based structure:
1. **Component (TS)** - Business logic
2. **Template (HTML)** - UI structure
3. **Styles (SCSS)** - Component styling
4. **Service (TS)** - API integration
5. **Model (TS)** - Type definitions

## Effort Estimation Algorithm

### Base Hours by Complexity

| Task Type | Simple | Moderate | Complex |
|-----------|--------|----------|---------|
| Design | 2h | 4h | 8h |
| Implementation | 4h | 8h | 16h |
| Testing | 2h | 4h | 8h |
| Code Review | 1h | 2h | 3h |
| Documentation | 1h | 2h | 3h |

### Adjustments
- **Language Factor**: Angular +10% (UI complexity)
- **Max Days Constraint**: Scale down if needed
- **Buffer**: 20% added to total

## Extension Points

The system is designed for extensibility:

### Adding New Languages
1. Update `PseudoCodeGenerator._get_*_steps()` methods
2. Add generation logic in `SourceCodeGenerator`
3. Update `ComplexityLevel` heuristics if needed

### Adding New Estimation Factors
1. Extend `BASE_HOURS` dictionary in `EffortEstimator`
2. Add new risk/assumption generators
3. Update `_generate_task_estimates()` method

### Adding New Output Formats
1. Create new formatter class (e.g., `JSONFormatter`)
2. Implement format interface
3. Add to `AgentConfig` options

## Error Handling Strategy

- MCP client failures → Graceful fallback with placeholder data
- Validation errors → Detailed error messages
- File I/O errors → Directory creation with error logging

## Future Enhancements

1. **AI Integration**: Use OpenAI for smarter code generation
2. **Multi-language Support**: Python, C#, Go, etc.
3. **Test Generation**: Auto-generate unit tests
4. **CI/CD Integration**: Generate pipeline configs
5. **Interactive Mode**: CLI with prompts
6. **Web Interface**: FastAPI-based web UI
7. **Analytics**: Track estimation accuracy over time
