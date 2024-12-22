import os

from arcadia.utils.settings import Settings

CONFIG_DIR = os.path.expanduser("~/.arcadia")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

settings = Settings()

if not settings.supabase_url or not settings.supabase_key:
    raise ValueError(
        "Missing Supabase configuration. Contact tim@timcvetko.com."
        "Please ensure SUPABASE_URL and SUPABASE_KEY environment variables are set."
    )
