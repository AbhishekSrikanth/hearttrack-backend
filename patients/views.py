from rest_framework import generics, permissions
from .models import Patient
from .serializers import PatientSerializer

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow doctors to see their own patients
        return Patient.objects.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the doctor to the logged-in user
        serializer.save(doctor=self.request.user)


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict access to patients of the logged-in doctor
        return Patient.objects.filter(doctor=self.request.user)
