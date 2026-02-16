from database import supabase
from datetime import datetime, timedelta

def generate_report(days=1):
    # Calculate the start date (1 for daily, 7 for weekly)
    start_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    try:
        response = supabase.table("attendance") \
            .select("name, timestamp") \
            .gte("timestamp", start_date) \
            .execute()
        
        data = response.data
        
        print(f"\n--- {'WEEKLY' if days==7 else 'DAILY'} ATTENDANCE REPORT ---")
        print(f"{'Name':<20} | {'Time'}")
        print("-" * 40)
        
        for record in data:
            # Format the timestamp for readability
            dt = record['timestamp'].split('.')[0].replace('T', ' ')
            print(f"{record['name']:<20} | {dt}")
            
        print(f"\nTotal Attendees: {len(data)}")
        print("-" * 40)

    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    # Choose report type
    choice = input("Enter '1' for Daily Report or '7' for Weekly Report: ")
    if choice in ['1', '7']:
        generate_report(int(choice))
    else:
        print("Invalid input.")