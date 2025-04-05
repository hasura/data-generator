#!/bin/bash

# Set environment variables to their default values
export QUERY_PORT="3280"
export FILE_PORT="8787"
export HOST="http://localhost"
export OPERATION_NAME="application_ownership_analysis"
export GQL_FILE="application.gql"
export SCHEMA_FILE="application_schema.json"
export VARIABLES_JSON="null"

# Print the environment variables for confirmation
echo "Using environment variables:"
echo "QUERY_PORT: $QUERY_PORT"
echo "FILE_PORT: $FILE_PORT"
echo "HOST: $HOST"
echo "OPERATION_NAME: $OPERATION_NAME"
echo "GQL_FILE: $GQL_FILE"
echo "SCHEMA_FILE: $SCHEMA_FILE"
echo "VARIABLES_JSON: $VARIABLES_JSON"

# Call the main script
../example.sh
