from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
# Email notification imports
import smtplib
from email.message import EmailMessage
from flask_cors import CORS  # <-- Add this import

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://wyattjoel.com"}}, supports_credentials=True)  # <-- Enable CORS for your domain
DB_PATH = 'inquiries.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            topic TEXT,
            message TEXT,
            submitted_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def send_email_notification(name, email, topic, message, submitted_at):
    # Configure your SMTP server and credentials here
    SMTP_SERVER = 'smtp.gmail.com'  # e.g., 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USER = 'steve@wyattjoel.com'  # Your Gmail address
    SMTP_PASS = 'YOUR_APP_PASSWORD'    # Your Gmail app password
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
    print("Headers:", request.headers)
    print("Data:", request.data)
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

    # Send email notification
    send_email_notification(name, email, topic, message, submitted_at)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)