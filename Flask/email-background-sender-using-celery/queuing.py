from flask import Flask, jsonify, request
from celery import Celery

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Define a Celery task
@celery.task
def send_async_email(email_data):
    # Simulate email sending
    print(f"Sending email to {email_data['to']} with subject '{email_data['subject']}'")
    # Here you would implement the actual email sending logic
    return {'status': 'Email sent successfully!'}

@app.route('/send_email', methods=['POST'])
def send_email():
    email_data = request.get_json()
    # Send the email asynchronously
    result = send_async_email.delay(email_data)
    print("Task ID:", result.id)
    return jsonify({"message": "Sending email in the background"}), 202

if __name__ == '__main__':
    app.run(debug=True)
