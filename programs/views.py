
# programs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Program, Enrollment
from .forms import ProgramForm, EnrollmentForm
from clients.models import Client
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

class ProgramListView(ListView):
    model = Program
    template_name = 'programs/index.html'
    context_object_name = 'programs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
            
        return queryset.order_by('-created_at')

def create_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, f'Program "{program.name}" created successfully!')
            return redirect('programs:index')
    else:
        form = ProgramForm()
    
    return render(request, 'programs/program_form.html', {'form': form})

def enroll_client(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            messages.success(request, f'Client enrolled in {enrollment.program.name} successfully!')
            return redirect('programs:index')
    else:
        form = EnrollmentForm()
    
    return render(request, 'programs/enroll_client.html', {'form': form})

def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    enrollments = program.enrollments.all().select_related('client')
    return render(request, 'programs/program_detail.html', {
        'program': program,
        'enrollments': enrollments
    })
def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_programs_count'] = Program.objects.filter(
            end_date__gte=timezone.now().date()
        ).count()
        context['total_enrollments'] = Enrollment.objects.count()
        return context
def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    enrollments = program.enrollments.all().select_related('client')
    
    active_clients_count = enrollments.count()
    new_enrollments_count = enrollments.filter(
        enrollment_date__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    return render(request, 'programs/program_detail.html', {
        'program': program,
        'enrollments': enrollments,
        'active_clients_count': active_clients_count,
        'new_enrollments_count': new_enrollments_count
    })
