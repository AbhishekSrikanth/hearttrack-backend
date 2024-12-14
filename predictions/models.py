from django.db import models
from patients.models import Patient

# Create your models here.
class ECGPrediction(models.Model):
    
    CLASSES = [
        ('N', 'Normal'),
        ('S', 'Supraventricular'),
        ('V', 'Ventricular'),
        ('F', 'Fusion'),
        ('Q', 'Unknown'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='predictions')
    ecg_image = models.ImageField(upload_to='ecg_images/')
    prediction_result = models.CharField(max_length=1, choices=CLASSES)
    softmax_outputs = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Classification for {self.patient} - {self.prediction_result}"