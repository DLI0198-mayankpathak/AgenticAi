"""
Minimal Agentic AI Agent - All-in-one module
Orchestrates Jira issue analysis, code generation, and effort estimation
"""
import os
import re
import requests
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# ENUMS & MODELS
# ============================================================================

class ComplexityLevel(str, Enum):
    SIMPLE = "Simple"
    MODERATE = "Moderate"
    COMPLEX = "Complex"

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

@dataclass
class PseudoCode:
    sections: List[Dict[str, str]]
    complexity: ComplexityLevel
    notes: List[str] = field(default_factory=list)

@dataclass
class SourceCode:
    language: str
    files: List[Dict[str, str]]
    dependencies: List[str] = field(default_factory=list)
    setup_instructions: List[str] = field(default_factory=list)

@dataclass
class EffortEstimate:
    task_name: str
    complexity: ComplexityLevel
    estimated_hours: float
    estimated_days: float
    risk_factors: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)

@dataclass
class TaskBreakdown:
    tasks: List[EffortEstimate]
    total_hours: float
    total_days: float
    buffer_percentage: float = 20.0
    
    @property
    def total_with_buffer(self) -> float:
        return self.total_days * (1 + self.buffer_percentage / 100)

@dataclass
class AnalysisResult:
    issue: JiraIssue
    pseudo_code: PseudoCode
    source_code: SourceCode
    effort_estimate: TaskBreakdown
    recommendations: List[str] = field(default_factory=list)

@dataclass
class AgentConfig:
    language: Literal["java", "angular", "fullstack", "BE", "UI"] = "java"
    backend_language: Optional[str] = None
    frontend_language: Optional[str] = None
    max_hours: float = 4.0
    jira_provider: str = "jira"
    pseudo_code_field: str = "Pseudo Code"
    source_code_field: str = "Source Code"
    original_estimate_field: str = ""
    bitbucket_provider: str = "bitbucket"

# ============================================================================
# JIRA CLIENT
# ============================================================================

