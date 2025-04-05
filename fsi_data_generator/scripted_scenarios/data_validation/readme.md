# Data Validation Demo Setup

This repository contains tools and scripts to demonstrate schema validation and cross-schema data quality rule enforcement in Hasura DDN transactions. It uses JSON Schema validation to enforce complex business rules across multiple domains of data.

## Overview

The demo showcases how to implement and validate data quality rules across related schemas:

1. **Cross-schema validation** - Enforcing data relationships between multiple domains
2. **Complex conditional rules** - Testing rules like "if loan term > 20 years, property must be built 1950 or later"
3. **Temporal validation** - Ensuring date-based constraints like "origination date must be after submission date"

## Prerequisites

- PostgreSQL database (username: "postgres", password: "password")
- Node.js environment with jq installed
- curl for API requests
- Hasura data validation plugin running on port 8787 (from [Hasura Plugin Hub](https://github.com/hasura/plugin-hub))
- Python environment for running the data generator

## Repository Contents

### Transaction Files
- `applications/application.gql` - Query for application management data with nested enterprise data
- `mortgages/mortgage.gql` - Query for mortgage services with nested application and property data

### JSON Schema Validation Files
- `applications/application_schema.json` - Schema enforcing data quality rules for applications:
  - Rule 1: Application owner must exist and be an object
  - Rule 2: Application that are in PRODUCTION the owner must have ACTIVE status and be an EMPLOYEE
  - Rule 3: Owner's department must match application's department

- `mortgages/mortgage_schema.json` - Schema enforcing data quality rules for mortgage loans:
  - Each application must have exactly one property
  - At least 5 loan records required
  - If loan term > 20 years (240 months), property must be built 1950 or later
  - Loan origination date must be on or after application submission date

### Demo Scripts
- `example.sh` - Main script for executing queries with JSON Schema validation
- `applications/application.sh` - Configuration for running the application data validation demo
- `mortgages/mortgage.sh` - Configuration for running the mortgage data validation demo

### Test Data
- `mortgages/mortgage_validation.sql` - SQL script to generate test data, including deliberate rule violations:
  - A property from 1940 paired with a 30-year loan (violates the post-1950 rule)
  - A loan with origination date before submission date
  - An application with no associated properties

## Setup Instructions

1. **Set up the database:**
   ```bash
   # Start PostgreSQL with default credentials (postgres/password)
   # Then generate and load test data
   python main.py
   ```
   
   > Note: The data generator automatically applies all the necessary SQL files (including mortgage_validation.sql) to set up the test data. No need to manually execute SQL scripts.

2. **Prepare the environment:**
   ```bash
   # Make the scripts executable
   chmod +x example.sh application.sh mortgage.sh
   ```

3. **Configure connection settings:**
   Edit `application.sh` and `mortgage.sh` if needed, but the defaults should work with the standard setup:
   - `QUERY_PORT` - Your GraphQL API port (default: 3280)
   - `FILE_PORT` - Your file server port (default: 8787 - used by the data validation plugin)
   - `HOST` - Your API host (default: http://localhost)
   
4. **Ensure the data validation plugin is running:**
   The plugin should be running on port 8787. If you haven't set it up yet:
   ```bash
   # Clone the plugin hub repository
   git clone https://github.com/hasura/plugin-hub
   
   # Follow the repository instructions to start the data validation plugin
   # The plugin should be accessible on port 8787
   ```

## Running the Demo

### Application Validation Demo

1. Run the application validation demo:
   ```bash
   ./application.sh
   ```

2. Observe the output:
   - The script will send a GraphQL query to retrieve application data
   - The JSON Schema will validate data quality rules
   - If validation passes, a valid JSON response will be returned
   - If validation fails, error messages will identify the specific violations

### Mortgage Validation Demo

1. Run the mortgage validation demo:
   ```bash
   ./mortgage.sh
   ```

2. Observe the output:
   - The script will check complex validation rules
   - Expected violations include:
     - Property from 1940 with 30-year loan (violating the 1950+ rule)
     - Origination date before submission date
     - Missing property for application #6

## Customizing the Demo

You can customize the demo by:

1. Modifying the `.gql` files to query different data or add additional fields
2. Updating the schema files to implement your own custom data quality rules
3. Changing the environment variables in the `.sh` files to test different scenarios

## Troubleshooting

- If you encounter "Permission denied" errors, ensure the scripts have proper execute permissions
- For connection errors, verify the `QUERY_PORT`, `FILE_PORT`, and `HOST` settings
- For schema validation errors, check the response for detailed error messages that explain which rules were violated

See `demo.md` for a detailed walkthrough of presenting this demo to stakeholders.
