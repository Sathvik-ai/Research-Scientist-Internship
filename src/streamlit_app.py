import streamlit as st
import sqlite3
import os
from datetime import datetime
import pandas as pd

DEFAULT_DB = os.environ.get('DATABASE_PATH', 'output/asana_simulation.sqlite')


def safe_connect(db_path):
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def load_projects_teams(conn):
    cur = conn.cursor()
    cur.execute('SELECT p.project_id, p.name as project_name, t.team_id, t.name as team_name FROM projects p JOIN teams t ON p.team_id = t.team_id')
    rows = cur.fetchall()
    return rows


def load_assignees_for_team(conn, team_id):
    cur = conn.cursor()
    cur.execute('SELECT u.user_id, u.full_name FROM users u JOIN team_memberships m ON u.user_id = m.user_id WHERE m.team_id = ?', (team_id,))
    return cur.fetchall()


def query_tasks(conn, project_id=None, team_id=None, assignee_id=None):
    cur = conn.cursor()
    q = '''SELECT tasks.task_id, tasks.name as task_name, tasks.description, tasks.created_at, tasks.due_date, tasks.completed,
                  projects.project_id, projects.name as project_name,
                  teams.team_id, teams.name as team_name,
                  users.user_id as assignee_id, users.full_name as assignee_name,
                  sections.name as section_name
           FROM tasks
           JOIN projects ON tasks.project_id = projects.project_id
           JOIN teams ON projects.team_id = teams.team_id
           LEFT JOIN users ON tasks.assignee_id = users.user_id
           LEFT JOIN sections ON tasks.section_id = sections.section_id
           WHERE 1=1'''
    params = []
    if project_id and project_id != 'ALL':
        q += ' AND projects.project_id = ?'
        params.append(project_id)
    if team_id and team_id != 'ALL':
        q += ' AND teams.team_id = ?'
        params.append(team_id)
    if assignee_id and assignee_id != 'ALL':
        q += ' AND users.user_id = ?'
        params.append(assignee_id)
    cur.execute(q, params)
    return cur.fetchall()


def compute_status(row):
    now = datetime.utcnow()
    if row['completed']:
        return 'Completed'
    due = row['due_date']
    section = row['section_name'] or ''
    try:
        if due:
            due_dt = datetime.fromisoformat(due)
            if due_dt < now:
                return 'Overdue'
    except Exception:
        pass
    if section.lower() == 'in progress':
        return 'In Progress'
    return 'Open'


st.set_page_config(page_title='Asana Simulation Explorer')
st.title('Asana Simulation — Read-only Explorer')

db_path = st.text_input('SQLite DB path', DEFAULT_DB)
conn = safe_connect(db_path)
if conn is None:
    st.warning('Database not found at path: ' + db_path)
    st.stop()

rows = load_projects_teams(conn)
projects = sorted({(r['project_id'], r['project_name']) for r in rows}, key=lambda x: x[1])
project_options = ['ALL'] + [p[0] for p in projects]
project_display = {p[0]: p[1] for p in projects}

selected_project = st.selectbox('Project (select to filter)', options=project_options, format_func=lambda x: 'All projects' if x == 'ALL' else project_display.get(x, x))

# derive teams based on project selection
if selected_project != 'ALL':
    team_list = [(r['team_id'], r['team_name']) for r in rows if r['project_id'] == selected_project]
else:
    team_list = sorted({(r['team_id'], r['team_name']) for r in rows}, key=lambda x: x[1])
team_options = ['ALL'] + [t[0] for t in team_list]
team_display = {t[0]: t[1] for t in team_list}

selected_team = st.selectbox('Team (select to filter)', options=team_options, format_func=lambda x: 'All teams' if x == 'ALL' else team_display.get(x, x))

# assignee options
assignees = []
if selected_team != 'ALL':
    ass_rows = load_assignees_for_team(conn, selected_team)
    assignees = [(a['user_id'], a['full_name']) for a in ass_rows]
else:
    cur = conn.cursor()
    cur.execute('SELECT user_id, full_name FROM users')
    assignees = [(r['user_id'], r['full_name']) for r in cur.fetchall()]
assignee_options = ['ALL'] + [a[0] for a in assignees]
assignee_display = {a[0]: a[1] for a in assignees}

selected_assignee = st.selectbox('Assignee (select to filter)', options=assignee_options, format_func=lambda x: 'All assignees' if x == 'ALL' else assignee_display.get(x, x))

st.markdown('---')

# Query tasks
task_rows = query_tasks(conn, project_id=selected_project, team_id=selected_team, assignee_id=selected_assignee)

# Build DataFrame for display
records = []
for r in task_rows:
    assigned_date = r['created_at'] if r['assignee_id'] else None
    status = compute_status(r)
    records.append({
        'project_id': r['project_id'],
        'project_name': r['project_name'],
        'team_id': r['team_id'],
        'team_name': r['team_name'],
        'task_id': r['task_id'],
        'task_description': r['description'],
        'assignee_name': r['assignee_name'],
        'assigned_date': assigned_date,
        'due_date': r['due_date'],
        'status': status
    })

df = pd.DataFrame.from_records(records)
st.subheader('Tasks')
st.dataframe(df[['project_id','project_name','team_id','team_name','task_id','task_description','assignee_name','assigned_date','due_date','status']])

st.markdown('---')
# QC metrics
cur = conn.cursor()
total_users = cur.execute('SELECT COUNT(1) FROM users').fetchone()[0]
total_projects = cur.execute('SELECT COUNT(1) FROM projects').fetchone()[0]
total_tasks = cur.execute('SELECT COUNT(1) FROM tasks').fetchone()[0]
unassigned = cur.execute('SELECT COUNT(1) FROM tasks WHERE assignee_id IS NULL').fetchone()[0]
overdue = cur.execute("SELECT COUNT(1) FROM tasks WHERE completed = 0 AND due_date IS NOT NULL AND due_date < ?", (datetime.utcnow().isoformat(),)).fetchone()[0]

st.subheader('QC Metrics')
cols = st.columns(5)
cols[0].metric('Total users', total_users)
cols[1].metric('Total projects', total_projects)
cols[2].metric('Total tasks', total_tasks)
cols[3].metric('% unassigned', f"{(unassigned/total_tasks*100):.1f}%")
cols[4].metric('% overdue', f"{(overdue/total_tasks*100):.1f}%")

st.caption('This explorer is read-only and will not modify the database. Use `src/main.py` to generate or update the database separately.')
