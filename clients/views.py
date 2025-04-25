from django.shortcuts import render
# clients/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Client
from .forms import ClientRegistrationForm
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

class ClientListView(ListView):
    model = Client
    template_name = 'clients/index.html'
    context_object_name = 'clients'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        gender_filter = self.request.GET.get('gender')
        
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(national_id__icontains=search_query) |
                Q(phone_number__icontains=search_query)
            )
        
        if gender_filter:
            queryset = queryset.filter(gender=gender_filter)
            
        return queryset.order_by('-registered_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        context['total_clients'] = Client.objects.count()
        context['active_clients'] = queryset.count()  # Adjust this if you have an active/inactive status
        context['new_this_month'] = Client.objects.filter(
            registered_at__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        return context

def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients:index')
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'clients/registration.html', {'form': form})

def client_profile(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/profile.html', {'client': client})

