from django.urls import path
from . import views
from .views import FitnessTipListView

app_name = 'fitness'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('tips/', FitnessTipListView.as_view(), name='tips'),
    path('tips/<int:pk>/', views.tip_detail, name='tip_detail'),
]