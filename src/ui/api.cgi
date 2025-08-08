#!/bin/bash

####################################################################
# Sample Package – CGI API Handler                                #
# Provides system information via JSON API                        #
####################################################################

PKG_NAME="Samplepackage"
PKG_ROOT="/var/packages/${PKG_NAME}"
TARGET_DIR="${PKG_ROOT}/target"
LOG_DIR="${PKG_ROOT}/var"
LOG_FILE="${LOG_DIR}/api.log"

# Create necessary directories and files
mkdir -p "${LOG_DIR}"
touch "${LOG_FILE}"
chmod 644 "${LOG_FILE}"

# Send HTTP headers for JSON response
echo "Content-Type: application/json"
echo ""

# Read POST data from stdin
read POST_DATA

# Extract action parameter from POST data
ACTION=$(echo "$POST_DATA" | grep -o 'action=[^&]*' | cut -d= -f2)

# Log API request
echo "[$(date '+%Y-%m-%d %H:%M:%S')] API Request - Action: $ACTION" >> "${LOG_FILE}"

case "$ACTION" in
    "info")
        # Collect system information
        MODEL=$(cat /proc/sys/kernel/syno_hw_version 2>/dev/null || echo "Unknown")
        PLATFORM=$(uname -m 2>/dev/null || echo "Unknown")
        DSM_VERSION=$(cat /etc.defaults/VERSION 2>/dev/null | grep productversion | cut -d'"' -f4 || echo "Unknown")
        UPTIME=$(uptime | cut -d',' -f1 | cut -d' ' -f4- || echo "Unknown")
        
        # Return system information as JSON
        echo "{\"success\": true, \"result\": \"{\\\"MODEL\\\":\\\"$MODEL\\\",\\\"PLATFORM\\\":\\\"$PLATFORM\\\",\\\"DSM_VERSION\\\":\\\"$DSM_VERSION\\\",\\\"Update\\\":\\\"$UPTIME\\\"}\"}"
        ;;
    *)
        # Handle unknown actions
        echo "{\"success\": false, \"message\": \"Unknown action: $ACTION\"}"
        ;;
esac
