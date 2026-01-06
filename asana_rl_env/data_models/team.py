"""Team data model for Asana RL environment."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid


@dataclass
class Team:
    """
    Represents a team in the Asana RL environment.
    
    Attributes:
        team_id: Unique identifier for the team
        name: Team name
        description: Team description
        owner_id: ID of the team owner
        member_ids: List of user IDs in this team
        project_ids: List of project IDs owned by this team
        created_at: Timestamp when team was created
        updated_at: Timestamp when team was last updated
        tags: List of tags associated with the team
        metadata: Additional metadata for RL training
    """
    
    team_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    owner_id: Optional[str] = None
    member_ids: List[str] = field(default_factory=list)
    project_ids: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert team to dictionary format."""
        return {
            "team_id": self.team_id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "member_ids": self.member_ids,
            "project_ids": self.project_ids,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "tags": self.tags,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Team":
        """Create team from dictionary."""
        team = cls()
        team.team_id = data.get("team_id", team.team_id)
        team.name = data.get("name", "")
        team.description = data.get("description", "")
        team.owner_id = data.get("owner_id")
        team.member_ids = data.get("member_ids", [])
        team.project_ids = data.get("project_ids", [])
        
        if "created_at" in data:
            team.created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data:
            team.updated_at = datetime.fromisoformat(data["updated_at"])
            
        team.tags = data.get("tags", [])
        team.metadata = data.get("metadata", {})
        
        return team
    
    def add_member(self, user_id: str) -> None:
        """Add a member to the team."""
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)
            self.updated_at = datetime.now()
    
    def remove_member(self, user_id: str) -> None:
        """Remove a member from the team."""
        if user_id in self.member_ids:
            self.member_ids.remove(user_id)
            self.updated_at = datetime.now()
    
    def add_project(self, project_id: str) -> None:
        """Add a project to the team."""
        if project_id not in self.project_ids:
            self.project_ids.append(project_id)
            self.updated_at = datetime.now()
