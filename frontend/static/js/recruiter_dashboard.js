document.addEventListener('DOMContentLoaded', async () => {
    if (!window.checkSession()) return;

    // Load Stats & Data
    loadDashboardData();
});

async function loadDashboardData() {
    const token = window.getAccessToken();
    const headers = { 'Authorization': `Bearer ${token}` };

    try {
        // 1. Fetch Jobs (for stats and list)
        // Since we don't have a dedicated stats endpoint, we fetch lists and count
        const jobsRes = await fetch('/api/jobs/', { headers }); // Assuming this returns recruiter's jobs if Recruiter
        const jobsData = await jobsRes.json();
        const jobs = jobsData.results || jobsData; // Handle pagination if present

        // Update Job Stats
        document.getElementById('active-jobs-count').innerText = jobs.length;

        // Render Recent Jobs (Top 5)
        const jobsContainer = document.getElementById('recent-jobs-list');
        jobsContainer.innerHTML = jobs.slice(0, 5).map(job => `
            <div class="p-4 bg-bg rounded-neu shadow-neu-in flex justify-between items-center">
                <div>
                    <h4 class="font-bold text-primary">${job.title}</h4>
                    <p class="text-xs text-gray-500">${new Date(job.created_at).toLocaleDateString()}</p>
                </div>
                <a href="/jobs/${job.id}/" class="text-accent hover:underline text-sm font-bold">View</a>
            </div>
        `).join('') || '<p class="text-center text-gray-500">No jobs posted yet.</p>';


        // 2. Fetch Applications (Received by this recruiter)
        // Ensure backend supports this view. /api/applications/ lists applications FOR the recruiter's jobs.
        const appsRes = await fetch('/api/applications/', { headers });
        const appsData = await appsRes.json();
        const applications = appsData.results || appsData;

        // Update Apps Stats
        document.getElementById('new-applications-count').innerText = applications.filter(a => a.status === 'applied').length;

        // Render Applications Table
        const appsContainer = document.getElementById('applications-list');
        appsContainer.innerHTML = applications.length ? applications.map(app => `
            <tr class="border-b border-gray-200 hover:bg-white/50 transition">
                <td class="py-3 px-4 font-medium">${app.freelancer_name || 'N/A'}</td> <!-- Assuming serializer sends name -->
                <td class="py-3 px-4">${app.job_title || 'Unknown Job'}</td> <!-- Assuming serializer sends job title -->
                <td class="py-3 px-4 text-sm text-gray-500">${new Date(app.applied_at).toLocaleDateString()}</td>
                <td class="py-3 px-4">
                    <span class="px-2 py-1 rounded-full text-xs font-bold ${getStatusColor(app.status)}">
                        ${app.status.toUpperCase()}
                    </span>
                </td>
                <td class="py-3 px-4 text-right">
                    ${app.status === 'applied' ? `
                        <button onclick="updateStatus(${app.id}, 'interviewing')" title="Shortlist" class="text-blue-500 hover:text-blue-700 mr-2 font-bold">✓</button>
                        <button onclick="updateStatus(${app.id}, 'rejected')" title="Reject" class="text-red-500 hover:text-red-700 font-bold">✗</button>
                    ` : ''}
                    <a href="/messages/?recipient=${app.freelancer}" title="Message" class="text-purple-500 hover:text-purple-700 mr-2 font-bold">💬</a>
                    <button onclick="viewApplication(${app.id})" class="text-gray-400 hover:text-primary ml-2">👁</button>
                </td>
            </tr>
        `).join('') : '<tr><td colspan="5" class="py-8 text-center text-gray-500">No applications received yet.</td></tr>';

    } catch (e) {
        console.error("Dashboard Load Error", e);
        window.showToast("Failed to load dashboard data", 'error');
    }
}

function getStatusColor(status) {
    switch (status) {
        case 'applied': return 'bg-yellow-100 text-yellow-600';
        case 'interviewing': return 'bg-blue-100 text-blue-600';
        case 'accepted': return 'bg-green-100 text-green-600';
        case 'rejected': return 'bg-red-100 text-red-600';
        default: return 'bg-gray-100 text-gray-600';
    }
}

window.updateStatus = async function (appId, newStatus) {
    if (!confirm(`Mark this application as ${newStatus}?`)) return;

    try {
        const res = await fetch(`/api/jobs/applications/${appId}/status/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${window.getAccessToken()}`
            },
            body: JSON.stringify({ status: newStatus })
        });

        if (res.ok) {
            window.showToast(`Application marked as ${newStatus}`, 'success');
            loadDashboardData(); // Reload
        } else {
            window.showToast('Failed to update status', 'error');
        }
    } catch (e) {
        window.showToast('Error updating status', 'error');
    }
}

window.viewApplication = function (appId) {
    // Implement modal or redirect to detail
    window.showToast("View Application Detail - To Be Implemented", 'info');
}
