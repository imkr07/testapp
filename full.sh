#!/bin/bash

# Configuration
PROMETHEUS_URL="http://10.198.24.252:9090"
GRAFANA_URL="http://10.198.24.252:3000"
EMAIL_FROM="cldm.devops@scbdev.com"
EMAIL_TO="CLOM-ITO-DevOps@sc.com"
EMAIL_SUBJECT="Status of the monitoring services"

# Function to send email alert
send_email_alert() {
    local service_name=$1
    local message=$2

    # Check if mail is installed
    if ! command -v mail &> /dev/null; then
        echo "mail command not found. Please install mailutils (Debian/Ubuntu) or mailx (Red Hat/CentOS)."
        exit 1
    fi

    echo "$message" | mail -s "$EMAIL_SUBJECT: $service_name" "$EMAIL_TO" -- -f "$EMAIL_FROM"
}

# Function to check HTTP status using curl
check_http_status() {
    local url=$1
    local service_name=$2
    local response_code
    response_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if [ "$response_code" -eq 200 ]; then
        echo "$service_name HTTP status: OK"
    else
        echo "$service_name HTTP status: DOWN (Status code: $response_code)"
        send_email_alert "$service_name" "$service_name is down. Status code: $response_code"
    fi
}

# Function to check HTTP status using wget
check_with_wget() {
    local url=$1
    local service_name=$2
    if wget --spider -S "$url" 2>&1 | grep "HTTP/1.1 200 OK"; then
        echo "$service_name is up and running (checked with wget)."
    else
        echo "$service_name is down (checked with wget)."
        send_email_alert "$service_name" "$service_name is down (checked with wget)."
    fi
}

# Function to check port using netcat (nc)
check_with_nc() {
    local host=$1
    local port=$2
    local service_name=$3
    if nc -zv "$host" "$port"; then
        echo "$service_name is up and running (checked with nc)."
    else
        echo "$service_name is down (checked with nc)."
        send_email_alert "$service_name" "$service_name is down (checked with nc)."
    fi
}

# Function to check port using telnet
check_with_telnet() {
    local host=$1
    local port=$2
    local service_name=$3
    if echo "quit" | telnet "$host" "$port" 2>&1 | grep "Connected to"; then
        echo "$service_name is up and running (checked with telnet)."
    else
        echo "$service_name is down (checked with telnet)."
        send_email_alert "$service_name" "$service_name is down (checked with telnet)."
    fi
}

# Extract host and port from URL
PROMETHEUS_HOST=$(echo $PROMETHEUS_URL | awk -F[/:] '{print $4}')
PROMETHEUS_PORT=$(echo $PROMETHEUS_URL | awk -F[/:] '{print $5}')
GRAFANA_HOST=$(echo $GRAFANA_URL | awk -F[/:] '{print $4}')
GRAFANA_PORT=$(echo $GRAFANA_URL | awk -F[/:] '{print $5}')

# Check Prometheus and Grafana using different methods
echo "Checking Prometheus..."
check_http_status "$PROMETHEUS_URL" "Prometheus"
check_with_wget "$PROMETHEUS_URL" "Prometheus"
check_with_nc "$PROMETHEUS_HOST" "$PROMETHEUS_PORT" "Prometheus"
check_with_telnet "$PROMETHEUS_HOST" "$PROMETHEUS_PORT" "Prometheus"

echo "Checking Grafana..."
check_http_status "$GRAFANA_URL" "Grafana"
check_with_wget "$GRAFANA_URL" "Grafana"
check_with_nc "$GRAFANA_HOST" "$GRAFANA_PORT" "Grafana"
check_with_telnet "$GRAFANA_HOST" "$GRAFANA_PORT" "Grafana"