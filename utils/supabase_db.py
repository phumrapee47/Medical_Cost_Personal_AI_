import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")

def get_supabase() -> Client:
    """Initialize and return the Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(f"Missing Supabase URL or Key in .env file. Got URL: {SUPABASE_URL}")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_data(table_name="sales"):
    """Fetch all rows from the specified table."""
    supabase = get_supabase()
    # Adding order by id desc so that we get the latest inserted items, bypassing the 1000 row limit of older data
    response = supabase.table(table_name).select("*").order("id", desc=True).limit(1000).execute()
    return response.data

def save_data(table_name, data):
    """Save data back to a Supabase table."""
    supabase = get_supabase()
    response = supabase.table(table_name).insert(data).execute()
    return response.data
