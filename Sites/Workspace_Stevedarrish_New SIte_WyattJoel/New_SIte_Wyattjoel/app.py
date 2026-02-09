import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
# Email notification imports
import smtplib
from email.message import EmailMessage
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://wyattjoel.com"}}, supports_credentials=True)
DB_PATH = '/tmp/inquiries.db'

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                topic TEXT,
                message TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {DB_PATH} and table 'inquiries' ensured with all columns.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

def send_email_notification(name, email, topic, message, submitted_at):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USER = 'steve@wyattjoel.com'
    SMTP_PASS = 'YOUR_APP_PASSWORD'
    TO_EMAIL = 'steve@wyattjoel.com'

    msg = EmailMessage()
    msg['Subject'] = f'New Inquiry from {name} ({email})'
    msg['From'] = SMTP_USER
    msg['To'] = TO_EMAIL
    msg.set_content(f'''
New inquiry received:

Name: {name}
Email: {email}
Topic: {topic}
Message: {message}
Submitted at: {submitted_at}
''')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
    except Exception as e:
        print('Failed to send email:', e)

@app.route('/inquiry', methods=['POST'])
def inquiry():
    print("Headers:", dict(request.headers))
    print("Raw data:", request.data)
    print("JSON:", request.get_json())
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    topic = data.get('topic', '')
    message = data.get('message', '')
    submitted_at = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO inquiries (name, email, topic, message, submitted_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, topic, message, submitted_at))
    conn.commit()
    conn.close()

    send_email_notification(name, email, topic, message, submitted_at)

    return jsonify({'status': 'success'}), 200

@app.route('/inquiries', methods=['GET'])
def get_inquiries():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, email, topic, message, submitted_at FROM inquiries ORDER BY submitted_at DESC')
    rows = c.fetchall()
    conn.close()
    inquiries = [
        {
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'topic': row[3],
            'message': row[4],
            'submitted_at': row[5]
        }
        for row in rows
    ]
    return jsonify(inquiries)

# Ensure DB is initialized only once using a global flag
db_initialized = False

@app.before_request
def initialize_database():
    global db_initialized
    if not db_initialized:
        init_db()
        db_initialized = True

if __name__ == '__main__':
    app.run(debug=True)