"""
Database initialization with sample data.
Run this script to set up the database with demo data.
"""
import random
from datetime import date, timedelta
from app.database.Connection import init_database, get_db_connection

def insert_sample_data():
    """Insert expanded sample data adhering to category constraints"""
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM events")
        cursor.execute("DELETE FROM exams")
        cursor.execute("DELETE FROM placements")
        
        today = date.today()
        
        # --- 1. Events (Strictly 'technical' or 'cultural') ---
        # Mapping various event names to the allowed DB categories
        event_pool = [
            ("AI Workshop", "technical"),
            ("Coding Contest", "technical"),
            ("Robotics Exhibition", "technical"),
            ("Dance Performance", "cultural"),
            ("Music Concert", "cultural"),
            ("Drama Night", "cultural"),
            ("Cloud Seminar", "technical"),
            ("Art Exhibition", "cultural")
        ]
        
        venues = ["Seminar Hall A", "Open Auditorium", "Main Ground", "Lab 101", "Conference Room"]
        
        events = []
        for i in range(50):
            event_date = today if i < 5 else today + timedelta(days=random.randint(0, 25))
            name, category = random.choice(event_pool)
            events.append((
                f"{name} #{i+1}", 
                category, # Must be 'technical' or 'cultural'
                str(event_date), 
                f"{random.choice(['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM'])}", 
                random.choice(venues), 
                "University Dept", 
                f"Description for {name} event {i+1}"
            ))

        cursor.executemany("""
            INSERT INTO events (title, category, date, time, venue, organizer, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, events)

        # --- 2. Exams (50 Records) ---
        subjects = ["Mathematics", "Physics", "Data Structures", "AI", "Operating Systems", "Thermodynamics"]
        depts = ["CSE", "ECE", "ME", "IT", "EEE"]
        
        exams = []
        for i in range(50):
            exam_date = today if i < 5 else today + timedelta(days=random.randint(1, 15))
            exams.append((
                "Semester Examination", 
                random.choice(subjects), 
                random.choice(depts), 
                random.randint(1, 8), 
                str(exam_date), 
                "10:00 AM", 
                f"Block {random.choice(['A', 'B', 'C'])} - {random.randint(100, 500)}"
            ))

        cursor.executemany("""
            INSERT INTO exams (exam_name, subject, department, semester, date, time, venue)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, exams)

        # --- 3. Placements (50 Records) ---
        companies = ["Google", "Microsoft", "Amazon", "Meta", "TCS", "Infosys", "Wipro"]
        
        placements = []
        for i in range(50):
            placement_date = today if i < 5 else today + timedelta(days=random.randint(1, 20))
            placements.append((
                random.choice(companies), 
                "Software Engineer", 
                "CSE,IT,ECE", 
                str(placement_date), 
                "9:30 AM", 
                "Placement Cell"
            ))

        cursor.executemany("""
            INSERT INTO placements (company, role, department, date, time, venue)
            VALUES (?, ?, ?, ?, ?, ?)
        """, placements)
        
        conn.commit()
        print(f"\n✅ Data inserted! 15 records set for today ({today}).")

if __name__ == "__main__":
    init_database()
    insert_sample_data()