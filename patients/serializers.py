from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField(read_only=True)  # Read-only field for the doctor username

    class Meta:
        model = Patient
        fields = ['id', 'doctor', 'first_name', 'last_name', 'date_of_birth', 'created_at', 'updated_at']
        read_only_fields = ['id', 'doctor', 'created_at', 'updated_at']
