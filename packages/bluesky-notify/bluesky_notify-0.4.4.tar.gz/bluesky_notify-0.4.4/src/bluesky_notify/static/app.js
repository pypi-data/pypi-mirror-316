// Constants and Utilities
const BSKY_BASE_URL = 'https://bsky.app/profile/';
const API_BASE_URL = '/api';
const REFRESH_INTERVAL = 5000; // 5 seconds

// Check if the browser supports passive event listeners
let supportsPassive = false;
try {
    window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
        get: function () { supportsPassive = true; }
    }));
} catch(e) {}

// Add passive event listeners for better scrolling performance
document.addEventListener('touchstart', function(){}, supportsPassive ? {passive: true} : false);
document.addEventListener('touchmove', function(){}, supportsPassive ? {passive: true} : false);
document.addEventListener('wheel', function(){}, supportsPassive ? {passive: true} : false);

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadAccounts();
    startPeriodicRefresh();
    
    // Add account form submission
    const addAccountForm = document.getElementById('addAccountForm');
    if (addAccountForm) {
        addAccountForm.addEventListener('submit', handleAddAccount);
    }
});

// Toast notification handler
function showNotification(message, type = 'success') {
    const toastEl = document.getElementById('toast');
    const toastBody = toastEl.querySelector('.toast-body');
    const toastTitle = toastEl.querySelector('.toast-header strong');
    
    toastTitle.textContent = type.charAt(0).toUpperCase() + type.slice(1);
    toastBody.textContent = message;
    
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

// Load and display accounts
async function loadAccounts() {
    try {
        const response = await fetch(`${API_BASE_URL}/accounts`);
        if (!response.ok) {
            throw new Error('Failed to load accounts');
        }
        
        const data = await response.json();
        const accounts = data.accounts || [];
        const accountsTable = document.getElementById('accountsTable');
        accountsTable.innerHTML = '';
        
        if (accounts.length === 0) {
            accountsTable.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center text-muted">
                        No accounts added yet. Add an account above to start monitoring.
                    </td>
                </tr>
            `;
            return;
        }
        
        accounts.forEach(account => {
            const row = document.createElement('tr');
            row.dataset.handle = account.handle;
            
            // Account info cell
            const accountCell = document.createElement('td');
            accountCell.innerHTML = `
                <div class="d-flex align-items-center">
                    <div>
                        <div class="fw-bold"><a href="${BSKY_BASE_URL}${account.handle}" target="_blank">${account.display_name || account.handle}</a></div>
                        <div class="text-muted">@${account.handle}</div>
                    </div>
                </div>
            `;
            
            // Status cell
            const statusCell = document.createElement('td');
            statusCell.innerHTML = `
                <span class="badge ${account.is_active ? 'bg-success' : 'bg-secondary'}">
                    ${account.is_active ? 'Active' : 'Inactive'}
                </span>
            `;
            
            // Desktop notifications cell
            const desktopCell = document.createElement('td');
            const desktopEnabled = account.notification_preferences?.desktop ?? false;
            desktopCell.innerHTML = `
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" role="switch" data-type="desktop" 
                           ${desktopEnabled ? 'checked' : ''} 
                           onchange="toggleNotification('${account.handle}', 'desktop', this.checked)">
                </div>
            `;
            
            // Email notifications cell
            const emailCell = document.createElement('td');
            const emailEnabled = account.notification_preferences?.email ?? false;
            emailCell.innerHTML = `
                <div class="form-check form-switch">
                    <input class="form-check-input" type="checkbox" role="switch" data-type="email" 
                           ${emailEnabled ? 'checked' : ''} 
                           onchange="toggleNotification('${account.handle}', 'email', this.checked)">
                </div>
            `;
            
            // Actions cell
            const actionsCell = document.createElement('td');
            actionsCell.innerHTML = `
                <button class="btn btn-sm btn-outline-danger" onclick="removeAccount('${account.handle}')">
                    <i class="bi bi-trash"></i>
                </button>
            `;
            
            row.appendChild(accountCell);
            row.appendChild(statusCell);
            row.appendChild(desktopCell);
            row.appendChild(emailCell);
            row.appendChild(actionsCell);
            
            accountsTable.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading accounts:', error);
        const accountsTable = document.getElementById('accountsTable');
        accountsTable.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-danger">
                    Error loading accounts. Please try again later.
                </td>
            </tr>
        `;
    }
}

// Add account handler
async function handleAddAccount(event) {
    event.preventDefault();
    const form = event.target;
    let handleValue = form.querySelector('#handle').value.trim();
    const desktopNotif = form.querySelector('#desktopNotif').checked;
    const emailNotif = form.querySelector('#emailNotif').checked;

    // Remove @ if present and clean invisible characters
    if (handleValue.startsWith('@')) {
        handleValue = handleValue.substring(1);
    }
    // Clean invisible characters and normalize
    handleValue = handleValue.replace(/[\u200B-\u200D\u202A-\u202E\uFEFF]/g, '').normalize();

    // Basic handle validation
    if (!handleValue) {
        showNotification('Please enter a Bluesky handle', 'error');
        return;
    }

    // Validate handle format (simplified regex)
    const handleRegex = /^[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9](\.[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])*$/;
    if (!handleRegex.test(handleValue)) {
        showNotification('Please enter a valid Bluesky handle (e.g., user.bsky.social)', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/accounts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                handle: handleValue,
                desktop: desktopNotif,
                email: emailNotif
            })
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to add account');
        }

        form.querySelector('#handle').value = '';
        await loadAccounts();
        showNotification('Account added successfully');
    } catch (error) {
        console.error('Error adding account:', error);
        showNotification(error.message || 'Failed to add account', 'error');
    }
}

