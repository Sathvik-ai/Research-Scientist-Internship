import sqlite3
import uuid
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()


def _uid():
    return str(uuid.uuid4())


def generate_users(conn: sqlite3.Connection, org_id: str, num_users: int):
    cur = conn.cursor()
    users = []
    start = datetime.utcnow() - timedelta(days=180)
    for _ in range(num_users):
        user_id = _uid()
        full_name = fake.name()
        email = fake.unique.company_email() if False else fake.unique.email()
        role = fake.job()
        created_at = start + timedelta(days=fake.random_int(0, 180))
        cur.execute('INSERT INTO users(user_id, org_id, email, full_name, role, created_at) VALUES (?,?,?,?,?,?)',
                    (user_id, org_id, email, full_name, role, created_at.isoformat()))
        users.append({'user_id': user_id, 'email': email, 'full_name': full_name})
    return users
