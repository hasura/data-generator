import inspect
import logging
import os
import random
import re
import traceback
from typing import Dict, List

import faker
import networkx as nx
import psycopg2
from anthropic import AnthropicError
from dotenv import load_dotenv
from faker.exceptions import UniquenessException
from psycopg2 import Error, extensions
from sentence_transformers import SentenceTransformer, util

from fsi_data_generator.fsi_generators.helpers.generate_random_interval import \
    generate_random_interval_with_optional_weights
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import (
    generate_unique_json_array, previous_responses)

load_dotenv()

# Configure logging based on LOG_LEVEL environment variable
log_level_str = os.environ.get('LOG_LEVEL', 'INFO').upper()
log_level = getattr(logging, log_level_str, logging.INFO)  # Default to INFO if invalid level

# Configure logger
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)
logging.getLogger('transformers').setLevel(logging.WARNING)
logging.getLogger('torch').setLevel(logging.WARNING)
logging.getLogger('tensorflow').setLevel(logging.WARNING)

logger.info(f"Logging configured with level: {log_level_str}")

import time
from functools import wraps


def timer_decorator(func):
    """Decorator to measure function execution time"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        return result

    return wrapper


class SkipRowGenerationError(Exception):
    """Custom exception to skip row generation for a specific column or table."""
    pass


class DataGenerator:
    """
    A class to generate fake data for a PostgreSQL database, respecting FK constraints
    and using vector search for intelligent Faker provider selection.
    Skips auto-generated columns like SERIAL primary keys.
    """
    inserted_pks: Dict[str, List] = {}

    def __init__(self, conn_params, schemas=None, exclude_schemas=None, exclusions=None, custom_generators=None,
                 batch_size=100, dbml=''):
        """
        Initialize the DataGenerator with database connection parameters and schema options.

        Args:
            conn_params (dict): A dictionary containing the database connection parameters.
            schemas (list, optional): List of schemas to include. If None, all non-system schemas are included.
            exclude_schemas (list, optional): List of schemas to exclude. Default excludes system schemas.
            exclusions (list, optional): List of (table_pattern, column_pattern) tuples specifying items to exclude.
                                        These are interpreted as regex patterns.
            custom_generators (list, optional): List of (table_pattern, column_pattern, generator_func) tuples.
                                              The generator_func should take (row_values, table, column) and return a value.
                                              These are processed after all other columns and can access previously generated values.
            batch_size (int, optional): Number of rows to collect before executing a batch insert. Default is 100.
        """
        self.tuple_cursor = None
        self.column_order = None
        self.conn_params = conn_params
        self.fake = faker.Faker()
        self.conn = None
        self.cur = None
        self.batch_size = batch_size
        self.batch_data = {}  # Storage for batched rows
        self.dbml = dbml

        # Schema management
        self.system_schemas = ['information_schema', 'pg_catalog', 'pg_toast', 'pg_temp']
        self.schemas = schemas  # If None, will be populated with all non-system schemas
        self.exclude_schemas = exclude_schemas + self.system_schemas if exclude_schemas else self.system_schemas

        # Exclusions management using regex patterns
        self.exclusions = list(exclusions) if exclusions else []
        self.exclusion_patterns = []

        # Custom generators using regex patterns
        self.custom_generators = list(custom_generators) if custom_generators else []
        self.custom_generator_patterns = []

        # Data structures to store database metadata
        self.foreign_keys = []
        self.columns = []
        self.auto_generated_columns = {}
        self.table_columns = {}
        self.table_dependencies = {}
        self.ordered_tables = []
        self.inserted_pks = {}
        self.all_table_column_pairs = []  # Will be populated with all (schema.table, column) pairs

        # Vector model components
        self.model = None
        self.faker_names = []
        self.faker_embeddings = None
        self.faker_embedding_map = {}
        self.populated_tables = set()
        self.not_populated_tables = dict()
        self.used_faker_funcs = set()
        self.faker_func_cache = {}  # Cache for faker_func
        self.text_columns = {}
        self.all_tables = []

    def connect_to_db(self):
        """Establish a connection to the database and get available schemas."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cur = self.conn.cursor()
            self.tuple_cursor = self.conn.cursor(cursor_factory=extensions.cursor)

            # If no specific schemas were provided, get all available non-system schemas
            if self.schemas is None:
                self._get_available_schemas()

            logger.debug(f"Working with schemas: {self.schemas}")
            return True
        except Error as e:
            logger.debug(f"Database connection error: {e}")
            return False

    def organize_tables_and_columns(self):
        """Organize table and column information from the database, preserving original column order."""
        # Store column order information separately
        self.column_order = {}

        # Query to get columns in their original order for each schema
        for schema in self.schemas:
            query = """
                SELECT table_name, column_name, data_type, column_default, is_nullable,
                       character_maximum_length, numeric_precision, numeric_scale
                FROM information_schema.columns
                WHERE table_schema = %s
                ORDER BY table_name, ordinal_position
            """
            self.tuple_cursor.execute(query, (schema,))
            ordered_columns = self.tuple_cursor.fetchall()

            # Process columns in their original order
            for table_name, column_name, data_type, column_default, is_nullable, \
                    character_maximum_length, numeric_precision, numeric_scale in ordered_columns:

                table_key = f"{schema}.{table_name}"

                if table_key not in self.table_columns:
                    self.table_columns[table_key] = []
                    self.column_order[table_key] = []

                # Add to ordered list first
                self.column_order[table_key].append(column_name)

                # Add detailed column info
                self.table_columns[table_key].append((
                    column_name, data_type, column_default, is_nullable,
                    character_maximum_length, numeric_precision, numeric_scale
                ))
                # store text columns
                if data_type.lower() in ("text", "varchar", "character varying", "char"):
                    if table_key not in self.text_columns:
                        self.text_columns[table_key] = []
                    self.text_columns[table_key].append(column_name)

            logger.debug(
                f"Organized columns for schema {schema}, tables count: {len(set(table_name for table_name, _, _, _, _, _, _, _ in ordered_columns))}")

        # Log the first few columns for some tables for verification
        for table_key in list(self.table_columns.keys())[:3]:  # Log first 3 tables for brevity
            logger.debug(f"Column order for {table_key}: {self.column_order[table_key][:5]}...")

    def generate_data(self, row_counts=None, commit_frequency=10, scale=1):
        """
        Generate fake data for all tables in the database, respecting dependencies and column order.
        Prioritizes foreign keys to ensure data consistency.

        Args:
            row_counts (dict, optional): A dictionary mapping table names (with schema prefix) to
                                      the desired number of rows to generate for each table.
                                      Defaults to 100 rows for each table if not specified.
                                      Example: {"schema1.table1": 500, "schema2.table2": 1000}
            commit_frequency (int, optional): Number of tables to process before committing.
                                           Set to 0 to only commit at the end.
            scale (float, optional): Scale factor to apply to row counts.
        """
        try:
            # Compile exclusion patterns if they exist
            if self.exclusions:
                self._compile_exclusion_patterns()

            # Compile custom generator patterns if they exist
            if self.custom_generators:
                self._compile_custom_generator_patterns()

            # Process all tables according to dependencies
            tables_processed = 0
            total_rows_generated = 0

            for table_key in self.ordered_tables:
                schema, table = table_key.split('.')

                # Check if the schema is in the excluded list
                if schema in self.exclude_schemas:
                    # logger.debug(f"Skipping excluded schema: {schema}")
                    continue

                logger.debug(f"Processing table {table_key}...")

                # Support both "schema.table" format and "table" format in row_counts
                num_rows = (row_counts.get(table_key, None) or
                            row_counts.get(table, 100) if row_counts else 100)  # Defaults to 100 rows
                num_rows = int(num_rows * scale)

                # Store the total row count for this table on the class instance
                # This allows _flush_batch to access it without complex data structures
                setattr(self, "total_rows_for_" + table_key.replace(".", "_"), num_rows)

                # Get the auto-generated columns for this table
                auto_gen_cols = self.auto_generated_columns.get(table_key, [])

                # Get all valid columns for this table
                valid_columns = set(col_info[0] for col_info in self.table_columns[table_key])
                # logger.debug(f"Valid columns for {table_key}: {valid_columns}")

                # Calculate number of batches for this table
                num_batches = (num_rows + self.batch_size - 1) // self.batch_size  # Ceiling division
                # logger.debug(f"Will insert in {num_batches} batches of up to {self.batch_size} rows each")

                # First determine which columns we'll use (not auto-generated or excluded)
                fk_columns = []  # Columns with foreign key relationships
                custom_columns = []  # Columns with custom generators
                standard_columns = []  # Regular columns (no FK, no custom generator)

                # Track columns that have both FK and custom generator
                fk_custom_columns = set()

                # Get all foreign key columns for this table
                table_fk_columns = set()
                for d in self.foreign_keys:
                    _, fk_schema, fk_table, fk_column, _, _, _ = d.values()
                    if fk_schema == schema and fk_table == table:
                        table_fk_columns.add(fk_column)

                # Use the ordered column list to maintain original order
                for column_name in self.column_order.get(table_key, []):
                    # Find the detailed column info
                    column_info = next((col_info for col_info in self.table_columns[table_key]
                                        if col_info[0] == column_name), None)

                    if not column_info:
                        continue

                    # Skip auto-generated columns
                    if column_name in auto_gen_cols:
                        continue

                    # Skip excluded columns
                    if self._is_excluded(table_key, column_name):
                        # logger.debug(f"Skipping excluded column {table_key}.{column_name}")
                        continue

                    # Check if this column has a custom generator
                    has_custom_generator = self._get_custom_generator(table_key, column_name) is not None

                    # Check if this column has a foreign key constraint
                    is_foreign_key = column_name in table_fk_columns

                    # Add to appropriate list based on characteristics
                    if is_foreign_key:
                        fk_columns.append(column_info)
                        # Also track if it has a custom generator
                        if has_custom_generator:
                            fk_custom_columns.add(column_name)
                    elif has_custom_generator:
                        custom_columns.append(column_info)
                    else:
                        standard_columns.append(column_info)

                # If no usable columns, skip this table entirely
                if not fk_columns and not custom_columns and not standard_columns:
                    logger.debug(f"Skipping table {table_key} - all columns are either auto-generated or excluded")
                    continue

                logger.debug(
                    f"Generating {num_rows} rows for {table_key} with {len(fk_columns)} FK columns, "
                    f"{len(custom_columns)} custom columns, and {len(standard_columns)} standard columns")

                # Generate data for each row
                for row_index in range(num_rows):
                    values = []
                    column_names = []
                    row_values = {}  # Dictionary to store column values for custom generators

                    try:
                        # STEP 1: Process foreign key columns first
                        for column, data_type, column_default, is_nullable, character_maximum_length, num_precision, num_scale in fk_columns:
                            # Skip if this column has already been populated by another process
                            if column in row_values:
                                # logger.debug(f"Column {column} already has a value set, skipping FK processing...")
                                continue

                            column_names.append(column)

                            # Check if this FK column also has a custom generator
                            if column in fk_custom_columns:
                                # For columns with both FK and custom generator, use the custom generator
                                generator_func = self._get_custom_generator(table_key, column)
                                try:
                                    # Call the custom generator with row_values, table_key, and column
                                    custom_value = generator_func(row_values, table_key, column)
                                    if isinstance(custom_value, str) and character_maximum_length and len(
                                            custom_value) > character_maximum_length:
                                        custom_value = custom_value[:character_maximum_length]

                                    values.append(custom_value)
                                    row_values[column] = custom_value

                                    # Check if any newly added columns in row_values are valid columns for this table
                                    for col, val in list(row_values.items()):
                                        if col not in column_names and col in valid_columns and col not in auto_gen_cols:
                                            column_names.append(col)
                                            values.append(val)
                                            # logger.debug(f"Added valid extra column {col} from FK custom generator")

                                except SkipRowGenerationError:
                                    raise
                                except Exception as e:
                                    logger.debug(f"Error in custom generator for FK {table_key}.{column}: {e}")
                                    # Fall back to standard FK handling if the custom generator fails
                                    fk_info = next(
                                        (fk for fk in self.foreign_keys
                                         if fk[1] == schema and fk[2] == table and fk[3] == column), None
                                    )
                                    self._handle_foreign_key(fk_info, table_key, column, is_nullable, values)
                                    row_values[column] = values[-1]
                            else:
                                # Standard FK handling for columns without custom generators
                                fk_info = next(
                                    (fk for fk in self.foreign_keys
                                     if fk.get('table_schema') == schema and fk.get('table_name') == table and fk.get(
                                        'column_name') == column), None
                                )
                                if fk_info:
                                    self._handle_foreign_key(fk_info, table_key, column, is_nullable, values)
                                else:
                                    # logger.debug(f"Warning: Column {column} marked as FK but no FK info found")
                                    self._generate_column_value(table_key,
                                                                column, data_type, column_default, is_nullable,
                                                                character_maximum_length, num_precision, num_scale,
                                                                values)

                                row_values[column] = values[-1]

                        # STEP 2: Process custom columns that are not foreign keys
                        for column, data_type, column_default, is_nullable, character_maximum_length, num_precision, num_scale in custom_columns:
                            # Skip if this column has already been populated by another custom generator
                            if column in row_values:
                                # logger.debug(f"Column {column} already has a value set, skipping custom generation...")
                                continue

                            # Get the custom generator for this column
                            generator_func = self._get_custom_generator(table_key, column)

                            try:
                                # Call the custom generator with row_values, table_key, and column
                                custom_value = generator_func(row_values, table_key, column)
                                if isinstance(custom_value, str) and character_maximum_length and len(
                                        custom_value) > character_maximum_length:
                                    custom_value = custom_value[:character_maximum_length]

                                # Add this column's value to both row_values and the column_names/values lists
                                row_values[column] = custom_value
                                column_names.append(column)
                                values.append(custom_value)

                                # Check if any newly added columns in row_values are valid columns for this table
                                for col, val in list(row_values.items()):
                                    if col not in column_names and col in valid_columns and col not in auto_gen_cols:
                                        column_names.append(col)
                                        values.append(val)
                                        # logger.debug(f"Added valid extra column {col} from custom generator")

                            except AttributeError as e:
                                stack_trace = traceback.format_exc()
                                logger.error(e)
                                logger.error(stack_trace)
                                if is_nullable == 'YES':
                                    row_values[column] = None
                                    column_names.append(column)
                                    values.append(None)
                                else:
                                    default_value = self._generate_default_value(data_type, character_maximum_length)
                                    row_values[column] = default_value
                                    column_names.append(column)
                                    values.append(default_value)
                            except SkipRowGenerationError as _e:
                                raise
                            except Exception as e:
                                logger.debug(f"Error in custom generator for {table_key}.{column}: {e}")
                                # Set to NULL if nullable, otherwise try a generic value
                                if is_nullable == 'YES':
                                    row_values[column] = None
                                    column_names.append(column)
                                    values.append(None)
                                else:
                                    default_value = self._generate_default_value(data_type, character_maximum_length)
                                    row_values[column] = default_value
                                    column_names.append(column)
                                    values.append(default_value)

                        # STEP 3: Process standard columns last
                        for column, data_type, column_default, is_nullable, character_maximum_length, num_precision, num_scale in standard_columns:
                            # Skip if this column has already been populated
                            if column in row_values:
                                # logger.debug(
                                #     f"Column {column} already has a value set, skipping standard generation...")
                                if column not in column_names:
                                    column_names.append(column)
                                    values.append(row_values[column])
                                continue

                            column_names.append(column)

                            # Generate data for regular columns
                            if data_type == 'text':
                                try:
                                    generate_unique_json_array(dbml_string=self.dbml,
                                                               fully_qualified_column_name=f"{table_key}.{column}",
                                                               count=num_rows)
                                except (AnthropicError, ValueError):
                                    pass
                            self._generate_column_value(table_key,
                                                        column, data_type, column_default, is_nullable,
                                                        character_maximum_length, num_precision, num_scale, values)

                            # Store the value in the row_values dictionary
                            row_values[column] = values[-1]

                        # Skip if no columns to insert (shouldn't happen due to earlier check, but just in case)
                        if not column_names:
                            continue

                        # Add the generated row to the batch
                        self._batch_row(table_key, column_names, values)
                        total_rows_generated += 1

                        # Display progress for large tables
                        if (row_index + 1) % self.batch_size == 0 or row_index == num_rows - 1:
                            current_batch = (row_index + 1) // self.batch_size
                            if (row_index + 1) % self.batch_size > 0:
                                current_batch += 1
                            logger.debug(
                                f"Generated {row_index + 1}/{num_rows} rows for {table_key} (Batch {current_batch}/{num_batches})")
                    except SkipRowGenerationError:
                        pass

                # Flush any remaining rows for this table
                self._flush_batch(table_key)

                # Increment processed tables count
                tables_processed += 1

                # Commit periodically if requested
                if commit_frequency > 0 and tables_processed % commit_frequency == 0:
                    self.conn.commit()
                    logger.debug(
                        f"Committed after processing {tables_processed} tables ({total_rows_generated} total rows generated)")
                    total_rows_generated = 0  # Reset counter after commit

            # Final commit for any remaining data
            self.conn.commit()
            logger.debug(
                f"Vectorized data generation complete. Processed {tables_processed} tables with {total_rows_generated} rows in final batch.")

        except Error as e:
            logger.debug(f"Error during data generation: {e}")
            self.conn.rollback()

    def _batch_row(self, table_key, column_names, values):
        """
        Add a row to the batch for the specified table, respecting column order and skipping generated columns.

        Args:
            table_key (str): The table identifier in the format "schema.table"
            column_names (list): List of column names for this row
            values (list): List of values corresponding to the column names
        """
        # Get auto-generated columns for this table
        auto_gen_cols = self.auto_generated_columns.get(table_key, [])

        # Filter out any generated columns that might have been included
        filtered_columns = []
        filtered_values = []

        for i, column in enumerate(column_names):
            if column not in auto_gen_cols:
                filtered_columns.append(column)
                if i < len(values):
                    filtered_values.append(values[i])

        # Skip if we have no columns left after filtering
        if not filtered_columns:
            return

        # Initialize batch structure for this table if it doesn't exist
        if table_key not in self.batch_data:
            self.batch_data[table_key] = {
                'column_names': filtered_columns,
                'rows': []
            }

        # Ensure column order matches for all rows in this batch
        if self.batch_data[table_key]['column_names'] != filtered_columns:
            # If column order differs, flush current batch and start a new one
            self._flush_batch(table_key)
            self.batch_data[table_key] = {
                'column_names': filtered_columns,
                'rows': []
            }

        # Add row values to batch
        self.batch_data[table_key]['rows'].append(filtered_values)

        # Flush batch when it reaches the specified size
        if len(self.batch_data[table_key]['rows']) >= self.batch_size:
            self._flush_batch(table_key)

    def _flush_batch(self, table_key):
        """
        Execute batch insert for the specified table, preserving column order.

        Args:
            table_key (str): The table identifier in the format "schema.table"
        """
        # Skip if no data to flush
        if table_key not in self.batch_data or not self.batch_data[table_key]['rows']:
            return

        schema, table = table_key.split('.')
        column_names = self.batch_data[table_key]['column_names']
        rows = self.batch_data[table_key]['rows']

        columns_str = ", ".join([f'"{col}"' for col in column_names])

        # Construct a multi-row VALUES statement
        placeholders_list = []
        all_values = []

        for row_values in rows:
            # Add placeholders for this row
            placeholders = "(" + ", ".join(["%s"] * len(row_values)) + ")"
            placeholders_list.append(placeholders)
            # Add values to flat list
            all_values.extend(row_values)

        placeholders_str = ", ".join(placeholders_list)
        query = f'INSERT INTO "{schema}"."{table}" ({columns_str}) VALUES {placeholders_str} RETURNING *'

        try:
            # logger.debug(f"Executing batch query: {query}")
            # logger.debug(f"all_values={all_values}")
            self.tuple_cursor.execute(query, all_values)

            # Process returned rows to store primary keys
            inserted_rows = self.tuple_cursor.fetchall()
            for row in inserted_rows:
                self._store_primary_key(table_key, row)
            # if inserted_rows:
            #     logger.debug(f"Stored PKs for {table_key}: {len(inserted_rows)} rows ")

            # Get the total rows for this table from the class instance
            total_rows = getattr(self, "total_rows_for_" + table_key.replace(".", "_"), 0)

            # Properly calculate the number of batches (ceiling division)
            num_batches = (total_rows + self.batch_size - 1) // self.batch_size if total_rows > 0 else 1

            # For logging purposes only
            logger.debug(f"Inserted batch for {table_key}: 1/{num_batches} ({len(rows)} rows)")

            self.populated_tables.add(table_key)

            # Clear the processed batch
            self.batch_data[table_key]['rows'] = []

        except psycopg2.Error as e:
            logger.debug(f"Error batch inserting into {table_key}: {e}")
            self.populated_tables.discard(table_key)
            self.not_populated_tables[table_key] = str(e)
            # Continue with the next batch even if this one fails
            self.conn.rollback()

    def identify_generated_columns(self):
        """
        Identify generated columns in the PostgreSQL database and add them to auto_generated_columns.
        This includes both identity columns (IAL) and computed columns (GENERATED ALWAYS AS).
        """
        for schema_name in self.schemas:
            try:
                # Query to find GENERATED columns (PostgreSQL 12+)
                generated_query = """
                    SELECT table_name, column_name
                    FROM information_schema.columns
                    WHERE table_schema = %s
                    AND (is_generated = 'ALWAYS' OR generation_expression IS NOT NULL)
                """
                self.tuple_cursor.execute(generated_query, (schema_name,))
                generated_cols = self.tuple_cursor.fetchall()

                # Process the results
                for table_name, column_name in generated_cols:
                    table_key = f"{schema_name}.{table_name}"
                    if table_key not in self.auto_generated_columns:
                        self.auto_generated_columns[table_key] = []
                    if column_name not in self.auto_generated_columns[table_key]:
                        self.auto_generated_columns[table_key].append(column_name)
                        logger.debug(f"Identified generated column: {table_key}.{column_name}")

                # Query to find identity columns (SERIAL, BIGSERIAL, etc.)
                identity_query = """
                    SELECT table_name, column_name
                    FROM information_schema.columns
                    WHERE table_schema = %s
                    AND (column_default LIKE 'nextval%%' OR is_identity = 'YES')
                """
                self.tuple_cursor.execute(identity_query, (schema_name,))
                identity_cols = self.tuple_cursor.fetchall()

                # Process the identity columns
                for table_name, column_name in identity_cols:
                    table_key = f"{schema_name}.{table_name}"
                    if table_key not in self.auto_generated_columns:
                        self.auto_generated_columns[table_key] = []
                    if column_name not in self.auto_generated_columns[table_key]:
                        self.auto_generated_columns[table_key].append(column_name)
                        logger.debug(f"Identified identity column: {table_key}.{column_name}")

            except Exception as e:
                logger.debug(f"Error identifying generated columns for schema {schema_name}: {e}")
                # Continue with other schemas even if one fails
                continue

    def identify_all_generated_columns(self):
        """
        Identify all types of auto-generated columns, including SERIAL and GENERATED columns.
        """
        # First identify standard auto-generated columns like SERIAL
        self.identify_auto_generated_columns()

        # Then identify PostgreSQL generated columns (GENERATED ALWAYS AS ...)
        self.identify_generated_columns()

        # Log totals for debugging
        total_tables_with_generated = len(self.auto_generated_columns)
        total_generated_columns = sum(len(cols) for cols in self.auto_generated_columns.values())
        logger.debug(
            f"Found a total of {total_generated_columns} generated columns across {total_tables_with_generated} tables")

    def _flush_all_batches(self):
        """Execute all remaining batch inserts"""
        for table_key in list(self.batch_data.keys()):
            if self.batch_data[table_key]['rows']:
                logger.debug(f"Flushing remaining {len(self.batch_data[table_key]['rows'])} rows for {table_key}")
                self._flush_batch(table_key)

    def _log_performance_stats(self, operation, row_count, start_time):
        """
        Log performance statistics for an operation.

        Args:
            operation (str): Description of the operation being measured
            row_count (int): Number of rows processed
            start_time (float): Start time of the operation (from time.time())
        """
        duration = time.time() - start_time
        rows_per_second = row_count / duration if duration > 0 else 0
        logger.info(f"{operation}: {row_count} rows in {duration:.2f} seconds ({rows_per_second:.2f} rows/sec)")

    def _get_available_schemas(self):
        """Get all available schemas, excluding system schemas and any in exclude_schemas."""
        try:
            # Query to get all schemas
            self.cur.execute("SELECT schema_name FROM information_schema.schemata;")
            all_schemas = [row['schema_name'] for row in self.cur.fetchall()]

            # Filter out excluded schemas
            self.schemas = [schema for schema in all_schemas
                            if schema not in self.exclude_schemas]

            logger.debug(f"Found schemas: {self.schemas}")
        except Error as e:
            logger.debug(f"Error retrieving schemas: {e}")
            # Default to public schema if there's an error
            self.schemas = ['public']

    def _compile_custom_generator_patterns(self):
        """
        Compile regex patterns for custom generators.
        Each custom generator is a (table_pattern, column_pattern, generator_func) tuple.
        """
        if not self.custom_generators:
            return

        logger.debug(f"Processing custom generator patterns...")
        self.custom_generator_patterns = []

        for table_pattern, column_pattern, generator_func in self.custom_generators:
            try:
                # Compile regex patterns
                table_regex = re.compile(table_pattern)
                column_regex = re.compile(column_pattern)
                self.custom_generator_patterns.append((table_regex, column_regex, generator_func))
                logger.debug(f"Added custom generator: table='{table_pattern}', column='{column_pattern}'")
            except re.error as e:
                logger.debug(
                    f"Warning: Invalid regex pattern in custom generator ({table_pattern}, {column_pattern}): {e}")

        # Test which table/column combinations match the patterns
        matches = []
        for table, column in self.all_table_column_pairs:
            for table_regex, column_regex, _ in self.custom_generator_patterns:
                if table_regex.search(table) and column_regex.search(column):
                    matches.append((table, column))
                    break

        if matches:
            logger.debug(f"Found {len(matches)} table/column combinations that will use custom generators:")
            for table, column in matches[:10]:  # Show first 10 for brevity
                logger.debug(f"  - {table}.{column}")
            if len(matches) > 10:
                logger.debug(f"  ... and {len(matches) - 10} more")
        else:
            logger.debug("No columns matched the custom generator patterns")

    def _get_custom_generator(self, table, column):
        """
        Find a matching custom generator for the given table and column.

        Args:
            table (str): Table name with schema (schema.table)
            column (str): Column name

        Returns:
            function or None: The custom generator function if found, None otherwise
        """
        for table_regex, column_regex, generator_func in self.custom_generator_patterns:
            if table_regex.search(table) and column_regex.search(column):
                return generator_func
        return None

    def get_foreign_keys(self):
        """
        Retrieve foreign key relationships from the database for all selected schemas.

        Captures cross-schema foreign key relationships while avoiding system schemas.
        """
        # Filter out system schemas
        user_schemas = [
            schema for schema in self.schemas
            if schema not in ['pg_toast', 'pg_catalog', 'information_schema']
        ]

        # Early return if no user schemas are specified
        if not user_schemas:
            logger.warning("No user schemas specified for foreign key retrieval.")
            self.foreign_keys = []
            return

        query = """
        WITH desired_foreign_keys AS (
            SELECT DISTINCT
                tc.table_catalog,
                tc.table_schema,
                tc.table_name,
                kcu.column_name,
                ccu.table_schema AS foreign_table_schema,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
            JOIN 
                information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
                AND tc.table_catalog = kcu.table_catalog
            JOIN 
                information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.constraint_catalog = tc.constraint_catalog
            JOIN
                information_schema.referential_constraints AS rc
                ON rc.constraint_name = tc.constraint_name
                AND rc.constraint_catalog = tc.table_catalog
            WHERE
                tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema NOT IN ('pg_toast', 'pg_catalog', 'information_schema')
                AND ccu.table_schema NOT IN ('pg_toast', 'pg_catalog', 'information_schema')
        )
        SELECT 
            table_catalog,
            table_schema,
            table_name,
            column_name,
            foreign_table_schema,
            foreign_table_name,
            foreign_column_name
        FROM 
            desired_foreign_keys
        WHERE 
            table_schema = ANY(%s)
            OR foreign_table_schema = ANY(%s)
        ORDER BY 
            table_catalog, 
            table_schema, 
            table_name, 
            column_name;
        """

        try:
            logger.debug(f"Executing query to retrieve foreign keys")
            logger.debug(f"User schemas used in the query: {user_schemas}")

            # Execute the query with user schemas
            self.cur.execute(query, (user_schemas, user_schemas))
            self.foreign_keys = self.cur.fetchall()

            logger.debug(f"Total foreign keys retrieved: {len(self.foreign_keys)}")

        except Exception as e:
            logger.error(f"Error retrieving foreign keys: {e}")
            logger.error(f"Original schemas: {self.schemas}")
            logger.error(f"User schemas: {user_schemas}")
            self.foreign_keys = []
            raise

    def get_all_tables(self) -> List[str]:
        """
        Retrieve all tables from the database for the specified schemas,
        excluding system schemas like 'pg_toast', 'pg_catalog', and 'information_schema'.
        """

        # Filter out system schemas
        user_schemas = [
            schema for schema in self.schemas
            if schema not in ['pg_toast', 'pg_catalog', 'information_schema']
        ]

        # Early return if no user schemas are specified
        if not user_schemas:
            logger.warning("No user schemas specified for table retrieval.")
            self.all_tables = []
            return self.all_tables

        query = """
                SELECT DISTINCT
            table_schema || '.' || table_name AS table_full_name,
            table_schema,
            table_name
        FROM 
            information_schema.tables
        WHERE
            table_schema = ANY(%s)
            AND table_type = 'BASE TABLE'
        ORDER BY 
            table_schema, 
            table_name;
        """

        try:
            logger.debug(f"Executing query to retrieve all tables")
            logger.debug(f"User schemas used in the query: {user_schemas}")

            # Execute the query with user schemas
            self.cur.execute(query, (user_schemas,))
            result = self.cur.fetchall()

            # Flatten result into a simple list of table names
            self.all_tables = [row.get('table_full_name') for row in result]

            logger.debug(f"Total tables retrieved: {len(self.all_tables)}")

            return self.all_tables

        except Exception as e:
            logger.error(f"Error retrieving tables: {e}")
            logger.error(f"Original schemas: {self.schemas}")
            logger.error(f"User schemas: {user_schemas}")
            self.all_tables = []
            raise

    def get_columns(self):
        """Retrieve column information for all tables in the specified schemas."""
        schema_placeholders = ', '.join(['%s'] * len(self.schemas))
        query = f"""
            SELECT 
                table_schema, table_name, column_name, data_type, column_default, 
                is_nullable, character_maximum_length, numeric_precision, numeric_scale
            FROM information_schema.columns
            WHERE table_schema IN ({schema_placeholders});
        """
        self.cur.execute(query, self.schemas)
        self.columns = self.cur.fetchall()

        # Build a list of all table.column combinations for exclusion matching
        self.all_table_column_pairs = []
        for column in self.columns:
            self.all_table_column_pairs.append(
                (f"{column.get('table_schema')}.{column.get('table_name')}", column.get('column_name')))

        logger.debug(f"Retrieved information for {len(self.columns)} columns across {len(self.schemas)} schemas")

    def _compile_exclusion_patterns(self):
        """
        Compile regex patterns for exclusions.
        Each exclusion is a (table_pattern, column_pattern) tuple where both are regex patterns.
        """
        if not self.exclusions:
            return

        logger.debug(f"Processing exclusion patterns: {self.exclusions}")
        self.exclusion_patterns = []

        for table_pattern, column_pattern in self.exclusions:
            try:
                # Compile regex patterns
                table_regex = re.compile(table_pattern)
                column_regex = re.compile(column_pattern)
                self.exclusion_patterns.append((table_regex, column_regex))
                logger.debug(f"Added exclusion pattern: table='{table_pattern}', column='{column_pattern}'")
            except re.error as e:
                logger.debug(f"Warning: Invalid regex pattern in exclusion ({table_pattern}, {column_pattern}): {e}")

        # Test which table/column combinations match the patterns
        logger.debug("Testing exclusion patterns against database columns:")
        excluded_combinations = self._get_excluded_columns()
        if excluded_combinations:
            logger.debug(f"Found {len(excluded_combinations)} excluded table/column combinations:")
            # Convert the set to a list for subscripting
            excluded_list = list(excluded_combinations)
            # Show the first 10 entries
            for table, column in excluded_list[:10]:
                logger.debug(f"  - {table}.{column}")
            if len(excluded_combinations) > 10:
                logger.debug(f"  ... and {len(excluded_combinations) - 10} more")
        else:
            logger.debug("No columns matched the exclusion patterns")

    def _get_excluded_columns(self):
        """
        Apply exclusion patterns to all table/column combinations to get a list
        of excluded columns. Returns a list of (table, column) tuples that should be excluded.
        """
        excluded = set()

        # Apply each pattern to all table/column combinations
        for table_regex, column_regex in self.exclusion_patterns:
            for table, column in self.all_table_column_pairs:
                if table_regex.search(table) and column_regex.search(column):
                    excluded.add((table, column))

        return excluded

    def _is_excluded(self, table, column):
        """
        Check if a specific table column is excluded by any of the patterns.

        Args:
            table (str): Table name with schema (schema.table)
            column (str): Column name

        Returns:
            bool: True if the column should be excluded, False otherwise
        """
        for table_regex, column_regex in self.exclusion_patterns:
            if table_regex.search(table) and column_regex.search(column):
                return True
        return False

    def identify_auto_generated_columns(self):
        """Identify auto-generated columns like SERIAL primary keys."""
        for schema_name, table_name, column_name, data_type, column_default, is_nullable, maximum_character_length, num_precision, num_scale in self.columns:
            table_key = f"{schema_name}.{table_name}"

            if table_key not in self.auto_generated_columns:
                self.auto_generated_columns[table_key] = []

            # Check if column is auto-generated
            is_auto_generated = False

            # Check for SERIAL, BIGSERIAL (they have defaults like "nextval('table_column_seq'::regclass)")
            if column_default and "nextval" in column_default:
                is_auto_generated = True

            # Add to auto-generated columns list if identified
            if is_auto_generated:
                self.auto_generated_columns[table_key].append(column_name)
                logger.debug(f"Identified auto-generated column: {table_key}.{column_name}")

    def determine_table_dependencies(self):
        """Determine table dependencies based on foreign key relationships,
        including tables with no upstream or downstream dependencies."""

        for fk in self.foreign_keys:
            # for _, child_schema, child_table, _, parent_schema, parent_table, _ in self.foreign_keys:
            child_key = f"{fk.get('table_schema')}.{fk.get('table_name')}"
            parent_key = f"{fk.get('foreign_table_schema')}.{fk.get('foreign_table_name')}"

            if parent_key not in self.table_dependencies:
                self.table_dependencies[parent_key] = []  # Ensure parent exists as a key
            if child_key not in self.table_dependencies:
                self.table_dependencies[child_key] = []

            # Use a list to maintain order, avoid duplicates
            if child_key != parent_key and parent_key not in self.table_dependencies[child_key]:
                self.table_dependencies[child_key].append(parent_key)  # Child depends on Parent

        # Handle tables with no dependencies at all
        for table in self.get_all_tables():
            if table not in self.table_dependencies:
                self.table_dependencies[table] = []

        # Print dependency graph for debugging
        logger.debug("Dependency Graph:")
        for table, dependencies in self.table_dependencies.items():
            logger.debug(f"{table} depends on: {dependencies}")

    def sort_tables_by_dependencies(self):
        """
        Sort tables based on their dependencies using topological sorting.
        Tables with no dependencies will be processed first.
        """
        logger.debug("Unsorted Tables (keys from table_dependencies):")
        logger.debug(list(self.table_dependencies.keys()))

        self.ordered_tables = self._topological_sort(self.table_dependencies)

        logger.debug("\nSorted Order:")
        logger.debug(self.ordered_tables)

    def _topological_sort(self, dependencies_dict):
        """
        Implements Kahn's algorithm for topological sorting.

        Args:
            dependencies_dict (dict): Dictionary mapping entities to their
            dependencies.

        Returns:
            list: Entities sorted in dependency order, with no-dependency
            entities first.

        Raises:
            ValueError: If a cycle is detected in the dependency graph.
        """
        # Create a complete set of all entities (including those that appear
        # only as dependencies)
        all_entities = set(dependencies_dict.keys())
        for deps in dependencies_dict.values():
            all_entities.update(deps)

        # Build the adjacency graph and in-degree counts
        graph = {entity: set() for entity in all_entities}
        in_degree = {entity: 0 for entity in all_entities}

        # Populate the graph with dependencies
        for entity, deps in dependencies_dict.items():
            for dep in deps:
                # Entity depends on dep, so there's an edge from dep to entity
                graph[dep].add(entity)
                in_degree[entity] += 1

        # Start with all nodes that have no dependencies (in-degree of 0)
        queue = [
            entity for entity, degree in in_degree.items() if degree == 0
        ]
        sorted_result = list()

        # Process the queue
        while queue:
            # Take a node with no dependencies
            current = queue.pop(0)
            sorted_result.append(current)

            # Remove this node's outgoing edges
            for dependent in graph[current]:
                in_degree[dependent] -= 1
                # If this node now has no dependencies, add it to the queue
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check if we have a cycle (if we couldn't process all nodes)
        if len(sorted_result) != len(all_entities):
            # Use networkx to find a cycle
            nx_graph = nx.DiGraph(graph)
            try:
                cycle = nx.find_cycle(nx_graph)
            except nx.NetworkXNoCycle:
                # No cycle found, which is unexpected at this point
                logger.debug(
                    "Warning: Inconsistency - No cycle found despite "
                    "unprocessed nodes"
                )
                # Handle remaining nodes (those involved in cycles)
                remaining = all_entities - set(sorted_result)
                sorted_result.extend(remaining)
                return sorted_result

            cycle_entities = [edge[0] for edge in cycle]
            error_message = f"Error: Cyclical dependency detected!\n\n"
            error_message += "The following entities form a cycle:\n\n"
            for i, entity in enumerate(cycle_entities):
                error_message += f"{i + 1}. {entity}\n"
            error_message += "\nPlease manually resolve the cycle and " \
                             "regenerate the topological sort.\n"
            raise ValueError(error_message)

        return sorted_result

    def setup_vector_model(self):
        """
        Set up the sentence transformer model and prepare Faker embeddings
        for intelligent provider selection.
        """
        # Vectorization using Sentence Transformers
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Create Faker name embeddings
        self.faker_names = []

        # Dynamically discover and collect methods from all providers
        for provider in self.fake.get_providers():
            for name in dir(provider):
                try:
                    # Get the callable attribute
                    attr = getattr(provider, name)
                    # logger.debug(f"Faker name: {name}")

                    if not name.startswith("_") and callable(attr):
                        # Inspect the number of parameters
                        sig = inspect.signature(attr)
                        if all(
                                param.default != inspect.Parameter.empty or param.kind == inspect.Parameter.VAR_POSITIONAL
                                for param in sig.parameters.values()
                        ):
                            try:
                                test_result = attr()
                                if not isinstance(test_result, list) and not isinstance(test_result,
                                                                                        tuple) and not isinstance(
                                    test_result, dict):
                                    self.faker_names.append(name)
                            except:
                                continue
                except (TypeError, ValueError):
                    # Skip attributes that raise errors
                    continue

        self.faker_embeddings = self.model.encode(self.faker_names, convert_to_tensor=True)

        # Create a dictionary to map embeddings to Faker names
        self.faker_embedding_map = {
            tuple(embedding.tolist()): name
            for embedding, name in zip(self.faker_embeddings, self.faker_names)
        }

    def _generate_default_value(self, data_type, max_length=None):
        """
        Generate a default value for a given data type when a custom generator fails.

        Args:
            data_type (str): The SQL data type
            max_length (int, optional): Maximum length for string types

        Returns:
            A value compatible with the specified data type
        """
        data_type = data_type.lower()
        if data_type in ["integer", "smallint", "bigint", "int"]:
            return 0
        elif data_type in ["numeric", "decimal", "real", "double precision"]:
            return 0.0
        elif data_type in ["boolean"]:
            return False
        elif data_type in ["text", "varchar", "character varying", "char"]:
            value = "default"
            if max_length and len(value) > max_length:
                return value[:max_length]
            return value
        elif data_type in ["uuid"]:
            return self.fake.unique.uuid4()
        elif data_type.startswith("date") or data_type.startswith("timestamp"):
            return self.fake.unique.date_time_between(start_date="-30y", end_date="now")
        elif data_type in ["json", "jsonb"]:
            return "{}"
        else:
            return None

    def _handle_foreign_key(self, fk_info, table_key, column, is_nullable, values):
        """Handle foreign key constraints when generating data."""
        fk_schema, fk_table, fk_column = fk_info.get('foreign_table_schema'), fk_info.get(
            'foreign_table_name'), fk_info.get('foreign_column_name')
        fk_table_key = f"{fk_schema}.{fk_table}"

        if fk_table_key in self.inserted_pks and self.inserted_pks[fk_table_key]:
            values.append(random.choice(self.inserted_pks[fk_table_key]))
        else:
            # If no primary keys exist, set value to NULL if allowed, otherwise try to create one
            if is_nullable == 'YES':
                values.append(None)
            else:
                raise SkipRowGenerationError(
                    f"Warning: Required FK {table_key}.{column} references {fk_table_key}.{fk_column} but no values exist")  # This might cause an error if NOT NULL constraint exists

    def _generate_column_value(self, table_key, column, data_type, _column_default, is_nullable,
                               character_maximum_length, num_precision, num_scale, values):
        """Generate an appropriate value for a database column based on its type."""
        try:
            cache_key = (table_key, column)
            if cache_key in self.faker_func_cache:
                faker_func = self.faker_func_cache[cache_key]
            else:
                # Retrieve table and column descriptions from the database
                schema, table_name = table_key.split('.')

                # Combine table name and column name for context
                context_name = f"{column} {table_name}"

                column_embedding = self.model.encode(context_name, convert_to_tensor=True)
                cosine_scores = util.cos_sim(column_embedding, self.faker_embeddings)
                best_match_index = cosine_scores.argmax()
                best_match_embedding = tuple(self.faker_embeddings[best_match_index].tolist())
                faker_func_name = self.faker_embedding_map[best_match_embedding]
                faker_func = getattr(self.fake.unique, faker_func_name)
                self.used_faker_funcs.add((table_key, column, faker_func_name))

                # Add this line to store the function in the cache
                self.faker_func_cache[cache_key] = faker_func

            self._generate_by_data_type(
                data_type, faker_func, is_nullable, character_maximum_length,
                num_precision, num_scale, values, fully_qualified_column_name=f"{table_key}.{column}"
            )
        except Exception as e:
            logger.debug(f"Error generating value for column '{column}' with type '{data_type}': {e}")
            self._handle_generation_error(is_nullable, character_maximum_length, values)

    def _get_table_description(self, schema, table_name):
        """Retrieve the description of a table."""
        try:
            query = """
                SELECT description
                FROM pg_description
                JOIN pg_class ON pg_description.objoid = pg_class.oid
                JOIN pg_namespace ON pg_class.relnamespace = pg_namespace.oid
                WHERE pg_class.relname = %s
                AND pg_namespace.nspname = %s
            """
            self.tuple_cursor.execute(query, (table_name, schema))
            result = self.tuple_cursor.fetchone()
            if result and result[0]:
                return result[0]
            return None
        except Exception as e:
            logger.debug(f"Error retrieving table description for {schema}.{table_name}: {e}")
            return None

    def _get_column_description(self, schema, table_name, column_name):
        """Retrieve the description of a column."""
        try:
            query = """
                SELECT description
                FROM pg_description
                JOIN pg_attribute ON pg_description.objoid = pg_attribute.attrelid AND pg_description.objsubid = pg_attribute.attnum
                JOIN pg_class ON pg_attribute.attrelid = pg_class.oid
                JOIN pg_namespace ON pg_class.relnamespace = pg_namespace.oid
                WHERE pg_class.relname = %s
                AND pg_namespace.nspname = %s
                AND pg_attribute.attname = %s
            """
            self.tuple_cursor.execute(query, (table_name, schema, column_name))
            result = self.tuple_cursor.fetchone()
            if result and result[0]:
                return result[0]
            return None
        except Exception as e:
            logger.debug(f"Error retrieving column description for {schema}.{table_name}.{column_name}: {e}")
            return None

    def _generate_by_data_type(self, data_type, faker_func, _is_nullable,
                               character_maximum_length, num_precision, num_scale, values,
                               fully_qualified_column_name=None):
        """Generate a value based on the specific data type."""
        data_type = data_type.lower()

        if data_type in ["integer", "smallint", "bigint", "int"]:
            self._generate_integer_value(data_type, num_precision, values)
        elif data_type in ["inet"]:
            values.append(self.fake.ipv4())
        elif data_type in ["numeric", "decimal", "real", "double precision"]:
            self._generate_numeric_value(num_precision, num_scale, values)
        elif data_type in ["boolean"]:
            values.append(self.fake.pybool())
        elif data_type in ["text"] and fully_qualified_column_name and previous_responses.get(
                fully_qualified_column_name):
            prev = previous_responses.get(fully_qualified_column_name)
            value = random.choice(prev)
            values.append(value)
        elif data_type in ["varchar", "character varying", "char"]:
            try:
                self._generate_string_value(faker_func, character_maximum_length, values)
            except UniquenessException as _e:
                value = self.fake.unique.paragraph()
                if value and character_maximum_length and len(str(value)) > character_maximum_length:
                    values.append(str(value)[:character_maximum_length])
                else:
                    values.append(value)
        elif data_type in ["uuid"]:
            values.append(self.fake.unique.uuid4())
        elif data_type in ["interval"]:
            values.append(generate_random_interval_with_optional_weights())
        elif data_type.startswith("date") or data_type.startswith("timestamp"):
            values.append(self.fake.unique.date_time_between(start_date="-30y", end_date="now"))
        elif data_type in ["json", "jsonb"]:
            values.append(self.fake.unique.json())  # Random JSON data
        else:
            # Default to the chosen faker function without special handling
            value = faker_func()
            # Truncate if too long
            if value and character_maximum_length and len(str(value)) > character_maximum_length:
                values.append(str(value)[:character_maximum_length])
            else:
                values.append(value)

    def _generate_integer_value(self, data_type, num_precision, values):
        """Generate an integer value based on the specific integer type."""
        if data_type == "smallint":
            values.append(self.fake.random_int(min=0, max=min(32767, 10 ** (num_precision or 5) - 1)))
        elif data_type == "bigint":
            values.append(self.fake.random_int(min=0, max=min(9223372036854775807, 10 ** (num_precision or 19) - 1)))
        else:  # integer or int
            values.append(self.fake.random_int(min=0, max=min(2147483647, 10 ** (num_precision or 10) - 1)))

    def _generate_numeric_value(self, num_precision, num_scale, values):
        """Generate a numeric value with appropriate precision and scale."""
        # Calculate the maximum value based on precision and scale
        max_value = 10 ** (num_precision - num_scale) - 1

        # Debug logging
        # logger.debug(f"num_precision={num_precision}, num_scale={num_scale}, max_value={max_value}")

        # Generate integer part within the max value
        int_part = self.fake.random_int(min=0, max=max_value)

        # Debug logging for int_part
        # logger.debug(f"int_part={int_part}")

        if num_scale and num_scale > 0:
            # Generate the decimal part with the right number of digits
            decimal_part = self.fake.random_int(min=0, max=10 ** num_scale - 1)

            # Debug logging for decimal_part
            # logger.debug(f"decimal_part={decimal_part}")

            # Format with leading zeros for proper scale
            decimal_str = str(decimal_part).zfill(num_scale)

            # Combine integer and decimal parts
            full_value = float(f"{int_part}.{decimal_str}")

            # Debug logging for full value
            # logger.debug(f"full_value={full_value}")

            values.append(full_value)
        else:
            values.append(int_part)

        # Debug logging to show final values list
        # logger.debug(f"values list length={len(values)}, last value={values[-1]}")

    def _generate_string_value(self, faker_func, character_maximum_length, values):
        """Generate a string value, respecting maximum length."""
        value = faker_func()

        # If value is a list of tuples, get the first tuple's second item (generator) and call it
        if isinstance(value, list) and value and isinstance(value[0], tuple):
            value = value[0][1]()
        elif isinstance(value, list) and value and isinstance(value[0], str):
            value = ' '.join(value)

        value = str(value)

        # Truncate if too long
        if value and character_maximum_length and len(str(value)) > character_maximum_length:
            values.append(str(value)[:character_maximum_length])
        else:
            values.append(value)

    def _handle_generation_error(self, is_nullable, character_maximum_length, values):
        """Handle errors during value generation."""
        # If nullable, set to NULL, otherwise try something generic
        if is_nullable == 'YES':
            values.append(None)
        else:
            # For required columns, try a simple string as fallback
            value = str(self.fake.word())
            if value and character_maximum_length and len(str(value)) > character_maximum_length:
                values.append(str(value)[:character_maximum_length])
            else:
                values.append(value)

    def _insert_row(self, table_key, column_names, values):
        """
        Add row to batch instead of inserting immediately.

        Args:
            table_key (str): The table identifier in the format "schema.table"
            column_names (list): List of column names for this row
            values (list): List of values corresponding to the column names
        """
        self._batch_row(table_key, column_names, values)

    def _store_primary_key(self, table_key, inserted_row):
        """
        Store the primary key value of the inserted row for foreign key references.
        Works with any type of primary key (serial, UUID, composite, etc.)

        Args:
            table_key (str): The table identifier in the format "schema.table"
            inserted_row (tuple): The row returned by the INSERT ... RETURNING * statement
        """
        schema, table = table_key.split('.')

        try:
            # Get the primary key column name(s) for this table
            pk_query = """
                SELECT kcu.column_name 
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                    AND tc.table_schema = %s
                    AND tc.table_name = %s
                ORDER BY kcu.ordinal_position
            """
            pk_cursor = self.conn.cursor(cursor_factory=extensions.cursor)
            pk_cursor.execute(pk_query, (schema, table))
            pk_columns = [row[0] for row in pk_cursor.fetchall()]
            pk_cursor.close()

            if not pk_columns:
                logger.debug(f"No primary key found for table {table_key}")
                return

            # Get the column names from the INSERT query
            query_cursor = self.conn.cursor(cursor_factory=extensions.cursor)
            query_cursor.execute(f'SELECT * FROM "{schema}"."{table}" WHERE FALSE')
            column_names = [desc.name for desc in query_cursor.description]
            query_cursor.close()

            # Find the indices of primary key columns in the returned row
            pk_values = []
            missing_pk_columns = []

            for pk_col in pk_columns:
                try:
                    # Find this primary key column in the list of all columns
                    if pk_col in column_names:
                        idx = column_names.index(pk_col)

                        # Check if this PK column is in our inserted data
                        if idx < len(inserted_row):
                            pk_values.append(inserted_row[idx])
                        else:
                            missing_pk_columns.append(pk_col)
                    else:
                        missing_pk_columns.append(pk_col)
                except ValueError:
                    missing_pk_columns.append(pk_col)

            if missing_pk_columns:
                logger.debug(f"Could not find these PK columns in result: {missing_pk_columns}")
                logger.debug(f"Available columns: {column_names}")
                logger.debug(f"Inserted row length: {len(inserted_row)}")
                logger.debug(f"Inserted row data sample: {inserted_row[:3]}...")
                return

            # For composite keys, store the tuple of values
            pk_value = tuple(pk_values) if len(pk_values) > 1 else pk_values[0]

            # Store the primary key for future reference
            if table_key not in self.inserted_pks:
                self.inserted_pks[table_key] = []

            self.inserted_pks[table_key].append(pk_value)
            # logger.debug(f"Stored PK for {table_key}: {pk_value} (columns: {pk_columns})")

        except Exception as e:
            logger.debug(f"Error storing primary key for {table_key}: {e}")

            # Additional error info
            logger.debug(f"Table: {table_key}")
            logger.debug(f"Inserted row data: {inserted_row}")

            # This is a problem with the RETURNING clause - log the issue
            if hasattr(self.cur, 'description') and self.cur.description:
                logger.debug(f"Current cursor description: {[desc.name for desc in self.cur.description]}")

            # Log our inserted columns for comparison
            if table_key in self.batch_data and 'column_names' in self.batch_data[table_key]:
                logger.debug(f"Columns we tried to insert: {self.batch_data[table_key]['column_names']}")

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            if self.cur:
                self.cur.close()
            self.conn.close()
            logger.debug("Database connection closed.")

    def generate_vectorized_data(self, row_counts=None, commit_frequency=10, scale=1):
        """
        Main method to orchestrate the entire data generation process with performance tracking.

        Args:
            row_counts (dict, optional): A dictionary mapping table names to row counts.
            commit_frequency (int, optional): Number of tables to process before committing.
            scale: multiplier for row_counts

        Returns:
            int: Total number of rows generated
        """
        total_start_time = time.time()
        total_rows = 0

        try:
            # Connect to the database
            if not self.connect_to_db():
                return 0

            # Retrieve database metadata
            metadata_start = time.time()
            self.get_foreign_keys()
            self.get_columns()
            self.identify_all_generated_columns()
            self.organize_tables_and_columns()

            # Compile exclusion patterns if they exist
            if self.exclusions:
                self._compile_exclusion_patterns()

            self.determine_table_dependencies()
            self.sort_tables_by_dependencies()
            logger.info(f"Database metadata processing: {time.time() - metadata_start:.2f} seconds")

            # Setup vector model for intelligent data generation
            vector_start = time.time()
            self.setup_vector_model()
            logger.info(f"Vector model setup: {time.time() - vector_start:.2f} seconds")

            # Generate and insert data
            insert_start = time.time()

            # Calculate total expected rows
            if row_counts:
                expected_total = sum(
                    row_counts.get(table, row_counts.get(table.split('.')[1], 100)) * scale
                    for table in self.ordered_tables
                )
            else:
                expected_total = len(self.ordered_tables) * 100

            logger.info(f"Starting data generation for approximately {expected_total} rows...")

            # Generate the data
            self.generate_data(row_counts, commit_frequency, scale)

            # Get actual total rows by summing table counts
            for table_key in self.ordered_tables:
                schema, table = table_key.split('.')
                try:
                    self.tuple_cursor.execute(f'SELECT COUNT(*) FROM "{schema}"."{table}"')
                    result = self.tuple_cursor.fetchone()
                    if result and result[0]:
                        total_rows += result[0]
                except psycopg2.Error as e:
                    logger.debug(f"Error counting rows in {table_key}: {e}")

            self._log_performance_stats("Data generation and insertion", total_rows, insert_start)
            logger.debug(f"\n\nPopulated these tables: {self.populated_tables}")
            logger.debug(f"\n\nUsed faker funcs: {self.used_faker_funcs}")
            logger.debug(f"\n\nNot populated tables: {self.not_populated_tables}")

        except Exception as e:
            logger.error(f"Error during data generation: {e}")
        finally:
            self.close_connection()

        # Log overall performance
        total_duration = time.time() - total_start_time
        logger.info(f"Total execution time: {total_duration:.2f} seconds")
        if total_rows > 0:
            logger.info(f"Overall performance: {total_rows / total_duration:.2f} rows/second")

        return total_rows


# Example usage:
if __name__ == "__main__":
    conn_params = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "password",
        "port": "32100"
    }

    # Example with table-specific row counts (using schema.table format):
    row_counts = {
        "public.users": 1000,
        "public.products": 500,
        "public.orders": 2000,
        "sales.transactions": 5000
    }

    # Example 1: Generate data for all non-system schemas
    generator = DataGenerator(conn_params)
    generator.generate_vectorized_data(row_counts=row_counts)

    # Example 2: Generate data with wildcard exclusions
    exclusions = [
        ('*', 'created_at'),  # Skip 'created_at' column in all tables
        ('users', '*'),  # Skip entire 'users' table in all schemas
        ('public.products', 'sku'),  # Skip 'sku' column in public.products
        ('sales.*', '*')  # Skip all tables in the 'sales' schema
    ]
    generator = DataGenerator(conn_params, exclusions=exclusions)
    generator.generate_vectorized_data(row_counts=row_counts)

    # Example 3: Generate data for specific schemas with exclusions
    generator = DataGenerator(
        conn_params,
        schemas=['public', 'customer'],
        exclusions=[
            ('public.users', 'email'),
            ('*', 'password'),
            ('customer.*', '*')  # Skip all tables in customer schema
        ]
    )
    generator.generate_vectorized_data()

    # Example 4: Generate data for all schemas except specific ones
    excluded_schemas = ['pg_catalog', 'information_schema', 'analytics']
    generator = DataGenerator(conn_params, exclude_schemas=excluded_schemas)
    generator.generate_vectorized_data()


    # Example 5: Default row counts (100 rows per table)
    # generator = DataGenerator(conn_params, schemas=['public'])
    # generator.generate_vectorized_data()

    # Example of custom generators
    def full_name_generator(row_values, _table, _column):
        # Generate a full name from first_name and last_name
        if 'first_name' in row_values and 'last_name' in row_values:
            return f"{row_values['first_name']} {row_values['last_name']}"
        return "Unknown"


    def email_generator(row_values, _table, _column):
        # Generate an email based on first_name and last_name
        if 'first_name' in row_values and 'last_name' in row_values:
            first = row_values['first_name'].lower()
            last = row_values['last_name'].lower()
            return f"{first}.{last}@example.com"
        return "unknown@example.com"


    def total_price_generator(row_values, _table, _column):
        # Calculate total price from price and quantity
        if 'price' in row_values and 'quantity' in row_values:
            return float(row_values['price']) * int(row_values['quantity'])
        return 0.0


    # Define custom generators
    custom_gens = [
        ('.*\\.users', 'full_name', full_name_generator),
        ('.*\\.users', 'email', email_generator),
        ('.*\\.order_items', 'total_price', total_price_generator)
    ]

    # Create generator with custom generators
    generator = DataGenerator(
        conn_params,
        schemas=['public'],
        custom_generators=custom_gens
    )
    generator.generate_vectorized_data()
