// SamplePackage System Information Display
// Handles system info loading and display only

document.addEventListener('DOMContentLoaded', () => {
    const systemInfo = document.getElementById('systemInfo');

    /**
     * API call function - simplified for system info only
     * @param {string} action - API action to perform  
     * @param {object} params - Additional parameters
     * @returns {Promise} - Promise resolving to JSON response
     */
    function callAPI(action, params = {}) {
        const urlParams = new URLSearchParams();
        urlParams.append('action', action);
        Object.keys(params).forEach(key => urlParams.append(key, params[key]));

        return fetch('api.cgi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: urlParams.toString()
        })
        .then(res => {
            if (!res.ok) throw new Error('Network response was not ok');
            return res.json();
        });
    }

    /**
     * Display system information in formatted grid layout
     * @param {object} infoObj - System information object
     */
    function displaySystemInfo(infoObj) {
        systemInfo.innerHTML = `
            <strong>MODEL:</strong> <span>${infoObj.MODEL || 'N/A'}</span>
            <strong>PLATFORM:</strong> <span>${infoObj.PLATFORM || 'N/A'}</span>
            <strong>DSM VERSION:</strong> <span>${infoObj.DSM_VERSION || 'N/A'}</span>
            <strong>UPTIME:</strong> <span>${infoObj.Update || 'N/A'}</span>
        `;
    }

    /**
     * Load system information from API
     * Updates the systemInfo element with current system data
     */
    function loadSystemInfo() {
        systemInfo.innerHTML = '<span class="loading">Loading system information...</span>';
        
        callAPI('info')
            .then(data => {
                if (data.success) {
                    let infoObj = {};
                    try {
                        infoObj = JSON.parse(data.result);
                    } catch (e) {
                        console.error('Failed to parse system info:', e);
                        systemInfo.innerHTML = '<span class="error">Failed to parse system information.</span>';
                        return;
                    }
                    displaySystemInfo(infoObj);
                } else {
                    systemInfo.innerHTML = `<span class="error">Failed to load system information: ${data.message || 'Unknown error'}</span>`;
                }
            })
            .catch(error => {
                systemInfo.innerHTML = `<span class="error">Error loading system information: ${error.message}</span>`;
                console.error('API Error:', error);
            });
    }

    // Initial load of system information
    loadSystemInfo();
    
    // Auto-refresh every 30 seconds
    setInterval(loadSystemInfo, 30000);
});
