# Asana RL Environment - High-Quality Seed Data Generator

## Overview

This project provides a comprehensive toolkit for generating high-quality seed data for training and evaluating reinforcement learning (RL) agents in an Asana-like task management environment.

## Features

- **Realistic Data Models**: Comprehensive data models for teams, users, projects, and tasks
- **Flexible Configuration**: Multiple predefined scenarios and custom configuration options
- **Quality Validation**: Built-in validation to ensure data consistency and quality
- **Multiple Export Formats**: Export data to JSON and CSV formats
- **Data Analysis Tools**: Utilities for analyzing task distributions, project health, and user workload
- **Extensive Examples**: Ready-to-use example scripts for various use cases

## Project Structure

```
asana_rl_env/
├── __init__.py                 # Package initialization
├── data_models/                # Data models for entities
│   ├── task.py                # Task model with status and priority
│   ├── project.py             # Project model
│   ├── user.py                # User model with roles and workload
│   └── team.py                # Team model
├── generators/                 # Seed data generators
│   └── seed_generator.py      # Main seed data generator
├── validators/                 # Quality validation
│   └── quality_validator.py   # Data quality validator
├── config/                     # Configuration
│   └── generation_config.py   # Generation configuration
├── utils/                      # Utilities
│   └── data_utils.py          # Export, load, and analysis utilities
└── examples/                   # Example scripts
    ├── generate_basic_data.py # Basic data generation
    ├── generate_scenarios.py  # Multiple scenario generation
    └── custom_config.py       # Custom configuration example
```

## Installation

No external dependencies are required for basic functionality. Simply clone the repository:

```bash
git clone https://github.com/Sathvik-ai/Research-Scientist-Internship.git
cd Research-Scientist-Internship
```

## Quick Start

### Basic Usage

```python
from asana_rl_env import SeedDataGenerator, GenerationConfig, QualityValidator

# Create configuration
config = GenerationConfig.medium_dataset()

# Generate data
generator = SeedDataGenerator(config)
data = generator.generate_all()

# Validate data quality
validator = QualityValidator()
is_valid, report = validator.validate_all(
    generator.teams,
    generator.users,
    generator.projects,
    generator.tasks,
)

# Print validation report
validator.print_report(report)
```

### Running Examples

```bash
# Generate basic seed data
python asana_rl_env/examples/generate_basic_data.py

# Generate multiple scenarios
python asana_rl_env/examples/generate_scenarios.py

# Use custom configuration
python asana_rl_env/examples/custom_config.py
```

## Data Models

### Task

Represents a task with the following attributes:
- **Status**: TODO, IN_PROGRESS, IN_REVIEW, COMPLETED, BLOCKED, CANCELLED
- **Priority**: LOW, MEDIUM, HIGH, CRITICAL
- **Metadata**: Assignee, project, due date, dependencies, subtasks, etc.

### Project

Represents a project containing tasks:
- **Status**: PLANNING, ACTIVE, ON_HOLD, COMPLETED, ARCHIVED
- **Attributes**: Owner, team, members, tasks, timeline, etc.

### User

Represents a user with:
- **Role**: VIEWER, MEMBER, ADMIN, OWNER
- **Workload**: Current workload and capacity tracking
- **Skills**: List of expertise areas

### Team

Represents a team with:
- **Members**: List of user IDs
- **Projects**: List of project IDs
- **Owner**: Team owner/leader

## Configuration Options

### Predefined Scenarios

```python
# Small dataset (for testing)
config = GenerationConfig.small_dataset()
# 2 teams, 10 users, 5 projects, 30 tasks

# Medium dataset (default)
config = GenerationConfig.medium_dataset()
# 5 teams, 25 users, 10 projects, 100 tasks

# Large dataset (for production)
config = GenerationConfig.large_dataset()
# 10 teams, 50 users, 25 projects, 300 tasks

# Stress test (high complexity)
config = GenerationConfig.stress_test()
# 20 teams, 100 users, 50 projects, 1000 tasks

# Edge cases (unusual scenarios)
config = GenerationConfig.edge_cases()
# Includes high dependency and subtask rates
```

