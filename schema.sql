PRAGMA foreign_keys = ON;

CREATE TABLE organizations (
  org_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  domain TEXT
);

CREATE TABLE teams (
  team_id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY(org_id) REFERENCES organizations(org_id)
);

CREATE TABLE users (
  user_id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  role TEXT,
  created_at TIMESTAMP,
  FOREIGN KEY(org_id) REFERENCES organizations(org_id)
);

CREATE TABLE team_memberships (
  membership_id TEXT PRIMARY KEY,
  team_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  role_in_team TEXT,
  FOREIGN KEY(team_id) REFERENCES teams(team_id),
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE projects (
  project_id TEXT PRIMARY KEY,
  team_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP,
  FOREIGN KEY(team_id) REFERENCES teams(team_id)
);

CREATE TABLE sections (
  section_id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY(project_id) REFERENCES projects(project_id)
);

CREATE TABLE tasks (
  task_id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  section_id TEXT,
  parent_task_id TEXT,
  name TEXT NOT NULL,
  description TEXT,
  assignee_id TEXT,
  due_date DATE,
  created_at TIMESTAMP,
  completed BOOLEAN DEFAULT 0,
  completed_at TIMESTAMP,
  FOREIGN KEY(project_id) REFERENCES projects(project_id),
  FOREIGN KEY(section_id) REFERENCES sections(section_id),
  FOREIGN KEY(assignee_id) REFERENCES users(user_id),
  FOREIGN KEY(parent_task_id) REFERENCES tasks(task_id)
);

CREATE TABLE comments (
  comment_id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  body TEXT,
  created_at TIMESTAMP,
  FOREIGN KEY(task_id) REFERENCES tasks(task_id),
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE custom_field_defs (
  field_id TEXT PRIMARY KEY,
  project_id TEXT,
  name TEXT NOT NULL,
  field_type TEXT NOT NULL
);

CREATE TABLE custom_field_values (
  value_id TEXT PRIMARY KEY,
  field_id TEXT NOT NULL,
  task_id TEXT NOT NULL,
  value TEXT,
  FOREIGN KEY(field_id) REFERENCES custom_field_defs(field_id),
  FOREIGN KEY(task_id) REFERENCES tasks(task_id)
);

CREATE TABLE tags (
  tag_id TEXT PRIMARY KEY,
  org_id TEXT NOT NULL,
  name TEXT NOT NULL,
  FOREIGN KEY(org_id) REFERENCES organizations(org_id)
);

CREATE TABLE task_tags (
  id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL,
  tag_id TEXT NOT NULL,
  FOREIGN KEY(task_id) REFERENCES tasks(task_id),
  FOREIGN KEY(tag_id) REFERENCES tags(tag_id)
);

CREATE TABLE attachments (
  attachment_id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL,
  filename TEXT NOT NULL,
  url TEXT,
  uploaded_by TEXT,
  created_at TIMESTAMP,
  FOREIGN KEY(task_id) REFERENCES tasks(task_id),
  FOREIGN KEY(uploaded_by) REFERENCES users(user_id)
);

CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_assignee ON tasks(assignee_id);
CREATE INDEX idx_users_org ON users(org_id);
