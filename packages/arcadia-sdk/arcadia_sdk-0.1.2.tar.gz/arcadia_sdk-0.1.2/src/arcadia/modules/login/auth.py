import json
import os

from supabase import Client, create_client

from .config import CONFIG_DIR, CONFIG_FILE, SUPABASE_KEY, SUPABASE_URL


def save_credentials(username: str, api_key: str):
    """Save credentials to config file"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"username": username, "api_key": api_key}, f)


def load_credentials():
    """Load credentials from config file"""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValueError("Not logged in. Please run 'arcadia login' first.")


def validate_credentials(username: str, api_key: str) -> bool:
    """Validate credentials against Supabase"""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = (
            supabase.table("users")
            .select("*")
            .eq("username", username)
            .eq("api_key", api_key)
            .execute()
        )
        return len(response.data) > 0
    except Exception as e:
        print(f"Error validating credentials: {e}")
        return False
