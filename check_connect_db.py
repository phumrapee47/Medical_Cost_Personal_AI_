import supabase
import os
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

supabase_client = supabase.create_client(url, key)

response = supabase_client.table("insurance").select("*").execute()

print(response)