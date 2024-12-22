import os

from dotenv import load_dotenv

load_dotenv()

CONFIG_DIR = os.path.expanduser("~/.arcadia")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Missing Supabase configuration. Contact tim@timcvetko.com."
        "Please ensure SUPABASE_URL and SUPABASE_KEY environment variables are set."
    )