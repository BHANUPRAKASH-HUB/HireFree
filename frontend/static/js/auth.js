// Auth Logic & State Management

window.API_BASE = '/api';

/**
 * Get Access Token from LocalStorage
 */
window.getAccessToken = function () {
    return localStorage.getItem('access_token');
}

/**
 * Get User Object from LocalStorage
 */
window.getUser = function () {
    try {
        return localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null;
    } catch (e) {
        return null;
    }
}

/**
 * Check if the current session is valid
 */
window.checkSession = function () {
    const token = getAccessToken();
    if (!token) return false;

    // Simple JWT expiry check (decoding payload)
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const now = Math.floor(Date.now() / 1000);
        if (payload.exp < now) {
            window.showToast('Session expired. Please log in again.', 'error');
            setTimeout(window.logout, 2000);
            return false;
        }
    } catch (e) {
        return false;
    }
    return true;
}

/**
 * Update Navigation Bar based on Auth State
 */
window.updateNav = function () {
    const user = getUser();
    const navLinks = document.getElementById('nav-links');
    const authButtons = document.getElementById('auth-buttons');
    const isLoggedIn = checkSession();

    if (isLoggedIn && user) {
        // Logged In State
        // Logged In State
        let linksHtml = `<a href="/" class="hover:text-accent transition font-medium">Home</a>`;

        if (user.user_type === 'freelancer') {
            linksHtml += `
                <a href="/jobs/" class="hover:text-accent transition font-medium">Browse Jobs</a>
                <a href="/dashboard/" class="hover:text-accent transition font-medium">Dashboard</a>
                <a href="/profile/" class="hover:text-accent transition font-medium">Profile</a>
            `;
        } else if (user.user_type === 'recruiter') {
            linksHtml += `
                <a href="/dashboard/" class="hover:text-accent transition font-medium">Dashboard</a>
                <a href="/talent/" class="hover:text-accent transition font-medium">Find Talent</a>
                <a href="/post-job/" class="bg-accent text-white px-3 py-1 rounded-neu hover:bg-blue-600 transition font-medium ml-4">Post Job</a>
            `;
        }


        if (navLinks) navLinks.innerHTML = linksHtml;

        if (authButtons) {
            authButtons.innerHTML = `
                <div class="flex items-center gap-4">
                    <a href="#" class="relative text-primary hover:text-accent mr-2" id="nav-notif-link">
                        <span class="text-2xl">🔔</span>
                        <span id="notification-badge" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center hidden"></span>
                    </a>
                    <span class="text-primary font-medium hidden md:block">Hi, ${(user.first_name && user.last_name) ? user.first_name : user.email.split('@')[0]}</span>
                    <button onclick="window.logout()" 
                        class="text-red-500 hover:text-red-700 font-medium transition">
                        Logout
                    </button>
                    ${user.freelancer_profile?.profile_image
                    ? `<img src="${user.freelancer_profile.profile_image}" class="w-8 h-8 rounded-full border border-gray-300">`
                    : ''}
                </div>
            `;
        }
    } else {
        // Clear if invalid session but data exists
        if (!isLoggedIn && localStorage.getItem('access_token')) {
            window.logout();
        }
    }
}

/**
 * Login Function
 */
window.login = async function (email, password) {
    try {
        const response = await fetch(`${API_BASE}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);

            // Get User Details
            const userRes = await fetch(`${API_BASE}/users/me/`, {
                headers: { 'Authorization': `Bearer ${data.access}` }
            });

            if (userRes.ok) {
                const userData = await userRes.json();
                localStorage.setItem('user', JSON.stringify(userData));

                window.showToast('Login successful!', 'success');
                setTimeout(() => window.location.href = '/dashboard/', 1000);
            } else {
                throw new Error('Failed to fetch user profile');
            }
        } else {
            window.showToast('Invalid credentials.', 'error');
            throw new Error('Login failed');
        }
    } catch (error) {
        console.error('Login Error:', error);
        window.showToast('Login failed. Please check your credentials.', 'error');
        throw error; // Re-throw for UI to catch
    }
}

/**
 * Logout Function
 */
window.logout = function () {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login/';
}

// Initial Run
document.addEventListener('DOMContentLoaded', () => {
    updateNav();
    // Check session every minute
    setInterval(checkSession, 60000);
});
