from django import forms
from .models import Equipment, CheckoutRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['price', 'asset_number', 'model_number']
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'asset_number': forms.TextInput(attrs={'placeholder': 'Enter Asset Number'}),
            'model_number': forms.TextInput(attrs={'placeholder': 'Enter Model Number'}),
        }

class CheckoutRequestForm(forms.ModelForm):
    class Meta:
        model = CheckoutRequest
        fields = ['equipment', 'use_case', 'date_needed_until']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-select'}),
            'use_case': forms.Textarea(attrs={'placeholder': 'Enter the reason for checkout'}),
            'date_needed_until': forms.DateInput(attrs={'type': 'date'}),
        }

class UserForm(UserCreationForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
        }
