import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
URL = "https://your-website.com"
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USER = 'your-email@example.com'
EMAIL_PASS = 'your-email-password'
EMAIL_TO = ['alert-recipient@example.com']
EMAIL_SUBJECT = 'Service Down Alert: HTTPS Monitoring'

# Function to send email alerts
def send_email_alert(subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = ', '.join(EMAIL_TO)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.quit()

        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

# Function to check HTTPS connection
def check_https_connection(url):
    try:
        response = requests.get(url, timeout=10, verify=True)  # Set timeout to 10 seconds
        if response.status_code == 200:
            print(f"Connection to {url} is successful. Status code: {response.status_code}")
            return True
        else:
            print(f"Connection to {url} failed. Status code: {response.status_code}")
            return False

    except requests.exceptions.SSLError as ssl_error:
        print(f"SSL error occurred: {ssl_error}")
        return False

    except requests.exceptions.ConnectionError as conn_error:
        print(f"Connection error occurred: {conn_error}")
        return False

    except requests.exceptions.Timeout:
        print("The request timed out.")
        return False

    except requests.exceptions.RequestException as req_error:
        print(f"An error occurred: {req_error}")
        return False

# Main monitoring function
def monitor_https_service(url):
    service_up = check_https_connection(url)
    if not service_up:
        alert_message = f"ALERT: Service at {url} is down."
        send_email_alert(EMAIL_SUBJECT, alert_message)
    else:
        print("Service is up and running smoothly.")

# Start monitoring
if __name__ == "__main__":
    monitor_https_service(URL)