// Utility Functions

// Toast Notification System
window.showToast = function (message, type = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');

    // Colors based on type
    const colors = type === 'error'
        ? 'text-red-500 border-l-4 border-red-500'
        : 'text-green-500 border-l-4 border-green-500';

    toast.className = `
        bg-bg text-text px-6 py-4 rounded-neu shadow-neu-out 
        flex items-center gap-3 min-w-[300px] toast-enter
        ${colors}
    `;

    toast.innerHTML = `
        <span class="font-bold text-lg">${type === 'error' ? '!' : '✓'}</span>
        <span class="font-medium text-sm">${message}</span>
    `;

    container.appendChild(toast);

    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('toast-enter');
        toast.classList.add('toast-exit');
        toast.addEventListener('animationend', () => toast.remove());
    }, 3000);
}

// Format Currency
window.formatCurrency = function (amount) {
    if (!amount) return '$0.00';
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
}
