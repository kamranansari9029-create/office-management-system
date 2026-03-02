"""
Database Operations for Office Management System
Using SQLite for Streamlit Cloud Deployment
"""
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import hashlib
import os
from config import DB_CONFIG


def get_connection():
    """Create and return a database connection"""
    try:
        conn = sqlite3.connect(DB_CONFIG['database'])
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return None


def init_database():
    """Initialize database with all tables and demo data"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Employee table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                emp_id TEXT PRIMARY KEY,
                emp_name TEXT NOT NULL,
                email_id TEXT,
                address TEXT,
                phone_no TEXT,
                post TEXT,
                password TEXT,
                date_of_join DATE,
                basic REAL
            )
        """)
        
        # Attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT NOT NULL,
                curr_date DATE NOT NULL,
                status TEXT,
                UNIQUE(emp_id, curr_date)
            )
        """)
        
        # Notice table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notice (
                notice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                notice TEXT,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Project table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project (
                project_id TEXT PRIMARY KEY,
                project_name TEXT,
                description TEXT,
                starting_date DATE,
                ending_date DATE,
                status TEXT,
                progression REAL
            )
        """)
        
        # Task table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT,
                emp_id TEXT,
                role TEXT
            )
        """)
        
        # Leave request table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leave_request (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT,
                start_date DATE,
                end_date DATE,
                reason TEXT,
                status TEXT DEFAULT 'Pending',
                request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Notification table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT,
                message TEXT,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Holiday table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS holiday (
                holiday_id INTEGER PRIMARY KEY AUTOINCREMENT,
                holiday_name TEXT,
                holiday_date DATE,
                description TEXT
            )
        """)
        
        # Payslip table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payslip (
                payslip_id INTEGER PRIMARY KEY AUTOINCREMENT,
                emp_id TEXT,
                month INTEGER,
                year INTEGER,
                basic_salary REAL,
                unpaid_leaves INTEGER,
                absences INTEGER,
                holidays INTEGER,
                deduction_amount REAL,
                net_salary REAL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Project document table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_document (
                doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT,
                file_name TEXT,
                file_data BLOB,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        
        # Check if demo data exists
        cursor.execute("SELECT COUNT(*) FROM employee")
        if cursor.fetchone()[0] == 0:
            # Add demo employees
            demo_employees = [
                ('EMP0001', 'Raju', 'EMP0001@company.com', '', '1234567890', 'HR', 'RAJU0001', date.today(), 50000),
                ('EMP0002', 'Saikumar', 'EMP0002@company.com', '', '1234567891', 'Employee', 'SAIK0002', date.today(), 30000),
                ('EMP0003', 'Arpit', 'EMP0003@company.com', '', '1234567892', 'Manager', 'ARPI0003', date.today(), 45000),
            ]
            cursor.executemany("""
                INSERT INTO employee (emp_id, emp_name, email_id, address, phone_no, post, password, date_of_join, basic)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, demo_employees)
            
            # Add demo projects
            demo_projects = [
                ('PROJ001', 'Website Redesign', 'Redesign company website with new branding', date.today(), date.today() + timedelta(days=60), 'In Progress', 45),
                ('PROJ002', 'Mobile App Development', 'Develop customer mobile application', date.today(), date.today() + timedelta(days=90), 'Not Started', 0),
                ('PROJ003', 'Database Migration', 'Migrate legacy database to new system', date.today() - timedelta(days=30), date.today() + timedelta(days=30), 'In Progress', 70),
            ]
            cursor.executemany("""
                INSERT INTO project (project_id, project_name, description, starting_date, ending_date, status, progression)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, demo_projects)
            
            # Add demo notices
            demo_notices = [
                ('Office will remain closed on Diwali'),
                ('New attendance policy effective from next month'),
                ('Team meeting scheduled for Friday at 3 PM'),
            ]
            for notice in demo_notices:
                cursor.execute("INSERT INTO notice (notice) VALUES (?)", (notice,))
            
            # Add demo holidays
            demo_holidays = [
                ('Republic Day', date(2026, 1, 26), 'National Holiday'),
                ('Independence Day', date(2026, 8, 15), 'National Holiday'),
                ('Diwali', date(2026, 10, 20), 'Festival'),
                ('Christmas', date(2026, 12, 25), 'Festival'),
            ]
            cursor.executemany("""
                INSERT INTO holiday (holiday_name, holiday_date, description)
                VALUES (?, ?, ?)
            """, demo_holidays)
            
            conn.commit()
            print("Demo data initialized successfully!")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False


def hash_password(password):
    """Hash a password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(emp_id, password):
    """Authenticate user with emp_id and password"""
    # Initialize database if needed
    init_database()
    
    conn = get_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE emp_id = ?", (emp_id,))
        user = cursor.fetchone()
        
        if user:
            # Check both plain password and hashed password
            if user['password'] == password or user['password'] == hash_password(password):
                conn.close()
                return dict(user)
        
        cursor.close()
        conn.close()
        return None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None


def update_password(emp_id, new_password):
    """Update user password with hashing"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        hashed_pw = hash_password(new_password)
        cursor.execute("UPDATE employee SET password = ? WHERE emp_id = ?", (hashed_pw, emp_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False


def get_employee_by_id(emp_id):
    """Get employee details by ID"""
    conn = get_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE emp_id = ?", (emp_id,))
        employee = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(employee) if employee else None
    except Exception as e:
        print(f"Error fetching employee: {e}")
        return None


def get_all_employees():
    """Get all employees"""
    init_database()
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql("SELECT * FROM employee ORDER BY emp_id", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return pd.DataFrame()


def add_employee(emp_id, emp_name, email_id, address, phone_no, post, password, date_of_join, basic):
    """Add a new employee"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employee (emp_id, emp_name, email_id, address, phone_no, post, password, date_of_join, basic)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (emp_id, emp_name, email_id, address, phone_no, post, password, date_of_join, basic))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding employee: {e}")
        return False


def update_employee(emp_id, emp_name, email_id, address, phone_no, post, basic):
    """Update employee details"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE employee 
            SET emp_name=?, email_id=?, address=?, phone_no=?, post=?, basic=?
            WHERE emp_id=?
        """, (emp_name, email_id, address, phone_no, post, basic, emp_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating employee: {e}")
        return False


def delete_employee(emp_id):
    """Delete an employee"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employee WHERE emp_id = ?", (emp_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting employee: {e}")
        return False


def get_attendance_records(emp_id=None, start_date=None, end_date=None):
    """Get attendance records"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = "SELECT * FROM attendance"
        conditions = []
        params = []
        
        if emp_id:
            conditions.append("emp_id = ?")
            params.append(emp_id)
        if start_date:
            conditions.append("curr_date >= ?")
            params.append(start_date)
        if end_date:
            conditions.append("curr_date <= ?")
            params.append(end_date)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY curr_date DESC, emp_id"
        
        df = pd.read_sql(query, conn, params=params if params else None)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching attendance: {e}")
        return pd.DataFrame()


def mark_attendance(emp_id, curr_date, status):
    """Mark attendance for an employee"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO attendance (emp_id, curr_date, status) 
            VALUES (?, ?, ?)
        """, (emp_id, curr_date, status))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error marking attendance: {e}")
        return False


def get_attendance_summary(emp_id=None, month=None, year=None):
    """Get attendance summary for an employee or all employees"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = """
            SELECT 
                emp_id,
                COUNT(*) as total_days,
                SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) as present,
                SUM(CASE WHEN status = 'A' THEN 1 ELSE 0 END) as absent,
                SUM(CASE WHEN status = 'H' THEN 1 ELSE 0 END) as holiday,
                SUM(CASE WHEN status = 'L' THEN 1 ELSE 0 END) as leave
            FROM attendance
        """
        conditions = []
        params = []
        
        if emp_id:
            conditions.append("emp_id = ?")
            params.append(emp_id)
        if month and year:
            conditions.append("strftime('%m', curr_date) = ?")
            params.append(f"{month:02d}")
            conditions.append("strftime('%Y', curr_date) = ?")
            params.append(str(year))
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " GROUP BY emp_id"
        
        df = pd.read_sql(query, conn, params=params if params else None)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching attendance summary: {e}")
        return pd.DataFrame()


def get_attendance_trend(days=7):
    """Get attendance counts for the last N days"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        end_date = date.today()
        start_date = end_date - timedelta(days=days-1)
        
        query = """
            SELECT curr_date, 
                   SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) as present,
                   SUM(CASE WHEN status = 'A' THEN 1 ELSE 0 END) as absent
            FROM attendance 
            WHERE curr_date BETWEEN ? AND ?
            GROUP BY curr_date
            ORDER BY curr_date
        """
        df = pd.read_sql(query, conn, params=(start_date, end_date))
        conn.close()
        
        if not df.empty:
            df['curr_date'] = pd.to_datetime(df['curr_date'])
            df['present'] = pd.to_numeric(df['present']).fillna(0).astype(int)
            df['absent'] = pd.to_numeric(df['absent']).fillna(0).astype(int)
            
        return df
    except Exception as e:
        print(f"Error fetching attendance trend: {e}")
        return pd.DataFrame()


def get_all_notices():
    """Get all notices ordered by time"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql("SELECT * FROM notice ORDER BY time DESC", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching notices: {e}")
        return pd.DataFrame()


def add_notice(notice_text):
    """Add a new notice and notify all employees"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Insert the notice
        cursor.execute("INSERT INTO notice (notice) VALUES (?)", (notice_text,))
        conn.commit()
        
        # Get all employees to send notifications
        cursor.execute("SELECT emp_id FROM employee")
        employees = cursor.fetchall()
        
        # Create notification message
        notice_preview = notice_text[:100] if len(notice_text) > 100 else notice_text
        notification_msg = f"New Notice Posted: {notice_preview}"
        
        # Send notification to all employees
        for emp in employees:
            cursor.execute("INSERT INTO notification (emp_id, message) VALUES (?, ?)", (emp[0], notification_msg))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding notice: {e}")
        return False


def delete_notice(notice_id):
    """Delete a notice"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notice WHERE notice_id = ?", (notice_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting notice: {e}")
        return False


def get_all_projects():
    """Get all projects"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql("SELECT * FROM project ORDER BY starting_date DESC", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return pd.DataFrame()


def add_project(project_id, project_name, description, starting_date, ending_date):
    """Add a new project"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO project (project_id, project_name, description, starting_date, ending_date, status, progression)
            VALUES (?, ?, ?, ?, ?, 'Not Started', 0)
        """, (project_id, project_name, description, starting_date, ending_date))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding project: {e}")
        return False


def update_project(project_id, project_name, description, status, progression):
    """Update project details"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE project 
            SET project_name=?, description=?, status=?, progression=?
            WHERE project_id=?
        """, (project_name, description, status, progression, project_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating project: {e}")
        return False


def delete_project(project_id):
    """Delete a project"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project WHERE project_id = ?", (project_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting project: {e}")
        return False


def get_all_tasks():
    """Get all tasks with project and employee details"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = """SELECT t.*, p.project_name, e.emp_name 
                   FROM task t 
                   JOIN project p ON t.project_id = p.project_id 
                   JOIN employee e ON t.emp_id = e.emp_id 
                   ORDER BY t.project_id"""
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return pd.DataFrame()


def get_tasks_by_employee(emp_id):
    """Get tasks assigned to a specific employee"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = """SELECT t.*, p.project_name, e.emp_name 
                   FROM task t 
                   JOIN project p ON t.project_id = p.project_id 
                   JOIN employee e ON t.emp_id = e.emp_id 
                   WHERE t.emp_id = ?
                   ORDER BY t.project_id"""
        df = pd.read_sql(query, conn, params=(emp_id,))
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching employee tasks: {e}")
        return pd.DataFrame()


def add_task(project_id, emp_id, role):
    """Assign a task to an employee"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO task (project_id, emp_id, role) VALUES (?, ?, ?)", 
                      (project_id, emp_id, role))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding task: {e}")
        return False


def delete_task(project_id, emp_id):
    """Remove a task from an employee"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM task WHERE project_id = ? AND emp_id = ?", (project_id, emp_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting task: {e}")
        return False


def get_managers():
    """Get all managers"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql("SELECT * FROM employee WHERE post = 'Manager'", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching managers: {e}")
        return pd.DataFrame()


def get_employees_list():
    """Get all non-HR employees"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = pd.read_sql("SELECT * FROM employee WHERE post != 'HR'", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return pd.DataFrame()


def update_project_status_by_employee(project_id, status, progression):
    """Update project status by employee"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE project SET status=?, progression=? WHERE project_id=?", 
                      (status, progression, project_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating project status: {e}")
        return False


def get_projects_by_employee(emp_id):
    """Get projects assigned to a specific employee"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = """SELECT DISTINCT p.* FROM project p 
                   JOIN task t ON p.project_id = t.project_id 
                   WHERE t.emp_id = ?"""
        df = pd.read_sql(query, conn, params=(emp_id,))
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching employee projects: {e}")
        return pd.DataFrame()


def add_leave_request(emp_id, start_date, end_date, reason):
    """Add a new leave request"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leave_request (emp_id, start_date, end_date, reason)
            VALUES (?, ?, ?, ?)
        """, (emp_id, start_date, end_date, reason))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding leave request: {e}")
        return False


def get_all_leave_requests():
    """Get all leave requests"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = """SELECT l.*, e.emp_name 
                   FROM leave_request l 
                   LEFT JOIN employee e ON l.emp_id = e.emp_id 
                   ORDER BY l.request_date DESC"""
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching leave requests: {e}")
        return pd.DataFrame()


def get_employee_leave_requests(emp_id):
    """Get leave requests for specific employee"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = "SELECT * FROM leave_request WHERE emp_id = ? ORDER BY request_date DESC"
        df = pd.read_sql(query, conn, params=(emp_id,))
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching employee leave requests: {e}")
        return pd.DataFrame()


def add_notification(emp_id, message):
    """Add a notification for an employee"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notification (emp_id, message) VALUES (?, ?)", (emp_id, message))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding notification: {e}")
        return False


def get_user_notifications(emp_id):
    """Get unread notifications for a user"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = "SELECT * FROM notification WHERE emp_id = ? AND is_read = 0 ORDER BY created_at DESC"
        df = pd.read_sql(query, conn, params=(emp_id,))
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching notifications: {e}")
        return pd.DataFrame()


def mark_notification_read(notification_id):
    """Mark notification as read"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE notification SET is_read = 1 WHERE id = ?", (notification_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error marking notification read: {e}")
        return False


def delete_notification(notification_id):
    """Delete a notification"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notification WHERE id = ?", (notification_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting notification: {e}")
        return False


def update_leave_status(request_id, status):
    """Update leave request status"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Get emp_id to notify
        cursor.execute("SELECT emp_id FROM leave_request WHERE request_id = ?", (request_id,))
        result = cursor.fetchone()
        
        cursor.execute("UPDATE leave_request SET status = ? WHERE request_id = ?", (status, request_id))
        conn.commit()
        cursor.close()
        
        if result:
            # Create notification message
            if status == 'Approved':
                notification_msg = "Your leave request has been APPROVED!"
            else:
                notification_msg = "Your leave request has been REJECTED."
            add_notification(result[0], notification_msg)
            
        return True
    except Exception as e:
        print(f"Error updating leave status: {e}")
        return False


def upload_project_document(project_id, file_name, file_data):
    """Upload a document for a project"""
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO project_document (project_id, file_name, file_data)
            VALUES (?, ?, ?)
        """, (project_id, file_name, file_data))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error uploading document: {e}")
        return False


def get_project_documents(project_id):
    """Get metadata of documents for a project"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    try:
        query = "SELECT doc_id, project_id, file_name, upload_date FROM project_document WHERE project_id = ? ORDER BY upload_date DESC"
        df = pd.read_sql(query, conn, params=(project_id,))
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching documents: {e}")
        return pd.DataFrame()


def get_document_content(doc_id):
    """Get specific document content"""
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        query = "SELECT file_name, file_data FROM project_document WHERE doc_id = ?"
        cursor.execute(query, (doc_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error fetching document content: {e}")
        return None


def delete_project_document(doc_id):
    """Delete a project document"""
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM project_document WHERE doc_id = ?", (doc_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting document: {e}")
        return False


# ====== Payslip & Salary Deduction Functions ======

def calculate_monthly_deductions(emp_id, month, year):
    """Calculate deductions for unpaid leaves and absences in a month"""
    conn = get_connection()
    if conn is None:
        return {'unpaid_leaves': 0, 'absences': 0, 'total_deduction': 0, 'holidays': 0}
    
    try:
        import calendar
        total_days = calendar.monthrange(year, month)[1]
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM attendance 
            WHERE emp_id = ? AND strftime('%m', curr_date) = ? AND strftime('%Y', curr_date) = ?
            GROUP BY status
        """, (emp_id, f"{month:02d}", str(year)))
        records = cursor.fetchall()
        
        unpaid_leaves = 0
        absences = 0
        holidays = 0
        
        for record in records:
            if record[0] == 'L':
                unpaid_leaves += record[1]
            elif record[0] == 'A':
                absences += record[1]
            elif record[0] == 'H':
                holidays += record[1]
        
        cursor.execute("SELECT basic FROM employee WHERE emp_id = ?", (emp_id,))
        result = cursor.fetchone()
        
        if result:
            daily_rate = result[0] / 26
            total_deduction = (unpaid_leaves + absences) * daily_rate
        else:
            daily_rate = 0
            total_deduction = 0
        
        cursor.close()
        conn.close()
        
        return {
            'unpaid_leaves': unpaid_leaves,
            'absences': absences,
            'holidays': holidays,
            'total_deduction': total_deduction,
            'daily_rate': daily_rate,
            'working_days': total_days
        }
    except Exception as e:
        print(f"Error calculating deductions: {e}")
        return {'unpaid_leaves': 0, 'absences': 0, 'holidays': 0, 'total_deduction': 0}


def generate_payslip(emp_id, month, year):
    """Generate payslip for an employee for a specific month"""
    conn = get_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE emp_id = ?", (emp_id,))
        employee = cursor.fetchone()
        
        if not employee:
            cursor.close()
            conn.close()
            return None
        
        deductions = calculate_monthly_deductions(emp_id, month, year)
        gross_salary = employee['basic']
        net_salary = gross_salary - deductions['total_deduction']
        
        # Check if payslip exists
        cursor.execute("""
            SELECT payslip_id FROM payslip 
            WHERE emp_id = ? AND month = ? AND year = ?
        """, (emp_id, month, year))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE payslip 
                SET basic_salary = ?, unpaid_leaves = ?, absences = ?, holidays = ?,
                    deduction_amount = ?, net_salary = ?
                WHERE payslip_id = ?
            """, (gross_salary, deductions['unpaid_leaves'], deductions['absences'], deductions['holidays'],
                  deductions['total_deduction'], net_salary, existing[0]))
        else:
            cursor.execute("""
                INSERT INTO payslip 
                (emp_id, month, year, basic_salary, unpaid_leaves, absences, holidays, deduction_amount, net_salary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (emp_id, month, year, gross_salary, deductions['unpaid_leaves'],
                  deductions['absences'], deductions['holidays'], deductions['total_deduction'], net_salary))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'emp_id': emp_id,
            'emp_name': employee['emp_name'],
            'post': employee['post'],
            'month': month,
            'year': year,
            'basic_salary': gross_salary,
            'unpaid_leaves': deductions['unpaid_leaves'],
            'absences': deductions['absences'],
            'holidays': deductions['holidays'],
            'deduction_amount': deductions['total_deduction'],
            'net_salary': net_salary,
            'working_days': deductions['working_days']
        }
    except Exception as e:
        print(f"Error generating payslip: {e}")
        return None


def get_payslip(emp_id, month, year):
    """Get payslip for a specific month"""
    conn = get_connection()
    if conn is None:
        return None
    
    try:
        query = """
            SELECT p.*, e.emp_name, e.post 
            FROM payslip p
            JOIN employee e ON p.emp_id = e.emp_id
            WHERE p.emp_id = ? AND p.month = ? AND p.year = ?
        """
        cursor = conn.cursor()
        cursor.execute(query, (emp_id, month, year))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting payslip: {e}")
        return None


def get_all_payslips(emp_id=None):
    """Get all payslips, optionally filtered by employee"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        if emp_id:
            query = """
                SELECT p.*, e.emp_name, e.post 
                FROM payslip p
                JOIN employee e ON p.emp_id = e.emp_id
                WHERE p.emp_id = ?
                ORDER BY p.year DESC, p.month DESC
            """
            df = pd.read_sql(query, conn, params=(emp_id,))
        else:
            query = """
                SELECT p.*, e.emp_name, e.post 
                FROM payslip p
                JOIN employee e ON p.emp_id = e.emp_id
                ORDER BY p.year DESC, p.month DESC
            """
            df = pd.read_sql(query, conn)
        
        conn.close()
        return df
    except Exception as e:
        print(f"Error getting payslips: {e}")
        return pd.DataFrame()


# ====== Holiday Calendar Functions ======

def add_holiday(holiday_name, holiday_date, description=""):
    """Add a new company holiday"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO holiday (holiday_name, holiday_date, description)
            VALUES (?, ?, ?)
        """, (holiday_name, holiday_date, description))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding holiday: {e}")
        return False


def get_all_holidays(year=None):
    """Get all company holidays, optionally filtered by year"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        if year:
            query = "SELECT * FROM holiday WHERE strftime('%Y', holiday_date) = ? ORDER BY holiday_date"
            df = pd.read_sql(query, conn, params=(str(year),))
        else:
            query = "SELECT * FROM holiday ORDER BY holiday_date"
            df = pd.read_sql(query, conn)
        
        conn.close()
        return df
    except Exception as e:
        print(f"Error getting holidays: {e}")
        return pd.DataFrame()


def delete_holiday(holiday_id):
    """Delete a company holiday"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM holiday WHERE holiday_id = ?", (holiday_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting holiday: {e}")
        return False


def is_holiday(check_date):
    """Check if a specific date is a company holiday"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM holiday WHERE holiday_date = ?", (check_date,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] > 0 if result else False
    except Exception as e:
        print(f"Error checking holiday: {e}")
        return False


def auto_mark_holidays():
    """Automatically mark all holidays for all employees"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id FROM employee")
        employees = cursor.fetchall()
        cursor.execute("SELECT holiday_date FROM holiday")
        holidays = cursor.fetchall()
        
        for emp in employees:
            for holiday in holidays:
                holiday_date = holiday[0]
                cursor.execute(
                    "SELECT COUNT(*) FROM attendance WHERE emp_id = ? AND curr_date = ?",
                    (emp[0], holiday_date)
                )
                result = cursor.fetchone()
                
                if result[0] == 0:
                    cursor.execute(
                        "INSERT INTO attendance (emp_id, curr_date, status) VALUES (?, ?, 'H')",
                        (emp[0], holiday_date)
                    )
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error auto marking holidays: {e}")
        return False


# Initialize database on module load
init_database()
