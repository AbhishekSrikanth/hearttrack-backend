from rest_framework import generics, permissions
from patients.models import Patient
from patients.serializers import PatientSerializer
from users.permissions import IsDoctor

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # Only allow doctors to see their own patients
        return Patient.objects.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the doctor to the logged-in user
        serializer.save(doctor=self.request.user)


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        # Restrict access to patients of the logged-in doctor
        return Patient.objects.filter(doctor=self.request.user)
