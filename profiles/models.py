from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    CATEGORY_CHOICES = (
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    bio = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
