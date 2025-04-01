#!/usr/bin/env python3
from dotenv import load_dotenv

import os
import pandas as pd
import psycopg2

pd.set_option('display.max_rows', None)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)  # ensures that there is no limit to the width of a column
pd.set_option('display.max_colwidth', None)  # ensures that each column shows all of the data in that column

# Load environment variables from .env file
load_dotenv()


def select_10_rows_from_each_table():
    # connect to the PostgreSQL server
    conn_params = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "database": "postgres",  # Connect to default postgres database first
        "user": os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASSWORD", "password"),
        "port": os.environ.get("DB_PORT", "5432")
    }

    conn = psycopg2.connect(**conn_params)

    # create a cursor
    cur = conn.cursor()

    # Get all schemas
    cur.execute("SELECT schema_name FROM information_schema.schemata;")
    schemas = cur.fetchall()

    for schema in schemas:

        if schema[0] in ['pg_catalog', 'pg_toast', 'public', 'information_schema']:
            continue

        # Get all tables in current schema
        cur.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema[0]}';")
        tables = cur.fetchall()

        for table in tables:
            # Select 10 rows from each table and print
            cur.execute(f"SELECT * FROM \"{schema[0]}\".\"{table[0]}\" LIMIT 10;")
            rows = cur.fetchall()
            # Get the column names from the query result
            colnames = [desc[0] for desc in cur.description]

            # Create a DataFrame with the rows and column names, then print it
            df = pd.DataFrame(rows, columns=colnames)
            print(f"The first 10 rows from table {table[0]} in schema {schema[0]}:")
            print(df)

    # close connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    select_10_rows_from_each_table()
