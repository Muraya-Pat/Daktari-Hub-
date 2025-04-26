from django.utils import timezone
from django.db.models import Q
from clients.models import Client
from programs.models import Program, Enrollment

def sidebar_data(request):
    today = timezone.now().date()
    
    return {
        'recent_clients': Client.objects.all().order_by('-registered_at')[:3],
        'recent_programs': Program.objects.all().order_by('-created_at')[:3],
        'recent_enrollments': Enrollment.objects.select_related('client', 'program')
                              .order_by('-enrollment_date')[:3],
        'total_clients': Client.objects.count(),
        'active_programs': Program.objects.filter(
            Q(end_date__gte=today) | Q(end_date__isnull=True)
        ).count(),
        'todays_enrollments': Enrollment.objects.filter(
            enrollment_date=today  # 
        ).count(),
    }