class MCPJiraClient:
    def __init__(self, provider: str = "jira"):
        self.provider = provider
        self.jira_base_url = os.getenv("JIRA_BASE_URL", "")
        self.jira_username = os.getenv("JIRA_USERNAME", "")
        self.jira_api_token = os.getenv("JIRA_API_TOKEN", "")
        self.use_direct_api = bool(self.jira_base_url and self.jira_username and self.jira_api_token)
        self._field_id_cache = {}
        
        if self.use_direct_api:
            print(f"🔐 Jira credentials loaded")
        else:
            print(f"⚠️  Jira credentials missing")

    def get_issue_detail(self, issue_id: str, **kwargs) -> Dict[str, Any]:
        if not self.use_direct_api:
            return {"issue_id": issue_id, "title": "Sample Issue", "description": "Sample description", 
                    "issue_type": "Task", "priority": "Medium", "status": "Open"}
        
        try:
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            response = requests.get(url, auth=auth, headers={"Accept": "application/json"})
            
            if response.status_code == 200:
                data = response.json()
                fields = data.get("fields", {})
                description = self._adf_to_text(fields.get("description", ""))
                
                return {
                    "issue_id": issue_id,
                    "title": fields.get("summary", ""),
                    "description": description or "No description",
                    "issue_type": fields.get("issuetype", {}).get("name", "Task"),
                    "priority": fields.get("priority", {}).get("name", "Medium"),
                    "status": fields.get("status", {}).get("name", "Open"),
                    "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
                    "labels": fields.get("labels", []),
                    "components": [c.get("name") for c in fields.get("components", [])],
                    "raw_data": data
                }
            raise ValueError(f"Failed to fetch issue: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
            raise

    def parse_issue_response(self, response: Dict[str, Any]) -> JiraIssue:
        return JiraIssue(**{k: response.get(k, v) for k, v in 
            [("issue_id", ""), ("title", ""), ("description", ""), ("issue_type", "Task"),
             ("priority", "Medium"), ("assignee", None), ("status", "Open"), 
             ("labels", []), ("components", []), ("raw_data", {})]})

    def add_comment(self, issue_id: str, comment: str, **kwargs) -> bool:
        if not self.use_direct_api:
            return False
        try:
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}/comment"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            payload = {"body": self._markdown_to_adf(comment)}
            response = requests.post(url, json=payload, auth=auth, 
                headers={"Accept": "application/json", "Content-Type": "application/json"})
            return response.status_code in [200, 201]
        except:
            return False

    def update_issue_field(self, issue_id: str, field_name: str, field_value: str) -> bool:
        if not self.use_direct_api:
            print(f"   ⚠️ No Jira credentials - cannot update {field_name}")
            return False
        try:
            field_id = self._get_field_id(field_name)
            print(f"   📝 Updating '{field_name}' → {field_id}")
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            
            if field_id == "originalEstimate":
                payload = {"fields": {"timetracking": {"originalEstimate": f"{int(int(field_value)/3600)}h"}}}
            elif field_id.startswith("customfield_"):
                # Custom fields need ADF format in Jira Cloud
                payload = {"fields": {field_id: self._text_to_adf(field_value)}}
            else:
                payload = {"fields": {field_id: self._markdown_to_adf(field_value)}}
            
            response = requests.put(url, json=payload, auth=auth,
                headers={"Accept": "application/json", "Content-Type": "application/json"})
            if response.status_code == 204:
                return True
            print(f"   ❌ Update failed: {response.status_code} - {response.text[:200]}")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def _text_to_adf(self, text: str) -> Dict:
        """Convert plain text to ADF format for custom fields"""
        content = []
        for line in text.split("\n"):
            content.append({"type": "paragraph", "content": [{"type": "text", "text": line}] if line.strip() else []})
        return {"type": "doc", "version": 1, "content": content}

    def _create_adf_table(self, headers: List[str], rows: List[List[str]]) -> Dict:
        """Create ADF table for Jira comments"""
        def cell(text, is_header=False):
            return {"type": "tableHeader" if is_header else "tableCell",
                    "content": [{"type": "paragraph", "content": [{"type": "text", "text": str(text)}]}]}
        table_rows = [{"type": "tableRow", "content": [cell(h, True) for h in headers]}]
        for row in rows:
            table_rows.append({"type": "tableRow", "content": [cell(c) for c in row]})
        return {"type": "table", "content": table_rows}

    def add_comment_with_table(self, issue_id: str, title: str, headers: List[str], rows: List[List[str]]) -> bool:
        """Add comment with properly formatted ADF table"""
        if not self.use_direct_api:
            return False
        try:
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}/comment"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            content = [
                {"type": "paragraph", "content": [{"type": "text", "text": title, "marks": [{"type": "strong"}]}]},
                self._create_adf_table(headers, rows)
            ]
            payload = {"body": {"type": "doc", "version": 1, "content": content}}
            response = requests.post(url, json=payload, auth=auth,
                headers={"Accept": "application/json", "Content-Type": "application/json"})
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"   ❌ Comment error: {e}")
            return False

    def assign_issue(self, issue_id: str, assignee: str) -> bool:
        if not self.use_direct_api:
            return False
        try:
            account_id = self._get_account_id(assignee)
            if not account_id:
                return False
            url = f"{self.jira_base_url}/rest/api/3/issue/{issue_id}/assignee"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            response = requests.put(url, json={"accountId": account_id}, auth=auth,
                headers={"Accept": "application/json", "Content-Type": "application/json"})
            return response.status_code == 204
        except:
            return False

    def _get_account_id(self, email: str) -> Optional[str]:
        try:
            url = f"{self.jira_base_url}/rest/api/3/user/search"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            response = requests.get(url, params={"query": email}, auth=auth, headers={"Accept": "application/json"})
            if response.status_code == 200:
                users = response.json()
                return users[0].get('accountId') if users else None
        except:
            pass
        return None

    def _get_field_id(self, field_name: str) -> str:
        if field_name.startswith("customfield_"):
            return field_name
        standard = {"description": "description", "originalEstimate": "originalEstimate", "originalestimate": "originalEstimate"}
        if field_name.lower() in standard:
            return standard[field_name.lower()]
        if field_name in self._field_id_cache:
            return self._field_id_cache[field_name]
        try:
            url = f"{self.jira_base_url}/rest/api/3/field"
            auth = HTTPBasicAuth(self.jira_username, self.jira_api_token)
            response = requests.get(url, auth=auth, headers={"Accept": "application/json"})
            if response.status_code == 200:
                for f in response.json():
                    if f.get("name", "").lower() == field_name.lower():
                        self._field_id_cache[field_name] = f.get("id")
                        return f.get("id")
        except:
            pass
        return field_name

    def _adf_to_text(self, adf: Any) -> str:
        if isinstance(adf, str):
            return adf
        if not isinstance(adf, dict):
            return ""
        parts = []
        def extract(node):
            if isinstance(node, dict):
                if node.get("type") == "text":
                    parts.append(node.get("text", ""))
                for child in node.get("content", []):
                    extract(child)
            elif isinstance(node, list):
                for item in node:
                    extract(item)
        extract(adf)
        return " ".join(parts)

    def _markdown_to_adf(self, text: str) -> Dict:
        paragraphs = text.split("\n\n") if "\n\n" in text else [text]
        content = []
        for para in paragraphs:
            if para.strip():
                content.append({"type": "paragraph", "content": [{"type": "text", "text": para.strip()}]})
        return {"type": "doc", "version": 1, "content": content}

