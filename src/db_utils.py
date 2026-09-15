from pathlib import Path
import sqlite3
import pandas as pd


# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Database path
DB_PATH = BASE_DIR / 'Data' / 'Processed' / 'ipl.db'


def create_database(matches, deliveries, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)

    matches.to_sql(
        'matches',
        conn,
        if_exists='replace',
        index=False
    )

    deliveries.to_sql(
        'deliveries',
        conn,
        if_exists='replace',
        index=False
    )

    conn.close()


def run_query(query, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)

    result = pd.read_sql_query(query, conn)

    conn.close()

    return result


def load_queries(sql_file=None):
    if sql_file is None:
        sql_file = BASE_DIR / 'sql' / 'queries.sql'

    queries = {}

    current_name = None
    current_sql = []

    with open(sql_file) as f:
        for line in f:

            if line.strip().startswith('-- name:'):

                if current_name:
                    queries[current_name] = '\n'.join(current_sql).strip()

                current_name = line.split('-- name:')[1].strip()
                current_sql = []

            else:
                current_sql.append(line)

        if current_name:
            queries[current_name] = '\n'.join(current_sql).strip()

    return queries