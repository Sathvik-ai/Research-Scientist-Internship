"""
Example: Basic seed data generation

This example demonstrates how to generate basic seed data
for the Asana RL environment.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from asana_rl_env.generators.seed_generator import SeedDataGenerator
from asana_rl_env.config.generation_config import GenerationConfig
from asana_rl_env.validators.quality_validator import QualityValidator
from asana_rl_env.utils.data_utils import DataExporter


def main():
    """Generate basic seed data."""
    print("Generating seed data for Asana RL environment...")
    print("-" * 60)
    
    # Create configuration for medium-sized dataset
    config = GenerationConfig.medium_dataset()
    print(f"Using configuration: {config.scenario}")
    print(f"  - Teams: {config.num_teams}")
    print(f"  - Users: {config.num_users}")
    print(f"  - Projects: {config.num_projects}")
    print(f"  - Tasks: {config.num_tasks}")
    print()
    
    # Generate data
    generator = SeedDataGenerator(config)
    data = generator.generate_all()
    
    # Print statistics
    print("Generation Statistics:")
    stats = generator.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Validate data quality
    print("Validating data quality...")
    validator = QualityValidator()
    is_valid, report = validator.validate_all(
        generator.teams,
        generator.users,
        generator.projects,
        generator.tasks,
    )
    validator.print_report(report)
    
    # Export data
    output_dir = Path(__file__).parent / "output"
    print(f"Exporting data to {output_dir}...")
    DataExporter.export_all_formats(data, str(output_dir))
    
    print("✓ Seed data generation complete!")
    print(f"✓ Data exported to: {output_dir}")


if __name__ == "__main__":
    main()
