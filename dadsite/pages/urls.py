from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('client-portal/', views.client_portal, name='client_portal'),
    path('health/', views.health_check, name='health_check'),

    # Management pages (avoid conflict with Django admin)
    path('manage/inquiries/pending/', views.admin_pending_inquiries, name='admin_pending_inquiries'),
    path('manage/clients/active/', views.admin_active_clients, name='admin_active_clients'),

    # Management actions
    path('manage/inquiries/<int:inquiry_id>/approve/', views.approve_inquiry, name='approve_inquiry'),
    path('manage/inquiries/<int:inquiry_id>/deny/', views.deny_inquiry, name='deny_inquiry'),
    path('manage/clients/<int:inquiry_id>/update-status/', views.update_client_status, name='update_client_status'),
    path('manage/inquiries/<int:inquiry_id>/onboard/', views.onboard_client, name='onboard_client'),  # Legacy
]
