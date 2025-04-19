from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Get environment variables for MySQL connection
DB_HOST = os.environ.get("DB_HOST", "mysql")  # Default to 'mysql' if not set
DB_USER = os.environ.get("DB_USER", "voteuser")  # Default to 'voteuser'
DB_PASSWORD = os.environ.get("DB_PASSWORD", "votepassword")  # Default to 'votepassword'
DB_NAME = os.environ.get("DB_NAME", "voting_app")  # Default to 'voting_app'

# Retry logic for database connection
def get_db_connection():
    attempts = 0
    while attempts < 5:
        try:
            print(f"Attempt {attempts + 1} to connect to MySQL at {DB_HOST}:3306...")
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            print(f"Successfully connected to MySQL at {DB_HOST}:3306")
            return conn
        except mysql.connector.errors.DatabaseError as e:
            print(f"Attempt {attempts + 1}: Database connection failed - {e}")
            attempts += 1
            time.sleep(5)  # Wait before retrying
    raise Exception("Database connection failed after multiple attempts.")

# Initialize the DB connection
db = get_db_connection()
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    if 'username' in session:
        return redirect('/vote')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, passwd))
        user = cursor.fetchone()
        if user:
            session['username'] = uname
            session['user_id'] = user['id']
            return redirect('/vote')
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        passwd = request.form['password']
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (uname, passwd))
            db.commit()
            return redirect('/login')
        except mysql.connector.errors.IntegrityError:
            return render_template('signup.html', error='Username already exists!')
    return render_template('signup.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'username' not in session:
        return redirect('/login')

    if request.method == 'POST':
        team = request.form['team']
        user_id = session['user_id']
        cursor.execute("INSERT INTO votes (user_id, team) VALUES (%s, %s)", (user_id, team))
        db.commit()
        return redirect('/results')
    return render_template('vote.html')

@app.route('/results')
def results():
    if 'username' not in session:
        return redirect('/login')

    cursor.execute("SELECT team, COUNT(*) as count FROM votes GROUP BY team")
    vote_data = cursor.fetchall()
    vote_result = {row['team']: row['count'] for row in vote_data}
    return render_template('result.html', votes=vote_result)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
