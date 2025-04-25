# clients/urls.py
from django.urls import path
from .views import ClientListView, register_client, client_profile

app_name = 'clients'

urlpatterns = [
    path('', ClientListView.as_view(), name='index'),
    path('register/', register_client, name='register'),
    path('<int:pk>/', client_profile, name='profile'),
    
]