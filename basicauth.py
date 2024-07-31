import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
PROMETHEUS_URL = "https://prometheus.example.com:9090"  # Update with your Prometheus URL
GRAFANA_URL = "http://grafana.example.com:3000"         # Update with your Grafana URL
PROMETHEUS_USERNAME = "your_prometheus_username"
PROMETHEUS_PASSWORD = "your_prometheus_password"

EMAIL_HOST = 'smtp.example.com'  # Update with your SMTP server
EMAIL_PORT = 25                 # Default port for SMTP without TLS
EMAIL_USER = 'your-email@example.com'
EMAIL_TO = ['alert-recipient@example.com']
EMAIL_SUBJECT = 'Service Down Alert: Monitoring'

# Function to send email alerts
def send_email_alert(subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = ', '.join(EMAIL_TO)
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Connect to SMTP server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        
        # Uncomment the next two lines if your SMTP server requires login
        # server.login(EMAIL_USER, EMAIL_PASS)

        # Send email
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        server.quit()

        print("Email alert sent successfully.")
    except Exception as e:
        print(f"Failed to send email alert: {e}")

# Function to check Prometheus
def check_prometheus():
    try:
        response = requests.get(
            PROMETHEUS_URL,
            auth=(PROMETHEUS_USERNAME, PROMETHEUS_PASSWORD),
            timeout=10,
            verify=False  # Disable SSL verification
        )
        if response.status_code == 200:
            print(f"Prometheus is up and running. Status code: {response.status_code}")
            return True
        else:
            print(f"Prometheus is down. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Prometheus: {e}")
        return False

# Function to check Grafana
def check_grafana():
    try:
        response = requests.get(GRAFANA_URL, timeout=10)
        if response.status_code == 200:
            print(f"Grafana is up and running. Status code: {response.status_code}")
            return True
        else:
            print(f"Grafana is down. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Grafana: {e}")
        return False

# Main monitoring function
def monitor_services():
    prometheus_status = check_prometheus()
    grafana_status = check_grafana()

    if not prometheus_status or not grafana_status:
        alert_message = "ALERT: The following services are down:\n"
        if not prometheus_status:
            alert_message += "- Prometheus\n"
        if not grafana_status:
            alert_message += "- Grafana\n"
        
        send_email_alert(EMAIL_SUBJECT, alert_message)
    else:
        print("All services are up and running smoothly.")

# Start monitoring
if __name__ == "__main__":
    monitor_services()





import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
PROMETHEUS_URL = "https://prometheus.example.com:9090"  # Change to your Prometheus URL
GRAFANA_URL = "http://grafana.example.com:3000"        # Change to your Grafana URL
PROMETHEUS_USERNAME = "your_prometheus_username"
PROMETHEUS_PASSWORD = "your_prometheus_password"

EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USER = 'your-email@example.com'
EMAIL_PASS = 'your-email-password'
EMAIL_TO = ['alert-recipient@example.com']
EMAIL_SUBJECT = 'Service Down Alert: Monitoring'

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

# Function to check Prometheus
def check_prometheus():
    try:
        response = requests.get(PROMETHEUS_URL, auth=(PROMETHEUS_USERNAME, PROMETHEUS_PASSWORD), timeout=10, verify=True)
        if response.status_code == 200:
            print(f"Prometheus is up and running. Status code: {response.status_code}")
            return True
        else:
            print(f"Prometheus is down. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Prometheus: {e}")
        return False

# Function to check Grafana
def check_grafana():
    try:
        response = requests.get(GRAFANA_URL, timeout=10)
        if response.status_code == 200:
            print(f"Grafana is up and running. Status code: {response.status_code}")
            return True
        else:
            print(f"Grafana is down. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Grafana: {e}")
        return False

# Main monitoring function
def monitor_services():
    prometheus_status = check_prometheus()
    grafana_status = check_grafana()

    if not prometheus_status or not grafana_status:
        alert_message = "ALERT: The following services are down:\n"
        if not prometheus_status:
            alert_message += "- Prometheus\n"
        if not grafana_status:
            alert_message += "- Grafana\n"
        
        send_email_alert(EMAIL_SUBJECT, alert_message)
    else:
        print("All services are up and running smoothly.")

# Start monitoring
if __name__ == "__main__":
    monitor_services()