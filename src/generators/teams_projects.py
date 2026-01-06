import sqlite3
import uuid
from faker import Faker
from datetime import datetime
from .users import generate_users

fake = Faker()


def _uid():
    return str(uuid.uuid4())


def generate_organization(conn: sqlite3.Connection, num_users: int = 200):
    cur = conn.cursor()
    org_id = _uid()
    org_name = fake.company() + ' Inc.'
    domain = org_name.replace(' ', '').lower() + '.com'
    cur.execute('INSERT INTO organizations(org_id, name, domain) VALUES (?,?,?)', (org_id, org_name, domain))

    # teams: create teams proportional to users (avg team size ~8-12)
    avg_team_size = 10
    num_teams = max(1, num_users // avg_team_size)
    teams = []
    for i in range(max(3, num_teams)):
        team_id = _uid()
        team_name = fake.bs().title()[:40]
        cur.execute('INSERT INTO teams(team_id, org_id, name) VALUES (?,?,?)', (team_id, org_id, team_name))
        teams.append({'team_id': team_id, 'name': team_name})

    users = generate_users(conn, org_id, num_users)

    # assign users to teams round-robin
    from itertools import cycle
    team_cycle = cycle(teams)
    for u in users:
        t = next(team_cycle)
        membership_id = _uid()
        cur.execute('INSERT INTO team_memberships(membership_id, team_id, user_id, role_in_team) VALUES (?,?,?,?)',
                    (membership_id, t['team_id'], u['user_id'], 'member'))

    # projects: 1-3 per team
    projects = []
    for t in teams:
        for _ in range(fake.random_int(1, 3)):
            project_id = _uid()
            name = fake.catch_phrase()[:80]
            desc = fake.sentence(nb_words=12)
            cur.execute('INSERT INTO projects(project_id, team_id, name, description, created_at) VALUES (?,?,?,?,?)',
                        (project_id, t['team_id'], name, desc, datetime.utcnow().isoformat()))
            # sections
            for sname in ['To Do', 'In Progress', 'Review', 'Done']:
                section_id = _uid()
                cur.execute('INSERT INTO sections(section_id, project_id, name) VALUES (?,?,?)', (section_id, project_id, sname))
            projects.append({'project_id': project_id, 'team_id': t['team_id']})

    conn.commit()
    return {'org_id': org_id, 'teams': teams, 'projects': projects}
