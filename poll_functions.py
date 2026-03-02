"""
Poll/Survey Functions for Office Management System
"""
import sqlite3
import pandas as pd
from datetime import datetime
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


def create_poll(question, options, created_by):
    """Create a new poll"""
    conn = get_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Insert the poll
        cursor.execute("""
            INSERT INTO poll (question, created_by)
            VALUES (?, ?)
        """, (question, created_by))
        poll_id = cursor.lastrowid
        
        # Insert options
        for option in options:
            cursor.execute("""
                INSERT INTO poll_option (poll_id, option_text)
                VALUES (?, ?)
            """, (poll_id, option))
        
        conn.commit()
        cursor.close()
        conn.close()
        return poll_id
    except Exception as e:
        print(f"Error creating poll: {e}")
        return None


def get_all_polls():
    """Get all polls"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        query = """SELECT p.*, e.emp_name as creator_name 
                   FROM poll p 
                   LEFT JOIN employee e ON p.created_by = e.emp_id 
                   ORDER BY p.created_at DESC"""
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching polls: {e}")
        return pd.DataFrame()


def get_poll_with_options(poll_id):
    """Get poll with its options and vote counts"""
    conn = get_connection()
    if conn is None:
        return None
    
    try:
        # Get poll details
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, e.emp_name as creator_name 
            FROM poll p 
            LEFT JOIN employee e ON p.created_by = e.emp_id 
            WHERE p.poll_id = ?
        """, (poll_id,))
        poll = cursor.fetchone()
        
        if not poll:
            cursor.close()
            conn.close()
            return None
        
        # Get options with vote counts
        cursor.execute("""
            SELECT po.*, 
                   (SELECT COUNT(*) FROM poll_vote pv WHERE pv.option_id = po.option_id) as vote_count
            FROM poll_option po
            WHERE po.poll_id = ?
            ORDER BY po.option_id
        """, (poll_id,))
        options = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            'poll': dict(poll),
            'options': [dict(opt) for opt in options]
        }
    except Exception as e:
        print(f"Error fetching poll: {e}")
        return None


def vote_poll(emp_id, poll_id, option_id):
    """Vote on a poll"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Check if already voted
        cursor.execute("""
            SELECT COUNT(*) FROM poll_vote 
            WHERE emp_id = ? AND poll_id = ?
        """, (emp_id, poll_id))
        
        if cursor.fetchone()[0] > 0:
            cursor.close()
            conn.close()
            return False  # Already voted
        
        # Record the vote
        cursor.execute("""
            INSERT INTO poll_vote (emp_id, poll_id, option_id)
            VALUES (?, ?, ?)
        """, (emp_id, poll_id, option_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error voting: {e}")
        return False


def has_voted(emp_id, poll_id):
    """Check if employee has voted on a poll"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM poll_vote 
            WHERE emp_id = ? AND poll_id = ?
        """, (emp_id, poll_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] > 0
    except Exception as e:
        print(f"Error checking vote: {e}")
        return False


def get_user_vote(emp_id, poll_id):
    """Get what option user voted for"""
    conn = get_connection()
    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pv.option_id, po.option_text
            FROM poll_vote pv
            JOIN poll_option po ON pv.option_id = po.option_id
            WHERE pv.emp_id = ? AND pv.poll_id = ?
        """, (emp_id, poll_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return dict(result) if result else None
    except Exception as e:
        print(f"Error getting user vote: {e}")
        return None


def delete_poll(poll_id):
    """Delete a poll and all its votes"""
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM poll_vote WHERE poll_id = ?", (poll_id,))
        cursor.execute("DELETE FROM poll_option WHERE poll_id = ?", (poll_id,))
        cursor.execute("DELETE FROM poll WHERE poll_id = ?", (poll_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting poll: {e}")
        return False
