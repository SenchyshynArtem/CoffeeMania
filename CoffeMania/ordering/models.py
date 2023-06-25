from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Orders(models.Model):
    session_key = models.CharField(max_length=32, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.TextField()