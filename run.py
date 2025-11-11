"""
Quick start script to run the Agentic AI system
"""
from src.agent import JiraAnalysisAgent
from src.config import AgentConfig


def main():
    """Run the Agentic AI system"""
    
    while True:  # Loop to allow retries
        print("=" * 80)
        print("🤖 AGENTIC AI - PSEUDO CODE & ASSIGNEE UPDATE BOT")
        print("=" * 80)
        print()
        
        # Get user input
        issue_id = input("Enter Jira Issue ID (e.g., DL -123): ").strip()
        
        if not issue_id:
            print("❌ Issue ID is required!")
            retry = input("\nTry again? (y/n): ").strip().lower()
            if retry != 'y':
                return
            continue
        
        print("\nSelect language:")
        print("1. Java/Spring Boot")
        print("2. Angular")
        language_choice = input("Enter choice (1 or 2) [default: 1]: ").strip() or "1"
        
        language = "java" if language_choice == "1" else "angular"
        
        max_hours_input = input(f"\nEnter max hours (default: 4.0): ").strip()
        max_hours = float(max_hours_input) if max_hours_input else 4.0
        
        # Ask if user wants to update Jira
        update_jira_input = input("\nUpdate Jira issue with analysis? (y/n) [default: n]: ").strip().lower()
        update_jira = update_jira_input == 'y'
        
        # Ask for developer assignment if updating Jira
        assign_to = None
        if update_jira:
            assign_input = input("Assign to developer (email/username) [press Enter to skip]: ").strip()
            if assign_input:
                assign_to = assign_input
        
        print(f"\n📋 Configuration:")
        print(f"   - Issue ID: {issue_id}")
        print(f"   - Language: {language.upper()}")
        print(f"   - Max Hours: {max_hours}")
        print(f"   - Update Jira: {'Yes' if update_jira else 'No'}")
        if assign_to:
            print(f"   - Assign To: {assign_to}")
        print("\n" + "=" * 80)
        print()
        
        # Configure agent
        config = AgentConfig(
            language=language,
            max_hours=max_hours
        )
        
        # Create and run agent
        agent = JiraAnalysisAgent(config)
        
        try:
            # Analyze issue
            print(f"🔄 Starting analysis...\n")
            result = agent.analyze_issue(issue_id=issue_id)
            
            # Generate report
            output_filename = f"{issue_id.replace('/', '-')}_{language}_analysis.md"
            report = agent.generate_report(result, output_filename=output_filename)
            
            # Update Jira if requested
            jira_update_success = False
            if update_jira:
                print("\n")
                jira_update_success = agent.update_jira_with_analysis(result, assign_to=assign_to)
            
            print("\n" + "=" * 80)
            print("✅ ANALYSIS COMPLETE!")
            print("=" * 80)
            print(f"\n📄 Markdown report saved to: output/{output_filename}")
            if update_jira:
                if jira_update_success:
                    print(f"✅ Jira issue updated successfully")
                else:
                    print(f"⚠️  Jira update failed (see error above)")
            print(f"📝 Total Effort: {result.effort_estimate.total_hours} hours ({result.effort_estimate.total_days} days)")
            print(f"📝 With Buffer: {result.effort_estimate.total_hours * 1.2:.2f} hours ({result.effort_estimate.total_with_buffer:.2f} days)")
            print(f"💻 Files Generated: {len(result.source_code.files)}")
            print()
            
            # If Jira update failed, offer to retry
            if update_jira and not jira_update_success:
                retry_jira = input("\nRetry Jira update with different issue ID? (y/n): ").strip().lower()
                if retry_jira == 'y':
                    continue
            
        except Exception as e:
            print(f"\n❌ Error during analysis: {e}")
            import traceback
            traceback.print_exc()
        
        # Ask if user wants to analyze another issue
        print("\n")
        another = input("Analyze another issue? (y/n): ").strip().lower()
        if another != 'y':
            print("\n👋 Thank you for using Agentic AI!")
            break


if __name__ == "__main__":
    main()