# ============================================================================
# CODE GENERATORS
# ============================================================================

class PseudoCodeGenerator:
    def __init__(self, language: str):
        self.language = language

    def generate(self, issue: JiraIssue) -> PseudoCode:
        complexity = self._analyze_complexity(issue)
        steps = self._generate_steps(issue)
        return PseudoCode(
            sections=[{"title": "Implementation Algorithm", "steps": steps}],
            complexity=complexity,
            notes=[f"Target: {self.language.upper()}", f"Complexity: {complexity.value}"]
        )

    def _analyze_complexity(self, issue: JiraIssue) -> ComplexityLevel:
        desc_len = len(issue.description)
        issue_type = issue.issue_type.lower()
        if issue_type in ["bug", "task"] and desc_len < 200:
            return ComplexityLevel.SIMPLE
        elif issue_type in ["feature", "story"] or desc_len > 500:
            return ComplexityLevel.COMPLEX
        return ComplexityLevel.MODERATE

    def _generate_steps(self, issue: JiraIssue) -> str:
        desc = issue.description.lower()
        has_api = any(w in desc for w in ['api', 'endpoint', 'service', 'rest'])
        has_db = any(w in desc for w in ['database', 'repository', 'store', 'query'])
        has_validation = any(w in desc for w in ['validate', 'check', 'verify'])
        
        steps = ["BEGIN"]
        if has_validation:
            steps.extend(["  // Input Validation", "  VALIDATE request parameters", "  IF invalid THEN THROW ValidationException", ""])
        steps.extend([f"  // Main Logic: {issue.title}", "  PROCESS request data", "  APPLY business rules"])
        if has_db:
            steps.append("  EXECUTE database operation")
        if has_api:
            steps.append("  CALL external API if needed")
        steps.extend(["", "  // Response", "  CREATE response", "  RETURN result", "END"])
        return "\n".join(steps)


class SourceCodeGenerator:
    def __init__(self, language: str):
        self.language = language

    def generate(self, issue: JiraIssue, pseudo_code: PseudoCode) -> SourceCode:
        class_name = self._to_class_name(issue.title)
        if self.language == "java":
            return self._java_code(class_name)
        return self._angular_code(class_name)

    def _to_class_name(self, title: str) -> str:
        skip = {'a','an','the','is','are','to','of','for','with','write','create','update','delete','new','this','that'}
        words = [w.capitalize() for w in re.sub(r'[^a-zA-Z0-9\s]', '', title).split() 
                 if w.lower() not in skip and len(w) > 2][:3]
        return "".join(words) or "Default"

    def _java_code(self, name: str) -> SourceCode:
        ctrl = f'''@RestController
@RequestMapping("/api/{name.lower()}")
@RequiredArgsConstructor
public class {name}Controller {{
    private final {name}Service service;
    
    @PostMapping
    public ResponseEntity<?> create(@Valid @RequestBody RequestDTO dto) {{
        return ResponseEntity.ok(service.create(dto));
    }}
    
    @GetMapping("/{{id}}")
    public ResponseEntity<?> getById(@PathVariable Long id) {{
        return ResponseEntity.ok(service.findById(id));
    }}
}}'''
        svc = f'''@Service
@RequiredArgsConstructor
public class {name}Service {{
    private final {name}Repository repository;
    
    @Transactional
    public ResponseDTO create(RequestDTO dto) {{
        validateBusinessRules(dto);
        Entity entity = mapToEntity(dto);
        return mapToResponse(repository.save(entity));
    }}
    
    public ResponseDTO findById(Long id) {{
        return repository.findById(id)
            .map(this::mapToResponse)
            .orElseThrow(() -> new NotFoundException("Not found: " + id));
    }}
}}'''
        return SourceCode("java", [
            {"filename": f"{name}Controller.java", "code": ctrl, "description": "REST Controller"},
            {"filename": f"{name}Service.java", "code": svc, "description": "Service Layer"}
        ], ["spring-boot-starter-web", "spring-boot-starter-data-jpa", "lombok"],
           ["Add dependencies to pom.xml", "Configure application.properties", "Run: mvn spring-boot:run"])

    def _angular_code(self, name: str) -> SourceCode:
        kebab = re.sub(r'([a-z])([A-Z])', r'\1-\2', name).lower()
        comp = f'''@Component({{
  selector: 'app-{kebab}',
  templateUrl: './{kebab}.component.html'
}})
export class {name}Component implements OnInit {{
  data: any[] = [];
  loading = false;
  
  constructor(private service: {name}Service) {{}}
  
  ngOnInit(): void {{ this.loadData(); }}
  
  loadData(): void {{
    this.loading = true;
    this.service.getData().subscribe({{
      next: (r) => {{ this.data = r; this.loading = false; }},
      error: (e) => {{ console.error(e); this.loading = false; }}
    }});
  }}
}}'''
        svc = f'''@Injectable({{ providedIn: 'root' }})
export class {name}Service {{
  private apiUrl = '/api/{kebab}';
  
  constructor(private http: HttpClient) {{}}
  
  getData(): Observable<any[]> {{
    return this.http.get<any[]>(this.apiUrl).pipe(catchError(this.handleError));
  }}
  
  create(data: any): Observable<any> {{
    return this.http.post<any>(this.apiUrl, data).pipe(catchError(this.handleError));
  }}
  
  private handleError(error: any): Observable<never> {{
    return throwError(() => error);
  }}
}}'''
        return SourceCode("angular", [
            {"filename": f"{kebab}.component.ts", "code": comp, "description": "Component"},
            {"filename": f"{kebab}.service.ts", "code": svc, "description": "Service"}
        ], ["@angular/core", "@angular/common", "rxjs"],
           ["Run: npm install", "Import in module", "Run: ng serve"])

