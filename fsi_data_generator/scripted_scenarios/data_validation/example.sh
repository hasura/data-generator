#!/bin/bash

# Constants with defaults, overridable by environment variables
queryPort="${QUERY_PORT:-3280}"                         # Default: 3280 (Can override with $QUERY_PORT)
filePort="${FILE_PORT:-8787}"                           # Default: 8787 (Can override with $FILE_PORT)
host="${HOST:-http://localhost}"                        # Default: http://localhost (Can override with $HOST)
operationName="${OPERATION_NAME:-mortgage_demo}"        # Default: mortgage_demo (Can override with $OPERATION_NAME)

# File paths with default values, overridable by environment variables
gqlFile="${GQL_FILE:-mortgage.gql}"                     # Default: mortgage.gql (Can override with $GQL_FILE)
schemaFile="${SCHEMA_FILE:-mortgage_schema.json}"       # Default: mortgage_schema.json (Can override with $SCHEMA_FILE)
queryResponseFile="${RESPONSE:-query_response.json}"    # Default: query_response.json (Can override with $RESPONSE)

# Optional variables dictionary passed as JSON (empty by default)
variablesJson="${VARIABLES_JSON:-null}"  # If not set, it defaults to "null" (excluded when constructing JSON)

# URLs
queryUrl="${host}:${queryPort}/graphql"
fileUrl="${host}:${filePort}/files/${operationName}.json"
outputFile="${operationName}.json"

echo "Query URL: $queryUrl"
echo "File URL: $fileUrl"
echo "GraphQL File: $gqlFile"
echo "Schema File: $schemaFile"
echo "Operation Name: $operationName"
echo "Variables JSON: ${variablesJson}"
echo "Query Response File: ${queryResponseFile}"

# Construct the JSON dynamically depending on whether VARIABLES_JSON was provided
if [[ "$variablesJson" != "null" && -n "$variablesJson" ]]; then
    # Include 'variables' key if VARIABLES_JSON is set
    payload=$(jq -n --arg query "$(cat "$gqlFile")" \
                     --arg opName "$operationName" \
                     --argjson variables "$variablesJson" \
                     '{query: $query, operationName: $opName, variables: $variables}')
else
    # Exclude 'variables' key if VARIABLES_JSON is not set
    payload=$(jq -n --arg query "$(cat $gqlFile)" \
                     --arg opName "$operationName" \
                     '{query: $query, operationName: $opName}')
fi

# Send the GraphQL query and save the response
echo "Query URL: '$queryUrl'"
echo "Sending GraphQL query..."
curl -X POST \
     -H "Content-Type: application/json" \
     -H "json-schema: $(jq -c . "$schemaFile")" \
     -H "validate-options: db,allerrors,verbose" \
     -H "x-hasura-user: admin" \
     --data-binary "$payload" \
     --output "$queryResponseFile" "$queryUrl"

echo "GraphQL query response saved to $queryResponseFile"

# Initialize the polling variables
maxRetries=12    # Poll for up to 1 minute (12 retries with a 5-second interval)
retryInterval=5  # Interval between retries in seconds
attempt=1

# Poll for the file
echo "Polling for the file: $fileUrl"
while (( attempt <= maxRetries )); do
    if curl --head --silent --fail "$fileUrl" > /dev/null; then
        echo "File found! Downloading..."
        curl -o "$outputFile" "$fileUrl"
        echo "Downloaded file saved as $outputFile"
        exit 0  # Exit successfully
    fi
    echo "File not found. Retrying in $retryInterval seconds... (Attempt: $attempt/$maxRetries)"
    sleep $retryInterval
    ((attempt++))
done

# If the loop completes without finding the file:
echo "Error: File not found after $((maxRetries * retryInterval)) seconds."
exit 1  # Exit with an error
