import requests
import smtplib

# Configuration
PROMETHEUS_URL = "http://10.198.24.252:9090"
GRAFANA_URL = "http://10.198.24.252:3000"
SMTP_SERVER = '10.23.225.37'
SENDER = 'cldm.devops@scbdev.com'
RECEIVER = 'indireddy.mohankrishnareddy@sc.com'
SUBJECT = 'Status of Monitoring Service'

# Function to send email
def send_email(subject, message):
    try:
        smtp_obj = smtplib.SMTP(SMTP_SERVER)
        email_message = f"From: {SENDER}\nTo: {RECEIVER}\nSubject: {subject}\n\n{message}"
        smtp_obj.sendmail(SENDER, RECEIVER, email_message)
        print("Mail sent")
    except Exception as e:
        print("Error: couldn't send the mail")
        print(e)

# Function to check service availability
def check_service(url, service_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{service_name} is up and running.")
            return None  # Service is up
        else:
            print(f"{service_name} is down. Status code: {response.status_code}")
            return f"{service_name} is down. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"{service_name} is down. Error: {e}")
        return f"{service_name} is down. Error: {e}"

# Check Prometheus and Grafana
prometheus_status = check_service(PROMETHEUS_URL, "Prometheus")
grafana_status = check_service(GRAFANA_URL, "Grafana")

# Send email if any service is down
if prometheus_status or grafana_status:
    message = ""
    if prometheus_status:
        message += f"Prometheus status: {prometheus_status}\n"
    if grafana_status:
        message += f"Grafana status: {grafana_status}\n"
    
    send_email(SUBJECT, message)
else:
    print("All services are running fine.")