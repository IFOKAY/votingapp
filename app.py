import os
import time
import mysql.connector
from flask import Flask

app = Flask(__name__)

# Get database connection details from environment variables
DB_HOST = os.getenv('DB_HOST', 'mysql')  # Default to 'mysql' if not set
DB_USER = os.getenv('DB_USER', 'voteuser')  # Default to 'voteuser'
DB_PASSWORD = os.getenv('DB_PASSWORD', 'votepassword')  # Default to 'votepassword'
DB_NAME = os.getenv('DB_NAME', 'voting_app')  # Default to 'voting_app'

# Retry logic for database connection
def get_db_connection():
    attempts = 0
    while attempts < 5:
        try:
            # Attempt to connect to the database
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return conn
        except mysql.connector.errors.DatabaseError as e:
            print(f"Attempt {attempts + 1}: Database connection failed - {e}")
            attempts += 1
            time.sleep(5)  # Wait before retrying
    raise Exception("Database connection failed after multiple attempts.")

@app.route('/')
def index():
    try:
        # Try connecting to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        return str(users)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
