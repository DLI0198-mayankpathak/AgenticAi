"""
Effort Estimation Module
Calculates effort estimates based on complexity and task breakdown
"""
from typing import List, Dict, Any
from .models import (
    JiraIssue, 
    PseudoCode, 
    EffortEstimate, 
    TaskBreakdown, 
    ComplexityLevel
)


class EffortEstimator:
    """Estimates effort for development tasks"""
    
    # Base hours for different task types by complexity
    BASE_HOURS = {
        ComplexityLevel.SIMPLE: {
            "design": 2,
            "implementation": 4,
            "testing": 2,
            "code_review": 1,
            "documentation": 1
        },
        ComplexityLevel.MODERATE: {
            "design": 4,
            "implementation": 8,
            "testing": 4,
            "code_review": 2,
            "documentation": 2
        },
        ComplexityLevel.COMPLEX: {
            "design": 8,
            "implementation": 16,
            "testing": 8,
            "code_review": 3,
            "documentation": 3
        }
    }
    
    def __init__(self, max_hours: float = 4.0, hours_per_day: float = 8.0):
        self.max_hours = max_hours
        self.hours_per_day = hours_per_day
        self.max_days = max_hours / hours_per_day  # Calculate max_days for compatibility
    
    def estimate(
        self, 
        issue: JiraIssue, 
        pseudo_code: PseudoCode,
        language: str
    ) -> TaskBreakdown:
        """Generate effort estimation breakdown based on issue description and requirements"""
        
        complexity = pseudo_code.complexity
        
        # Analyze description for effort factors
        description = issue.description.lower()
        title = issue.title.lower()
        
        # Detect complexity factors from description
        has_api = any(word in description or word in title for word in ['api', 'endpoint', 'service', 'rest'])
        has_db = any(word in description or word in title for word in ['database', 'table', 'repository', 'query', 'store'])
        has_ui = any(word in description or word in title for word in ['ui', 'form', 'page', 'component', 'display', 'screen'])
        has_validation = any(word in description for word in ['validate', 'check', 'verify', 'validation'])
        has_integration = any(word in description for word in ['integrate', 'third-party', 'external', 'api call'])
        is_crud = any(word in description or word in title for word in ['create', 'update', 'delete', 'fetch', 'list', 'crud'])
        
        # Count number of requirements (rough estimate)
        requirement_indicators = description.count('\n') + description.count(',') + description.count('and')
        
        # Adjust complexity based on description analysis
        if requirement_indicators > 10 or (has_api and has_db and has_ui):
            if complexity == ComplexityLevel.SIMPLE:
                complexity = ComplexityLevel.MODERATE
            elif complexity == ComplexityLevel.MODERATE:
                complexity = ComplexityLevel.COMPLEX
        
        # Generate task estimates based on actual requirements
        tasks = self._generate_task_estimates_from_description(
            issue, complexity, language, has_api, has_db, has_ui, 
            has_validation, has_integration, is_crud
        )
        
        # Calculate totals
        total_hours = sum(task.estimated_hours for task in tasks)
        total_days = total_hours / self.hours_per_day
        
        # Adjust if exceeds max hours
        if total_hours > self.max_hours:
            tasks = self._scale_down_estimates(tasks, total_hours, self.max_hours)
            total_hours = sum(task.estimated_hours for task in tasks)
            total_days = total_hours / self.hours_per_day
        
        return TaskBreakdown(
            tasks=tasks,
            total_hours=round(total_hours, 2),
            total_days=round(total_days, 2),
            buffer_percentage=20.0
        )
    
    def _generate_task_estimates_from_description(
        self, 
        issue: JiraIssue, 
        complexity: ComplexityLevel,
        language: str,
        has_api: bool,
        has_db: bool,
        has_ui: bool,
        has_validation: bool,
        has_integration: bool,
        is_crud: bool
    ) -> List[EffortEstimate]:
        """Generate individual task estimates based on description analysis"""
        
        base_hours = self.BASE_HOURS[complexity]
        tasks = []
        
        # 1. Analysis & Design (always required)
        design_hours = base_hours["design"]
        if has_integration or (has_api and has_db and has_ui):
            design_hours *= 1.3  # More design needed for complex integrations
        
        tasks.append(EffortEstimate(
            task_name=f"Analysis & Technical Design - {issue.title[:40]}",
            complexity=complexity,
            estimated_hours=round(design_hours, 2),
            estimated_days=round(design_hours / self.hours_per_day, 2),
            assumptions=[
                f"Requirements from Jira: {issue.issue_id}",
                "All dependencies and APIs are documented"
            ],
            risk_factors=self._get_design_risks(issue, complexity)
        ))
        
        # 2. Implementation - break down by components mentioned in description
        impl_hours = base_hours["implementation"]
        impl_tasks = []
        
        if has_api or 'api' in issue.description.lower():
            impl_tasks.append("API Endpoint Development")
        if has_db or 'database' in issue.description.lower():
            impl_tasks.append("Database Layer Implementation")
        if has_ui or language == "angular":
            impl_tasks.append("UI Component Development")
        if has_validation:
            impl_tasks.append("Validation Logic")
        if is_crud:
            impl_tasks.append("CRUD Operations")
        
        if not impl_tasks:
            impl_tasks = ["Core Implementation"]
        
        # Adjust implementation hours based on number of components
        if len(impl_tasks) > 2:
            impl_hours *= 1.2
        
        tasks.append(EffortEstimate(
            task_name=f"Implementation ({', '.join(impl_tasks[:2])})",
            complexity=complexity,
            estimated_hours=round(impl_hours, 2),
            estimated_days=round(impl_hours / self.hours_per_day, 2),
            assumptions=[
                f"Based on requirements: {issue.title}",
                f"Components needed: {', '.join(impl_tasks)}"
            ],
            risk_factors=self._get_implementation_risks(issue, language, has_integration)
        ))
        
        # 3. Testing
        test_hours = base_hours["testing"]
        if has_integration or has_api:
            test_hours *= 1.2  # More testing for integrations
        
        tasks.append(EffortEstimate(
            task_name="Unit & Integration Testing",
            complexity=complexity,
            estimated_hours=round(test_hours, 2),
            estimated_days=round(test_hours / self.hours_per_day, 2),
            assumptions=[
                "Test framework is already set up",
                "Mock data/services are available"
            ],
            risk_factors=self._get_testing_risks(issue, complexity)
        ))
        
        # 4. Code Review
        tasks.append(EffortEstimate(
            task_name="Code Review & Fixes",
            complexity=complexity,
            estimated_hours=base_hours["code_review"],
            estimated_days=round(base_hours["code_review"] / self.hours_per_day, 2),
            assumptions=[
                "Code follows project standards",
                "Single round of review"
            ],
            risk_factors=[]
        ))
        
        # 5. Documentation
        doc_hours = base_hours["documentation"]
        if has_api:
            doc_hours *= 1.3  # More docs for APIs
        
        tasks.append(EffortEstimate(
            task_name="Technical Documentation",
            complexity=complexity,
            estimated_hours=round(doc_hours, 2),
            estimated_days=round(doc_hours / self.hours_per_day, 2),
            assumptions=[
                "API documentation required" if has_api else "Standard code documentation",
                "README and inline comments"
            ],
            risk_factors=[]
        ))
        
        return tasks
    
    def _generate_task_estimates(
        self, 
        issue: JiraIssue, 
        complexity: ComplexityLevel,
        language: str
    ) -> List[EffortEstimate]:
        """Generate individual task estimates (legacy method)"""
        
        base_hours = self.BASE_HOURS[complexity]
        tasks = []
        
        # 1. Analysis & Design
        tasks.append(EffortEstimate(
            task_name="Analysis & Technical Design",
            complexity=complexity,
            estimated_hours=base_hours["design"],
            estimated_days=round(base_hours["design"] / self.hours_per_day, 2),
            assumptions=[
                "Requirements are clear and well-defined",
                "All necessary APIs/dependencies are identified"
            ],
            risk_factors=self._get_design_risks(issue, complexity)
        ))
        
        # 2. Implementation
        impl_hours = base_hours["implementation"]
        # Add language-specific adjustments
        if language == "angular":
            impl_hours *= 1.1  # Angular setup can be more involved
        
        tasks.append(EffortEstimate(
            task_name=f"Implementation ({language.upper()})",
            complexity=complexity,
            estimated_hours=impl_hours,
            estimated_days=round(impl_hours / self.hours_per_day, 2),
            assumptions=[
                "Development environment is set up",
                "No major blockers or dependencies",
                "Code follows existing patterns"
            ],
            risk_factors=self._get_implementation_risks(issue, complexity, language)
        ))
        
        # 3. Unit Testing
        tasks.append(EffortEstimate(
            task_name="Unit Testing",
            complexity=complexity,
            estimated_hours=base_hours["testing"],
            estimated_days=round(base_hours["testing"] / self.hours_per_day, 2),
            assumptions=[
                "Test framework is already configured",
                "Mocking libraries are available"
            ],
            risk_factors=["Complex business logic may require additional test cases"]
        ))
        
        # 4. Code Review & Fixes
        tasks.append(EffortEstimate(
            task_name="Code Review & Fixes",
            complexity=complexity,
            estimated_hours=base_hours["code_review"],
            estimated_days=round(base_hours["code_review"] / self.hours_per_day, 2),
            assumptions=[
                "Review feedback is timely",
                "No major refactoring required"
            ],
            risk_factors=["Multiple review cycles may be needed"]
        ))
        
        # 5. Documentation
        tasks.append(EffortEstimate(
            task_name="Documentation",
            complexity=complexity,
            estimated_hours=base_hours["documentation"],
            estimated_days=round(base_hours["documentation"] / self.hours_per_day, 2),
            assumptions=[
                "Documentation templates exist",
                "API documentation is auto-generated"
            ],
            risk_factors=[]
        ))
        
        # 6. Integration (if complex)
        if complexity == ComplexityLevel.COMPLEX:
            tasks.append(EffortEstimate(
                task_name="Integration & E2E Testing",
                complexity=complexity,
                estimated_hours=4,
                estimated_days=0.5,
                assumptions=[
                    "Integration environment is available",
                    "Test data is prepared"
                ],
                risk_factors=[
                    "External API dependencies may cause delays",
                    "Environment issues may require troubleshooting"
                ]
            ))
        
        return tasks
    
    def _get_design_risks(self, issue: JiraIssue, complexity: ComplexityLevel) -> List[str]:
        """Identify design-related risks"""
        risks = []
        
        if complexity == ComplexityLevel.COMPLEX:
            risks.append("Complex requirements may need clarification")
            risks.append("Architecture decisions may require senior review")
        
        if "integration" in issue.description.lower():
            risks.append("Third-party API integration may have unknowns")
        
        if "performance" in issue.description.lower():
            risks.append("Performance requirements may need prototyping")
        
        return risks if risks else ["Minimal risk for simple design"]
    
    def _get_implementation_risks(
        self, 
        issue: JiraIssue, 
        language: str,
        has_integration: bool
    ) -> List[str]:
        """Identify implementation-related risks based on issue description"""
        risks = []
        description = issue.description.lower()
        
        if has_integration:
            risks.append("Third-party integration may have unexpected issues")
        
        if "database" in description:
            risks.append("Database schema changes may need migration")
        
        if language == "angular":
            risks.append("UI/UX feedback may require changes")
            if "form" in description:
                risks.append("Complex form validation may need extra time")
        elif language == "java":
            if "transaction" in description:
                risks.append("Transactional logic requires careful testing")
        
        return risks if risks else ["Standard implementation with minimal risk"]
    
    def _get_testing_risks(self, issue: JiraIssue, complexity: ComplexityLevel) -> List[str]:
        """Identify testing-related risks"""
        risks = []
        description = issue.description.lower()
        
        if complexity == ComplexityLevel.COMPLEX:
            risks.append("Complex scenarios require extensive test coverage")
        
        if "integration" in description or "third-party" in description:
            risks.append("Integration testing may require mock services")
        
        if "database" in description:
            risks.append("Database tests need test data setup")
        
        return risks if risks else []
    
    def _get_implementation_risks_old(
        self, 
        issue: JiraIssue, 
        complexity: ComplexityLevel,
        language: str
    ) -> List[str]:
        """Identify implementation-related risks (legacy method)"""
        risks = []
        
        if complexity == ComplexityLevel.COMPLEX:
            risks.append("Complex logic may require multiple iterations")
        
        if language == "angular":
            risks.append("UI/UX feedback may require UI changes")
            if "form" in issue.description.lower():
                risks.append("Complex form validation may need extra time")
        elif language == "java":
            if "database" in issue.description.lower():
                risks.append("Database schema changes may need migration")
            if "transaction" in issue.description.lower():
                risks.append("Transactional logic requires careful testing")
        
        return risks if risks else ["Standard implementation with minimal risk"]
    
    def _scale_down_estimates(
        self, 
        tasks: List[EffortEstimate], 
        current_hours: float,
        max_hours: float
    ) -> List[EffortEstimate]:
        """Scale down estimates to fit within max hours"""
        
        scale_factor = max_hours / current_hours
        
        scaled_tasks = []
        for task in tasks:
            new_hours = task.estimated_hours * scale_factor
            scaled_tasks.append(EffortEstimate(
                task_name=task.task_name,
                complexity=task.complexity,
                estimated_hours=round(new_hours, 2),
                estimated_days=round(new_hours / self.hours_per_day, 2),
                assumptions=task.assumptions + [
                    f"Estimate scaled to fit {max_hours} hour constraint"
                ],
                risk_factors=task.risk_factors + [
                    "Reduced time may impact quality or require shortcuts"
                ]
            ))
        
        return scaled_tasks
    
    def generate_effort_table(self, breakdown: TaskBreakdown) -> Dict[str, Any]:
        """Generate a structured effort table for display"""
        
        table_data = {
            "headers": ["Task", "Complexity", "Hours", "Days", "Assumptions", "Risks"],
            "rows": [],
            "totals": {
                "total_hours": breakdown.total_hours,
                "total_days": breakdown.total_days,
                "buffer_percentage": breakdown.buffer_percentage,
                "total_with_buffer": round(breakdown.total_with_buffer, 2)
            }
        }
        
        for task in breakdown.tasks:
            table_data["rows"].append({
                "task": task.task_name,
                "complexity": task.complexity.value,
                "hours": task.estimated_hours,
                "days": task.estimated_days,
                "assumptions": "; ".join(task.assumptions) if task.assumptions else "None",
                "risks": "; ".join(task.risk_factors) if task.risk_factors else "None"
            })
        
        return table_data
