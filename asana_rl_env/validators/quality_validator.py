"""Quality validator for seed data."""

from typing import List, Dict, Any, Tuple
from datetime import datetime

from ..data_models.task import Task, TaskStatus
from ..data_models.project import Project
from ..data_models.user import User
from ..data_models.team import Team


class QualityValidator:
    """
    Validates the quality of generated seed data.
    
    Checks for:
    - Data consistency
    - Relationship integrity
    - Realistic distributions
    - Edge cases coverage
    """
    
    def __init__(self):
        """Initialize the quality validator."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.metrics: Dict[str, Any] = {}
    
    def validate_all(
        self,
        teams: List[Team],
        users: List[User],
        projects: List[Project],
        tasks: List[Task],
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate all generated data.
        
        Args:
            teams: List of teams
            users: List of users
            projects: List of projects
            tasks: List of tasks
            
        Returns:
            Tuple of (is_valid, report_dict)
        """
        self.errors = []
        self.warnings = []
        self.metrics = {}
        
        # Run validation checks
        self._validate_teams(teams, users, projects)
        self._validate_users(users, teams, projects)
        self._validate_projects(projects, teams, users, tasks)
        self._validate_tasks(tasks, projects, users)
        self._validate_relationships(teams, users, projects, tasks)
        self._calculate_metrics(teams, users, projects, tasks)
        
        is_valid = len(self.errors) == 0
        
        report = {
            "is_valid": is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "metrics": self.metrics,
        }
        
        return is_valid, report
    
    def _validate_teams(
        self,
        teams: List[Team],
        users: List[User],
        projects: List[Project],
    ) -> None:
        """Validate team data."""
        if not teams:
            self.errors.append("No teams generated")
            return
        
        team_ids = {t.team_id for t in teams}
        
        for team in teams:
            # Check required fields
            if not team.name:
                self.errors.append(f"Team {team.team_id} has no name")
            
            # Check team has members
            if not team.member_ids:
                self.warnings.append(f"Team {team.name} has no members")
            
            # Check team owner exists in members
            if team.owner_id and team.owner_id not in team.member_ids:
                self.errors.append(f"Team {team.name} owner is not a member")
            
            # Check team members exist
            user_ids = {u.user_id for u in users}
            for member_id in team.member_ids:
                if member_id not in user_ids:
                    self.errors.append(f"Team {team.name} has non-existent member {member_id}")
    
    def _validate_users(
        self,
        users: List[User],
        teams: List[Team],
        projects: List[Project],
    ) -> None:
        """Validate user data."""
        if not users:
            self.errors.append("No users generated")
            return
        
        user_ids = {u.user_id for u in users}
        team_ids = {t.team_id for t in teams}
        project_ids = {p.project_id for p in projects}
        
        for user in users:
            # Check required fields
            if not user.name:
                self.errors.append(f"User {user.user_id} has no name")
            if not user.email:
                self.errors.append(f"User {user.user_id} has no email")
            
            # Check workload bounds
            if not 0 <= user.current_workload <= 1:
                self.errors.append(f"User {user.name} has invalid current_workload: {user.current_workload}")
            if not 0 <= user.workload_capacity <= 1:
                self.errors.append(f"User {user.name} has invalid workload_capacity: {user.workload_capacity}")
            
            # Check team memberships exist
            for team_id in user.team_ids:
                if team_id not in team_ids:
                    self.errors.append(f"User {user.name} belongs to non-existent team {team_id}")
            
            # Warn if user has no team
            if not user.team_ids:
                self.warnings.append(f"User {user.name} is not in any team")
    
    def _validate_projects(
        self,
        projects: List[Project],
        teams: List[Team],
        users: List[User],
        tasks: List[Task],
    ) -> None:
        """Validate project data."""
        if not projects:
            self.errors.append("No projects generated")
            return
        
        project_ids = {p.project_id for p in projects}
        team_ids = {t.team_id for t in teams}
        user_ids = {u.user_id for u in users}
        
        for project in projects:
            # Check required fields
            if not project.name:
                self.errors.append(f"Project {project.project_id} has no name")
            
            # Check owner exists
            if project.owner_id and project.owner_id not in user_ids:
                self.errors.append(f"Project {project.name} has non-existent owner {project.owner_id}")
            
            # Check team exists
            if project.team_id and project.team_id not in team_ids:
                self.errors.append(f"Project {project.name} belongs to non-existent team {project.team_id}")
            
            # Check date consistency
            if project.start_date and project.due_date and project.start_date > project.due_date:
                self.errors.append(f"Project {project.name} start_date is after due_date")
            
            # Check members exist
            for member_id in project.member_ids:
                if member_id not in user_ids:
                    self.errors.append(f"Project {project.name} has non-existent member {member_id}")
            
            # Warn if project has no members
            if not project.member_ids:
                self.warnings.append(f"Project {project.name} has no members")
    
    def _validate_tasks(
        self,
        tasks: List[Task],
        projects: List[Project],
        users: List[User],
    ) -> None:
        """Validate task data."""
        if not tasks:
            self.warnings.append("No tasks generated")
            return
        
        task_ids = {t.task_id for t in tasks}
        project_ids = {p.project_id for p in projects}
        user_ids = {u.user_id for u in users}
        
        for task in tasks:
            # Check required fields
            if not task.name:
                self.errors.append(f"Task {task.task_id} has no name")
            
            # Check project exists
            if task.project_id and task.project_id not in project_ids:
                self.errors.append(f"Task {task.name} belongs to non-existent project {task.project_id}")
            
            # Check assignee exists
            if task.assignee_id and task.assignee_id not in user_ids:
                self.errors.append(f"Task {task.name} assigned to non-existent user {task.assignee_id}")
            
            # Check date consistency
            if task.due_date and task.due_date < task.created_at:
                self.errors.append(f"Task {task.name} due_date is before created_at")
            
            # Check completed_at consistency
            if task.status == TaskStatus.COMPLETED:
                if not task.completed_at:
                    self.warnings.append(f"Completed task {task.name} has no completed_at date")
            else:
                if task.completed_at:
                    self.warnings.append(f"Non-completed task {task.name} has completed_at date")
            
            # Check dependencies exist
            for dep_id in task.dependencies:
                if dep_id not in task_ids:
                    self.errors.append(f"Task {task.name} has non-existent dependency {dep_id}")
            
            # Check subtasks exist
            for subtask_id in task.subtasks:
                if subtask_id not in task_ids:
                    self.errors.append(f"Task {task.name} has non-existent subtask {subtask_id}")
            
            # Check for circular dependencies
            self._check_circular_dependencies(task, tasks)
    
    def _validate_relationships(
        self,
        teams: List[Team],
        users: List[User],
        projects: List[Project],
        tasks: List[Task],
    ) -> None:
        """Validate bidirectional relationships."""
        # Check team-user relationships
        for team in teams:
            for member_id in team.member_ids:
                user = next((u for u in users if u.user_id == member_id), None)
                if user and team.team_id not in user.team_ids:
                    self.warnings.append(
                        f"User {user.name} is in team {team.name} but team not in user's team_ids"
                    )
        
        # Check project-task relationships
        for project in projects:
            for task_id in project.task_ids:
                task = next((t for t in tasks if t.task_id == task_id), None)
                if task and task.project_id != project.project_id:
                    self.errors.append(
                        f"Task {task.name} is in project {project.name} but has different project_id"
                    )
    
    def _check_circular_dependencies(self, task: Task, all_tasks: List[Task]) -> None:
        """Check for circular dependencies in tasks."""
        visited = set()
        
        def has_cycle(current_id: str, path: set) -> bool:
            if current_id in path:
                return True
            if current_id in visited:
                return False
            
            visited.add(current_id)
            path.add(current_id)
            
            current_task = next((t for t in all_tasks if t.task_id == current_id), None)
            if current_task:
                for dep_id in current_task.dependencies:
                    if has_cycle(dep_id, path):
                        return True
            
            path.remove(current_id)
            return False
        
        if has_cycle(task.task_id, set()):
            self.errors.append(f"Task {task.name} has circular dependencies")
    
    def _calculate_metrics(
        self,
        teams: List[Team],
        users: List[User],
        projects: List[Project],
        tasks: List[Task],
    ) -> None:
        """Calculate quality metrics."""
        # Coverage metrics
        self.metrics["total_teams"] = len(teams)
        self.metrics["total_users"] = len(users)
        self.metrics["total_projects"] = len(projects)
        self.metrics["total_tasks"] = len(tasks)
        
        # Distribution metrics
        if tasks:
            status_dist = {}
            for task in tasks:
                status_dist[task.status.value] = status_dist.get(task.status.value, 0) + 1
            self.metrics["task_status_distribution"] = status_dist
            
            priority_dist = {}
            for task in tasks:
                priority_dist[task.priority.value] = priority_dist.get(task.priority.value, 0) + 1
            self.metrics["task_priority_distribution"] = priority_dist
        
        # Relationship metrics
        if projects:
            self.metrics["avg_tasks_per_project"] = len(tasks) / len(projects)
            self.metrics["projects_with_no_tasks"] = sum(1 for p in projects if not p.task_ids)
        
        if teams:
            self.metrics["avg_users_per_team"] = sum(len(t.member_ids) for t in teams) / len(teams)
            self.metrics["teams_with_no_members"] = sum(1 for t in teams if not t.member_ids)
        
        # Complexity metrics
        if tasks:
            self.metrics["tasks_with_dependencies"] = sum(1 for t in tasks if t.dependencies)
            self.metrics["tasks_with_subtasks"] = sum(1 for t in tasks if t.subtasks)
            self.metrics["overdue_tasks"] = sum(1 for t in tasks if t.is_overdue())
            self.metrics["blocked_tasks"] = sum(1 for t in tasks if t.status == TaskStatus.BLOCKED)
        
        # Quality scores (0-100)
        self.metrics["completeness_score"] = self._calculate_completeness_score(teams, users, projects, tasks)
        self.metrics["consistency_score"] = self._calculate_consistency_score()
        self.metrics["diversity_score"] = self._calculate_diversity_score(tasks)
    
    def _calculate_completeness_score(
        self,
        teams: List[Team],
        users: List[User],
        projects: List[Project],
        tasks: List[Task],
    ) -> float:
        """Calculate completeness score."""
        score = 100.0
        
        # Deduct for missing data
        if not teams:
            score -= 25
        if not users:
            score -= 25
        if not projects:
            score -= 25
        if not tasks:
            score -= 25
        
        # Deduct for incomplete relationships
        if teams:
            teams_without_members = sum(1 for t in teams if not t.member_ids)
            score -= (teams_without_members / len(teams)) * 10
        
        if projects:
            projects_without_tasks = sum(1 for p in projects if not p.task_ids)
            score -= (projects_without_tasks / len(projects)) * 10
        
        return max(0.0, score)
    
    def _calculate_consistency_score(self) -> float:
        """Calculate consistency score based on errors."""
        if not self.errors:
            return 100.0
        return max(0.0, 100.0 - len(self.errors) * 10)
    
    def _calculate_diversity_score(self, tasks: List[Task]) -> float:
        """Calculate diversity score based on data variety."""
        if not tasks:
            return 0.0
        
        score = 0.0
        
        # Check status diversity
        unique_statuses = len(set(t.status for t in tasks))
        score += (unique_statuses / len(TaskStatus)) * 25
        
        # Check priority diversity
        from ..data_models.task import TaskPriority
        unique_priorities = len(set(t.priority for t in tasks))
        score += (unique_priorities / len(TaskPriority)) * 25
        
        # Check for tasks with dependencies
        tasks_with_deps = sum(1 for t in tasks if t.dependencies)
        score += min((tasks_with_deps / len(tasks)) * 25, 25)
        
        # Check for tasks with subtasks
        tasks_with_subtasks = sum(1 for t in tasks if t.subtasks)
        score += min((tasks_with_subtasks / len(tasks)) * 25, 25)
        
        return score
    
    def print_report(self, report: Dict[str, Any]) -> None:
        """Print validation report."""
        print("\n" + "="*60)
        print("SEED DATA QUALITY VALIDATION REPORT")
        print("="*60)
        
        print(f"\nValidation Status: {'✓ PASSED' if report['is_valid'] else '✗ FAILED'}")
        
        if report['errors']:
            print(f"\nErrors ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"  ✗ {error}")
        
        if report['warnings']:
            print(f"\nWarnings ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"  ⚠ {warning}")
        
        print("\nMetrics:")
        metrics = report['metrics']
        print(f"  Teams: {metrics.get('total_teams', 0)}")
        print(f"  Users: {metrics.get('total_users', 0)}")
        print(f"  Projects: {metrics.get('total_projects', 0)}")
        print(f"  Tasks: {metrics.get('total_tasks', 0)}")
        
        print("\nQuality Scores:")
        print(f"  Completeness: {metrics.get('completeness_score', 0):.1f}/100")
        print(f"  Consistency: {metrics.get('consistency_score', 0):.1f}/100")
        print(f"  Diversity: {metrics.get('diversity_score', 0):.1f}/100")
        
        print("\n" + "="*60 + "\n")
