"""Utility functions for data export and manipulation."""

import json
import csv
from typing import List, Dict, Any
from pathlib import Path

from ..data_models.task import Task
from ..data_models.project import Project
from ..data_models.user import User
from ..data_models.team import Team


class DataExporter:
    """Export seed data to various formats."""
    
    @staticmethod
    def export_to_json(
        data: Dict[str, List[Any]],
        filepath: str,
        pretty: bool = True
    ) -> None:
        """
        Export data to JSON file.
        
        Args:
            data: Dictionary containing data to export
            filepath: Output file path
            pretty: Whether to format JSON with indentation
        """
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            if pretty:
                json.dump(data, f, indent=2, default=str)
            else:
                json.dump(data, f, default=str)
    
    @staticmethod
    def export_to_csv(
        items: List[Any],
        filepath: str,
        fieldnames: List[str] = None
    ) -> None:
        """
        Export data to CSV file.
        
        Args:
            items: List of items to export (must have to_dict method)
            filepath: Output file path
            fieldnames: Optional list of field names to include
        """
        if not items:
            return
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        # Convert items to dictionaries
        dicts = [item.to_dict() if hasattr(item, 'to_dict') else item for item in items]
        
        if not fieldnames:
            fieldnames = list(dicts[0].keys())
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in dicts:
                # Flatten nested structures for CSV
                flat_item = {}
                for key, value in item.items():
                    if isinstance(value, (list, dict)):
                        flat_item[key] = json.dumps(value)
                    else:
                        flat_item[key] = value
                writer.writerow(flat_item)
    
    @staticmethod
    def export_all_formats(
        data: Dict[str, List[Any]],
        output_dir: str
    ) -> None:
        """
        Export data to multiple formats.
        
        Args:
            data: Dictionary containing all data
            output_dir: Output directory path
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Export complete dataset as JSON
        DataExporter.export_to_json(
            data,
            str(output_path / "seed_data.json")
        )
        
        # Export individual entity types as CSV
        for entity_type, items in data.items():
            if items:
                DataExporter.export_to_csv(
                    items,
                    str(output_path / f"{entity_type}.csv")
                )


class DataLoader:
    """Load seed data from files."""
    
    @staticmethod
    def load_from_json(filepath: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load data from JSON file.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Dictionary containing loaded data
        """
        with open(filepath, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def load_entities_from_json(filepath: str) -> Dict[str, List[Any]]:
        """
        Load data from JSON and convert to entity objects.
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            Dictionary containing entity objects
        """
        data = DataLoader.load_from_json(filepath)
        
        return {
            'teams': [Team.from_dict(t) for t in data.get('teams', [])],
            'users': [User.from_dict(u) for u in data.get('users', [])],
            'projects': [Project.from_dict(p) for p in data.get('projects', [])],
            'tasks': [Task.from_dict(t) for t in data.get('tasks', [])],
        }


class DataAnalyzer:
    """Analyze seed data and provide insights."""
    
    @staticmethod
    def analyze_task_distribution(tasks: List[Task]) -> Dict[str, Any]:
        """
        Analyze task distribution.
        
        Args:
            tasks: List of tasks
            
        Returns:
            Dictionary containing analysis results
        """
        if not tasks:
            return {}
        
        from ..data_models.task import TaskStatus, TaskPriority
        
        # Status distribution
        status_counts = {status.value: 0 for status in TaskStatus}
        for task in tasks:
            status_counts[task.status.value] += 1
        
        # Priority distribution
        priority_counts = {priority.value: 0 for priority in TaskPriority}
        for task in tasks:
            priority_counts[task.priority.value] += 1
        
        # Calculate metrics
        total_estimated = sum(t.estimated_hours or 0 for t in tasks)
        total_actual = sum(t.actual_hours or 0 for t in tasks)
        
        return {
            "total_tasks": len(tasks),
            "status_distribution": status_counts,
            "priority_distribution": priority_counts,
            "total_estimated_hours": total_estimated,
            "total_actual_hours": total_actual,
            "tasks_with_estimates": sum(1 for t in tasks if t.estimated_hours),
            "overdue_tasks": sum(1 for t in tasks if t.is_overdue()),
            "blocked_tasks": sum(1 for t in tasks if t.is_blocked()),
        }
    
    @staticmethod
    def analyze_project_health(
        projects: List[Project],
        tasks: List[Task]
    ) -> Dict[str, Any]:
        """
        Analyze project health metrics.
        
        Args:
            projects: List of projects
            tasks: List of tasks
            
        Returns:
            Dictionary containing project health analysis
        """
        if not projects:
            return {}
        
        project_metrics = []
        
        for project in projects:
            project_tasks = [t for t in tasks if t.project_id == project.project_id]
            
            if project_tasks:
                completed = sum(1 for t in project_tasks if t.status.value == 'completed')
                completion_rate = completed / len(project_tasks)
                overdue = sum(1 for t in project_tasks if t.is_overdue())
            else:
                completion_rate = 0
                overdue = 0
            
            project_metrics.append({
                "project_id": project.project_id,
                "name": project.name,
                "status": project.status.value,
                "total_tasks": len(project_tasks),
                "completion_rate": completion_rate,
                "overdue_tasks": overdue,
            })
        
        return {
            "total_projects": len(projects),
            "projects": project_metrics,
            "avg_completion_rate": sum(p["completion_rate"] for p in project_metrics) / len(project_metrics) if project_metrics else 0,
        }
    
    @staticmethod
    def analyze_user_workload(users: List[User], tasks: List[Task]) -> Dict[str, Any]:
        """
        Analyze user workload distribution.
        
        Args:
            users: List of users
            tasks: List of tasks
            
        Returns:
            Dictionary containing workload analysis
        """
        if not users:
            return {}
        
        user_metrics = []
        
        for user in users:
            user_tasks = [t for t in tasks if t.assignee_id == user.user_id]
            active_tasks = [t for t in user_tasks if t.status.value in ['todo', 'in_progress', 'in_review']]
            
            user_metrics.append({
                "user_id": user.user_id,
                "name": user.name,
                "total_tasks": len(user_tasks),
                "active_tasks": len(active_tasks),
                "current_workload": user.current_workload,
                "capacity": user.workload_capacity,
                "is_available": user.is_available(),
            })
        
        return {
            "total_users": len(users),
            "users": user_metrics,
            "avg_workload": sum(u["current_workload"] for u in user_metrics) / len(user_metrics),
            "overloaded_users": sum(1 for u in user_metrics if u["current_workload"] > u["capacity"]),
            "available_users": sum(1 for u in user_metrics if u["is_available"]),
        }
