#!/bin/bash
#
# Script to initialize Hasura DDN project with specified subgraphs
# Requires Bash 4.0+ for associative arrays and mapfile.
# Current time: Saturday, May 3, 2025 at 9:05:11 AM EDT. Location: Charlotte, North Carolina, United States.
#
# Example Usage:
# Provide URI explicitly (preferred):
#   bash ./your_script_name.sh \
#     -u "postgres://user:password@host:port/db" \
#     -s "consumer_banking,security"
#
# Omit URI on EC2 with public hostname (will attempt auto-detection with defaults):
#   bash ./your_script_name.sh -s "consumer_banking,security"
#
# Process ALL subgraphs with auto-detected URI:
#   bash ./your_script_name.sh
#
# Specify project name, custom URLs, but auto-detect URI:
#   bash ./your_script_name.sh \
#     -s "consumer_banking,security" \
#     -P "my-custom-project" \
#     -v "http://my-validate-service:8080/validate" \
#     -f "http://my-file-service:8080/file-out" \
#     -p "http://my-profile-service:8080/profile" \
#     -x "http://my-fdx-service:9000"
#

# --- Function to display usage ---
usage() {
  # Updated usage string to include -P
  echo "Usage: $0 [-u <postgres_connection_uri>] [-P <project_name>] [-s <subgraph_list>] [-v <validate_url>] [-f <file_output_url>] [-p <profile_url>] [-x <fdx_url>]"
  # Modified -u description to indicate it's now semi-optional with auto-detect
  echo "  -u : PostgreSQL connection URI. If omitted on EC2, attempts auto-detection using public hostname."
  echo "       Example: postgres://user:password@host:port/database"
  # --- Project Name Argument ---
  echo "  -P : Optional. The Hasura DDN project name."
  echo "       Default: fsi"
  echo "  -s : Optional. Comma-separated list of subgraphs to process."
  echo "       If omitted, ALL available subgraphs will be processed."
  echo "       Available: consumer_banking, consumer_lending, mortgage_services, credit_cards,"
  echo "                  small_business_banking, enterprise, security, app_mgmt, data_quality"
  echo "       Example: consumer_banking,security,data_quality"
  # --- Optional URL Arguments ---
  echo "  -v : Optional. Validate URL."
  echo "       Default: http://local.hasura.dev:8787/validate"
  echo "  -f : Optional. File Output URL."
  echo "       Default: http://local.hasura.dev:8787/file-out"
  echo "  -p : Optional. Profile URL."
  echo "       Default: http://local.hasura.dev:8787/profile"
  echo "  -x : Optional. FDX URL."
  echo "       Default: http://local.hasura.dev:3000"
  exit 1
}

# --- Initialize variables ---
PG_CONNECTION_URI=""
SUBGRAPH_LIST_CSV="" # Will store value from -s if provided

# --- Initialize Optional Variables with Defaults ---
PROJECT_NAME_ARG="fsi" # Default project name
VALIDATE_URL_ARG="http://local.hasura.dev:8787/validate"
FILE_OUTPUT_URL_ARG="http://local.hasura.dev:8787/file-out"
PROFILE_URL_ARG="http://local.hasura.dev:8787/profile"
FDX_URL_ARG="http://local.hasura.dev:3000"

# --- Parse Command Line Arguments ---
# Updated getopts string to include P (requires argument)
while getopts ":hu:P:s:v:f:p:x:" opt; do
  case ${opt} in
    h ) usage ;;
    u ) PG_CONNECTION_URI="$OPTARG" ;;
    P ) PROJECT_NAME_ARG="$OPTARG" ;;      # Override default project name
    s ) SUBGRAPH_LIST_CSV="$OPTARG" ;;     # Store the provided list
    v ) VALIDATE_URL_ARG="$OPTARG" ;;      # Override default URL
    f ) FILE_OUTPUT_URL_ARG="$OPTARG" ;;   # Override default URL
    p ) PROFILE_URL_ARG="$OPTARG" ;;      # Override default URL
    x ) FDX_URL_ARG="$OPTARG" ;;         # Override default URL
    \? ) echo "Invalid Option: -$OPTARG" 1>&2; usage ;;
    : ) # Handle missing argument for options that require one (like -u if flag is present but value is missing)
        # If the missing argument is for -u, we let the auto-detection logic handle it later.
        # For other options, it's an error.
        if [ "$OPTARG" == "u" ]; then
          # Let the subsequent check handle the missing -u value
          echo "Info: -u flag provided without value, will attempt auto-detection."
        else
          echo "Invalid Option: -$OPTARG requires an argument" 1>&2; usage
        fi
         ;;
  esac
