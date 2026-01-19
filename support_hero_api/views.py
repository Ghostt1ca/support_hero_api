from django.shortcuts import render
from .models import Ticket, Category
from rest_framework import generics, permissions, viewsets
from .serializers import TicketSerializer
# Create your views here.

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(creator=user)
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)