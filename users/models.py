from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model with email as the unique identifier
    """
    ROLES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='doctor')

    def is_admin(self)-> bool:
        """
        Check if the user is an admin

        Returns:
            bool: True if the user is an admin, False otherwise
        """
        return self.role == 'admin'

    def is_doctor(self)-> bool:
        """
        Check if the user is a doctor

        Returns:
            bool: True if the user is a doctor, False otherwise
        """
        return self.role == 'doctor'
