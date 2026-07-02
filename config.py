import os

from dotenv import load_dotenv


load_dotenv()


def get_api_keys():
    """Get app configuration from environment variables."""
    app_mode = os.environ.get("APP_MODE", "live").lower()
    keys = {
        "openai": os.environ.get("OPENAI_API_KEY"),
        "anthropic": os.environ.get("ANTHROPIC_API_KEY"),
        "qdrant": os.environ.get("QDRANT_API_KEY"),
        "qdrant_url": os.environ.get("QDRANT_URL"),
        "app_password": os.environ.get("APP_PASSWORD")
        or os.environ.get("APP_ACCESS_PASSWORD"),
        "app_mode": "mock" if app_mode == "mock" else "live",
    }

    # Check if we're in deployment environment
    if os.environ.get("REPLIT_DEPLOYMENT") and not any(keys.values()):
        raise ValueError("API keys not found in deployment environment")

    return keys


if __name__ == "__main__":
    keys = get_api_keys()
    print("API keys loaded")