### Custom Configuration

```python
config = GenerationConfig(
    num_teams=5,
    num_users=25,
    num_projects=10,
    num_tasks=100,
    team_size_range=(3, 8),
    project_size_range=(5, 20),
    task_complexity_range=(0.1, 0.9),
    dependency_probability=0.2,
    subtask_probability=0.15,
    overdue_probability=0.1,
    realistic_mode=True,
    seed=42,
    scenario="custom",
)
```

## Quality Validation

The quality validator checks for:

- **Data Consistency**: Ensures all references are valid
- **Relationship Integrity**: Validates bidirectional relationships
- **Realistic Distributions**: Checks for realistic data patterns
- **Edge Cases Coverage**: Ensures diverse scenarios are represented

Quality metrics include:
- **Completeness Score**: Measures data completeness (0-100)
- **Consistency Score**: Measures data consistency (0-100)
- **Diversity Score**: Measures data variety (0-100)

## Data Export

### JSON Export

```python
from asana_rl_env.utils import DataExporter

DataExporter.export_to_json(data, "output/seed_data.json")
```

### CSV Export

```python
DataExporter.export_to_csv(tasks, "output/tasks.csv")
```

### Multi-format Export

```python
DataExporter.export_all_formats(data, "output/")
```

## Data Analysis

### Task Distribution Analysis

```python
from asana_rl_env.utils import DataAnalyzer

task_analysis = DataAnalyzer.analyze_task_distribution(tasks)
print(f"Total tasks: {task_analysis['total_tasks']}")
print(f"Overdue tasks: {task_analysis['overdue_tasks']}")
```

### Project Health Analysis

```python
project_health = DataAnalyzer.analyze_project_health(projects, tasks)
print(f"Average completion rate: {project_health['avg_completion_rate']:.1%}")
```

### User Workload Analysis

```python
workload_analysis = DataAnalyzer.analyze_user_workload(users, tasks)
print(f"Available users: {workload_analysis['available_users']}")
```

## Use Cases

### 1. Training RL Agents

Generate diverse scenarios for training task management agents:

```python
# Generate training data
config = GenerationConfig.large_dataset()
config.realistic_mode = True
generator = SeedDataGenerator(config)
training_data = generator.generate_all()
```

### 2. Testing and Validation

Create edge cases for testing agent robustness:

```python
# Generate edge case data
config = GenerationConfig.edge_cases()
generator = SeedDataGenerator(config)
test_data = generator.generate_all()
```

### 3. Performance Benchmarking

Generate stress test data for performance evaluation:

```python
# Generate stress test data
config = GenerationConfig.stress_test()
generator = SeedDataGenerator(config)
benchmark_data = generator.generate_all()
```

## Advanced Features

### Dependency Management

The generator automatically creates realistic task dependencies:
- Tasks within the same project can depend on each other
- Circular dependencies are avoided
- Blocked status is assigned to tasks with incomplete dependencies

### Subtask Generation

Complex tasks can have subtasks:
- Configurable subtask probability
- Subtasks inherit parent task properties
- Realistic subtask completion tracking

### Realistic Distributions

When `realistic_mode=True`:
- Task statuses follow realistic distributions
- Due dates align with project timelines
- User workloads are balanced
- Completion rates are realistic

## Statistics and Metrics

Get comprehensive statistics about generated data:

```python
stats = generator.get_statistics()
print(stats)
```

Returns:
- Total counts for each entity type
- Status and priority distributions
- Dependency and subtask counts
- Average metrics per entity

## Contributing

This is a research project. Contributions and feedback are welcome!

## License

This project is part of research work and is provided as-is for educational and research purposes.

## Contact

For questions or issues, please create an issue in the GitHub repository.

## Acknowledgments

This seed data generator was designed to facilitate research in reinforcement learning for task management systems, inspired by platforms like Asana.
