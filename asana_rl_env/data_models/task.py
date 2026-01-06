"""Task data model for Asana RL environment."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import uuid


class TaskStatus(Enum):
    """Task status enumeration."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    """
    Represents a task in the Asana RL environment.
    
    Attributes:
        task_id: Unique identifier for the task
        name: Task name/title
        description: Detailed task description
        status: Current task status
        priority: Task priority level
        assignee_id: ID of the user assigned to this task
        project_id: ID of the project this task belongs to
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        due_date: Optional due date for the task
        completed_at: Optional timestamp when task was completed
        tags: List of tags associated with the task
        dependencies: List of task IDs this task depends on
        estimated_hours: Estimated hours to complete
        actual_hours: Actual hours spent on the task
        subtasks: List of subtask IDs
        metadata: Additional metadata for RL training
    """
    
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee_id: Optional[str] = None
    project_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    subtasks: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary format."""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "assignee_id": self.assignee_id,
            "project_id": self.project_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "tags": self.tags,
            "dependencies": self.dependencies,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "subtasks": self.subtasks,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        task = cls()
        task.task_id = data.get("task_id", task.task_id)
        task.name = data.get("name", "")
        task.description = data.get("description", "")
        task.status = TaskStatus(data.get("status", "todo"))
        task.priority = TaskPriority(data.get("priority", "medium"))
        task.assignee_id = data.get("assignee_id")
        task.project_id = data.get("project_id")
        
        if "created_at" in data:
            task.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            task.updated_at = datetime.fromisoformat(data["updated_at"])
        if "due_date" in data and data["due_date"]:
            task.due_date = datetime.fromisoformat(data["due_date"])
        if "completed_at" in data and data["completed_at"]:
            task.completed_at = datetime.fromisoformat(data["completed_at"])
            
        task.tags = data.get("tags", [])
        task.dependencies = data.get("dependencies", [])
        task.estimated_hours = data.get("estimated_hours")
        task.actual_hours = data.get("actual_hours")
        task.subtasks = data.get("subtasks", [])
        task.metadata = data.get("metadata", {})
        
        return task
    
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.due_date is None or self.status == TaskStatus.COMPLETED:
            return False
        return datetime.now() > self.due_date
    
    def is_blocked(self) -> bool:
        """Check if task is blocked by dependencies."""
        return self.status == TaskStatus.BLOCKED or len(self.dependencies) > 0
