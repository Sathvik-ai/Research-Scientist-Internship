"""Configuration for seed data generation."""

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class GenerationConfig:
    """
    Configuration for seed data generation.
    
    Attributes:
        num_teams: Number of teams to generate
        num_users: Number of users to generate
        num_projects: Number of projects to generate
        num_tasks: Number of tasks to generate
        team_size_range: Min and max team size (members)
        project_size_range: Min and max project size (tasks)
        task_complexity_range: Min and max task complexity (0-1)
        dependency_probability: Probability of task having dependencies
        subtask_probability: Probability of task having subtasks
        overdue_probability: Probability of task being overdue
        realistic_mode: Use realistic distributions and patterns
        seed: Random seed for reproducibility
        scenario: Predefined scenario name
        custom_params: Additional custom parameters
    """
    
    num_teams: int = 5
    num_users: int = 25
    num_projects: int = 10
    num_tasks: int = 100
    team_size_range: tuple = (3, 8)
    project_size_range: tuple = (5, 20)
    task_complexity_range: tuple = (0.1, 0.9)
    dependency_probability: float = 0.2
    subtask_probability: float = 0.15
    overdue_probability: float = 0.1
    realistic_mode: bool = True
    seed: int = 42
    scenario: str = "default"
    custom_params: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def small_dataset(cls) -> "GenerationConfig":
        """Create configuration for a small dataset."""
        return cls(
            num_teams=2,
            num_users=10,
            num_projects=5,
            num_tasks=30,
            scenario="small"
        )
    
    @classmethod
    def medium_dataset(cls) -> "GenerationConfig":
        """Create configuration for a medium dataset."""
        return cls(
            num_teams=5,
            num_users=25,
            num_projects=10,
            num_tasks=100,
            scenario="medium"
        )
    
    @classmethod
    def large_dataset(cls) -> "GenerationConfig":
        """Create configuration for a large dataset."""
        return cls(
            num_teams=10,
            num_users=50,
            num_projects=25,
            num_tasks=300,
            scenario="large"
        )
    
    @classmethod
    def stress_test(cls) -> "GenerationConfig":
        """Create configuration for stress testing."""
        return cls(
            num_teams=20,
            num_users=100,
            num_projects=50,
            num_tasks=1000,
            dependency_probability=0.4,
            subtask_probability=0.3,
            scenario="stress_test"
        )
    
    @classmethod
    def edge_cases(cls) -> "GenerationConfig":
        """Create configuration with edge cases."""
        return cls(
            num_teams=3,
            num_users=15,
            num_projects=8,
            num_tasks=50,
            dependency_probability=0.5,
            subtask_probability=0.4,
            overdue_probability=0.3,
            realistic_mode=False,
            scenario="edge_cases"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "num_teams": self.num_teams,
            "num_users": self.num_users,
            "num_projects": self.num_projects,
            "num_tasks": self.num_tasks,
            "team_size_range": self.team_size_range,
            "project_size_range": self.project_size_range,
            "task_complexity_range": self.task_complexity_range,
            "dependency_probability": self.dependency_probability,
            "subtask_probability": self.subtask_probability,
            "overdue_probability": self.overdue_probability,
            "realistic_mode": self.realistic_mode,
            "seed": self.seed,
            "scenario": self.scenario,
            "custom_params": self.custom_params,
        }
