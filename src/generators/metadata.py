import sqlite3
import uuid
from faker import Faker
from datetime import datetime

fake = Faker()


def _uid():
    return str(uuid.uuid4())


def generate_metadata(conn: sqlite3.Connection, org_struct: dict):
    cur = conn.cursor()
    org_id = org_struct['org_id']
    # create some org-level tags
    tags = []
    tag_names = ['bug', 'feature', 'urgent', 'customer', 'research', 'low-priority', 'qa']
    for name in tag_names:
        tag_id = _uid()
        cur.execute('INSERT INTO tags(tag_id, org_id, name) VALUES (?,?,?)', (tag_id, org_id, name))
        tags.append({'tag_id': tag_id, 'name': name})

    # custom fields per project
    custom_fields = []
    for proj in org_struct.get('projects', []):
        ndefs = fake.random_int(0, 3)
        for _ in range(ndefs):
            field_id = _uid()
            name = fake.word().title()
            field_type = fake.random_element(elements=['text', 'number', 'enum'])
            cur.execute('INSERT INTO custom_field_defs(field_id, project_id, name, field_type) VALUES (?,?,?,?)',
                        (field_id, proj['project_id'], name, field_type))
            custom_fields.append({'field_id': field_id, 'project_id': proj['project_id'], 'name': name, 'field_type': field_type})

    conn.commit()
    org_struct['tags'] = tags
    org_struct['custom_fields'] = custom_fields
    return org_struct
