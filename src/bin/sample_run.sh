#!/bin/bash

# Setting
PKG_ROOT="/var/packages/Samplepackage"
VAR_DIR="${PKG_ROOT}/var"
BIN_DIR="${PKG_ROOT}/target/bin"

# Make log dir
mkdir -p "${VAR_DIR}"

# Log Function
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "${LOG_FILE}"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

