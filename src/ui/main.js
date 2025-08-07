document.addEventListener('DOMContentLoaded', () => {
    const optionSelect = document.getElementById('optionSelect');
    const runBtn = document.getElementById('runBtn');
    const status = document.getElementById('status');
    const output = document.getElementById('output');
    const systemInfo = document.getElementById('systemInfo');

    function parseSystemInfo(data) {
        if (!data) return {};
        const info = {};
        data.split('\n').forEach(line => {
            const colonIndex = line.indexOf(': ');
            if (colonIndex !== -1) {
                const key = line.substring(0, colonIndex).trim();
                const value = line.substring(colonIndex + 2).trim();
                info[key] = value;
            }
        });
        return info;
    }

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

    function loadSystemInfo() {
        systemInfo.innerHTML = '<span style="color: #0066cc;">Loading system information...</span>';

        callAPI('info')
            .then(data => {
                if (data.success) {
                    let infoObj = {};
                    try {
                        infoObj = JSON.parse(data.result);
                    } catch (e) {
                        console.error('Failed to parse system info:', e);
                    }
                    systemInfo.innerHTML = `
                        <strong>MODEL:</strong> <span>${infoObj.MODEL || 'N/A'}</span>
                        <strong>PLATFORM:</strong> <span>${infoObj.PLATFORM || 'N/A'}</span>
                        <strong>DSM_VERSION:</strong> <span>${infoObj.DSM_VERSION || 'N/A'}</span>
                        <strong>Update:</strong> <span>${infoObj.Update || 'N/A'}</span>
                    `;
                } else {
                    systemInfo.innerHTML = `<span style="color: red;">Failed to load system information: ${data.message || 'Unknown error'}</span>`;
                }
            })
            .catch(error => {
                systemInfo.innerHTML = `<span style="color: red;">Error loading system information: ${error.message}</span>`;
            });
    }

    loadSystemInfo();
});
//
