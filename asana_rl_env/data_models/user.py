"""User data model for Asana RL environment."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import uuid


class UserRole(Enum):
    """User role enumeration."""
    VIEWER = "viewer"
    MEMBER = "member"
    ADMIN = "admin"
    OWNER = "owner"


@dataclass
class User:
    """
    Represents a user in the Asana RL environment.
    
    Attributes:
        user_id: Unique identifier for the user
        name: User's full name
        email: User's email address
        role: User's role in the organization
        team_ids: List of team IDs the user belongs to
        project_ids: List of project IDs the user has access to
        created_at: Timestamp when user was created
        last_active: Timestamp of last activity
        skills: List of skills/expertise areas
        workload_capacity: User's workload capacity (0.0 to 1.0)
        current_workload: Current workload level (0.0 to 1.0)
        preferences: User preferences and settings
        metadata: Additional metadata for RL training
    """
    
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    email: str = ""
    role: UserRole = UserRole.MEMBER
    team_ids: List[str] = field(default_factory=list)
    project_ids: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    skills: List[str] = field(default_factory=list)
    workload_capacity: float = 1.0
    current_workload: float = 0.0
    preferences: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary format."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value,
            "team_ids": self.team_ids,
            "project_ids": self.project_ids,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat(),
            "skills": self.skills,
            "workload_capacity": self.workload_capacity,
            "current_workload": self.current_workload,
            "preferences": self.preferences,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create user from dictionary."""
        user = cls()
        user.user_id = data.get("user_id", user.user_id)
        user.name = data.get("name", "")
        user.email = data.get("email", "")
        user.role = UserRole(data.get("role", "member"))
        user.team_ids = data.get("team_ids", [])
        user.project_ids = data.get("project_ids", [])
        
        if "created_at" in data:
            user.created_at = datetime.fromisoformat(data["created_at"])
        if "last_active" in data:
            user.last_active = datetime.fromisoformat(data["last_active"])
            
        user.skills = data.get("skills", [])
        user.workload_capacity = data.get("workload_capacity", 1.0)
        user.current_workload = data.get("current_workload", 0.0)
        user.preferences = data.get("preferences", {})
        user.metadata = data.get("metadata", {})
        
        return user
    
    def is_available(self) -> bool:
        """Check if user has available capacity."""
        return self.current_workload < self.workload_capacity
    
    def update_workload(self, workload_delta: float) -> None:
        """Update user's current workload."""
        self.current_workload = max(0.0, min(1.0, self.current_workload + workload_delta))
        self.last_active = datetime.now()
