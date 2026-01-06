"""
Quick start guide for the Asana RL Environment seed data generator.

This script provides a simple interactive demonstration of the key features.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from asana_rl_env import SeedDataGenerator, GenerationConfig, QualityValidator
from asana_rl_env.utils.data_utils import DataExporter, DataAnalyzer


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def main():
    """Run quick start demonstration."""
    
    print_section("ASANA RL ENVIRONMENT - SEED DATA GENERATOR")
    
    print("Welcome to the Asana RL Environment Seed Data Generator!")
    print("This tool creates high-quality synthetic data for training RL agents.\n")
    
    # Step 1: Choose configuration
    print_section("STEP 1: Choose a Configuration")
    
    print("Available predefined scenarios:")
    print("  1. Small Dataset    - 2 teams, 10 users, 5 projects, ~30 tasks")
    print("  2. Medium Dataset   - 5 teams, 25 users, 10 projects, ~100 tasks")
    print("  3. Large Dataset    - 10 teams, 50 users, 25 projects, ~300 tasks")
    print("  4. Stress Test      - 20 teams, 100 users, 50 projects, ~1000 tasks")
    print("  5. Edge Cases       - Focus on unusual scenarios and edge cases\n")
    
    # For demo, use medium dataset
    config = GenerationConfig.medium_dataset()
    print(f"Using: Medium Dataset (scenario='{config.scenario}')")
    
    # Step 2: Generate data
    print_section("STEP 2: Generate Data")
    
    print("Generating seed data...")
    generator = SeedDataGenerator(config)
    data = generator.generate_all()
    
    stats = generator.get_statistics()
    print(f"✓ Generated successfully!")
    print(f"\nData Summary:")
    print(f"  • Teams:    {stats['total_teams']}")
    print(f"  • Users:    {stats['total_users']}")
    print(f"  • Projects: {stats['total_projects']}")
    print(f"  • Tasks:    {stats['total_tasks']}")
    
    # Step 3: Validate quality
    print_section("STEP 3: Validate Data Quality")
    
    print("Running quality validation...")
    validator = QualityValidator()
    is_valid, report = validator.validate_all(
        generator.teams,
        generator.users,
        generator.projects,
        generator.tasks,
    )
    
    metrics = report['metrics']
    print(f"Validation Result: {'✓ PASSED' if is_valid else '✗ FAILED'}\n")
    print(f"Quality Metrics:")
    print(f"  • Completeness Score: {metrics.get('completeness_score', 0):.1f}/100")
    print(f"  • Consistency Score:  {metrics.get('consistency_score', 0):.1f}/100")
    print(f"  • Diversity Score:    {metrics.get('diversity_score', 0):.1f}/100")
    
    if report['errors']:
        print(f"\n⚠ Found {len(report['errors'])} error(s)")
    if report['warnings']:
        print(f"⚠ Found {len(report['warnings'])} warning(s)")
    
    # Step 4: Analyze data
    print_section("STEP 4: Analyze Data")
    
    # Task distribution
    task_analysis = DataAnalyzer.analyze_task_distribution(generator.tasks)
    print("Task Distribution:")
    print(f"  • Total tasks:        {task_analysis['total_tasks']}")
    print(f"  • With dependencies:  {task_analysis.get('tasks_with_estimates', 0)}")
    print(f"  • Overdue:            {task_analysis['overdue_tasks']}")
    print(f"  • Blocked:            {task_analysis['blocked_tasks']}")
    
    print(f"\n  Status breakdown:")
    for status, count in task_analysis['status_distribution'].items():
        percentage = (count / task_analysis['total_tasks']) * 100
        print(f"    - {status:15s}: {count:3d} ({percentage:5.1f}%)")
    
    # Project health
    project_health = DataAnalyzer.analyze_project_health(generator.projects, generator.tasks)
    print(f"\nProject Health:")
    print(f"  • Total projects:         {project_health['total_projects']}")
    print(f"  • Avg completion rate:    {project_health['avg_completion_rate']:.1%}")
    
    # User workload
    workload = DataAnalyzer.analyze_user_workload(generator.users, generator.tasks)
    print(f"\nUser Workload:")
    print(f"  • Total users:       {workload['total_users']}")
    print(f"  • Average workload:  {workload['avg_workload']:.1%}")
    print(f"  • Available users:   {workload['available_users']}")
    
    # Step 5: Export data
    print_section("STEP 5: Export Data")
    
    output_dir = Path(__file__).parent / "output" / "quickstart"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Exporting data to: {output_dir}\n")
    
    # Export JSON
    json_path = output_dir / "seed_data.json"
    DataExporter.export_to_json(data, str(json_path))
    print(f"✓ Exported complete dataset: seed_data.json")
    
    # Export CSVs
    DataExporter.export_to_csv(data['teams'], str(output_dir / "teams.csv"))
    DataExporter.export_to_csv(data['users'], str(output_dir / "users.csv"))
    DataExporter.export_to_csv(data['projects'], str(output_dir / "projects.csv"))
    DataExporter.export_to_csv(data['tasks'], str(output_dir / "tasks.csv"))
    print(f"✓ Exported individual CSVs: teams.csv, users.csv, projects.csv, tasks.csv")
    
    # Summary
    print_section("NEXT STEPS")
    
    print("Your seed data is ready! Here's what you can do next:\n")
    print("1. Load the data into your RL environment:")
    print("   from asana_rl_env.utils import DataLoader")
    print(f"   data = DataLoader.load_entities_from_json('{json_path}')\n")
    
    print("2. Customize the configuration:")
    print("   config = GenerationConfig(")
    print("       num_teams=3,")
    print("       num_users=15,")
    print("       dependency_probability=0.3,")
    print("       # ... more options")
    print("   )\n")
    
    print("3. Try other scenarios:")
    print("   python asana_rl_env/examples/generate_scenarios.py\n")
    
    print("4. Run comprehensive tests:")
    print("   python asana_rl_env/examples/comprehensive_test.py\n")
    
    print("For more information, see SEED_DATA_README.md")
    
    print_section("THANK YOU FOR USING THE ASANA RL SEED DATA GENERATOR!")


if __name__ == "__main__":
    main()