// Toggle notification preferences
async function toggleNotification(handle, type, enabled) {
    try {
        const response = await fetch(`${API_BASE_URL}/accounts/${handle}/preferences`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                [type]: enabled
            }),
        });
        
        if (!response.ok) {
            throw new Error('Failed to update preferences');
        }
        
        loadAccounts();
    } catch (error) {
        console.error('Error updating preferences:', error);
        alert('Failed to update notification preferences');
    }
}

// Remove account
async function removeAccount(handle) {
    if (!confirm(`Are you sure you want to stop monitoring @${handle}?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/accounts/${handle}`, {
            method: 'DELETE',
        });
        
        if (!response.ok) {
            throw new Error('Failed to remove account');
        }
        
        loadAccounts();
    } catch (error) {
        console.error('Error removing account:', error);
        alert('Failed to remove account');
    }
}

// Start periodic refresh
function startPeriodicRefresh() {
    setInterval(loadAccounts, REFRESH_INTERVAL);
}

// WebSocket connection for real-time notifications
let ws;
let wsRetryCount = 0;
const MAX_RETRIES = 5;

// Check if we're running in Docker by looking at the hostname
// Docker containers will have a hostname that's different from localhost/127.0.0.1
const isDocker = !['localhost', '127.0.0.1'].includes(window.location.hostname);

// Only initialize WebSocket and request notification permission in Docker
if (isDocker) {
    // Request notification permission on page load
    if ("Notification" in window) {
        if (Notification.permission !== "granted" && Notification.permission !== "denied") {
            Notification.requestPermission().then(function (permission) {
                if (permission === "granted") {
                    console.log("Notification permission granted");
                }
            });
        }
    }

    // Initialize WebSocket connection
    function connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        ws = new WebSocket(wsUrl);
        
        ws.onopen = function() {
            console.log('WebSocket connected');
            wsRetryCount = 0;
        };
        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type === 'notification' && Notification.permission === "granted") {
                const notification = new Notification(data.title, {
                    body: data.message
                });
                
                notification.onclick = function() {
                    window.open(data.url, '_blank');
                    notification.close();
                };
            }
        };
        
        ws.onclose = function() {
            console.log('WebSocket disconnected');
            if (wsRetryCount < MAX_RETRIES) {
                wsRetryCount++;
                setTimeout(connectWebSocket, 1000 * Math.pow(2, wsRetryCount));
            }
        };
        
        ws.onerror = function(error) {
            console.error('WebSocket error:', error);
        };
    }

    // Start WebSocket connection
    connectWebSocket();
}
