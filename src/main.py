import argparse
import sqlite3
import os
import uuid
from dotenv import load_dotenv

from generators.users import generate_users
from generators.teams_projects import generate_organization
from generators.tasks import generate_tasks


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_schema(conn, schema_path):
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--users', type=int, default=200, help='Number of users to generate')
    parser.add_argument('--db', type=str, default=os.path.join(OUTPUT_DIR, 'asana_simulation.sqlite'))
    args = parser.parse_args()

    load_dotenv()

    db_path = args.db
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON;')

    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
    load_schema(conn, schema_path)

    # create org, teams, projects and users
    org = generate_organization(conn, num_users=args.users)

    # metadata: tags, custom fields
    from generators.metadata import generate_metadata
    org = generate_metadata(conn, org)

    # tasks and related artifacts
    generate_tasks(conn, org, density=1.0)

    conn.commit()
    conn.close()
    print('Wrote DB to', db_path)


if __name__ == '__main__':
    main()
