#!/usr/bin/env python3
import os
import sys
import time

import psycopg2
from dotenv import load_dotenv
from faker import Faker
from psycopg2 import sql
import pandas as pd
pd.set_option('display.max_rows', None)
from fsi_data_generator import generate_banking_data

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)  # ensures that there is no limit to the width of a column
pd.set_option('display.max_colwidth', None)  # ensures that each column shows all of the data in that column

# Load environment variables from .env file
load_dotenv()

# Import the DataGenerator class
# Assuming the DataGenerator code is in a file named data_generator.py
try:
    from data_generator import DataGenerator
except ImportError:
    print("Error: Could not import DataGenerator. Make sure data_generator.py is in the same directory.")
    sys.exit(1)

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

select_10_rows_from_each_table()

def create_test_database():
    """
    Create a test database with a random schema for testing the DataGenerator.
    Returns connection parameters for the test database and the schema name.
    """
    # Database connection parameters from .env file with fallbacks
    conn_params = {
        "host": os.environ.get("DB_HOST", "localhost"),
        "database": "postgres",  # Connect to default postgres database first
        "user": os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASSWORD", "password"),
        "port": os.environ.get("DB_PORT", "5432")
    }

    test_db_name = f"test_data_generator_{int(time.time())}"
    # Create a random schema name for better isolation
    test_schema_name = f"test_schema_{int(time.time())}"

    try:
        # Connect to the default postgres database to create our test database
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cur = conn.cursor()

        # Create a new test database
        print(f"Creating test database: {test_db_name}")
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(test_db_name)))

        # Close connection to postgres
        cur.close()
        conn.close()

        # Update connection parameters to use our new test database
        conn_params["database"] = test_db_name

        # Connect to the new test database
        conn = psycopg2.connect(**conn_params)
        conn.autocommit = True
        cur = conn.cursor()

        # Create a custom schema for the test
        print(f"Creating schema: {test_schema_name}")
        cur.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(test_schema_name)))

        # Create test schema with related tables
        print("Creating test tables in the new schema...")

        # Create a simple schema with related tables - now in custom schema
        setup_queries = [
            sql.SQL("""
            CREATE TABLE {}.users (
                user_id SERIAL PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(100) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                birthdate DATE,
                created_at TIMESTAMP DEFAULT NOW()
            )
            """).format(sql.Identifier(test_schema_name)),

            sql.SQL("""
            CREATE TABLE {}.categories (
                category_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                parent_category_id INTEGER REFERENCES {}.categories(category_id)
            )
            """).format(sql.Identifier(test_schema_name), sql.Identifier(test_schema_name)),

            sql.SQL("""
            CREATE TABLE {}.products (
                product_id SERIAL PRIMARY KEY,
                name VARCHAR(200) NOT NULL,
                description TEXT,
                price NUMERIC(10, 2) NOT NULL,
                category_id INTEGER REFERENCES {}.categories(category_id) NOT NULL,
                created_by INTEGER REFERENCES {}.users(user_id) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                stock_quantity INTEGER NOT NULL DEFAULT 0
            )
            """).format(sql.Identifier(test_schema_name), sql.Identifier(test_schema_name),
                        sql.Identifier(test_schema_name)),

            sql.SQL("""
            CREATE TABLE {}.orders (
                order_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES {}.users(user_id) NOT NULL,
                order_date TIMESTAMP DEFAULT NOW(),
                total_amount NUMERIC(12, 2) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'pending'
            )
            """).format(sql.Identifier(test_schema_name), sql.Identifier(test_schema_name)),

            sql.SQL("""
            CREATE TABLE {}.order_items (
                order_item_id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES {}.orders(order_id) NOT NULL,
                product_id INTEGER REFERENCES {}.products(product_id) NOT NULL,
                quantity INTEGER NOT NULL,
                price NUMERIC(10, 2) NOT NULL,
                subtotal NUMERIC(20, 2) GENERATED ALWAYS AS (quantity * price) STORED
            )
            """).format(sql.Identifier(test_schema_name), sql.Identifier(test_schema_name),
                        sql.Identifier(test_schema_name))
        ]

        for query in setup_queries:
            cur.execute(query)

        # Close connection
        cur.close()
        conn.close()

        print(f"Test database '{test_db_name}' with schema '{test_schema_name}' created successfully")
        return conn_params, test_schema_name

    except Exception as e:
        print(f"Error setting up test database: {e}")
        # Try to clean up if something went wrong
        try:
            if 'conn' in locals() and conn:
                conn.close()
            # Connect to postgres to drop the test database if it was created
            cleanup_conn = psycopg2.connect(**{**conn_params, "database": "postgres"})
            cleanup_conn.autocommit = True
            cleanup_cur = cleanup_conn.cursor()
            cleanup_cur.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
            cleanup_conn.close()
        except Exception as cleanup_error:
            print(f"Error during cleanup: {cleanup_error}")
        sys.exit(1)


