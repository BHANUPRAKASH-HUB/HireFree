from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/freelancer/', views.freelancer_dashboard_view, name='freelancer_dashboard'),
    path('dashboard/recruiter/', views.recruiter_dashboard_view, name='recruiter_dashboard'),
    path('jobs/', views.job_list_view, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail_view, name='job_detail'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('talent/', views.talent_list_view, name='talent_list'),
    path('profile/', views.profile_view, name='profile'),
    path('messages/', views.chat_view, name='chat'),
]
