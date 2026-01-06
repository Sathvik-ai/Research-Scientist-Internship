"""
Comprehensive test demonstrating all features of the Asana RL seed data generator.

This script tests:
1. All predefined scenarios
2. Custom configuration
3. Data validation
4. Quality metrics
5. Data export in multiple formats
6. Data analysis utilities
"""

import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from asana_rl_env.generators.seed_generator import SeedDataGenerator
from asana_rl_env.config.generation_config import GenerationConfig
from asana_rl_env.validators.quality_validator import QualityValidator
from asana_rl_env.utils.data_utils import DataExporter, DataLoader, DataAnalyzer


def test_scenario(scenario_name: str, config: GenerationConfig) -> dict:
    """Test a specific scenario."""
    print(f"\nTesting {scenario_name}...")
    print("-" * 60)
    
    # Generate data
    generator = SeedDataGenerator(config)
    data = generator.generate_all()
    
    # Get statistics
    stats = generator.get_statistics()
    print(f"Generated: {stats['total_teams']} teams, {stats['total_users']} users, "
          f"{stats['total_projects']} projects, {stats['total_tasks']} tasks")
    
    # Validate
    validator = QualityValidator()
    is_valid, report = validator.validate_all(
        generator.teams,
        generator.users,
        generator.projects,
        generator.tasks,
    )
    
    print(f"Validation: {'✓ PASSED' if is_valid else '✗ FAILED'}")
    if not is_valid:
        print(f"Errors: {len(report['errors'])}")
        for error in report['errors'][:3]:  # Show first 3 errors
            print(f"  - {error}")
    
    metrics = report['metrics']
    print(f"Quality Scores: Completeness={metrics.get('completeness_score', 0):.0f}%, "
          f"Consistency={metrics.get('consistency_score', 0):.0f}%, "
          f"Diversity={metrics.get('diversity_score', 0):.0f}%")
    
    return {
        "scenario": scenario_name,
        "valid": is_valid,
        "stats": stats,
        "quality": metrics,
    }


def main():
    """Run comprehensive tests."""
    print("=" * 60)
    print("COMPREHENSIVE TEST - ASANA RL SEED DATA GENERATOR")
    print("=" * 60)
    
    results = []
    
    # Test 1: Predefined scenarios
    print("\n[TEST 1] Testing all predefined scenarios...")
    scenarios = [
        ("small_dataset", GenerationConfig.small_dataset()),
        ("medium_dataset", GenerationConfig.medium_dataset()),
        ("large_dataset", GenerationConfig.large_dataset()),
        ("stress_test", GenerationConfig.stress_test()),
        ("edge_cases", GenerationConfig.edge_cases()),
    ]
    
    for scenario_name, config in scenarios:
        result = test_scenario(scenario_name, config)
        results.append(result)
    
    # Test 2: Custom configuration
    print("\n[TEST 2] Testing custom configuration...")
    custom_config = GenerationConfig(
        num_teams=2,
        num_users=8,
        num_projects=4,
        num_tasks=20,
        dependency_probability=0.3,
        subtask_probability=0.2,
        seed=999,
        scenario="custom_test",
    )
    result = test_scenario("custom_test", custom_config)
    results.append(result)
    
    # Test 3: Data export and load
    print("\n[TEST 3] Testing data export and load...")
    print("-" * 60)
    
    generator = SeedDataGenerator(GenerationConfig.small_dataset())
    data = generator.generate_all()
    
    output_dir = Path(__file__).parent / "output" / "test"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test JSON export
    json_path = output_dir / "test_data.json"
    DataExporter.export_to_json(data, str(json_path))
    print(f"✓ Exported to JSON: {json_path}")
    
    # Test JSON load
    loaded_data = DataLoader.load_from_json(str(json_path))
    print(f"✓ Loaded {len(loaded_data['tasks'])} tasks from JSON")
    
    # Test CSV export
    DataExporter.export_to_csv(data['tasks'], str(output_dir / "test_tasks.csv"))
    print(f"✓ Exported tasks to CSV")
    
    # Test multi-format export
    DataExporter.export_all_formats(data, str(output_dir / "multi"))
    print(f"✓ Exported all formats to {output_dir / 'multi'}")
    
    # Test 4: Data analysis
    print("\n[TEST 4] Testing data analysis utilities...")
    print("-" * 60)
    
    # Load entities
    entities = DataLoader.load_entities_from_json(str(json_path))
    
    # Task analysis
    task_analysis = DataAnalyzer.analyze_task_distribution(entities['tasks'])
    print(f"✓ Task analysis: {task_analysis['total_tasks']} tasks, "
          f"{task_analysis['overdue_tasks']} overdue")
    
    # Project health
    project_health = DataAnalyzer.analyze_project_health(
        entities['projects'],
        entities['tasks']
    )
    print(f"✓ Project health: {project_health['total_projects']} projects, "
          f"{project_health['avg_completion_rate']:.1%} avg completion")
    
    # User workload
    workload = DataAnalyzer.analyze_user_workload(
        entities['users'],
        entities['tasks']
    )
    print(f"✓ Workload analysis: {workload['total_users']} users, "
          f"{workload['available_users']} available")
    
    # Final Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for r in results if r['valid'])
    total = len(results)
    
    print(f"\nScenarios tested: {total}")
    print(f"Validation passed: {passed}/{total}")
    
    print("\nResults by scenario:")
    for result in results:
        status = "✓ PASS" if result['valid'] else "✗ FAIL"
        print(f"  {result['scenario']:20s} - {status:8s} - "
              f"Tasks: {result['stats']['total_tasks']:4d}, "
              f"Quality: {result['quality'].get('completeness_score', 0):.0f}%")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED")
        return 0
    else:
        print(f"\n✗ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
