from flask import Flask, render_template, request, redirect
import mysql.connector
import os
import time

app = Flask(__name__)

def get_db_connection(retries=5, delay=5):
    for attempt in range(retries):
        try:
            return mysql.connector.connect(
                host=os.environ['DB_HOST'],
                user=os.environ['DB_USER'],
                password=os.environ['DB_PASSWORD'],
                database=os.environ['DB_NAME']
            )
        except mysql.connector.Error as err:
            print(f"Attempt {attempt + 1}: Failed to connect to DB - {err}")
            time.sleep(delay)
    raise Exception("Database connection failed after multiple attempts.")

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT team, COUNT(*) FROM votes GROUP BY team")
    votes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', votes=votes)

@app.route('/vote', methods=['POST'])
def vote():
    team = request.form['team']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO votes (team) VALUES (%s)", (team,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
