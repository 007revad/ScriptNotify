#!/bin/bash

# Sample Package Runner Script
# This script serves as an example only - not used in production
# The package operates via web interface without background processes

PKG_ROOT="/var/packages/Samplepackage"
VAR_DIR="${PKG_ROOT}/var"
BIN_DIR="${PKG_ROOT}/target/bin"
LOG_FILE="${VAR_DIR}/sample_run.log"

# Create log directory if it doesn't exist
mkdir -p "${VAR_DIR}"

# Log function with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "${LOG_FILE}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Handle different execution modes
case "$1" in
    daemon)
        log_message "Sample daemon mode started (example only - not used in production)"
        # This is just an example - no actual daemon functionality
        while true; do
            sleep 60
            log_message "Sample daemon heartbeat (example only)"
        done
        ;;
    test)
        log_message "Sample test mode executed"
        echo "This is a sample script for testing purposes"
        echo "No actual processing is performed"
        ;;
    *)
        log_message "Sample script executed with parameter: $1"
        echo "Sample Package Runner Script"
        echo "This script serves as an example only"
        echo "Available modes: daemon, test"
        echo "Note: This package operates via web interface only"
        ;;
esac
