# clients/forms.py
from django import forms
from .models import Client
from django.core.validators import RegexValidator

class ClientRegistrationForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone_number = forms.CharField(validators=[phone_regex], required=False)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Format: YYYY-MM-DD"
    )
    
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'gender': forms.RadioSelect(choices=Client.GENDER_CHOICES),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
            if field == 'national_id':
                self.fields[field].widget.attrs['placeholder'] = 'e.g. 12345678'
            if field == 'email':
                self.fields[field].widget.attrs['placeholder'] = 'e.g. client@example.com'