# AgenticAi - Jira Issue Analysis System

An intelligent agentic AI system that fetches Jira issues (via MCP) and automatically generates:
- **Pseudo Code** - Step-by-step implementation logic
- **Source Code** - Production-ready code for Java or Angular
- **Effort Estimation Table** - Detailed task breakdown with time estimates

## 🚀 Features

- 🔍 Fetch Jira issues using Model Context Protocol (MCP) integration
- 💡 Generate detailed pseudo code with complexity analysis (single BEGIN/END block)
- 💻 Auto-generate source code for:
  - **Java/Spring Boot** (Controller, Service, Repository, DTO, Entity)
  - **Angular** (Component, Template, Service, Model, Styles)
- 📊 Calculate effort estimates with task breakdown
- 📝 Generate comprehensive Markdown reports
- 📤 **Update Jira issues directly**:
  - Update "Pseudo Code" custom field with implementation algorithm
  - Update "Source Code" custom field with full generated code
  - Update "Original Estimate" field with average effort (total + buffered) / 2
  - Post effort estimation as a comment
  - Optionally assign to a developer
- ⚙️ Configurable parameters (language, max hours, pseudo code field name)

## 📋 Prerequisites

- Python 3.9+
- VS Code with MCP support (for Jira/Bitbucket integration)
- GitKraken MCP server configured

## 🛠️ Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
   - The `.env` file contains your MCP credentials and settings
   - Update values in `.env` if needed for your environment

## 📖 Usage

### Basic Usage

```python
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig

# Configure the agent
config = AgentConfig(
    language="java",  # or "angular"
    max_hours=4.0  # Maximum 4 hours (default)
)

# Create agent
agent = JiraAnalysisAgent(config)

# Analyze a Jira issue
result = agent.analyze_issue(
    issue_id="DL-123",
    repository_name="my-repo",
    repository_organization="my-org"
)

# Generate report
report = agent.generate_report(
    result,
    output_filename="analysis_report.md"
)
```

### Update Jira with Analysis

```python
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig

# Configure and create agent
config = AgentConfig(language="angular", max_hours=4.0)
agent = JiraAnalysisAgent(config)

# Analyze issue
result = agent.analyze_issue(issue_id="DL-61404")

# Generate local report
agent.generate_report(result, output_filename="report.md")

# Update Jira issue with analysis
# - Updates "Pseudo Code" field with implementation algorithm
# - Posts effort estimation as a comment
# - Optionally assign to a developer
agent.update_jira_with_analysis(
    result=result,
    assign_to="developer@example.com"  # Optional: assign to developer
)
```

### Quick Start - Interactive Mode

```bash
python run.py
```

This will prompt you for:
- Jira Issue ID
- Language (Java/Angular)
- Max Hours (default: 4.0)
- **Whether to update Jira issue directly**
- **Developer to assign the issue to (optional)**

### Run Examples

```bash
# Basic example
python example_usage.py

# Update Jira example
python example_jira_update.py
```

## 📊 Output Examples

### Effort Estimation Table

```
================================================================================
                        EFFORT ESTIMATION TABLE                        
================================================================================
Task                                    Hours       Days     Complexity
--------------------------------------------------------------------------------
Analysis & Technical Design              2.00       0.25         Simple
Implementation (JAVA)                    4.00       0.50         Simple
Unit Testing                             2.00       0.25         Simple
Code Review & Fixes                      1.00       0.12         Simple
Documentation                            1.00       0.12         Simple
--------------------------------------------------------------------------------
TOTAL                                   10.00       1.25
WITH BUFFER (20%)                       12.00       1.50
================================================================================
```

### Generated Artifacts

For each Jira issue analysis, the system generates:

1. **Pseudo Code** - Structured algorithm with:
   - Input validation steps
   - Main logic flow
   - Error handling
   - Output generation
   - Implementation notes

2. **Source Code** - Complete implementation with:
   - **Java**: Controller, Service, Repository, DTO, Entity classes
   - **Angular**: Component, Template, Service, Model, Styles
   - Dependencies list
   - Setup instructions

3. **Effort Estimation** - Detailed breakdown including:
   - Task-by-task hours and days
   - Complexity assessment
   - Key assumptions
   - Risk factors
   - Total with buffer

## 🔧 Configuration

### AgentConfig Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `language` | `"java"` or `"angular"` | `"java"` | Target programming language |
| `max_days` | `float` | `2.0` | Maximum days for effort estimation |
| `output_dir` | `string` | `"output"` | Directory for generated reports |

### Example Configuration

```python
config = AgentConfig(
    language="angular",
    max_days=1.5,
    output_dir="reports"
)
```

## 📁 Project Structure

```
AgenticAi/
├── src/
│   ├── __init__.py
│   ├── agent.py              # Main orchestrator
│   ├── config.py             # Configuration models
│   ├── models.py             # Data models
│   ├── mcp_client.py         # MCP integration
│   ├── code_generator.py     # Pseudo & source code generation
│   ├── effort_estimator.py   # Effort calculation
│   └── formatter.py          # Output formatting
├── tests/                    # Unit tests
├── output/                   # Generated reports
├── docs/                     # Documentation
├── example_usage.py          # Usage examples
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Project configuration
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🔌 MCP Integration

This system integrates with GitKraken MCP Server for:

- **Jira**: Fetch issue details, add comments
- **Bitbucket**: Access repository files, create PRs

### Available MCP Tools Used

- `mcp_gitkraken_issues_get_detail` - Fetch Jira issue
- `mcp_gitkraken_issues_add_comment` - Update Jira issue
- `mcp_gitkraken_repository_get_file_content` - Get repo files
- `mcp_gitkraken_pull_request_create` - Create pull requests

## 🎯 Workflow

1. **Fetch** - Retrieve Jira issue details via MCP
2. **Analyze** - Assess complexity and requirements
3. **Generate Pseudo Code** - Create implementation algorithm (single BEGIN/END block)
4. **Generate Source Code** - Produce language-specific code
5. **Estimate Effort** - Calculate time breakdown
6. **Format Report** - Create comprehensive Markdown report
7. **Update Jira** (Optional) - Post analysis directly to Jira issue as comment

### What Gets Posted to Jira

When you use `update_jira_with_analysis()`, a comment is added to the Jira issue containing:

- 🔍 **Pseudo Code** - Complete BEGIN/END block with all logic
- 💻 **Source Code Summary** - List of generated files and dependencies
- 📊 **Effort Estimation Table** - Complete task breakdown with hours/days

This allows team members to review the analysis directly in Jira without opening external files.

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📝 Generated Report Format

Each analysis generates a Markdown report with:

1. Issue Details (ID, type, priority, description)
2. Pseudo Code (with complexity level)
3. Source Code (all files with syntax highlighting)
4. Effort Estimation (detailed table and summary)
5. Recommendations (based on analysis)

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Additional language support (Python, C#, etc.)
- AI-powered code generation using OpenAI
- Integration with more issue tracking systems
- Advanced complexity analysis algorithms
- Test case generation

## 📄 License

MIT License - See LICENSE file for details

## 🔗 Related Projects

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [GitKraken MCP Server](https://github.com/gitkraken/mcp-server)

## 📞 Support

For issues or questions:
- Open an issue in the repository
- Check the `docs/` directory for detailed documentation

---

**Made with ❤️ using Model Context Protocol**
