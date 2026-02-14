let currentPage = 1;
let currentFilters = {};

document.addEventListener('DOMContentLoaded', () => {
    loadTalent();

    document.getElementById('talent-filter-form').addEventListener('submit', (e) => {
        e.preventDefault();
        applyFilters();
    });

    document.getElementById('clear-talent-filters').addEventListener('click', () => {
        document.getElementById('talent-filter-form').reset();
        currentFilters = {};
        currentPage = 1;
        loadTalent();
    });

    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadTalent();
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        currentPage++;
        loadTalent();
    });
});

function applyFilters() {
    currentPage = 1;
    currentFilters = {
        skills: document.getElementById('skills_filter').value,
        hourly_rate: document.getElementById('hourly_rate_max').value,
    };
    Object.keys(currentFilters).forEach(key => !currentFilters[key] && delete currentFilters[key]);
    loadTalent();
}

async function loadTalent() {
    const container = document.getElementById('talent-container');
    container.innerHTML = '<div class="col-span-2 p-8 text-center text-gray-400 flex justify-center"><span class="animate-spin mr-2">↻</span> Loading talent...</div>';

    try {
        const params = new URLSearchParams({ page: currentPage, ...currentFilters });
        // The endpoint from backend/users/views.py for TalentListView
        // It filters user_type='freelancer' automatically
        const response = await fetch(`/api/users/?${params.toString()}`);
        const data = await response.json();

        document.getElementById('prev-page').disabled = !data.previous;
        document.getElementById('next-page').disabled = !data.next;
        document.getElementById('page-info').innerText = `Page ${currentPage}`;

        const users = data.results;

        if (users.length === 0) {
            container.innerHTML = `
                <div class="col-span-2 bg-bg p-10 rounded-neu shadow-neu-out text-center">
                    <p class="text-xl font-bold text-gray-500">No freelancers found.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = users.map(user => {
            const profile = user.freelancer_profile || {};
            const initials = user.email ? user.email.substring(0, 2).toUpperCase() : '?';

            return `
            <div class="bg-bg p-6 rounded-neu shadow-neu-out hover:shadow-neu-in transition group">
                <div class="flex items-center gap-4 mb-4">
                    <div class="w-16 h-16 rounded-full bg-gray-200 flex items-center justify-center text-xl font-bold text-gray-500 shadow-neu-out">
                         ${profile.profile_image ? `<img src="${profile.profile_image}" class="w-full h-full rounded-full object-cover">` : initials}
                    </div>
                    <div>
                        <h3 class="font-bold text-lg text-primary">${user.email.split('@')[0]}</h3> <!-- Use name if available -->
                        <p class="text-sm text-gray-500">${profile.title || 'Freelancer'}</p>
                    </div>
                    <div class="ml-auto text-right">
                        <p class="font-bold text-accent">$${profile.hourly_rate || 0}/hr</p>
                    </div>
                </div>
                
                <p class="text-sm text-gray-600 line-clamp-3 mb-4 h-16">${profile.bio || 'No bio available.'}</p>
                
                <div class="flex flex-wrap gap-2 mb-4">
                    ${(profile.skills || []).slice(0, 4).map(s => `<span class="px-2 py-1 bg-gray-100 rounded text-xs font-medium text-gray-600">${s}</span>`).join('')}
                </div>
                
                <div class="flex gap-2">
                    <button class="flex-1 py-2 bg-bg rounded-neu shadow-neu-out text-primary font-bold hover:shadow-neu-in active:translate-y-px transition opacity-50 cursor-not-allowed" title="Coming Soon">
                        View Profile
                    </button>
                    <a href="/messages/?recipient=${user.id}" class="flex-1 py-2 bg-accent text-white rounded-neu shadow-neu-btn text-center font-bold hover:shadow-neu-in active:translate-y-px transition flex items-center justify-center gap-2">
                        <span>💬</span> Message
                    </a>
                </div>
            </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Error loading talent:', error);
        container.innerHTML = '<div class="col-span-2 text-center text-red-500">Failed to load talent.</div>';
    }
}
