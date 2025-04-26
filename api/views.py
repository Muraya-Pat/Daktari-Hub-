from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Q
from clients.models import Client
from .serializers import ClientSerializer
from rest_framework.decorators import action


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Client.objects.all().prefetch_related('enrollments__program')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.GET.get('q', '')
        clients = self.queryset.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(national_id__icontains=query)
        )
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data)
