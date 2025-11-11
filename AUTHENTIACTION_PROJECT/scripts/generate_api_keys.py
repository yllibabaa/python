from uuid import uuid4
from dotenv import load_dotenv, set_key
import os


def generate_and_save_api_keys():
    load_dotenv()

    api_key = str(uuid4())
    print(f"generated api key: {api_key}")

    foot_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(foot_directory, '.env')

    if not os.path.exists(env_path):
        open(env_path, 'w').close

        existing_keys = os.getenv("API_KEYS", "")

    if existing_keys:
        existing_keys = existing_keys.strip(",")
        new_keys = f"{existing_keys},{api_key}" if existing_keys else api_key
    else:
        new_keys = api_key

    set_key(env_path, "API_KEYS", new_keys)
    print(f"API key saved to {env_path}")

    if __name__ == "__main__":
        generate_and_save_api_keys()



