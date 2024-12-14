from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'date_of_birth', 'doctor', 'created_at')
    list_filter = ('doctor',)
    search_fields = ('first_name', 'last_name', 'doctor__username')
