import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def log_attendance(name):
    """
    Checks if a user has already been logged TODAY.
    If not, inserts a new record.
    """
    # Get today's date in YYYY-MM-DD format
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        # 1. Query Supabase for this name on this specific day
        # We check if 'timestamp' is between the start and end of today
        start_of_day = f"{today_date}T00:00:00"
        end_of_day = f"{today_date}T23:59:59"

        existing_record = supabase.table("attendance") \
            .select("*") \
            .eq("name", name) \
            .gte("timestamp", start_of_day) \
            .lte("timestamp", end_of_day) \
            .execute()

        # 2. If record exists, skip insertion
        if len(existing_record.data) > 0:
            return "ALREADY_LOGGED"

        # 3. If no record, insert new entry
        data = {"name": name, "status": "Present"}
        supabase.table("attendance").insert(data).execute()
        return "SUCCESS"
        
    except Exception as e:
        print(f"Database Query Error: {e}")
        return "ERROR"