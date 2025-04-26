# programs/urls.py
from django.urls import path
from .views import ProgramListView, create_program, enroll_client, program_detail

app_name = 'programs'

urlpatterns = [
    path('', ProgramListView.as_view(), name='index'),
    path('new/', create_program, name='create'),
    path('enroll/', enroll_client, name='enroll'),
    path('<int:pk>/', program_detail, name='detail'),
]