# ============================================================================
# EFFORT ESTIMATOR
# ============================================================================

class EffortEstimator:
    BASE_HOURS = {
        ComplexityLevel.SIMPLE: {"design": 1, "implementation": 2, "testing": 1, "review": 0.5},
        ComplexityLevel.MODERATE: {"design": 2, "implementation": 4, "testing": 2, "review": 1},
        ComplexityLevel.COMPLEX: {"design": 4, "implementation": 8, "testing": 4, "review": 2}
    }

    def __init__(self, max_hours: float = 4.0, hours_per_day: float = 8.0):
        self.max_hours = max_hours
        self.hours_per_day = hours_per_day

    def estimate(self, issue: JiraIssue, pseudo_code: PseudoCode, language: str) -> TaskBreakdown:
        base = self.BASE_HOURS[pseudo_code.complexity]
        tasks = [
            EffortEstimate(f"Design - {issue.title[:30]}", pseudo_code.complexity, base["design"], base["design"]/self.hours_per_day),
            EffortEstimate(f"Implementation ({language})", pseudo_code.complexity, base["implementation"], base["implementation"]/self.hours_per_day),
            EffortEstimate("Testing", pseudo_code.complexity, base["testing"], base["testing"]/self.hours_per_day),
            EffortEstimate("Code Review", pseudo_code.complexity, base["review"], base["review"]/self.hours_per_day)
        ]
        total_hours = sum(t.estimated_hours for t in tasks)
        if total_hours > self.max_hours:
            scale = self.max_hours / total_hours
            tasks = [EffortEstimate(t.task_name, t.complexity, round(t.estimated_hours*scale, 2), 
                     round(t.estimated_hours*scale/self.hours_per_day, 2)) for t in tasks]
            total_hours = self.max_hours
        return TaskBreakdown(tasks, round(total_hours, 2), round(total_hours/self.hours_per_day, 2))

# ============================================================================
# FORMATTER
# ============================================================================

class MarkdownFormatter:
    def format(self, result: AnalysisResult) -> str:
        issue = result.issue
        pseudo = result.pseudo_code
        source = result.source_code
        effort = result.effort_estimate
        
        sections = [
            f"# {issue.issue_id}: {issue.title}\n\n---",
            f"## Issue Details\n| Field | Value |\n|-------|-------|\n| Type | {issue.issue_type} |\n| Priority | {issue.priority} |\n| Status | {issue.status} |\n\n### Description\n{issue.description}",
            f"## Pseudo Code\n**Complexity:** `{pseudo.complexity.value}`\n\n```\n{pseudo.sections[0]['steps']}\n```",
            f"## Source Code ({source.language.upper()})\n" + "\n\n".join([f"### {f['filename']}\n```\n{f['code']}\n```" for f in source.files]),
            "## Effort Estimation\n| Task | Hours | Days |\n|------|-------|------|\n" + "\n".join([f"| {t.task_name} | {t.estimated_hours} | {t.estimated_days:.2f} |" for t in effort.tasks]) + f"\n| **Total** | **{effort.total_hours}** | **{effort.total_days:.2f}** |\n| **With Buffer** | **{effort.total_hours*1.2:.2f}** | **{effort.total_with_buffer:.2f}** |",
            f"---\n_Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}_"
        ]
        return "\n\n".join(sections)

