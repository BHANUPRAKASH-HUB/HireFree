document.addEventListener('DOMContentLoaded', async () => {
    if (!window.checkSession()) return;

    loadDashboardData();
});

async function loadDashboardData() {
    const token = window.getAccessToken();
    const headers = { 'Authorization': `Bearer ${token}` };

    try {
        // 1. Fetch My Applications
        const appsRes = await fetch('/api/applications/', { headers });
        const appsData = await appsRes.json();
        const applications = appsData.results || appsData;

        // Update Stats
        document.getElementById('applied-count').innerText = applications.length;
        document.getElementById('interviews-count').innerText = applications.filter(a => a.status === 'interviewing').length;

        // Render Applications Table
        const appsContainer = document.getElementById('applications-list');
        if (applications.length > 0) {
            appsContainer.innerHTML = applications.map(app => `
                <tr class="border-b border-gray-200 hover:bg-white/50 transition">
                    <td class="py-3 px-4 font-bold text-primary">
                        <a href="/jobs/${app.job}/" class="hover:underline">${app.job_title || 'View Job'}</a>
                    </td>
                    <td class="py-3 px-4">${app.company_name || 'Hidden'}</td>
                    <td class="py-3 px-4 text-sm text-gray-500">${new Date(app.applied_at).toLocaleDateString()}</td>
                    <td class="py-3 px-4">
                        <span class="px-2 py-1 rounded-full text-xs font-bold ${getStatusColor(app.status)}">
                            ${app.status.toUpperCase()}
                        </span>
                     <a href="/messages/?recipient=${app.recruiter}" title="Message Recruiter" class="ml-2 text-purple-500 hover:text-purple-700">💬</a>
                </td>
                </tr>
            `).join('');
        } else {
            appsContainer.innerHTML = '<tr><td colspan="4" class="py-8 text-center text-gray-500">You haven\'t applied to any jobs yet.</td></tr>';
        }

        // 2. Fetch Recommended Jobs (Simply recent jobs for now)
        const jobsRes = await fetch('/api/jobs/?limit=5', { headers }); // Assuming pagination limit support or default
        const jobsData = await jobsRes.json();
        const jobs = jobsData.results || jobsData;

        // Render Jobs
        const jobsContainer = document.getElementById('recommended-jobs-list');
        if (jobs.length > 0) {
            jobsContainer.innerHTML = jobs.map(job => `
                <div class="p-4 bg-bg rounded-neu shadow-neu-in flex justify-between items-center group hover:bg-white/40 transition">
                    <div>
                        <h4 class="font-bold text-primary group-hover:text-accent transition">${job.title}</h4>
                        <p class="text-xs text-gray-500">$${job.pay_per_hour}/hr • ${job.experience_level}</p>
                    </div>
                    <a href="/jobs/${job.id}/" class="text-accent hover:underline text-sm font-bold">Apply</a>
                </div>
            `).join('');
        } else {
            jobsContainer.innerHTML = '<p class="text-center text-gray-500">No jobs found.</p>';
        }

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
