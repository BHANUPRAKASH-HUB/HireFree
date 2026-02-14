from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'auth/login.html')

def register_view(request):
    return render(request, 'auth/register.html')

def dashboard_view(request):
    # This can be a simple redirector logic or just render the freelancer one by default if we want
    # Better to have a generic dash that redirects based on JS
    return render(request, 'dashboard/redirect.html')

def freelancer_dashboard_view(request):
    return render(request, 'dashboard/freelancer_dashboard.html')

def recruiter_dashboard_view(request):
    return render(request, 'dashboard/recruiter_dashboard.html')

def job_list_view(request):
    return render(request, 'jobs/job_list.html')

def job_detail_view(request, pk):
    return render(request, 'jobs/job_detail.html')

def post_job_view(request):
    return render(request, 'jobs/post_job.html')

def talent_list_view(request):
    return render(request, 'talent/browse_talent.html')

def profile_view(request):
    return render(request, 'profile/profile.html')

def chat_view(request):
    return render(request, 'chat/chat.html')
