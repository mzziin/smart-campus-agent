"""
Database initialization with sample data.
Run this script to set up the database with demo data.
"""
from app.database.Connection import init_database, get_db_connection
from datetime import date, timedelta


def insert_sample_data():
    """Insert sample data for demo purposes"""
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Clear existing data (for fresh initialization)
        cursor.execute("DELETE FROM events")
        cursor.execute("DELETE FROM exams")
        cursor.execute("DELETE FROM placements")
        
        # Calculate dates relative to today
        today = date.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        
        # Sample Events
        events = [
            ("Tech Talk on AI and Machine Learning", "technical", str(today), "10:00 AM", 
             "Seminar Hall A", "CSE Department", "Industry expert session on latest AI trends"),
            
            ("Annual Cultural Fest - Day 1", "cultural", str(today), "2:00 PM", 
             "Open Auditorium", "Student Council", "Dance, music, and cultural performances"),
            
            ("Hackathon 2026: Code Sprint", "technical", str(tomorrow), "9:00 AM", 
             "Computer Lab Block B", "Tech Club", "24-hour coding competition with exciting prizes"),
            
            ("Traditional Day Celebrations", "cultural", str(tomorrow), "11:00 AM", 
             "Main Ground", "Cultural Committee", "Celebrate diversity with traditional attire"),
            
            ("Workshop on Cloud Computing", "technical", str(next_week), "3:00 PM", 
             "Seminar Hall C", "IT Department", "Hands-on workshop on AWS and Azure platforms"),
        ]
        
        cursor.executemany("""
            INSERT INTO events (title, category, date, time, venue, organizer, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, events)
        
        # Sample Exams
        exams = [
            ("Mid Semester Examination", "Data Structures", "CSE", 3, str(today + timedelta(days=3)), 
             "9:30 AM", "Block B - Room 204"),
            
            ("Mid Semester Examination", "Digital Electronics", "ECE", 3, str(today + timedelta(days=4)), 
             "2:00 PM", "Block A - Room 101"),
            
            ("End Semester Examination", "Database Management Systems", "CSE", 5, str(today + timedelta(days=10)), 
             "10:00 AM", "Block C - Room 305"),
            
            ("Mid Semester Examination", "Engineering Mechanics", "ME", 2, str(today + timedelta(days=5)), 
             "9:30 AM", "Block D - Room 102"),
            
            ("End Semester Examination", "Computer Networks", "IT", 5, str(today + timedelta(days=12)), 
             "2:00 PM", "Block B - Room 201"),
        ]
        
        cursor.executemany("""
            INSERT INTO exams (exam_name, subject, department, semester, date, time, venue)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, exams)
        
        # Sample Placements
        placements = [
            ("Infosys", "System Engineer", "CSE,IT", str(today + timedelta(days=2)), 
             "9:00 AM", "Placement Cell"),
            
            ("TCS", "Assistant System Engineer", "CSE,IT,ECE", str(today + timedelta(days=6)), 
             "10:00 AM", "Seminar Hall A"),
            
            ("Wipro", "Project Engineer", "CSE,IT", str(today + timedelta(days=8)), 
             "9:30 AM", "Placement Cell"),
            
            ("Accenture", "Software Developer", "CSE,IT,ECE", str(today + timedelta(days=14)), 
             "11:00 AM", "Auditorium"),
            
            ("Cognizant", "Programmer Analyst", "CSE,IT", str(today + timedelta(days=20)), 
             "9:00 AM", "Placement Cell"),
        ]
        
        cursor.executemany("""
            INSERT INTO placements (company, role, department, date, time, venue)
            VALUES (?, ?, ?, ?, ?, ?)
        """, placements)
        
        conn.commit()
        
        # Print summary
        cursor.execute("SELECT COUNT(*) FROM events")
        event_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM exams")
        exam_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM placements")
        placement_count = cursor.fetchone()[0]
        
        print(f"\n✅ Sample data inserted successfully!")
        print(f"   - Events: {event_count}")
        print(f"   - Exams: {exam_count}")
        print(f"   - Placements: {placement_count}\n")


if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    print("\nInserting sample data...")
    insert_sample_data()
    print("Database setup complete! 🎉")