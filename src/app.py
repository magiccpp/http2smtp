from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import os

load_dotenv()

app = Flask(__name__)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'your.smtp.server.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 25))
FROM_EMAIL = os.getenv('FROM_EMAIL', 'llm@example.com')

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    to_email = data.get('recipient')
    subject = data.get('subject')
    message = data.get('body')
    
    if not all([to_email, subject, message]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())

        return jsonify({'success': 'Email sent'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

