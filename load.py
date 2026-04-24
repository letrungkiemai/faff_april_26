import csv
import itertools
import os
import re
import sys
from io import StringIO
from pathlib import Path

import psycopg2

CSV_TABLE_MAP = {
    'Badges.csv':      'badges',
    'Comments.csv':    'comments',
    'PostHistory.csv': 'post_history',
    'PostLinks.csv':   'post_links',
    'Posts.csv':       'posts',
    'Tags.csv':        'tags',
    'Users.csv':       'users',
    'Votes.csv':       'votes',
}


def to_snake_case(name):
    s = re.sub(r'([A-Z][a-z]+)', r'_\1', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s).strip('_').lower()


def create_tables(conn, schema_file):
    sql = schema_file.read_text()
    sql = sql.replace('CREATE TABLE ', 'CREATE TABLE IF NOT EXISTS ')
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    print("Tables ready.")


def load_csv(conn, csv_file, table, batch_size=100_000):
    print(f"Loading {csv_file.name} -> {table} ...")
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        cols = ', '.join(to_snake_case(h) for h in headers)

        with conn.cursor() as cur:
            cur.execute(f"CREATE TEMP TABLE tmp_{table} (LIKE {table})")
        conn.commit()

        total_inserted = 0
        batch_num = 0
        while True:
            rows = list(itertools.islice(reader, batch_size))
            if not rows:
                break

            batch_num += 1
            buf = StringIO()
            csv.writer(buf).writerows(rows)
            buf.seek(0)

            with conn.cursor() as cur:
                cur.execute(f"TRUNCATE tmp_{table}")
                cur.copy_expert(f"COPY tmp_{table} ({cols}) FROM STDIN WITH CSV", buf)
                cur.execute(f"""
                    INSERT INTO {table} ({cols})
                    SELECT {cols} FROM tmp_{table}
                    ON CONFLICT DO NOTHING
                """)
                total_inserted += cur.rowcount
            conn.commit()
            print(f"  batch {batch_num}: {total_inserted} rows inserted so far")

        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE tmp_{table}")
        conn.commit()

    print(f"  -> done ({total_inserted} total inserted)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python load.py <data_dir>", file=sys.stderr)
        sys.exit(1)

    root = Path(__file__).parent
    csv_dir = Path(sys.argv[1]) / 'csv'

    if not csv_dir.exists():
        print(f"csv/ folder not found under {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)

    conn = psycopg2.connect(
        host=os.getenv('PGHOST', 'localhost'),
        port=os.getenv('PGPORT', '5432'),
        dbname=os.getenv('PGDATABASE', 'samples'),
        user=os.getenv('PGUSER', 'postgres'),
        password=os.getenv('PGPASSWORD', 'postgres'),
    )

    try:
        create_tables(conn, root / 'schema.sql')

        for filename, table in CSV_TABLE_MAP.items():
            csv_file = csv_dir / filename
            if csv_file.exists():
                load_csv(conn, csv_file, table)
            else:
                print(f"Skipping {filename} (not found)")
    finally:
        conn.close()

    print("\nAll done!")


if __name__ == '__main__':
    main()
