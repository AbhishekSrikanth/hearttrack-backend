from rest_framework import serializers
from predictions.models import ECGPrediction

class ECGPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ECGPrediction
        fields = ['id', 'patient', 'ecg_image', 'prediction_result', 'softmax_outputs', 'created_at']
        read_only_fields = ['id', 'prediction_result', 'softmax_outputs', 'created_at']