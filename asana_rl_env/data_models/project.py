"""Project data model for Asana RL environment."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import uuid


class ProjectStatus(Enum):
    """Project status enumeration."""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Project:
    """
    Represents a project in the Asana RL environment.
    
    Attributes:
        project_id: Unique identifier for the project
        name: Project name
        description: Project description
        status: Current project status
        owner_id: ID of the project owner
        team_id: ID of the team owning this project
        created_at: Timestamp when project was created
        updated_at: Timestamp when project was last updated
        start_date: Project start date
        due_date: Project due date
        completed_at: Optional timestamp when project was completed
        task_ids: List of task IDs in this project
        member_ids: List of member IDs with access to this project
        tags: List of tags associated with the project
        color: Color code for the project
        metadata: Additional metadata for RL training
    """
    
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    status: ProjectStatus = ProjectStatus.PLANNING
    owner_id: Optional[str] = None
    team_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    task_ids: List[str] = field(default_factory=list)
    member_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    color: str = "#4A90E2"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary format."""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "owner_id": self.owner_id,
            "team_id": self.team_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "task_ids": self.task_ids,
            "member_ids": self.member_ids,
            "tags": self.tags,
            "color": self.color,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Create project from dictionary."""
        project = cls()
        project.project_id = data.get("project_id", project.project_id)
        project.name = data.get("name", "")
        project.description = data.get("description", "")
        project.status = ProjectStatus(data.get("status", "planning"))
        project.owner_id = data.get("owner_id")
        project.team_id = data.get("team_id")
        
        if "created_at" in data:
            project.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            project.updated_at = datetime.fromisoformat(data["updated_at"])
        if "start_date" in data and data["start_date"]:
            project.start_date = datetime.fromisoformat(data["start_date"])
        if "due_date" in data and data["due_date"]:
            project.due_date = datetime.fromisoformat(data["due_date"])
        if "completed_at" in data and data["completed_at"]:
            project.completed_at = datetime.fromisoformat(data["completed_at"])
            
        project.task_ids = data.get("task_ids", [])
        project.member_ids = data.get("member_ids", [])
        project.tags = data.get("tags", [])
        project.color = data.get("color", "#4A90E2")
        project.metadata = data.get("metadata", {})
        
        return project
    
    def add_task(self, task_id: str) -> None:
        """Add a task to the project."""
        if task_id not in self.task_ids:
            self.task_ids.append(task_id)
            self.updated_at = datetime.now()
    
    def remove_task(self, task_id: str) -> None:
        """Remove a task from the project."""
        if task_id in self.task_ids:
            self.task_ids.remove(task_id)
            self.updated_at = datetime.now()
    
    def add_member(self, user_id: str) -> None:
        """Add a member to the project."""
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)
            self.updated_at = datetime.now()
