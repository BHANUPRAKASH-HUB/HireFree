let currentPage = 1;
let currentFilters = {};

document.addEventListener('DOMContentLoaded', () => {
    loadJobs();

    document.getElementById('filter-form').addEventListener('submit', (e) => {
        e.preventDefault();
        applyFilters();
    });

    document.getElementById('clear-filters').addEventListener('click', () => {
        document.getElementById('filter-form').reset();
        currentFilters = {};
        currentPage = 1;
        loadJobs();
    });

    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadJobs();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        currentPage++;
        loadJobs();
    });
});

function applyFilters() {
    currentPage = 1;
    currentFilters = {
        search: document.getElementById('search').value,
        job_type: document.getElementById('job_type').value,
        experience_level: document.getElementById('experience_level').value,
        pay_per_hour__gte: document.getElementById('pay_per_hour_min').value,
        ordering: document.getElementById('ordering').value,
    };
    // Remove empty filters
    Object.keys(currentFilters).forEach(key => !currentFilters[key] && delete currentFilters[key]);

    loadJobs();
}

async function loadJobs() {
    const container = document.getElementById('jobs-container');
    container.innerHTML = '<div class="p-8 text-center text-gray-400 flex justify-center"><span class="animate-spin mr-2">↻</span> Loading jobs...</div>';

    try {
        // Build Query String
        const params = new URLSearchParams({ page: currentPage, ...currentFilters });

        const response = await fetch(`/api/jobs/?${params.toString()}`);
        const data = await response.json();

        // Handle Pagination State
        document.getElementById('prev-page').disabled = !data.previous;
        document.getElementById('next-page').disabled = !data.next;
        document.getElementById('page-info').innerText = `Page ${currentPage}`;

        const jobs = data.results;

        if (jobs.length === 0) {
            container.innerHTML = `
                <div class="bg-bg p-10 rounded-neu shadow-neu-out text-center">
                    <p class="text-xl font-bold text-gray-500">No jobs found matching your criteria.</p>
                    <button onclick="document.getElementById('clear-filters').click()" class="mt-4 text-accent hover:underline">Clear Filters</button>
                </div>
            `;
            return;
        }

        container.innerHTML = jobs.map(job => `
            <div class="bg-bg p-6 rounded-neu shadow-neu-out hover:shadow-neu-in transition group relative">
                <div class="flex justify-between items-start">
                    <div>
                        <h2 class="text-2xl font-bold text-primary mb-1 group-hover:text-accent transition">
                            <a href="/jobs/${job.id}/">${job.title}</a>
                        </h2>
                        <p class="text-sm font-medium text-gray-500 mb-4">
                            ${job.company_name || 'Generic Company'} • ${job.location || 'Remote'}
                        </p>
                        
                        <div class="flex flex-wrap gap-2 mb-4">
                            <span class="px-3 py-1 bg-gray-200 rounded-full text-xs font-bold text-gray-600 uppercase">${job.job_type.replace('_', ' ')}</span>
                            <span class="px-3 py-1 bg-gray-200 rounded-full text-xs font-bold text-gray-600 uppercase">${job.experience_level}</span>
                            ${job.required_skills ? job.required_skills.slice(0, 3).map(s => `<span class="px-2 py-1 border border-accent/30 text-accent rounded-full text-xs font-medium">${s}</span>`).join('') : ''}
                        </div>
                    </div>
                    
                    <div class="text-right">
                        <p class="text-xl font-bold text-primary mb-2">$${job.pay_per_hour}<span class="text-sm font-normal text-gray-500">/hr</span></p>
                        <span class="text-xs text-gray-400">${new Date(job.created_at).toLocaleDateString()}</span>
                    </div>
                </div>

                <div class="border-t border-gray-200 mt-4 pt-4 flex justify-between items-center">
                    <p class="text-sm text-gray-500 line-clamp-2 w-3/4">${job.description}</p>
                    <a href="/jobs/${job.id}/" class="text-accent font-bold hover:underline">View Details →</a>
                </div>
            </div>
        `).join('');

        // Recruiter View Enhancements
        const user = window.getUser();
        if (user && user.user_type === 'recruiter') {
            // Optional: Add Edit/Delete buttons logic here if we were fetching only recruiter's jobs
            // For general browse, just keep View Details
        }

    } catch (error) {
        console.error('Error loading jobs:', error);
        container.innerHTML = '<div class="text-center text-red-500 font-bold">Failed to load jobs. Please try again.</div>';
    }
}
