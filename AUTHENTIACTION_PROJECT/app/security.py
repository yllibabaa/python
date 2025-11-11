from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from dotnev import load_dotenv
imporos

load_dotenv()

API_KEY_NAME = "api-kay"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key: str = Depends(api_key_header)):
    allowed_api_keys = os.getenv("API_KEYS", "").split(",")

    print(f"Received API key:", api_key)
    print(f"Allowed API keys:", allowed_api_keys)
    if api_key not in allowed_api_keys:
        print("API key is invalid")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    print("API key is valid")
    return api_key
