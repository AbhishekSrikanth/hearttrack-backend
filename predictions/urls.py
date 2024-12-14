from django.urls import path

from predictions.views import ECGPredictionListCreateView, ECGPredictionRetrieveDeleteView

urlpatterns = [
    path('', ECGPredictionListCreateView.as_view(), name='ecg-prediction-list-create'),
    path('<int:pk>/', ECGPredictionRetrieveDeleteView.as_view(), name='ecg-prediction-retrieve-delete'),
]
