# Fullstack Code Generation

The agent now supports generating both Backend (Java) and Frontend (Angular) code together!

## 🎯 Usage

### Option 1: Single Language (Original)

```python
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig

# Java only
config = AgentConfig(language="java", max_hours=4.0)

# OR Angular only
config = AgentConfig(language="angular", max_hours=4.0)
```

### Option 2: Fullstack (NEW!)

```python
config = AgentConfig(
    language="fullstack",
    backend_language="java",
    frontend_language="angular",
    max_hours=8.0
)

agent = JiraAnalysisAgent(config)
result = agent.analyze_issue("DL-123")
```

## 🌐 API Usage

### Single Language

```bash
curl -X POST http://10.232.187.6:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "java",
    "max_hours": 4.0
  }'
```

### Fullstack (NEW!)

```bash
curl -X POST http://10.232.187.6:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": "DL-123",
    "language": "fullstack",
    "backend_language": "java",
    "frontend_language": "angular",
    "max_hours": 8.0
  }'
```

## 📊 What Gets Generated

### Backend (Java)
- REST API Controllers
- Service Layer
- Repository/DAO
- Entity Models
- DTOs
- Validation logic
- Database operations

### Frontend (Angular)
- Components
- Services
- Models/Interfaces
- Templates (HTML)
- Reactive Forms
- API integration

### Pseudo Code
- Separate sections for Backend and Frontend
- Backend: API endpoints, database logic, validation
- Frontend: Component lifecycle, form handling, service calls

### Effort Estimation
- Combined effort for both BE and FE
- Separate tasks for backend and frontend work
- Realistic estimates based on fullstack complexity

## 🔥 Example Result

When you analyze a Jira issue with fullstack:

1. **Pseudo Code**:
   - Section 1: Backend Implementation (JAVA)
   - Section 2: Frontend Implementation (ANGULAR)

2. **Source Code**:
   - 5 Java files (Controller, Service, Repository, DTO, Entity)
   - 4 Angular files (Component.ts, Template.html, Service.ts, Model.ts)

3. **Effort Estimate**:
   - Tasks include both BE and FE implementation
   - Realistic hours for fullstack development

4. **Updates Jira**:
   - Pseudo Code field: Contains both BE and FE algorithms
   - Source Code field: Contains all Java + Angular files
   - Comment: Effort breakdown with fullstack tasks

## 💡 Benefits

✅ **Complete Solution**: Get both backend and frontend code together
✅ **Consistent**: Both generated from the same Jira description
✅ **Time-Saving**: No need to run analysis twice
✅ **Realistic Estimates**: Effort reflects fullstack complexity

## 🧪 Test It

```bash
# Run fullstack test
python test_fullstack.py
```

---

**API Server**: http://10.232.187.6:8000

**Try it now!** 🚀
