"""
Main Agent Module
Orchestrates the entire workflow from Jira issue fetch to report generation
"""
from typing import Optional
from .config import AgentConfig
from .models import JiraIssue, AnalysisResult, PseudoCode, SourceCode
from .mcp_client import MCPJiraClient, MCPBitbucketClient
from .code_generator import PseudoCodeGenerator, SourceCodeGenerator
from .effort_estimator import EffortEstimator
from .formatter import MarkdownFormatter


class JiraAnalysisAgent:
    """Main agent that orchestrates the analysis workflow"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        
        # Map BE/UI to actual languages
        language = config.language
        if language == "BE":
            actual_language = "java"
        elif language == "UI":
            actual_language = "angular"
        else:
            actual_language = language
        
        # Determine actual languages to use
        if actual_language == "fullstack":
            self.backend_lang = config.backend_language or "java"
            self.frontend_lang = config.frontend_language or "angular"
            self.is_fullstack = True
        else:
            self.backend_lang = actual_language if actual_language == "java" else None
            self.frontend_lang = actual_language if actual_language == "angular" else None
            self.is_fullstack = False
        
        self.jira_client = MCPJiraClient(provider=config.jira_provider)
        self.bitbucket_client = MCPBitbucketClient(provider=config.bitbucket_provider)
        self.effort_estimator = EffortEstimator(max_hours=config.max_hours)
        self.markdown_formatter = MarkdownFormatter()
    
    def analyze_issue(
        self,
        issue_id: str,
        repository_name: Optional[str] = None,
        repository_organization: Optional[str] = None,
        azure_organization: Optional[str] = None,
        azure_project: Optional[str] = None
    ) -> AnalysisResult:
        """
        Main workflow to analyze a Jira issue
        
        Args:
            issue_id: Jira issue ID (e.g., "DL-123")
            repository_name: Optional repository name for Bitbucket
            repository_organization: Optional organization name
            azure_organization: Optional Azure DevOps organization
            azure_project: Optional Azure DevOps project
            
        Returns:
            AnalysisResult containing all generated artifacts
        """
        
        # Step 1: Fetch Jira Issue
        print(f"📥 Fetching Jira issue: {issue_id}")
        issue_data = self.jira_client.get_issue_detail(
            issue_id=issue_id,
            repository_name=repository_name,
            repository_organization=repository_organization,
            azure_organization=azure_organization,
            azure_project=azure_project
        )
        issue = self.jira_client.parse_issue_response(issue_data)
        print(f"✅ Issue fetched: {issue.title}")
        
        # Step 2: Generate Pseudo Code
        be_pseudo_code = None  # Initialize for fullstack
        fe_pseudo_code = None  # Initialize for fullstack
        
        if self.is_fullstack:
            backend_lang = self.backend_lang or "java"
            frontend_lang = self.frontend_lang or "angular"
            print(f"🔍 Generating pseudo code for FULLSTACK (BE: {backend_lang.upper()}, FE: {frontend_lang.upper()})")
            # Generate for both backend and frontend
            be_pseudo_generator = PseudoCodeGenerator(language=backend_lang)
            fe_pseudo_generator = PseudoCodeGenerator(language=frontend_lang)
            
            be_pseudo_code = be_pseudo_generator.generate(issue)
            fe_pseudo_code = fe_pseudo_generator.generate(issue)
            
            # Combine pseudo codes
            combined_sections = [
                {"title": f"Backend Implementation ({backend_lang.upper()})", "steps": be_pseudo_code.sections[0]['steps']},
                {"title": f"Frontend Implementation ({frontend_lang.upper()})", "steps": fe_pseudo_code.sections[0]['steps']}
            ]
            pseudo_code = PseudoCode(
                sections=combined_sections,
                complexity=be_pseudo_code.complexity,  # Use backend complexity as primary
                notes=be_pseudo_code.notes + fe_pseudo_code.notes
            )
            print(f"✅ Pseudo code generated for both BE and FE (Complexity: {pseudo_code.complexity.value})")
        else:
            lang = self.backend_lang or self.frontend_lang or "java"
            print(f"🔍 Generating pseudo code for {lang.upper()}")
            pseudo_generator = PseudoCodeGenerator(language=lang)
            pseudo_code = pseudo_generator.generate(issue)
            print(f"✅ Pseudo code generated (Complexity: {pseudo_code.complexity.value})")
        
        # Step 3: Generate Source Code
        if self.is_fullstack:
            backend_lang = self.backend_lang or "java"
            frontend_lang = self.frontend_lang or "angular"
            print(f"💻 Generating source code for FULLSTACK")
            be_source_generator = SourceCodeGenerator(language=backend_lang)
            fe_source_generator = SourceCodeGenerator(language=frontend_lang)
            
            # Ensure pseudo codes are available
            if be_pseudo_code and fe_pseudo_code:
                be_source = be_source_generator.generate(issue, be_pseudo_code)
                fe_source = fe_source_generator.generate(issue, fe_pseudo_code)
            else:
                raise ValueError("Pseudo codes not generated for fullstack")
            
            # Combine source codes
            combined_files = []
            combined_files.extend([{**f, "type": "backend"} for f in be_source.files])
            combined_files.extend([{**f, "type": "frontend"} for f in fe_source.files])
            
            source_code = SourceCode(
                language="fullstack",
                files=combined_files,
                dependencies=be_source.dependencies + fe_source.dependencies,
                setup_instructions=be_source.setup_instructions + ["---"] + fe_source.setup_instructions
            )
            print(f"✅ Generated {len(be_source.files)} BE + {len(fe_source.files)} FE files")
        else:
            print(f"💻 Generating source code")
            lang = self.backend_lang or self.frontend_lang or "java"
            source_generator = SourceCodeGenerator(language=lang)
            source_code = source_generator.generate(issue, pseudo_code)
            print(f"✅ Generated {len(source_code.files)} source files")
        
        # Step 4: Estimate Effort
        print(f"📊 Calculating effort estimation")
        lang = "fullstack" if self.is_fullstack else (self.backend_lang or self.frontend_lang or "java")
        effort_estimate = self.effort_estimator.estimate(issue, pseudo_code, lang)
        print(f"✅ Estimated: {effort_estimate.total_days} days (without buffer)")
        
        # Step 5: Generate Recommendations
        recommendations = self._generate_recommendations(
            issue, 
            pseudo_code, 
            source_code, 
            effort_estimate
        )
        
        return AnalysisResult(
            issue=issue,
            pseudo_code=pseudo_code,
            source_code=source_code,
            effort_estimate=effort_estimate,
            recommendations=recommendations
        )
    
    def generate_report(
        self,
        result: AnalysisResult,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Generate markdown report from analysis result
        
        Args:
            result: Analysis result to format
            output_filename: Optional filename (deprecated, kept for compatibility)
            
        Returns:
            Markdown formatted report as string
        """
        
        print(f"📝 Generating markdown report")
        markdown_report = self.markdown_formatter.format(result)
        
        return markdown_report
    
    def update_jira_with_analysis(
        self,
        result: AnalysisResult,
        repository_name: Optional[str] = None,
        repository_organization: Optional[str] = None,
        azure_organization: Optional[str] = None,
        azure_project: Optional[str] = None,
        assign_to: Optional[str] = None
    ) -> bool:
        """
        Update Jira issue with pseudo code, source code, and effort estimation
        
        Args:
            result: Analysis result to post to Jira
            repository_name: Optional repository name
            repository_organization: Optional organization name
            azure_organization: Optional Azure DevOps organization
            azure_project: Optional Azure DevOps project
            assign_to: Optional developer email or name to assign issue to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Format pseudo code for Jira field
            pseudo_section = self._format_pseudo_for_jira(result)
            
            # Update Pseudo Code field (not description)
            print(f"📝 Updating 'Pseudo Code' field in issue: {result.issue.issue_id}")
            
            pseudo_code_success = self.jira_client.update_issue_field(
                issue_id=result.issue.issue_id,
                field_name=self.config.pseudo_code_field,  # Use configured field name
                field_value=pseudo_section
            )
            
            if pseudo_code_success:
                print(f"✅ Successfully updated 'Pseudo Code' field")
            
            # Update Source Code field if configured
            source_code_success = True
            if self.config.source_code_field:
                source_section = self._format_source_for_jira(result)
                print(f"📝 Updating 'Source Code' field in issue: {result.issue.issue_id}")
                
                source_code_success = self.jira_client.update_issue_field(
                    issue_id=result.issue.issue_id,
                    field_name=self.config.source_code_field,
                    field_value=source_section
                )
                
                if source_code_success:
                    print(f"✅ Successfully updated 'Source Code' field")
            
            # Update Original Estimate field (optional)
            estimate_success = True
            if self.config.original_estimate_field:
                # Average of total_hours and total_hours_with_buffer
                total_hours = result.effort_estimate.total_hours
                total_hours_with_buffer = total_hours * (1 + result.effort_estimate.buffer_percentage / 100)
                avg_hours = (total_hours + total_hours_with_buffer) / 2
                avg_seconds = int(avg_hours * 3600)  # Convert to seconds for Jira
                
                print(f"⏱️  Updating 'Original Estimate' field: {avg_hours:.2f} hours")
                estimate_success = self.jira_client.update_issue_field(
                    issue_id=result.issue.issue_id,
                    field_name=self.config.original_estimate_field,
                    field_value=str(avg_seconds)
                )
                
                if estimate_success:
                    print(f"✅ Successfully updated 'Original Estimate' to {avg_hours:.2f} hours")
            
            # Format effort estimation for Jira comment
            effort_section = self._format_effort_for_jira(result)
            
            # Post comment to Jira issue (only effort estimate table)
            print(f"📤 Posting effort estimate to Jira comment: {result.issue.issue_id}")
            comment_success = self.jira_client.add_comment(
                issue_id=result.issue.issue_id,
                comment=effort_section,
                repository_name=repository_name,
                repository_organization=repository_organization,
                azure_organization=azure_organization,
                azure_project=azure_project
            )
            
            if comment_success:
                print(f"✅ Successfully posted effort estimate comment")
            
            # Assign issue if developer name provided
            if assign_to:
                print(f"👤 Assigning issue to: {assign_to}")
                assign_success = self.jira_client.assign_issue(
                    issue_id=result.issue.issue_id,
                    assignee=assign_to
                )
                if assign_success:
                    print(f"✅ Successfully assigned issue to {assign_to}")
                    # Update the issue object with the new assignee
                    result.issue.assignee = assign_to
                    return pseudo_code_success and source_code_success and estimate_success and comment_success and assign_success
                else:
                    print(f"⚠️  Updates posted but assignment failed")
                    return pseudo_code_success and source_code_success and estimate_success and comment_success
            
            return pseudo_code_success and source_code_success and estimate_success and comment_success
            
        except Exception as e:
            print(f"❌ Failed to update Jira: {e}")
            return False
    
    def _format_pseudo_for_jira(self, result: AnalysisResult) -> str:
        """Format pseudo code section for Jira field as plain text"""
        pseudo = result.pseudo_code
        output = [f"🔍 Pseudo Code (Complexity: {pseudo.complexity.value})\n"]
        
        for section in pseudo.sections:
            # Just add the pseudo code steps directly, no formatting
            output.append(section['steps'])
        
        return "\n".join(output)
    
    def _format_source_for_jira(self, result: AnalysisResult) -> str:
        """Format source code for Jira field with structured formatting"""
        source = result.source_code
        output = []
        
        # Header with language
        output.append("=" * 80)
        output.append(f"💻 GENERATED SOURCE CODE ({source.language.upper()})")
        output.append("=" * 80)
        output.append("")
        
        # Summary
        output.append(f"📁 Total Files: {len(source.files)}")
        output.append(f"🔧 Language: {source.language.upper()}")
        output.append("")
        
        # Dependencies Section
        if source.dependencies:
            output.append("-" * 80)
            output.append("📦 DEPENDENCIES")
            output.append("-" * 80)
            for dep in source.dependencies:
                output.append(f"  • {dep}")
            output.append("")
        
        # Source Files Section
        output.append("-" * 80)
        output.append("📂 SOURCE FILES")
        output.append("-" * 80)
        output.append("")
        
        for i, file_info in enumerate(source.files, 1):
            filename = file_info['filename']
            description = file_info.get('description', 'Source file')
            code = file_info['code']
            
            # File header
            output.append(f"\n{'=' * 80}")
            output.append(f"FILE #{i}: {filename}")
            output.append(f"{'=' * 80}")
            output.append(f"Description: {description}")
            output.append(f"{'-' * 80}")
            output.append("")
            
            # Code block with proper indentation
            output.append("{code:java}" if source.language == "java" else "{code:typescript}" if source.language == "angular" else "{code}")
            output.append(code)
            output.append("{code}")
            output.append("")
        
        # Setup Instructions Section
        if source.setup_instructions:
            output.append("-" * 80)
            output.append("⚙️ SETUP INSTRUCTIONS")
            output.append("-" * 80)
            for i, instruction in enumerate(source.setup_instructions, 1):
                output.append(f"{i}. {instruction}")
            output.append("")
        
        # Footer
        output.append("=" * 80)
        output.append("✅ END OF SOURCE CODE")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    def _format_effort_for_jira(self, result: AnalysisResult) -> str:
        """Format effort estimation for Jira comment as table"""
        breakdown = result.effort_estimate
        output = ["📊 Effort Estimation\n"]
        
        output.append("| Task | Hours | Days | Complexity |")
        output.append("|------|-------|------|------------|")
        
        for task in breakdown.tasks:
            output.append(
                f"| {task.task_name} | {task.estimated_hours:.2f} | "
                f"{task.estimated_days:.2f} | {task.complexity.value} |"
            )
        
        output.append(f"| TOTAL | {breakdown.total_hours:.2f} | {breakdown.total_days:.2f} | |")
        output.append(
            f"| WITH BUFFER ({breakdown.buffer_percentage}%) | "
            f"{breakdown.total_hours * (1 + breakdown.buffer_percentage/100):.2f} | "
            f"{breakdown.total_with_buffer:.2f} | |"
        )
        
        return "\n".join(output)
    
    
    
    def _generate_recommendations(
        self,
        issue: JiraIssue,
        pseudo_code,
        source_code,
        effort_estimate
    ) -> list:
        """Generate recommendations based on analysis"""
        
        recommendations = []
        
        # Complexity-based recommendations
        if pseudo_code.complexity.value == "Complex":
            recommendations.append(
                "Consider breaking this task into smaller sub-tasks for better manageability"
            )
            recommendations.append(
                "Schedule a technical design review before implementation"
            )
        
        # Effort-based recommendations
        max_days = self.config.max_hours / 8.0  # Convert hours to days
        if effort_estimate.total_with_buffer > max_days:
            recommendations.append(
                f"Estimated effort ({effort_estimate.total_with_buffer:.1f} days / {effort_estimate.total_hours * 1.2:.1f} hours) exceeds "
                f"max hours ({self.config.max_hours}h / {max_days:.1f} days). Consider scope reduction or timeline adjustment."
            )
        
        # Language-specific recommendations
        if self.config.language == "java":
            recommendations.append(
                "Ensure proper exception handling and logging throughout the implementation"
            )
            recommendations.append(
                "Write comprehensive unit tests using JUnit and Mockito"
            )
        elif self.config.language == "angular":
            recommendations.append(
                "Follow Angular style guide and use reactive forms for complex scenarios"
            )
            recommendations.append(
                "Implement proper error handling and loading states in the UI"
            )
        
        # Priority-based recommendations
        if issue.priority in ["Critical", "High"]:
            recommendations.append(
                "Given the high priority, consider pair programming or code review during development"
            )
        
        return recommendations


def main():
    """Example usage of the agent"""
    
    # Configure the agent
    config = AgentConfig(
        language="java",  # or "angular"
        max_hours=4.0  # Maximum 4 hours
    )
    
    # Create agent
    agent = JiraAnalysisAgent(config)
    
    # Analyze a Jira issue
    # In real usage with MCP, you would provide actual issue ID
    result = agent.analyze_issue(
        issue_id="DL-123",
        repository_name="my-repo",
        repository_organization="my-org"
    )
    
    # Print effort table
    
    # Generate and save report
    report = agent.generate_report(
        result,
        output_filename=f"{result.issue.issue_id}_analysis.md"
    )
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
