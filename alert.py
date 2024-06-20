import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuration
PROMETHEUS_URL = 'http://your-prometheus-url:9090'
GRAFANA_URL = 'http://your-grafana-url:3000'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_ADDRESS = 'your-email@example.com'
EMAIL_PASSWORD = 'your-email-password'
TO_EMAIL = 'recipient@example.com'

def send_email_alert(subject, message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_service_availability(url, service_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{service_name} is up and running.")
        else:
            print(f"{service_name} returned status code {response.status_code}")
            send_email_alert(f"{service_name} Alert", f"{service_name} is down. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to reach {service_name}: {e}")
        send_email_alert(f"{service_name} Alert", f"Failed to reach {service_name}. Error: {e}")

def main():
    check_service_availability(PROMETHEUS_URL, "Prometheus")
    check_service_availability(GRAFANA_URL, "Grafana")

if __name__ == "__main__":
    main()