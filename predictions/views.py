import base64
import requests

from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import generics, permissions, serializers

from users.permissions import IsDoctor
from patients.models import Patient
from predictions.models import ECGPrediction
from predictions.serializers import ECGPredictionSerializer


# Create, Retrieve, Delete APIs for ECGPrediction
class ECGPredictionListCreateView(generics.ListCreateAPIView):
    queryset = ECGPrediction.objects.all()
    serializer_class = ECGPredictionSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # Doctors can only view predictions they created for their patients
        return self.queryset.filter(patient__doctor=self.request.user)

    def perform_create(self, serializer):
        patient = get_object_or_404(Patient, id=self.request.data.get('patient'))
        ecg_image = self.request.FILES.get('ecg_image')

        # Check if the logged-in user is allowed to create predictions for this patient
        if patient.doctor != self.request.user:
            raise serializers.ValidationError("You do not have permission to create predictions for this patient.")

        # Call FastAPI for prediction
        fastapi_url = settings.FASTAPI_URL + '/predict/'
        with open(ecg_image.temporary_file_path(), "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode('utf-8')

        response = requests.post(fastapi_url, json={'file': base64_image})

        if response.status_code != 200:
            raise serializers.ValidationError("Failed to get prediction from classifier.")

        prediction_data = response.json()
        prediction_result = prediction_data['prediction'][0]

        # Save prediction result
        serializer.save(
            patient=patient,
            ecg_image=ecg_image,
            prediction_result=prediction_result,
            softmax_outputs=prediction_data['prediction']
        )

class ECGPredictionRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    queryset = ECGPrediction.objects.all()
    serializer_class = ECGPredictionSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # Doctors can only access predictions they created for their patients
        return self.queryset.filter(patient__doctor=self.request.user)