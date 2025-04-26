# programs/forms.py
from django import forms
from .models import Program, Enrollment
from django.core.exceptions import ValidationError
from django.utils import timezone

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if end_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date")
        
        return cleaned_data

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['client', 'program']
        widgets = {
            'client': forms.Select(attrs={'class': 'select2'}),
            'program': forms.Select(attrs={'class': 'select2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})