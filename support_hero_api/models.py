from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
# Create your models here.
class Category(models.Model):
    name = models.CharField()
    color = ColorField()

    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    choice = (
        ('Draft', 'Draft'),
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    )
    title = models.CharField()
    description = models.CharField()
    status = models.CharField(choices=choice, default="Open")
    assigned = models.CharField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title