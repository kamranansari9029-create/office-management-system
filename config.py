"""
Database Configuration for Office Management System
"""
import os

# MySQL Database Configuration
# For XAMPP (default - empty password)
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'project_database',
    'port': 3306
}

# Alternative - if password is 'root'
# DB_CONFIG = {
#     'host': '127.0.0.1',
#     'user': 'root',
#     'password': 'root',
#     'database': 'project_database',
#     'port': 3306
# }

# Session timeout in seconds
SESSION_TIMEOUT = 3600
