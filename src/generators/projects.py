"""Compatibility wrapper exposing project-related generator functions.

Some consumers expect a `generators.projects` module. This file delegates to
`generators.teams_projects` which contains the authoritative implementation.
"""

from .teams_projects import generate_organization


def generate_projects(conn, num_users=200):
    """Create an organization (teams, users, projects, sections) and return
    the generated org structure.
    """
    return generate_organization(conn, num_users=num_users)
