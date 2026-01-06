"""Seed data generator for Asana RL environment."""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import json

from ..data_models.task import Task, TaskStatus, TaskPriority
from ..data_models.project import Project, ProjectStatus
from ..data_models.user import User, UserRole
from ..data_models.team import Team
from ..config.generation_config import GenerationConfig


class SeedDataGenerator:
    """
    Generator for high-quality seed data for Asana RL environment.
    
    This class generates realistic task management scenarios including
    users, teams, projects, and tasks with appropriate relationships
    and dependencies.
    """
    
    # Realistic task names by category
    TASK_CATEGORIES = {
        "development": [
            "Implement authentication system",
            "Fix login bug",
            "Add payment integration",
            "Optimize database queries",
            "Refactor user service",
            "Write unit tests",
            "Update API documentation",
            "Review code changes",
            "Deploy to production",
            "Setup CI/CD pipeline",
        ],
        "design": [
            "Create wireframes",
            "Design landing page",
            "Update brand guidelines",
            "Create user flow diagrams",
            "Design mobile mockups",
            "Conduct user research",
            "Create design system",
            "Prepare design handoff",
        ],
        "marketing": [
            "Plan social media campaign",
            "Write blog post",
            "Create email newsletter",
            "Analyze campaign metrics",
            "Update website content",
            "Prepare press release",
            "Schedule product launch",
            "Coordinate with partners",
        ],
        "operations": [
            "Process customer feedback",
            "Update onboarding documentation",
            "Review team processes",
            "Prepare quarterly report",
            "Conduct team meeting",
            "Update project timeline",
            "Review budget allocation",
            "Coordinate cross-team sync",
        ],
    }
    
    SKILLS = [
        "Python", "JavaScript", "React", "Node.js", "DevOps",
        "UI/UX Design", "Data Analysis", "Project Management",
        "Marketing", "Content Writing", "SEO", "Customer Support",
        "Quality Assurance", "Security", "Machine Learning",
    ]
    
    PROJECT_TYPES = [
        "Website Redesign",
        "Mobile App Development",
        "Marketing Campaign",
        "Product Launch",
        "Infrastructure Upgrade",
        "Customer Portal",
        "Analytics Dashboard",
        "Security Audit",
        "Performance Optimization",
        "Content Strategy",
    ]
    
    def __init__(self, config: GenerationConfig = None):
        """
        Initialize the seed data generator.
        
        Args:
            config: Generation configuration
        """
        self.config = config or GenerationConfig()
        random.seed(self.config.seed)
        
        self.teams: List[Team] = []
        self.users: List[User] = []
        self.projects: List[Project] = []
        self.tasks: List[Task] = []
    
    def generate_all(self) -> Dict[str, List[Any]]:
        """
        Generate all seed data.
        
        Returns:
            Dictionary containing lists of teams, users, projects, and tasks
        """
        self.teams = self._generate_teams()
        self.users = self._generate_users()
        self.projects = self._generate_projects()
        self.tasks = self._generate_tasks()
        
        return {
            "teams": [t.to_dict() for t in self.teams],
            "users": [u.to_dict() for u in self.users],
            "projects": [p.to_dict() for p in self.projects],
            "tasks": [t.to_dict() for t in self.tasks],
        }
    
    def _generate_teams(self) -> List[Team]:
        """Generate teams."""
        teams = []
        team_names = [
            "Engineering",
            "Design",
            "Marketing",
            "Product",
            "Operations",
            "Sales",
            "Customer Success",
            "Data Science",
            "DevOps",
            "Quality Assurance",
        ]
        
        for i in range(self.config.num_teams):
            team = Team(
                name=team_names[i % len(team_names)] if i < len(team_names) else f"Team {i+1}",
                description=f"Team responsible for {team_names[i % len(team_names)].lower()} tasks",
                tags=[team_names[i % len(team_names)].lower()],
            )
            teams.append(team)
        
        return teams
    
    def _generate_users(self) -> List[User]:
        """Generate users and assign them to teams."""
        users = []
        first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        
        roles = [UserRole.OWNER, UserRole.ADMIN] + [UserRole.MEMBER] * (self.config.num_users - 2)
        random.shuffle(roles)
        
        for i in range(self.config.num_users):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            email = f"{first_name.lower()}.{last_name.lower()}@company.com"
            
            user = User(
                name=name,
                email=email,
                role=roles[i] if i < len(roles) else UserRole.MEMBER,
                skills=random.sample(self.SKILLS, k=random.randint(2, 5)),
                workload_capacity=random.uniform(0.8, 1.0) if self.config.realistic_mode else 1.0,
                current_workload=random.uniform(0.0, 0.5) if self.config.realistic_mode else 0.0,
            )
            users.append(user)
        
        # Assign users to teams
        unassigned_users = users.copy()
        
        for team in self.teams:
            if not unassigned_users:
                break
            
            team_size = random.randint(*self.config.team_size_range)
            team_size = min(team_size, len(unassigned_users))
            team_members = random.sample(unassigned_users, k=team_size)
            
            # Set team owner
            if team_members:
                team.owner_id = team_members[0].user_id
            
            for user in team_members:
                team.add_member(user.user_id)
                user.team_ids.append(team.team_id)
                unassigned_users.remove(user)
        
        # Assign any remaining users to random teams
        for user in unassigned_users:
            random_team = random.choice(self.teams)
            random_team.add_member(user.user_id)
            user.team_ids.append(random_team.team_id)
        
        return users
    
    def _generate_projects(self) -> List[Project]:
        """Generate projects and assign them to teams."""
        projects = []
        
        for i in range(self.config.num_projects):
            # Assign to random team
            team = random.choice(self.teams)
            team_members = [u for u in self.users if team.team_id in u.team_ids]
            
            # Select project owner from team members
            owner = random.choice(team_members) if team_members else random.choice(self.users)
            
            project_type = random.choice(self.PROJECT_TYPES)
            
            # Generate realistic dates
            created_at = datetime.now() - timedelta(days=random.randint(1, 180))
            start_date = created_at + timedelta(days=random.randint(1, 14))
            due_date = start_date + timedelta(days=random.randint(30, 120))
            
            # Determine project status based on dates
            if self.config.realistic_mode:
                now = datetime.now()
                if now < start_date:
                    status = ProjectStatus.PLANNING
                elif now < due_date:
                    status = random.choice([ProjectStatus.ACTIVE, ProjectStatus.ACTIVE, ProjectStatus.ACTIVE, ProjectStatus.ON_HOLD])
                else:
                    status = random.choice([ProjectStatus.COMPLETED, ProjectStatus.ACTIVE])
            else:
                status = random.choice(list(ProjectStatus))
            
            project = Project(
                name=f"{project_type} - Q{random.randint(1, 4)} 2024",
                description=f"Project focused on {project_type.lower()} for the team",
                status=status,
                owner_id=owner.user_id,
                team_id=team.team_id,
                created_at=created_at,
                start_date=start_date,
                due_date=due_date,
                color=random.choice(["#4A90E2", "#E24A4A", "#4AE290", "#E2904A", "#904AE2"]),
                tags=[project_type.lower().replace(" ", "_")],
            )
            
            # Add project members
            num_members = random.randint(2, min(6, len(team_members)))
            project_members = random.sample(team_members, k=min(num_members, len(team_members)))
            for member in project_members:
                project.add_member(member.user_id)
                member.project_ids.append(project.project_id)
            
            team.add_project(project.project_id)
            projects.append(project)
        
        return projects
    
    def _generate_tasks(self) -> List[Task]:
        """Generate tasks and assign them to projects."""
        tasks = []
        
        # Get all task names
        all_task_names = []
        for category_tasks in self.TASK_CATEGORIES.values():
            all_task_names.extend(category_tasks)
        
        for i in range(self.config.num_tasks):
            # Assign to random project
            project = random.choice(self.projects)
            
            # Get project members
            project_members = [u for u in self.users if project.project_id in u.project_ids]
            assignee = random.choice(project_members) if project_members else random.choice(self.users)
            
            # Generate task name
            task_name = random.choice(all_task_names) if all_task_names else f"Task {i+1}"
            
            # Generate realistic dates
            created_at = project.created_at + timedelta(days=random.randint(0, 30))
            
            # Due date based on project timeline
            if project.due_date:
                days_until_project_due = (project.due_date - created_at).days
                due_date = created_at + timedelta(days=random.randint(1, max(1, days_until_project_due)))
            else:
                due_date = created_at + timedelta(days=random.randint(1, 30))
            
            # Determine if task is overdue
            is_overdue = random.random() < self.config.overdue_probability
            if is_overdue and self.config.realistic_mode:
                # Make sure overdue tasks are created in the past
                old_created_at = datetime.now() - timedelta(days=random.randint(15, 60))
                created_at = min(created_at, old_created_at)
                due_date = datetime.now() - timedelta(days=random.randint(1, 14))
            
            # Determine task status
            if self.config.realistic_mode:
                now = datetime.now()
                if is_overdue:
                    status = random.choice([TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.BLOCKED])
                elif now > due_date:
                    status = TaskStatus.COMPLETED
                else:
                    status = random.choice([
                        TaskStatus.TODO, TaskStatus.TODO,
                        TaskStatus.IN_PROGRESS, TaskStatus.IN_PROGRESS,
                        TaskStatus.IN_REVIEW,
                        TaskStatus.COMPLETED,
                    ])
            else:
                status = random.choice(list(TaskStatus))
            
            # Set completed_at if completed
            completed_at = None
            if status == TaskStatus.COMPLETED:
                completed_at = due_date - timedelta(days=random.randint(0, 5))
            
            # Priority distribution
            priority_weights = [0.2, 0.5, 0.25, 0.05]  # LOW, MEDIUM, HIGH, CRITICAL
            priority = random.choices(list(TaskPriority), weights=priority_weights)[0]
            
            # Generate estimated and actual hours
            estimated_hours = random.uniform(1, 40) if random.random() > 0.3 else None
            actual_hours = None
            if status in [TaskStatus.COMPLETED, TaskStatus.IN_REVIEW]:
                if estimated_hours:
                    actual_hours = estimated_hours * random.uniform(0.8, 1.5)
                else:
                    actual_hours = random.uniform(1, 40)
            
            task = Task(
                name=task_name,
                description=f"Complete {task_name.lower()} for {project.name}",
                status=status,
                priority=priority,
                assignee_id=assignee.user_id,
                project_id=project.project_id,
                created_at=created_at,
                due_date=due_date,
                completed_at=completed_at,
                tags=project.tags,
                estimated_hours=estimated_hours,
                actual_hours=actual_hours,
            )
            
            tasks.append(task)
            project.add_task(task.task_id)
        
        # Add dependencies
        self._add_task_dependencies(tasks)
        
        # Add subtasks
        self._add_subtasks(tasks)
        
        return tasks
    
    def _add_task_dependencies(self, tasks: List[Task]) -> None:
        """Add dependencies between tasks."""
        for task in tasks:
            if random.random() < self.config.dependency_probability:
                # Add 1-3 dependencies from the same project
                project_tasks = [t for t in tasks if t.project_id == task.project_id and t.task_id != task.task_id]
                if project_tasks:
                    num_deps = random.randint(1, min(3, len(project_tasks)))
                    deps = random.sample(project_tasks, k=num_deps)
                    task.dependencies = [d.task_id for d in deps]
                    
                    # If task has dependencies and is not completed, it might be blocked
                    if task.status != TaskStatus.COMPLETED and random.random() < 0.3:
                        task.status = TaskStatus.BLOCKED
    
    def _add_subtasks(self, tasks: List[Task]) -> None:
        """Add subtasks to some tasks."""
        # Create subtasks (these are also tasks, just linked)
        original_task_count = len(tasks)
        
        for i in range(original_task_count):
            task = tasks[i]
            if random.random() < self.config.subtask_probability:
                # Create 2-5 subtasks
                num_subtasks = random.randint(2, 5)
                
                for j in range(num_subtasks):
                    subtask_status = random.choice([TaskStatus.TODO, TaskStatus.IN_PROGRESS, TaskStatus.COMPLETED])
                    
                    # Set completed_at for completed subtasks
                    completed_at = None
                    if subtask_status == TaskStatus.COMPLETED and task.due_date:
                        completed_at = task.due_date - timedelta(days=random.randint(0, 5))
                    
                    subtask = Task(
                        name=f"{task.name} - Subtask {j+1}",
                        description=f"Subtask of: {task.name}",
                        status=subtask_status,
                        priority=task.priority,
                        assignee_id=task.assignee_id,
                        project_id=task.project_id,
                        created_at=task.created_at,
                        due_date=task.due_date,
                        completed_at=completed_at,
                        tags=task.tags,
                        estimated_hours=random.uniform(0.5, 5),
                    )
                    
                    tasks.append(subtask)
                    task.subtasks.append(subtask.task_id)
    
    def save_to_json(self, filepath: str) -> None:
        """
        Save generated data to JSON file.
        
        Args:
            filepath: Path to output JSON file
        """
        data = self.generate_all()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the generated data.
        
        Returns:
            Dictionary containing statistics
        """
        if not self.tasks:
            self.generate_all()
        
        task_statuses = {}
        for status in TaskStatus:
            task_statuses[status.value] = sum(1 for t in self.tasks if t.status == status)
        
        task_priorities = {}
        for priority in TaskPriority:
            task_priorities[priority.value] = sum(1 for t in self.tasks if t.priority == priority)
        
        project_statuses = {}
        for status in ProjectStatus:
            project_statuses[status.value] = sum(1 for p in self.projects if p.status == status)
        
        return {
            "total_teams": len(self.teams),
            "total_users": len(self.users),
            "total_projects": len(self.projects),
            "total_tasks": len(self.tasks),
            "task_statuses": task_statuses,
            "task_priorities": task_priorities,
            "project_statuses": project_statuses,
            "tasks_with_dependencies": sum(1 for t in self.tasks if t.dependencies),
            "tasks_with_subtasks": sum(1 for t in self.tasks if t.subtasks),
            "overdue_tasks": sum(1 for t in self.tasks if t.is_overdue()),
            "avg_tasks_per_project": len(self.tasks) / len(self.projects) if self.projects else 0,
            "avg_users_per_team": sum(len(t.member_ids) for t in self.teams) / len(self.teams) if self.teams else 0,
        }
