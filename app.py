from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# Read environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'voting_app')

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT team, COUNT(*) as votes FROM votes GROUP BY team")
    vote_counts = cursor.fetchall()
    conn.close()
    return render_template('index.html', vote_counts=vote_counts)

@app.route('/vote', methods=['POST'])
def vote():
    team = request.form.get('team')
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password or not team:
        return "Missing information", 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if user exists or register
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        user_id = cursor.lastrowid
    else:
        if user['password'] != password:
            conn.close()
            return "Incorrect password", 401
        user_id = user['id']

    # Record vote
    cursor.execute("INSERT INTO votes (user_id, team) VALUES (%s, %s)", (user_id, team))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
