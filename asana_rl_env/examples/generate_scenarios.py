"""
Example: Generate data for different scenarios

This example demonstrates how to generate seed data
for various training scenarios.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from asana_rl_env.generators.seed_generator import SeedDataGenerator
from asana_rl_env.config.generation_config import GenerationConfig
from asana_rl_env.validators.quality_validator import QualityValidator
from asana_rl_env.utils.data_utils import DataExporter


def generate_scenario(scenario_name: str, config: GenerationConfig):
    """Generate data for a specific scenario."""
    print(f"\nGenerating {scenario_name} scenario...")
    print("-" * 60)
    
    generator = SeedDataGenerator(config)
    data = generator.generate_all()
    
    # Validate
    validator = QualityValidator()
    is_valid, report = validator.validate_all(
        generator.teams,
        generator.users,
        generator.projects,
        generator.tasks,
    )
    
    print(f"Validation: {'✓ PASSED' if is_valid else '✗ FAILED'}")
    print(f"Quality Scores:")
    metrics = report['metrics']
    print(f"  - Completeness: {metrics.get('completeness_score', 0):.1f}/100")
    print(f"  - Consistency: {metrics.get('consistency_score', 0):.1f}/100")
    print(f"  - Diversity: {metrics.get('diversity_score', 0):.1f}/100")
    
    # Export
    output_dir = Path(__file__).parent / "output" / scenario_name
    DataExporter.export_to_json(data, str(output_dir / "seed_data.json"))
    print(f"✓ Exported to: {output_dir}")
    
    return generator, report


def main():
    """Generate seed data for multiple scenarios."""
    print("=" * 60)
    print("ASANA RL ENVIRONMENT - SCENARIO GENERATION")
    print("=" * 60)
    
    scenarios = [
        ("small_dataset", GenerationConfig.small_dataset()),
        ("medium_dataset", GenerationConfig.medium_dataset()),
        ("large_dataset", GenerationConfig.large_dataset()),
        ("stress_test", GenerationConfig.stress_test()),
        ("edge_cases", GenerationConfig.edge_cases()),
    ]
    
    results = {}
    
    for scenario_name, config in scenarios:
        try:
            generator, report = generate_scenario(scenario_name, config)
            results[scenario_name] = {
                "success": True,
                "stats": generator.get_statistics(),
                "quality": report['metrics'],
            }
        except Exception as e:
            print(f"✗ Error generating {scenario_name}: {e}")
            results[scenario_name] = {
                "success": False,
                "error": str(e),
            }
    
    # Summary
    print("\n" + "=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    
    for scenario_name, result in results.items():
        if result['success']:
            print(f"\n{scenario_name}:")
            print(f"  Status: ✓ Success")
            print(f"  Tasks: {result['stats']['total_tasks']}")
            print(f"  Quality: {result['quality'].get('completeness_score', 0):.0f}%")
        else:
            print(f"\n{scenario_name}:")
            print(f"  Status: ✗ Failed")
            print(f"  Error: {result['error']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
