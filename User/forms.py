from django import forms
from .models import *

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['bed_number', 'patient_name']


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['drug_name', 'dosage', 'before_or_after_meal', 'is_machine_dispensed', 'morning_dosage', 'noon_dosage', 'evening_dosage', 'night_dosage']