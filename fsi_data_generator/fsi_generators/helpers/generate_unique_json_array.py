import anthropic
import json
import os
from dotenv import load_dotenv  # Import load_dotenv

load_dotenv()  # Load environment variables from .env file
# Assuming you have your Anthropic API key set as an environment variable or otherwise accessible
client = anthropic.Anthropic()

PREVIOUS_RESPONSES_FILE = "previous_responses.json"


def load_previous_responses():
    """Loads previous responses from disk."""
    if os.path.exists(PREVIOUS_RESPONSES_FILE):
        try:
            with open(PREVIOUS_RESPONSES_FILE, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    return {}


def save_previous_responses(responses):
    """Saves previous responses to disk."""
    try:
        with open(PREVIOUS_RESPONSES_FILE, "w") as f:
            json.dump(responses, f, indent=4)
    except IOError as e:
        print(f"Error saving previous responses: {e}")


previous_responses = load_previous_responses()  # Load on startup


def generate_unique_json_array(dbml_string, fully_qualified_column_name, count, cache_key=None):
    """
    Generates a unique JSON string array of TEXT elements using Anthropic API.
    If cached results exist but are fewer than requested, only requests the additional needed elements.

    Args:
        dbml_string (str): The DBML string representing the database schema.
        fully_qualified_column_name (str): The fully qualified name of the table column.
        count (int): The number of unique elements to generate.
        cache_key (str, optional): An optional key to use for caching. Defaults to None.

    Returns:
        list: A list of unique TEXT elements.
    """

    key_to_use = cache_key if cache_key is not None else fully_qualified_column_name

    # Check if we have cached results
    if key_to_use in previous_responses:
        cached_results = previous_responses[key_to_use]

        # If we already have enough elements, return the requested number
        if len(cached_results) >= count:
            return cached_results[:count]

        # If we have some but not enough, only request the additional elements needed
        additional_needed = count - len(cached_results)
        print(f"Found {len(cached_results)} cached elements. Requesting {additional_needed} additional elements.")
    else:
        cached_results = []
        additional_needed = count

    # Adjust the prompt to request only the additional elements needed
    prompt = f"""
    Here is a DBML string representing a database schema:

    {dbml_string}

    Generate a JSON string array of TEXT elements suitable for the column: {fully_qualified_column_name}.

    I requested {additional_needed} NEW and UNIQUE elements.
    
    {"I already have the following elements, please DO NOT duplicate any of these: " + json.dumps(cached_results) if cached_results else ""}

    Instructions:
    - If the DBML and field name indicate that each element should be unique and distinct (e.g., customer complaint notes), generate exactly {additional_needed} elements.
    - If the context suggests that a large number of elements is unreasonable (e.g., insurance company names), generate a reasonable amount, which may be significantly less than {additional_needed}.
    - Otherwise, generate a reasonable amount.
    - IMPORTANT: The response must be a valid, properly formatted JSON array of strings ONLY.
    - Do not include any explanations, markdown formatting, or additional text.
    - Do not use backticks or code blocks.
    - Ensure the JSON array is complete and properly closed with a final bracket.
    - Make sure all new elements are DIFFERENT from the existing cached elements.

    Example output:
    ["new_value1", "new_value2", "new_value3"]
    """

    try:
        # Using the messages API with streaming to handle long responses
        complete_response = ""

        # Stream the response to ensure we get the full content
        with client.messages.stream(
                model=os.environ.get('ANTHROPIC_MODEL', 'claude-3-7-sonnet-20250219'),
                max_tokens=8000,  # Significantly increased token limit for long responses
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2  # Lower temperature for more consistent formatting
        ) as stream:
            for text in stream.text_stream:
                complete_response += text

        response_text = complete_response

        # Clean up response if it's wrapped in markdown code blocks
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "", 1)
            if response_text.endswith("```"):
                response_text = response_text[:-3]
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "", 1)
            if response_text.endswith("```"):
                response_text = response_text[:-3]

        response_text = response_text.strip()

        try:
            # Attempt to parse the response as JSON
            new_data = json.loads(response_text)
            if isinstance(new_data, list) and all(isinstance(item, str) for item in new_data):
                # Combine cached results with new results
                combined_results = cached_results + new_data

                # Remove any potential duplicates (just to be safe)
                combined_results = list(dict.fromkeys(combined_results))

                # Update the cache with the combined results
                previous_responses[key_to_use] = combined_results
                save_previous_responses(previous_responses)

                return combined_results
            else:
                raise ValueError("Anthropic response was not a valid JSON string array of strings.")
        except json.JSONDecodeError as e:
            # Attempt recovery for incomplete JSON responses
            print(f"Received potentially incomplete JSON: {e}")

            # Try to recover truncated JSON array
            if response_text.startswith("[") and not response_text.endswith("]"):
                try:
                    # Add closing bracket and try parsing again
                    recovered_text = response_text + "]"
                    new_data = json.loads(recovered_text)
                    if isinstance(new_data, list) and all(isinstance(item, str) for item in new_data):
                        print("Successfully recovered from truncated JSON array")
                        combined_results = cached_results + new_data
                        combined_results = list(dict.fromkeys(combined_results))
                        previous_responses[key_to_use] = combined_results
                        save_previous_responses(previous_responses)
                        return combined_results
                except:
                    pass  # If recovery fails, continue to original error

            # For other common truncation patterns
            if "," in response_text and not response_text.endswith("]"):
                try:
                    # Find last complete item by finding the last valid comma
                    last_comma = response_text.rstrip().rfind(",")
                    if last_comma > 0:
                        recovered_text = response_text[:last_comma] + "]"
                        new_data = json.loads(recovered_text)
                        if isinstance(new_data, list) and all(isinstance(item, str) for item in new_data):
                            print("Successfully recovered from malformed JSON array")
                            combined_results = cached_results + new_data
                            combined_results = list(dict.fromkeys(combined_results))
                            previous_responses[key_to_use] = combined_results
                            save_previous_responses(previous_responses)
                            return combined_results
                except:
                    pass  # If recovery fails, continue to original error

            # If all recovery attempts fail, raise the original error
            print(f"Error decoding JSON: {e}")
            print(f"Raw response: {response_text}")
            raise ValueError("Anthropic response was not valid JSON and could not be recovered.")

    except anthropic.APIConnectionError as e:
        print(f"Error connecting to Anthropic API: {e}")
        raise
    except anthropic.APIStatusError as e:
        print(f"Anthropic API returned an error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
