from django.shortcuts import render
from .models import Ticket, Category, Comment
from rest_framework import generics, permissions, viewsets
from .serializers import TicketSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        ticket = self.get_object()
        comm = ticket.comments
        if not request.user.is_staff:
            return Response({"error": "Only agents can take the ticket !"}, status=status.HTTP_403_FORBIDDEN)
        
        ticket.status = 'resolved'
        Comment.objects.create(
            ticket=ticket,
            author=request.user,
            text=f"Sistem: Tichetul a fost marcat ca rezolvat de {request.user.username}."
        )
        ticket.save()

        return Response({"status": "Ticket was marked as resolve !"})

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(creator=user)
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)