document.addEventListener('DOMContentLoaded', () => {
    if (window.checkSession()) {
        startNotificationPolling();
    }
});

function startNotificationPolling() {
    // Poll every 30 seconds
    setInterval(checkNotifications, 30000);
    // Initial check
    checkNotifications();
}

async function checkNotifications() {
    const token = window.getAccessToken();
    if (!token) return;

    try {
        const response = await fetch('/api/notifications/unread/', {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const data = await response.json();
            const count = data.count || data.length || 0;

            updateNotificationUI(count);

            // If new high-priority notifications, show toast
            // For MVP, just show generic if count > 0 and not on notifications page
            if (count > 0 && !window.location.pathname.includes('/notifications/')) {
                // Optional: Store last count to only toast on increase
                const lastCount = parseInt(localStorage.getItem('last_notif_count') || '0');
                if (count > lastCount) {
                    window.showToast(`You have ${count} unread notifications`, 'info');
                }
                localStorage.setItem('last_notif_count', count);
            }
        }
    } catch (e) {
        console.error('Notification poll error', e);
    }
}

function updateNotificationUI(count) {
    // Look for a notification badge in Navbar (to be added)
    const badge = document.getElementById('notification-badge');
    if (badge) {
        badge.innerText = count > 0 ? count : '';
        badge.classList.toggle('hidden', count === 0);
    }
}
