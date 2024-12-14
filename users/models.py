from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    DOCTOR = 'doctor'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (DOCTOR, 'Doctor'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=DOCTOR)

    # Add related_name to resolve clashes
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True
    )
