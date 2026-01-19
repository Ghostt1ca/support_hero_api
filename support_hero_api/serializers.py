from rest_framework import serializers
from .models import Category, Ticket, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
   comments = CommentSerializer(many=True, read_only=True)
   category = CategorySerializer(many=True, read_only=True)
   creator = serializers.ReadOnlyField(source='creator.username')
   class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'status', 'creator', 'assigned', 'category', 'comments']