done
shift $((OPTIND -1)) # Shift off the options

# --- Check if PG URI was provided OR attempt EC2 auto-detection ---
if [ -z "${PG_CONNECTION_URI}" ]; then
    echo "--- PostgreSQL connection URI (-u) not provided. Attempting EC2 auto-detection... ---"

    # Check if curl is available
    if ! command -v curl &> /dev/null; then
         echo "Error: 'curl' command not found, cannot auto-detect EC2 hostname."
         echo "Error: PostgreSQL connection URI (-u) is mandatory if not running on EC2 or if 'curl' is unavailable."
         usage
    fi

    # Attempt to get EC2 public hostname using IMDS (try v2 then v1)
    public_hostname=""
    # Try getting a token (suppress stderr for timeout cases on non-EC2, short timeout)
    echo "Attempting to fetch IMDSv2 token..."
    token=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60" --connect-timeout 2 --silent --show-error 2>/dev/null)

    if [ -n "$token" ]; then
        # Got a token (likely EC2 with IMDSv2), try getting public hostname
        echo "Using IMDSv2 to fetch public hostname..."
        public_hostname=$(curl -H "X-aws-ec2-metadata-token: $token" --connect-timeout 2 --silent http://169.254.169.254/latest/meta-data/public-hostname 2>/dev/null)
    else
        # Token failed, try IMDSv1 (less secure, might be disabled)
         echo "IMDSv2 token failed, trying IMDSv1 to fetch public hostname..."
        public_hostname=$(curl --connect-timeout 2 --silent http://169.254.169.254/latest/meta-data/public-hostname 2>/dev/null)
    fi

    # Check if we got a non-empty hostname
    if [ -n "$public_hostname" ]; then
        # Construct the default URI - DEFINE DEFAULTS CLEARLY
        DEFAULT_PG_USER="postgres"
        DEFAULT_PG_PASS="password"
        DEFAULT_PG_PORT="5432"
        DEFAULT_PG_DB="postgres"
        PG_CONNECTION_URI="postgres://${DEFAULT_PG_USER}:${DEFAULT_PG_PASS}@${public_hostname}:${DEFAULT_PG_PORT}/${DEFAULT_PG_DB}"
        REDACTED_URI="postgres://${DEFAULT_PG_USER}:[REDACTED]@${public_hostname}:${DEFAULT_PG_PORT}/${DEFAULT_PG_DB}"

        echo "Warning: Successfully detected EC2 public hostname: ${public_hostname}"
        echo "Warning: Using auto-detected PostgreSQL connection URI: ${REDACTED_URI}"
        echo "##########################################################################################"
        echo "Warning: Ensure default user '${DEFAULT_PG_USER}', password, port '${DEFAULT_PG_PORT}', and DB '${DEFAULT_PG_DB}'"
        echo "         are correct for your PostgreSQL instance accessible at ${public_hostname}."
        echo "##########################################################################################"
    else
        # Failed to get public hostname
        echo "Error: Could not retrieve a public hostname from EC2 Instance Metadata Service."
        echo "       This could be because the instance has no public hostname, IMDS is inaccessible/disabled,"
        echo "       or the script is not running on an EC2 instance."
        echo "Error: PostgreSQL connection URI (-u) is mandatory in this case."
        usage
    fi
    echo "--- End of EC2 auto-detection ---"
# else
    # PG_CONNECTION_URI was provided via -u, use the provided value.
fi


# --- Configuration: Define mapping from subgraph name to GraphQL prefix ---
declare -A subgraph_prefixes # Associative array for prefixes
subgraph_prefixes=(
    ["consumer_banking"]="ConsumerBanking"
    ["consumer_lending"]="ConsumerLending"
    ["mortgage_services"]="MortgageServices"
    ["credit_cards"]="CreditCards"
    ["small_business_banking"]="SmallBusinessBanking"
    ["enterprise"]="Enterprise"
    ["security"]="Security"
    ["app_mgmt"]="App_Mgmt"  # Note: Custom prefix
    ["data_quality"]="DQ"      # Note: Custom prefix
)

# --- Determine which subgraphs to process ---
declare -A requested_subgraph_set # Use a set for quick lookups of requested graphs
declare -a requested_subgraphs_ordered=() # Use an ordered array for processing loop

if [ -z "${SUBGRAPH_LIST_CSV}" ]; then
    # -s was NOT provided, process ALL known subgraphs
    echo "--- Subgraph list (-s) not provided. Processing all defined subgraphs. ---"
    # Get all keys (subgraph names) from the prefixes map
    declare -a all_subgraphs_temp=("${!subgraph_prefixes[@]}")
    # Sort keys line by line and read into array using mapfile (preferred over IFS+array=($(...)))
    mapfile -t requested_subgraphs_ordered < <(printf "%s\n" "${all_subgraphs_temp[@]}" | sort)
    # Populate the set
    for sub in "${requested_subgraphs_ordered[@]}"; do
        requested_subgraph_set["$sub"]=1
    done
else
    # -s was provided, parse the list and validate against known subgraphs
    echo "--- Parsing provided subgraph list (-s) ---"
    IFS=',' read -r -a parsed_subgraphs <<< "$SUBGRAPH_LIST_CSV"
    # Populate the set and the final ordered array, trimming whitespace, ensuring uniqueness, and validating
    for sub in "${parsed_subgraphs[@]}"; do
        # Use quoted command substitution for trimming variable assignment
        sub_trimmed="$(echo "$sub" | xargs)" # Trim leading/trailing whitespace
        if [ -n "$sub_trimmed" ]; then
             # Check if the requested subgraph is actually known/defined
             if [[ -v subgraph_prefixes["$sub_trimmed"] ]]; then
                 if [[ ! -v requested_subgraph_set["$sub_trimmed"] ]]; then # Check set for uniqueness
                     requested_subgraphs_ordered+=("$sub_trimmed") # Add to final ordered array
                     requested_subgraph_set["$sub_trimmed"]=1      # Add to set
                     echo "  Registered requested subgraph: $sub_trimmed"
                 fi
             else
                 echo "  Warning: Requested subgraph '$sub_trimmed' is unknown and will be ignored."
             fi
        fi
    done
    if [ ${#requested_subgraphs_ordered[@]} -eq 0 ]; then
        echo "Error: Provided subgraph list (-s) contained no valid/known subgraph names after parsing."
        usage # Or exit 1
    fi
fi

# Final check if any subgraphs are selected
if [ ${#requested_subgraphs_ordered[@]} -eq 0 ]; then
    echo "Error: No subgraphs selected for processing."
    exit 1
fi
echo "--- Subgraphs selected for processing: ${requested_subgraphs_ordered[*]}"


# --- Script Execution ---
echo "--- Using DDN Project Name: ${PROJECT_NAME_ARG}"
# Display connection URI carefully (Redact if auto-detected with default pass)
if [[ "$PG_CONNECTION_URI" == "postgres://postgres:postgres@"* ]]; then
    REDACTED_URI=$(echo "$PG_CONNECTION_URI" | sed 's/:postgres@/:\[REDACTED]@/')
    echo "--- Using PostgreSQL Connection URI: ${REDACTED_URI} (Auto-detected)"
else
    # Assume user-provided URI might have sensitive info, redact password part generically
    REDACTED_URI=$(echo "$PG_CONNECTION_URI" | sed -E 's#:([^/:]+)@#:[REDACTED]@#')
    echo "--- Using PostgreSQL Connection URI: ${REDACTED_URI} (Provided)"
fi
echo "--- Using Validate URL: ${VALIDATE_URL_ARG}"
echo "--- Using File Output URL: ${FILE_OUTPUT_URL_ARG}"
echo "--- Using Profile URL: ${PROFILE_URL_ARG}"
echo "--- Using FDX URL: ${FDX_URL_ARG}"

# --- Initial Setup ---
# (Assuming execution within the parent directory of 'example')
echo "--- Starting Initial Setup ---"
if [ ! -d "example" ]; then mkdir example; fi
cd example || { echo "Error: Failed to change directory to 'example'"; exit 1; }

# --- Idempotent supergraph init with retry logic ---
if [ ! -f "./supergraph.yaml" ]; then
    echo "Initializing supergraph for project '${PROJECT_NAME_ARG}'...";
    # Try the first command
    if ! ddn supergraph init . --no-subgraph --with-promptql --project-name "${PROJECT_NAME_ARG}"; then
        # If the first command failed...
        echo "Initial supergraph init failed, retrying with --with-project flag..."
        # Try the second command
        if ! ddn project init --with-project "${PROJECT_NAME_ARG}"; then
             # If the second command also failed...
             echo "Error: Failed to initialize supergraph even with --with-project flag."
             exit 1
         else
            echo "Supergraph initialized successfully using --with-project flag."
         fi
    else
      echo "Supergraph initialized successfully."
    fi
else
    echo "Supergraph file ./supergraph.yaml already exists, skipping init.";
fi


# Idempotent project setup - Use PROJECT_NAME_ARG
# Use quoted command substitution for variable assignment
current_project="$(ddn context get project 2>/dev/null)"
if [ "$current_project" != "${PROJECT_NAME_ARG}" ]; then
    echo "Setting project context to ${PROJECT_NAME_ARG}..."
    # Try setting context first, as create fails if it exists
    if ! ddn context set project "${PROJECT_NAME_ARG}"; then
        echo "Failed to set project context directly, attempting to create project '${PROJECT_NAME_ARG}'..."
        if ! ddn project create "${PROJECT_NAME_ARG}"; then
            echo "Project '${PROJECT_NAME_ARG}' might already exist, attempting to set context again..."
            ddn context set project "${PROJECT_NAME_ARG}" || { echo "Error: Failed to create or set project context '${PROJECT_NAME_ARG}'"; exit 1; }
        else
             echo "Project '${PROJECT_NAME_ARG}' created successfully."
             # Explicitly set context after creation, though 'create' might do it automatically
             ddn context set project "${PROJECT_NAME_ARG}" || { echo "Error: Failed to set project context after creating '${PROJECT_NAME_ARG}'"; exit 1; }
        fi
    else
         echo "Project context successfully set to '${PROJECT_NAME_ARG}'."
    fi
else echo "Project context '${PROJECT_NAME_ARG}' already set."; fi

# Idempotent globals copy
if [ ! -d "globals" ]; then mkdir globals; fi
# Use SOURCE_METADATA_DIR defined earlier
SCRIPTS_DIR=$(dirname "$SOURCE_METADATA_DIR") # Assumes SOURCE_METADATA_DIR is ../scripts/cross_schema_relationships
if [ -d "${SCRIPTS_DIR}/globals" ]; then
    echo "Copying globals from ${SCRIPTS_DIR}/globals ..."
    cp -r "${SCRIPTS_DIR}/globals"/* globals/;
else
    echo "Warning: Source directory ${SCRIPTS_DIR}/globals not found.";
fi


# Idempotent .env writes
echo "Updating .env files..."
# Construct env_vars array using the potentially overridden URL arguments
declare -a env_vars=(
    'M_AUTH_KEY="secret"'                             # Static secret
    "VALIDATE_URL=\"${VALIDATE_URL_ARG}\""            # Use variable (default or from -v)
    "FILE_OUTPUT_URL=\"${FILE_OUTPUT_URL_ARG}\""     # Use variable (default or from -f)
    "PROFILE_URL=\"${PROFILE_URL_ARG}\""            # Use variable (default or from -p)
    "FDX_URL=\"${FDX_URL_ARG}\""                    # Use variable (default or from -x)
)
# Loop through the dynamically constructed array
for var_line in "${env_vars[@]}"; do
    grep -qxF "$var_line" .env || echo "$var_line" >> .env
    grep -qxF "$var_line" .env.cloud || echo "$var_line" >> .env.cloud
done
echo "--- Initial Setup Complete ---"
echo

# --- Loop through *selected* subgraphs to initialize, configure, and copy metadata ---
echo "--- Processing Selected Subgraphs ---"
declare -A processed_subgraph_set # Use a set to track successfully processed graphs
processed_count=0 # Initialize count of successfully processed subgraphs

# Check if the source metadata directory exists before the loop
metadata_source_exists=false
# Use SOURCE_METADATA_DIR defined earlier
if [ -d "$SOURCE_METADATA_DIR" ]; then
    metadata_source_exists=true
else
     echo "Warning: Source metadata directory not found: $SOURCE_METADATA_DIR. Will skip copying relationship files."
fi


for subgraph_name in "${requested_subgraphs_ordered[@]}"; do
    # We already filtered requested_subgraphs, so we know it's in subgraph_prefixes
    graphql_prefix="${subgraph_prefixes["$subgraph_name"]}"
    echo "--> Processing subgraph: ${subgraph_name} (Prefix: ${graphql_prefix})"
    subgraph_processed_successfully=false # Flag for this specific subgraph

    # --- Perform ddn actions for this subgraph ---
    # Use subshell for sequence of commands for a subgraph; exit subshell on error
    ( set -e # Exit subshell immediately if a command exits with a non-zero status
        if [ ! -d "${subgraph_name}" ]; then echo "Initializing subgraph directory: ${subgraph_name}"; ddn subgraph init "${subgraph_name}"; else echo "Directory ${subgraph_name} already exists, skipping init."; fi
        if ! grep -q "name: ${subgraph_name}" ./supergraph.yaml 2>/dev/null; then echo "Adding subgraph ${subgraph_name} to supergraph..."; ddn subgraph add --subgraph "${subgraph_name}/subgraph.yaml" --target-supergraph ./supergraph.yaml; else echo "Subgraph ${subgraph_name} seems already added to supergraph.yaml, skipping add."; fi
        echo "Setting context and running codemod for ${subgraph_name}..."; ddn context set subgraph "${subgraph_name}/subgraph.yaml"; ddn codemod rename-graphql-prefixes --graphql-type-name "${graphql_prefix}_"
        # Check for compose.yaml before attempting to init connector (safer if file might not exist yet)
        if [ ! -f "./compose.yaml" ]; then echo "Creating missing compose.yaml file..."; touch ./compose.yaml; fi # Ensure compose.yaml exists
        if ! grep -q "container_name: ${subgraph_name}" ./compose.yaml 2>/dev/null; then echo "Initializing connector for ${subgraph_name}..."; ddn connector init "${subgraph_name}" --hub-connector hasura/postgres --add-env CONNECTION_URI="${PG_CONNECTION_URI}" --add-to-compose-file ./compose.yaml; else echo "Connector for ${subgraph_name} seems already present in compose.yaml, skipping init."; fi
        echo "Introspecting connector, adding models/relationships for ${subgraph_name}..."; ddn connector introspect "${subgraph_name}"; ddn model add "${subgraph_name}" "${subgraph_name}*"; ddn relationship add "${subgraph_name}" "*"
        # Use PROJECT_NAME_ARG when creating the project subgraph association
        echo "Creating/associating project subgraph ${subgraph_name} with project '${PROJECT_NAME_ARG}'...";
        ddn project subgraph create "${subgraph_name}" || echo "Warning: Subgraph '${subgraph_name}' might already exist in project '${PROJECT_NAME_ARG}' or failed to create/associate."
    )

    # Check the exit status of the subshell
    if [ $? -eq 0 ]; then
        echo "--> DDN commands for subgraph ${subgraph_name} completed successfully."
        processed_subgraph_set["$subgraph_name"]=1 # Mark as successfully processed
        subgraph_processed_successfully=true
        ((processed_count++)) # Increment overall success count

        # --- Copy relevant cross-schema relationships INTO this subgraph (if source dir exists) ---
        if [[ "$metadata_source_exists" = true ]]; then
            echo "    Checking for cross-schema relationships to copy into ${subgraph_name}/metadata..."
            copied_count_for_subgraph=0
            shopt -s nullglob
            for filepath in "${SOURCE_METADATA_DIR}/"*.relationships.hml; do
                filename=$(basename "$filepath")
                base_name="${filename%.relationships.hml}" # e.g., subgraphA__subgraphB

                if [[ "$base_name" == *__* ]]; then
                    subgraphA="${base_name%%__*}"
                    subgraphB="${base_name#*__}"

                    # Check if the current subgraph is the FIRST part of the filename
                    # AND the SECOND part was requested.
                    if [[ "$subgraphA" == "$subgraph_name" && -v requested_subgraph_set["$subgraphB"] ]]; then
                         # We know subgraphA (current subgraph_name) was processed successfully because we are inside this if block.
                         dest_dir="${subgraph_name}/metadata/"
                         mkdir -p "$dest_dir" # Ensure metadata dir exists
                         echo "      Copying ${filename} (defines relationships from ${subgraphA} to ${subgraphB}) to ${dest_dir}"
                         cp "$filepath" "$dest_dir"
                         ((copied_count_for_subgraph++))
                    fi
                fi
            done
            shopt -u nullglob
            if [[ "$copied_count_for_subgraph" -gt 0 ]]; then
                 echo "    Copied ${copied_count_for_subgraph} relationship file(s) into ${subgraph_name}/metadata."
            else
                 echo "    No relevant relationship files found to copy into ${subgraph_name}/metadata."
            fi
        fi # end check for metadata_source_exists

        echo # Add blank line after processing a subgraph
    else
        echo "Error processing subgraph ${subgraph_name}. Skipping subsequent steps for this subgraph."
        echo
    fi
done

# Check if ANY subgraphs were successfully processed
if [ "$processed_count" -eq 0 ]; then echo "Error: No subgraphs were successfully processed."; exit 1; fi
echo "--- Subgraph Processing Complete (${processed_count} successfully processed) ---"
echo

# --- Final Steps ---
echo "--- Running Final Steps ---"
# Use SCRIPTS_DIR derived earlier
SOURCE_CONFIG_SAMPLE="${SCRIPTS_DIR}/promptql_config.yaml.sample"
DEST_CONFIG="promptql_config.yaml"

# Always overwrite destination if source sample exists
if [ -f "$SOURCE_CONFIG_SAMPLE" ]; then
    echo "Copying $SOURCE_CONFIG_SAMPLE to $DEST_CONFIG (overwriting)..."
    cp "$SOURCE_CONFIG_SAMPLE" "$DEST_CONFIG"
else
    # Source sample doesn't exist, nothing to copy. Issue a warning.
    echo "Warning: Source sample config file not found, cannot create/overwrite $DEST_CONFIG: $SOURCE_CONFIG_SAMPLE"
    # Consider if this should be a fatal error depending on requirements:
    # exit 1
fi

echo "Building supergraph..."
# Build commands don't typically need the project name explicitly if the context is set
ddn supergraph build local || { echo "Error: Failed to build local supergraph"; exit 1; }
ddn supergraph build create --apply || { echo "Error: Failed to build cloud supergraph"; exit 1; }

echo "--- Script Complete ---"
exit 0