# ============================================================================
# MAIN AGENT
# ============================================================================

class JiraAnalysisAgent:
    def __init__(self, config: AgentConfig):
        self.config = config
        lang = {"BE": "java", "UI": "angular"}.get(config.language, config.language)
        self.is_fullstack = lang == "fullstack"
        self.backend_lang = config.backend_language or "java" if self.is_fullstack or lang == "java" else None
        self.frontend_lang = config.frontend_language or "angular" if self.is_fullstack or lang == "angular" else None
        
        self.jira_client = MCPJiraClient(config.jira_provider)
        self.effort_estimator = EffortEstimator(config.max_hours)
        self.formatter = MarkdownFormatter()

    def analyze_issue(self, issue_id: str, **kwargs) -> AnalysisResult:
        print(f"📥 Fetching: {issue_id}")
        issue = self.jira_client.parse_issue_response(self.jira_client.get_issue_detail(issue_id, **kwargs))
        print(f"✅ {issue.title}")

        lang = self.backend_lang or self.frontend_lang or "java"
        print(f"🔍 Generating pseudo code ({lang})")
        pseudo = PseudoCodeGenerator(lang).generate(issue)
        
        print(f"💻 Generating source code")
        source = SourceCodeGenerator(lang).generate(issue, pseudo)
        
        print(f"📊 Estimating effort")
        effort = self.effort_estimator.estimate(issue, pseudo, lang)
        
        recommendations = []
        if pseudo.complexity == ComplexityLevel.COMPLEX:
            recommendations.append("Consider breaking into smaller tasks")
        if effort.total_with_buffer > self.config.max_hours / 8:
            recommendations.append(f"Effort exceeds {self.config.max_hours}h limit")
        
        return AnalysisResult(issue, pseudo, source, effort, recommendations)

    def generate_report(self, result: AnalysisResult, **kwargs) -> str:
        return self.formatter.format(result)

    def update_jira_with_analysis(self, result: AnalysisResult, assign_to: Optional[str] = None, **kwargs) -> bool:
        try:
            # 1. Update Pseudo Code field
            print(f"📝 Updating Pseudo Code field...")
            pseudo_text = f"🔍 Pseudo Code ({result.pseudo_code.complexity.value})\n\n{result.pseudo_code.sections[0]['steps']}"
            if self.jira_client.update_issue_field(result.issue.issue_id, self.config.pseudo_code_field, pseudo_text):
                print(f"✅ Pseudo Code updated")
            else:
                print(f"⚠️ Pseudo Code update failed")
            
            # 2. Update Source Code field
            if self.config.source_code_field:
                print(f"📝 Updating Source Code field...")
                source_text = f"💻 Source Code ({result.source_code.language.upper()})\n\n"
                for f in result.source_code.files:
                    source_text += f"// === {f['filename']} ===\n{f['code']}\n\n"
                if self.jira_client.update_issue_field(result.issue.issue_id, self.config.source_code_field, source_text):
                    print(f"✅ Source Code updated")
                else:
                    print(f"⚠️ Source Code update failed")
            
            # 3. Add effort estimation as ADF table comment
            print(f"📊 Adding effort estimation comment...")
            headers = ["Task", "Hours", "Days"]
            rows = [[t.task_name, str(t.estimated_hours), f"{t.estimated_days:.2f}"] for t in result.effort_estimate.tasks]
            rows.append(["TOTAL", str(result.effort_estimate.total_hours), f"{result.effort_estimate.total_days:.2f}"])
            rows.append([f"With Buffer ({int(result.effort_estimate.buffer_percentage)}%)",
                        f"{result.effort_estimate.total_hours * 1.2:.2f}",
                        f"{result.effort_estimate.total_with_buffer:.2f}"])
            if self.jira_client.add_comment_with_table(result.issue.issue_id, "📊 Effort Estimation", headers, rows):
                print(f"✅ Effort table added")
            else:
                print(f"⚠️ Effort comment failed")
            
            # 4. Assign if requested
            if assign_to:
                if self.jira_client.assign_issue(result.issue.issue_id, assign_to):
                    print(f"✅ Assigned to {assign_to}")
            
            print(f"✅ Jira updated: {result.issue.issue_id}")
            return True
        except Exception as e:
            print(f"❌ Failed: {e}")
            return False


def main():
    config = AgentConfig(language="java", max_hours=4.0)
    agent = JiraAnalysisAgent(config)
    result = agent.analyze_issue("DL-123")
    print(agent.generate_report(result))


if __name__ == "__main__":
    main()
