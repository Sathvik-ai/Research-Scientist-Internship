import sqlite3
import uuid
from faker import Faker
from datetime import datetime, timedelta
from .llm_stub import generate_task_name, generate_description

fake = Faker()


def _uid():
    return str(uuid.uuid4())


def _choose_assignee(conn, team_id):
    cur = conn.cursor()
    cur.execute('''SELECT u.user_id FROM users u JOIN team_memberships m ON u.user_id = m.user_id WHERE m.team_id = ? LIMIT 200''', (team_id,))
    rows = cur.fetchall()
    if not rows:
        return None
    return rows[fake.random_int(0, len(rows)-1)][0]


def generate_tasks(conn: sqlite3.Connection, org_struct: dict, density=1.0):
    cur = conn.cursor()
    projects = org_struct.get('projects', [])
    tags = org_struct.get('tags', [])
    custom_fields = org_struct.get('custom_fields', [])
    now = datetime.utcnow()
    for p in projects:
        # create tasks per project: scaled with density
        n_tasks = int(20 * density * fake.random_int(1, 5))
        # get section ids for project
        cur.execute('SELECT section_id, name FROM sections WHERE project_id = ?', (p['project_id'],))
        sections = cur.fetchall()
        for i in range(n_tasks):
            task_id = _uid()
            name = generate_task_name()
            desc = generate_description(name, project_context='')
            section = fake.random_element(elements=sections) if sections else (None, None)
            section_id = section[0] if section else None
            # assign with 85% probability
            assignee = _choose_assignee(conn, p['team_id']) if fake.random_int(1,100) <= 85 else None
            created = now - timedelta(days=fake.random_int(0, 720))
            # due date heuristics
            if fake.random_int(1,100) <= 90:
                due = created + timedelta(days=fake.random_int(1,90))
            else:
                due = None
            # completion
            completed = False
            completed_at = None
            if fake.random_int(1,100) <= 60:
                completed = True
                completed_at = created + timedelta(days=fake.random_int(0, 60))
                if completed_at > now:
                    completed_at = now - timedelta(days=fake.random_int(0,3))

            cur.execute('''INSERT INTO tasks(task_id, project_id, section_id, parent_task_id, name, description, assignee_id, due_date, created_at, completed, completed_at)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
                        (task_id, p['project_id'], section_id, None, name, desc, assignee, due.isoformat() if due else None, created.isoformat(), int(completed), completed_at.isoformat() if completed_at else None))

            # occasional comment
            if fake.random_int(1,100) <= 40 and assignee:
                comment_id = _uid()
                body = fake.sentence()
                cur.execute('INSERT INTO comments(comment_id, task_id, user_id, body, created_at) VALUES (?,?,?,?,?)',
                            (comment_id, task_id, assignee, body, (created + timedelta(days=1)).isoformat()))

            # attach tags randomly
            if tags and fake.random_int(1,100) <= 35:
                t = fake.random_element(elements=tags)
                tt_id = _uid()
                cur.execute('INSERT INTO task_tags(id, task_id, tag_id) VALUES (?,?,?)', (tt_id, task_id, t['tag_id']))

            # assign some custom field values for fields that belong to this project
            for cf in [c for c in custom_fields if c['project_id'] == p['project_id']]:
                value_id = _uid()
                if cf['field_type'] == 'text':
                    val = fake.sentence(nb_words=6)
                elif cf['field_type'] == 'number':
                    val = str(fake.random_int(1, 100))
                else:
                    # enum
                    val = fake.random_element(elements=['A', 'B', 'C', 'D'])
                cur.execute('INSERT INTO custom_field_values(value_id, field_id, task_id, value) VALUES (?,?,?,?)', (value_id, cf['field_id'], task_id, val))

            # occasional attachment
            if fake.random_int(1,100) <= 10:
                attachment_id = _uid()
                filename = fake.file_name(extension='pdf')
                url = f"https://files.example/{attachment_id}/{filename}"
                uploaded_by = assignee
                cur.execute('INSERT INTO attachments(attachment_id, task_id, filename, url, uploaded_by, created_at) VALUES (?,?,?,?,?,?)',
                            (attachment_id, task_id, filename, url, uploaded_by, (created + timedelta(hours=2)).isoformat()))

    conn.commit()
