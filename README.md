# Research-Scientist-Internship

## Creating High-Quality Seed Data for Asana RL Environment

This repository provides a comprehensive toolkit for generating high-quality seed data for training and evaluating reinforcement learning (RL) agents in an Asana-like task management environment.

### 🚀 Quick Start

```bash
# Quick start demo
python asana_rl_env/examples/quickstart.py

# Generate basic seed data
python asana_rl_env/examples/generate_basic_data.py

# Generate multiple scenarios
python asana_rl_env/examples/generate_scenarios.py

# Use custom configuration
python asana_rl_env/examples/custom_config.py

# Run comprehensive tests
python asana_rl_env/examples/comprehensive_test.py
```

### 📋 Features

- **Realistic Data Models**: Teams, users, projects, and tasks with comprehensive attributes
- **Flexible Configuration**: Predefined scenarios (small, medium, large, stress test, edge cases)
- **Quality Validation**: Built-in validation for data consistency and quality
- **Multiple Export Formats**: JSON and CSV export capabilities
- **Data Analysis Tools**: Task distribution, project health, and workload analysis
- **Circular Dependency Prevention**: Automatic prevention of circular task dependencies
- **No External Dependencies**: Uses only Python standard library

### 📖 Documentation

For detailed documentation, see [SEED_DATA_README.md](SEED_DATA_README.md)

### 🎯 Use Cases

1. **Training RL Agents**: Generate diverse scenarios for agent training
2. **Testing & Validation**: Create edge cases for robustness testing
3. **Performance Benchmarking**: Generate stress test data for evaluation

### 📊 Example Usage

```python
from asana_rl_env import SeedDataGenerator, GenerationConfig, QualityValidator

# Generate data
config = GenerationConfig.medium_dataset()
generator = SeedDataGenerator(config)
data = generator.generate_all()

# Validate quality
validator = QualityValidator()
is_valid, report = validator.validate_all(
    generator.teams, generator.users, 
    generator.projects, generator.tasks
)
validator.print_report(report)

# Get statistics
stats = generator.get_statistics()
print(f"Generated {stats['total_tasks']} tasks across {stats['total_projects']} projects")
```

### 🏗️ Project Structure

```
asana_rl_env/
├── data_models/     # Task, Project, User, Team models
├── generators/      # Seed data generator
├── validators/      # Quality validator
├── config/          # Configuration options
├── utils/           # Export, load, and analysis utilities
└── examples/        # Example scripts (quickstart, scenarios, custom, tests)
```

### ✨ Key Features

- **Smart Dependency Management**: Automatically creates realistic task dependencies while preventing circular references
- **Workload Balancing**: Realistic user workload distribution with capacity tracking
- **Date Consistency**: Ensures all dates are logically consistent (creation, due dates, completion)
- **Comprehensive Validation**: 100/100 quality scores on completeness and consistency metrics
- **Multiple Scenarios**: 5 predefined scenarios + unlimited custom configurations

### 📄 License

This project is part of research work and is provided as-is for educational and research purposes.
