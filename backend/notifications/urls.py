from django.urls import path
from .views import NotificationListView, UnreadNotificationListView, MarkReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/unread/', UnreadNotificationListView.as_view(), name='unread_notifications'),
    path('notifications/<int:pk>/read/', MarkReadView.as_view(), name='mark_read'),
]
