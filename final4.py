import requests
import smtplib
from datetime import datetime

# Configuration
PROMETHEUS_URL = "http://10.198.24.252:9090"
GRAFANA_URL = "http://10.198.24.252:3000"
SMTP_SERVER = '10.23.225.37'
SENDER = 'cldm.devops@scbdev.com'
RECEIVERS = ['indireddy.mohankrishnareddy@sc.com', 'second.email@example.com']
SUBJECT = 'Status of Monitoring Service'

# Function to send email
def send_email(subject, message):
    try:
        smtp_obj = smtplib.SMTP(SMTP_SERVER)
        email_message = f"From: {SENDER}\nTo: {', '.join(RECEIVERS)}\nSubject: {subject}\n\n{message}"
        smtp_obj.sendmail(SENDER, RECEIVERS, email_message)
        smtp_obj.quit()
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
            return service_name, "UP"
        else:
            print(f"{service_name} is down. Status code: {response.status_code}")
            return service_name, "DOWN"
    except requests.exceptions.RequestException as e:
        print(f"{service_name} is down. Error: {e}")
        return service_name, "DOWN"

# Check Prometheus and Grafana
services = [
    check_service(PROMETHEUS_URL, "Prometheus"),
    check_service(GRAFANA_URL, "Grafana")
]

# Prepare data for table
table_data = [["Service", "Status"]]
for service in services:
    table_data.append([service[0], service[1]])

# Create the table as a string
table = ""
for row in table_data:
    table += "{:<20} {:<6}\n".format(*row)

# Print the table to console
print(table)

# Send email with the table content
message = "Status of Monitoring Services:\n\n"
message += table
message += "\n\nPlease review the status."

print("Sending email...")
send_email(SUBJECT, message)