def test_data_generator():
    """Run a test of the DataGenerator with the test database."""
    # Create the test database and get connection parameters
    conn_params, test_schema_name = create_test_database()

    try:
        print("\nStarting DataGenerator test...")

        fake = Faker()

        # Define custom generators for more realistic data
        def email_generator(row_values, _table, _column):
            """Generate email based on first and last name"""
            if 'first_name' in row_values and 'last_name' in row_values:
                first = row_values['first_name'].lower()
                last = row_values['last_name'].lower()
                return f"{first}.{last}@example.com"
            return "unknown@example.com"

        def order_status_generator(_row_values, _table, _column):
            """Generate realistic order status"""
            import random
            statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            weights = [0.1, 0.2, 0.3, 0.3, 0.1]  # Weighted probabilities
            return random.choices(statuses, weights=weights, k=1)[0]

        def fake_words(_row_values, _table, _column):
            return fake.paragraph()

        # Define custom generators - now with the test schema prefix
        custom_generators = [
            (f'{test_schema_name}\\.users', 'email', email_generator),
            (f'{test_schema_name}\\.orders', 'status', order_status_generator),
            (f'{test_schema_name}\\.products', 'description', lambda row_values, table, column: fake.paragraph())
        ]

        # Define row counts for each table - now with the test schema prefix
        row_counts = {
            f"{test_schema_name}.users": 50,
            f"{test_schema_name}.categories": 10,
            f"{test_schema_name}.products": 100,
            f"{test_schema_name}.orders": 200,
            f"{test_schema_name}.order_items": 500
        }

        # Define exclusions
        exclusions = [
            ('.*', 'created_at')  # Skip created_at columns in all tables
        ]

        # Initialize the DataGenerator
        # Now use the custom schema name instead of 'public'
        generator = DataGenerator(
            conn_params=conn_params,
            schemas=[test_schema_name],  # Only include our custom test schema
            custom_generators=custom_generators,
            exclusions=exclusions
        )

        # Generate data
        generator.generate_vectorized_data(row_counts=row_counts)

        # Verify data was generated
        print("\nVerifying generated data...")
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        tables = ["users", "categories", "products", "orders", "order_items"]
        for table in tables:
            # Query with schema prefix
            cur.execute(sql.SQL("SELECT COUNT(*) FROM {}.{}").format(
                sql.Identifier(test_schema_name),
                sql.Identifier(table)
            ))
            count = cur.fetchone()[0]
            expected = row_counts.get(f"{test_schema_name}.{table}", 100)
            print(f"Table {test_schema_name}.{table}: {count} rows generated (expected ~{expected})")

        # Sample data from each table
        print("\nSample data from tables:")
        for table in tables:
            print(f"\n--- Sample from {test_schema_name}.{table} table ---")
            cur.execute(sql.SQL("SELECT * FROM {}.{} LIMIT 3").format(
                sql.Identifier(test_schema_name),
                sql.Identifier(table)
            ))
            columns = [desc[0] for desc in cur.description]
            print("Columns:", columns)
            for row in cur.fetchall():
                print(row)

        cur.close()
        conn.close()

        print("\nDataGenerator test completed successfully!")

    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        # Clean up - drop the test database
        try:
            # First close any existing connections to the test database
            if 'conn' in locals() and conn:
                conn.close()

            # Connect to postgres to drop the test database
            cleanup_conn = psycopg2.connect(**{**conn_params, "database": "postgres"})
            cleanup_conn.autocommit = True
            cleanup_cur = cleanup_conn.cursor()

            # Force disconnect any remaining sessions to this database
            cleanup_cur.execute(f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = '{conn_params['database']}'
                AND pid <> pg_backend_pid()
            """)

            # Now we can drop the database
            # cleanup_cur.execute(f"DROP DATABASE IF EXISTS {conn_params['database']}")
            cleanup_conn.close()
            # print(f"\nTest database '{conn_params['database']}' with schema '{test_schema_name}' has been dropped")
        except Exception as cleanup_error:
            print(f"Error during cleanup: {cleanup_error}")


def test_banking_data():
    generate_banking_data()

def test_select_from_each_table():
    select_10_rows_from_each_table()

if __name__ == "__main__":
    test_select_from_each_table()
