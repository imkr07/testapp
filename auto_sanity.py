import subprocess
import json
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to run ansible playbook and capture the output
def run_ansible_playbook(playbook_path, inventory_path, limit=None, tags=None):
    # Build the command to run the ansible playbook
    command = ['ansible-playbook', '-i', inventory_path, playbook_path]

    # Add limit (labels) if specified
    if limit:
        command.extend(['-l', limit])

    # Add tags if specified
    if tags:
        command.extend(['--tags', tags])

    # Run the ansible playbook using subprocess and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Print stdout and stderr for verification
    print(f"Playbook STDOUT:\n{result.stdout}")
    print(f"Playbook STDERR:\n{result.stderr}")

    # Write stdout and stderr to log files
    with open('ansible_stdout.log', 'w') as f_stdout:
        f_stdout.write(result.stdout)
    with open('ansible_stderr.log', 'w') as f_stderr:
        f_stderr.write(result.stderr)

    return result.stdout, result.stderr, result.returncode

# Function to parse the ansible output (as JSON) and structure it into a table
def parse_ansible_output(ansible_output):
    # Assuming ansible_output is in JSON format
    try:
        output_json = json.loads(ansible_output)
    except json.JSONDecodeError:
        print("Error: Output is not in valid JSON format.")
        return None
    
    # Prepare an empty list to hold the task data
    task_data = []

    # Iterate over the playbook results
    for play in output_json['plays']:
        for task in play['tasks']:
            task_name = task['task']['name']
            status = task['host']['status']
            description = task.get('host', {}).get('msg', 'No description available')
            comment = task.get('result', {}).get('msg', 'No additional comments')

            # Append the task data as a dictionary
            task_data.append({
                "Task Name": task_name,
                "Description": description,
                "Status": status,
                "Comments": comment
            })

    return task_data

# Function to generate a tabular report and return it as a string
def generate_table(task_data):
    if not task_data:
        return "No data available to display in table."
    
    df = pd.DataFrame(task_data)
    return df.to_string(index=False)

# Function to send an email with the playbook result
def send_email(subject, body, to_email, from_email, smtp_server):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server) as server:
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    # Define variables
    playbook_path = '/colt/Kaviya/Colt_Sanity/gb-devops-app-deploy/cc_service.yml'
    inventory_path = '/colt/Kaviya/Colt_Sanity/gb-devops-app-deploy/non-prod'
    to_email = 'aravind.tv@sc.com'
    #to_email = 'CLDM-ITO-DevOps@sc.com'
    from_email = 'cldm.devops@scbdev.com'
    smtp_server = '10.23.225.37'  # Specify your SMTP server IP address
    limit = 'colt-lb-02-fbservers'  # Specify your label here
    tags = 'health_check_fb'  # Specify your tags here (comma-separated if multiple)

    # Step 1: Run the Ansible playbook
    stdout, stderr, returncode = run_ansible_playbook(playbook_path, inventory_path, limit, tags)

    # Step 2: Parse the output into task data
    task_data = parse_ansible_output(stdout)

    # Step 3: Generate and display the result table
    result_table = generate_table(task_data)

    # Step 4: Determine if an alert needs to be sent based on the output
    if returncode != 0:
        subject = 'Ansible Playbook Execution Failed'
    else:
        subject = 'Ansible Playbook Execution Succeeded'

    # The body of the email contains both the output and the tabular report
    body = f"Ansible playbook resulted in the following output:\n\n{stdout}\n\nTabular Report:\n{result_table}"

    # Step 5: Send the email
    send_email(subject, body, to_email, from_email, smtp_server)

if __name__ == '__main__':
    main()