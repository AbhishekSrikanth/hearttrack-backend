from rest_framework import serializers
from patients.models import Patient
from predictions.serializers import ECGPredictionSerializer

class PatientSerializer(serializers.ModelSerializer):
    doctor = serializers.StringRelatedField(read_only=True)  # Read-only field for the doctor username
    predictions = ECGPredictionSerializer(many=True, read_only=True, source='predictions')  # Add related predictions

    class Meta:
        model = Patient
        fields = ['id', 'doctor', 'first_name', 'last_name', 'date_of_birth', 'created_at', 'updated_at', 'predictions']
        read_only_fields = ['id', 'doctor', 'created_at', 'updated_at']
