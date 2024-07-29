import requests
import smtplib

# Configuration
PROMETHEUS_URL = "https://your.prometheus.url"  # Replace with your Prometheus URL
GRAFANA_URL = "http://your.grafana.url"         # Replace with your Grafana URL
AUTH_SERVER_URL = "https://auth.example.com/token"  # Replace with your OAuth2 token endpoint
AUTH_CODE = 'your_authorization_code'           # Replace with your actual authorization code
CLIENT_ID = 'your_client_id'                    # Replace with your actual client ID
CLIENT_SECRET = 'your_client_secret'            # Replace with your actual client secret
REDIRECT_URI = 'https://your.redirect.uri/callback'  # Replace with your redirect URI
PROMETHEUS_USER = 'your_prometheus_username'    # Replace with your Prometheus username
PROMETHEUS_PASSWORD = 'your_prometheus_password'# Replace with your Prometheus password
SMTP_SERVER = '10.23.225.37'
SMTP_PORT = 25
SENDER = 'cldm.devops@scbdev.com'
RECEIVERS = ['indireddy.mohankrishnareddy@sc.com', 'second.email@example.com']
SUBJECT = 'Status of Monitoring Service'

# Function to get access token using the authorization code
def get_access_token():
    try:
        response = requests.post(
            AUTH_SERVER_URL,
            data={
                'grant_type': 'authorization_code',
                'code': AUTH_CODE,
                'redirect_uri': REDIRECT_URI,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            }
        )
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data['access_token']
        print("Access token obtained successfully.")
        return access_token
    except requests.exceptions.RequestException as e:
        print("Error obtaining access token:", e)
        return None

# Function to send email
def send_email(subject, message):
    try:
        smtp_obj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_obj.starttls()
        # smtp_obj.login('your_email', 'your_password')  # Uncomment if login is required
        email_message = f"From: {SENDER}\nTo: {', '.join(RECEIVERS)}\nSubject: {subject}\n\n{message}"
        smtp_obj.sendmail(SENDER, RECEIVERS, email_message)
        smtp_obj.quit()
        print("Mail sent successfully.")
    except Exception as e:
        print("Error: couldn't send the mail")
        print(e)

# Function to check service availability with Basic Authentication
def check_service(url, service_name, headers=None, auth=None, verify_ssl=True):
    try:
        response = requests.get(url, headers=headers, auth=auth, verify=verify_ssl)
        if response.status_code == 200:
            print(f"{service_name} is up and running.")
            return service_name, "UP"
        else:
            print(f"{service_name} is down. Status code: {response.status_code}")
            return service_name, "DOWN"
    except requests.exceptions.SSLError as ssl_err:
        print(f"{service_name} SSL error: {ssl_err}")
        return service_name, "SSL_ERROR"
    except requests.exceptions.RequestException as e:
        print(f"{service_name} is down. Error: {e}")
        return service_name, "DOWN"

# Get the access token
access_token = get_access_token()

# If access token is obtained, proceed with checking services
if access_token:
    # Prepare headers for Prometheus with Bearer Token
    prometheus_headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Check Prometheus and Grafana
    services = [
        check_service(PROMETHEUS_URL, "Prometheus", headers=prometheus_headers, auth=(PROMETHEUS_USER, PROMETHEUS_PASSWORD), verify_ssl=True),
        check_service(GRAFANA_URL, "Grafana", verify_ssl=False)
    ]

    # Prepare data for table
    table_data = [["Service", "Status"]]
    for service in services:
        table_data.append([service[0], service[1]])

    # Create the table as a string
    table = ""
    for row in table_data:
        table += "{:<20} {:<10}\n".format(*row)

    # Print the table to console
    print(table)

    # Send email only if any service is down or there is an SSL error
    down_services = [service for service in services if service[1] in ["DOWN", "SSL_ERROR"]]
    if down_services:
        message = "The following services are down or have SSL issues:\n\n"
        message += table
        message += "\n\nPlease investigate immediately."
        
        print("Sending email...")
        send_email(SUBJECT, message)
    else:
        print("All services are running fine.")
else:
    print("Failed to obtain access token. Exiting script.")