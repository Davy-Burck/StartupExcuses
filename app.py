import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT'),
        sslmode='require'
    )
    return conn

# Créer la table si elle n'existe pas
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS excuses (
            id SERIAL PRIMARY KEY,
            excuse TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT excuse FROM excuses;')
    excuses = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', excuses=excuses)

@app.route('/add', methods=['POST'])
def add():
    new_excuse = request.form.get('excuse')
    if new_excuse:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO excuses (excuse) VALUES (%s);', (new_excuse,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
