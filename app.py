import os
import smtplib
from email.message import EmailMessage

from flask import Flask, jsonify, redirect, request, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')
INQUIRY_RECIPIENTS = ('stevedarrish@gmail.com', 'steve@wyattjoel.com')


def send_inquiry_email(payload):
    smtp_host = os.getenv('SMTP_HOST', '').strip()
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER', '').strip()
    smtp_pass = os.getenv('SMTP_PASS', '')
    smtp_from = os.getenv('SMTP_FROM', smtp_user).strip()

    if not (smtp_host and smtp_user and smtp_pass and smtp_from):
        app.logger.warning('SMTP not configured. Inquiry email not sent.')
        return False

    name = payload.get('name', '(no name)')
    email = payload.get('email', '(no email)')
    topic = payload.get('topic', '(no topic)')
    message = payload.get('message', '')

    msg = EmailMessage()
    msg['Subject'] = f'New WyattJoel inquiry: {topic}'
    msg['From'] = smtp_from
    msg['To'] = ', '.join(INQUIRY_RECIPIENTS)
    msg.set_content(
        '\n'.join(
            [
                'A new inquiry was submitted from wyattjoel.com',
                '',
                f'Name: {name}',
                f'Email: {email}',
                f'Topic: {topic}',
                '',
                'Message:',
                message or '(empty)',
            ]
        )
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_pass)
        smtp.send_message(msg)

    return True


@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


@app.route('/insights.json')
def insights():
    return send_from_directory('.', 'insights.json')


@app.route('/inquiry', methods=['POST'])
def submit_inquiry():
    # Supports both HTML form posts and JSON API calls.
    payload = request.form.to_dict() if request.form else (request.get_json(silent=True) or {})

    app.logger.info('New inquiry received: %s', payload)
    try:
        sent = send_inquiry_email(payload)
    except Exception:
        app.logger.exception('Failed sending inquiry email')
        sent = False

    if request.form:
        return redirect(f'/?submitted=1&email_sent={int(sent)}#contact')

    return jsonify(
        {
            'status': 'success',
            'message': 'Inquiry received',
            'data': payload,
            'email_sent': sent,
        }
    ), 200


@app.route('/api/contact', methods=['POST'])
def api_contact():
    return submit_inquiry()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
