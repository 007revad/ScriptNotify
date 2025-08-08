#!/bin/bash

#########################################################################
# SamplePackage - System Information API CGI Handler                   #
# Provides system information only, no SMART functionality             #
#########################################################################

# Package configuration
PKG_NAME="Samplepackage"
PKG_ROOT="/var/packages/${PKG_NAME}"
TARGET_DIR="${PKG_ROOT}/target"
LOG_DIR="${PKG_ROOT}/var"
LOG_FILE="${LOG_DIR}/api.log"

# Create necessary directories
mkdir -p "${LOG_DIR}"
touch "${LOG_FILE}"
chmod 644 "${LOG_FILE}"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "${LOG_FILE}"
}

# HTTP headers
echo "Content-Type: application/json; charset=utf-8"
echo "Access-Control-Allow-Origin: *"
echo "Access-Control-Allow-Methods: GET, POST"
echo "Access-Control-Allow-Headers: Content-Type"
echo ""

# URL decode function
urldecode() { : "${*//+/ }"; echo -e "${_//%/\\x}"; }

declare -A PARAM

# Parse key-value pairs from URL encoded data
parse_kv() {
    local kv_pair key val
    IFS='&' read -ra kv_pair <<< "$1"
    for pair in "${kv_pair[@]}"; do
        IFS='=' read -r key val <<< "${pair}"
        key="$(urldecode "${key}")"
        val="$(urldecode "${val}")"
        PARAM["${key}"]="${val}"
    done
}

# Handle different HTTP methods
case "$REQUEST_METHOD" in
    POST)
        CONTENT_LENGTH=${CONTENT_LENGTH:-0}
        if [ "$CONTENT_LENGTH" -gt 0 ]; then
            read -r -n "$CONTENT_LENGTH" POST_DATA
        else
            POST_DATA=""
        fi
        parse_kv "${POST_DATA}"
        ;;
    GET)
        parse_kv "${QUERY_STRING}"
        ;;
    *)
        log "Unsupported HTTP method: ${REQUEST_METHOD}"
        echo '{"success":false,"message":"Unsupported HTTP method","result":null}'
        exit 0
        ;;
esac

ACTION="${PARAM[action]}"
log "API Request - Action: ${ACTION}"

# JSON utility functions
json_escape() {
    echo "$1" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'
}

json_response() {
    local success="$1" message="$2" data="$3"
    local msg_json=$(echo "$message" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))')
    
    if [ -z "$data" ]; then
        echo "{\"success\":$success, \"message\":$msg_json, \"result\":null}"
    else
        local data_json=$(json_escape "$data")
        echo "{\"success\":$success, \"message\":$msg_json, \"result\":$data_json}"
    fi
}

# Clean system string function
clean_system_string() {
    local input="$1"
    # Remove "unknown" strings and extra spaces
    input=$(echo "$input" | sed 's/ unknown//g; s/unknown //g; s/^unknown$//')
    input=$(echo "$input" | sed 's/  */ /g; s/^ *//; s/ *$//')
    
    if [ -z "$input" ] || [ "$input" = " " ]; then
        echo "N/A"
    else
        echo "$input"
    fi
}

# Get system information function
get_system_info() {
    local model platform productversion build version smallfix

    # Collect system information from various sources
    model="$(cat /proc/sys/kernel/syno_hw_version 2>/dev/null || echo '')"
    platform="$(/bin/get_key_value /etc.defaults/synoinfo.conf platform_name 2>/dev/null || echo '')"
    productversion="$(/bin/get_key_value /etc.defaults/VERSION productversion 2>/dev/null || echo '')"
    build="$(/bin/get_key_value /etc.defaults/VERSION buildnumber 2>/dev/null || echo '')"
    
    # Combine version and build
    if [ -n "$productversion" ] && [ -n "$build" ]; then
        version="${productversion}-${build}"
    else
        version="$productversion"
    fi
    
    smallfix="$(/bin/get_key_value /etc.defaults/VERSION smallfixnumber 2>/dev/null || echo '')"

    # Clean all strings
    model="$(clean_system_string "$model")"
    platform="$(clean_system_string "$platform")"
    version="$(clean_system_string "$version")"
    smallfix="$(clean_system_string "$smallfix")"

    # Generate JSON using Python3
    python3 -c "
import json
print(json.dumps({
    'MODEL': '$model',
    'PLATFORM': '$platform',
    'DSM_VERSION': '$version',
    'Update': '$smallfix'
}))
"
}

# Main action handler
case "${ACTION}" in
    info)
        log "[INFO] Processing system information request"
        DATA="$(get_system_info)"
        json_response true "System information retrieved successfully" "${DATA}"
        ;;
    *)
        log "[ERROR] Invalid action requested: ${ACTION}"
        json_response false "Invalid action: ${ACTION}" ""
        ;;
esac

exit 0
