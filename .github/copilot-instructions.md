# Copilot Instructions for AgenticAi Project

## Project Overview
This is a Python-based Agentic AI system that analyzes Jira issues and generates:
- Pseudo code with implementation algorithms
- Source code for Java/Spring Boot or Angular
- Effort estimation tables with task breakdowns

## Project Type
- **Language**: Python 3.9+
- **Framework**: None (pure Python with MCP integration)
- **Purpose**: Agentic AI for Jira issue analysis and code generation

## Key Technologies
- Model Context Protocol (MCP) for Jira/Bitbucket integration
- Python dataclasses and type hints
- Markdown report generation
- GitKraken MCP Server tools

## Code Style Guidelines
- Use type hints for all function parameters and returns
- Follow PEP 8 style guide
- Use dataclasses for data models
- Keep functions focused and single-purpose
- Add docstrings to all public methods

## Module Structure
```
src/
├── agent.py              # Main orchestrator
├── config.py             # Configuration
├── models.py             # Data models
├── mcp_client.py         # MCP integration
├── code_generator.py     # Code generation
├── effort_estimator.py   # Effort calculation
└── formatter.py          # Output formatting
```

## When Adding New Features
1. Update relevant model in `models.py` if needed
2. Add business logic to appropriate module
3. Update `agent.py` if orchestration changes
4. Add example to `example_usage.py`
5. Update README.md with new capabilities

## Common Tasks
- **Add language support**: Extend `PseudoCodeGenerator` and `SourceCodeGenerator`
- **Modify estimation**: Update `BASE_HOURS` in `EffortEstimator`
- **Change output format**: Create new formatter in `formatter.py`
- **Add MCP tools**: Extend `MCPJiraClient` or `MCPBitbucketClient`

## Testing Considerations
- Mock MCP tool responses for unit tests
- Test all language variants (Java and Angular)
- Validate estimation calculations
- Check markdown formatting

## Dependencies
- Core: openai, python-dotenv, jinja2, pydantic, rich
- Dev: pytest, black, ruff

## Important Notes
- This project is meant to run in VS Code with MCP support
- MCP tools are called via VS Code's MCP integration
- Output reports are saved to `output/` directory
- Configuration is set via `.env` file (already contains credentials) or `AgentConfig`
- Never commit `.env` file to version control
