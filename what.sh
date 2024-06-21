#!/bin/bash

PROMETHEUS_URL="http://your-prometheus-url:9090"
GRAFANA_URL="http://your-grafana-url:3000"

# Check using wget
check_with_wget() {
    local url=$1
    if wget --spider -S "$url" 2>&1 | grep "HTTP/1.1 200 OK"; then
        echo "$url is up and running (checked with wget)."
    else
        echo "$url is down (checked with wget)."
    fi
}

# Check using netcat
check_with_nc() {
    local host=$1
    local port=$2
    if nc -zv "$host" "$port"; then
        echo "$host:$port is up and running (checked with nc)."
    else
        echo "$host:$port is down (checked with nc)."
    fi
}

# Check using telnet
check_with_telnet() {
    local host=$1
    local port=$2
    if echo "quit" | telnet "$host" "$port" 2>&1 | grep "Connected to"; then
        echo "$host:$port is up and running (checked with telnet)."
    else
        echo "$host:$port is down (checked with telnet)."
    fi
}

# Extract host and port from URL
PROMETHEUS_HOST=$(echo $PROMETHEUS_URL | awk -F[/:] '{print $4}')
PROMETHEUS_PORT=$(echo $PROMETHEUS_URL | awk -F[/:] '{print $5}')
GRAFANA_HOST=$(echo $GRAFANA_URL | awk -F[/:] '{print $4}')
GRAFANA_PORT=$(echo $GRAFANA_URL | awk -F[/:] '{print $5}')

# Check Prometheus and Grafana
check_with_wget "$PROMETHEUS_URL"
check_with_nc "$PROMETHEUS_HOST" "$PROMETHEUS_PORT"
check_with_telnet "$PROMETHEUS_HOST" "$PROMETHEUS_PORT"

check_with_wget "$GRAFANA_URL"
check_with_nc "$GRAFANA_HOST" "$GRAFANA_PORT"
check_with_telnet "$GRAFANA_HOST" "$GRAFANA_PORT"