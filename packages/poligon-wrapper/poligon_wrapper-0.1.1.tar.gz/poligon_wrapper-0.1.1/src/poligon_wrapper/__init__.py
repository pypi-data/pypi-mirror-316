import os
from dotenv import load_dotenv, find_dotenv, set_key, unset_key


def ensure_dotenv():
    """Ensure the .env file exists and is correctly located."""
    # Locate the .env file (search for it in the current directory or parent directories)
    dotenv_path = find_dotenv()

    # If .env file is not found, create it in the current directory
    if not dotenv_path:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        # Only create the file if it doesn't exist, don't overwrite existing file
        if not os.path.exists(dotenv_path):
            with open(dotenv_path, 'w') as f:
                f.write("")  # Create an empty .env file if not found

    return dotenv_path

# Load environment variables from .env file
dotenv_path = ensure_dotenv()
load_dotenv(dotenv_path)

# Get the API key from the .env file or environment
polygon_apikey = os.getenv("polygon_apikey")

def request_api_key():
    """Prompt the user for the API key."""
    api_key = input("Please enter your API key: ").strip()
    if not api_key:
        raise ValueError("API key cannot be empty.")
    return api_key

# If no API key found, request it from the user and store it in .env
if not polygon_apikey:
    # Prompt the user for an API key
    polygon_apikey = request_api_key()

    # Store the API key in the .env file
    set_key(dotenv_path, "polygon_apikey", polygon_apikey)
    print(f"API key has been set: {polygon_apikey[:4]}****")  # Mask part of the API key
else:
    print(f"API key is already set: {polygon_apikey[:4]}****")  # Show part of the existing API key


# Function to change the API key
def change_api_key():
    new_api_key = request_api_key()
    set_key(dotenv_path, "polygon_apikey", new_api_key)
    print(f"API key has been updated: {new_api_key[:4]}****")

# Function to delete the API key from .env file
def delete_api_key():
    unset_key(dotenv_path, "polygon_apikey")
    print("API key has been deleted.")




