"""
Example: Custom configuration

This example demonstrates how to create custom configurations
for specific use cases.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from asana_rl_env.generators.seed_generator import SeedDataGenerator
from asana_rl_env.config.generation_config import GenerationConfig
from asana_rl_env.validators.quality_validator import QualityValidator
from asana_rl_env.utils.data_utils import DataExporter, DataAnalyzer


def main():
    """Generate seed data with custom configuration."""
    print("Creating custom configuration...")
    
    # Create custom configuration
    custom_config = GenerationConfig(
        num_teams=3,
        num_users=15,
        num_projects=6,
        num_tasks=50,
        team_size_range=(4, 6),
        project_size_range=(8, 12),
        dependency_probability=0.3,
        subtask_probability=0.25,
        overdue_probability=0.15,
        realistic_mode=True,
        seed=123,
        scenario="custom_balanced",
        custom_params={
            "focus": "balanced_workload",
            "difficulty": "medium",
        }
    )
    
    print(f"Configuration: {custom_config.scenario}")
    print(f"Custom parameters: {custom_config.custom_params}")
    print()
    
    # Generate data
    generator = SeedDataGenerator(custom_config)
    data = generator.generate_all()
    
    # Validate
    validator = QualityValidator()
    is_valid, report = validator.validate_all(
        generator.teams,
        generator.users,
        generator.projects,
        generator.tasks,
    )
    validator.print_report(report)
    
    # Analyze data
    print("Detailed Analysis:")
    print("-" * 60)
    
    # Task analysis
    task_analysis = DataAnalyzer.analyze_task_distribution(generator.tasks)
    print("\nTask Distribution:")
    print(f"  Total tasks: {task_analysis['total_tasks']}")
    print(f"  Estimated hours: {task_analysis['total_estimated_hours']:.1f}")
    print(f"  Overdue tasks: {task_analysis['overdue_tasks']}")
    print(f"  Blocked tasks: {task_analysis['blocked_tasks']}")
    
    # Project health
    project_health = DataAnalyzer.analyze_project_health(generator.projects, generator.tasks)
    print(f"\nProject Health:")
    print(f"  Total projects: {project_health['total_projects']}")
    print(f"  Avg completion rate: {project_health['avg_completion_rate']:.1%}")
    
    # User workload
    workload_analysis = DataAnalyzer.analyze_user_workload(generator.users, generator.tasks)
    print(f"\nUser Workload:")
    print(f"  Total users: {workload_analysis['total_users']}")
    print(f"  Average workload: {workload_analysis['avg_workload']:.1%}")
    print(f"  Available users: {workload_analysis['available_users']}")
    print(f"  Overloaded users: {workload_analysis['overloaded_users']}")
    
    # Export
    output_dir = Path(__file__).parent / "output" / "custom"
    DataExporter.export_all_formats(data, str(output_dir))
    
    print(f"\n✓ Data exported to: {output_dir}")


if __name__ == "__main__":
    main()
