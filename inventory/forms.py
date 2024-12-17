from django import forms
from django.core.validators import EmailValidator, RegexValidator
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
    use_case = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter the reason for checkout'}),
        validators=[RegexValidator(r'^[\s\S]{10,500}$', 'Use case must be between 10 and 500 characters.')]
    )

    class Meta:
        model = CheckoutRequest
        fields = ['equipment', 'use_case', 'date_needed_until']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-select'}),
            'date_needed_until': forms.DateInput(attrs={'type': 'date'}),
        }


class UserForm(UserCreationForm):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    username = forms.CharField(
        max_length=150,
        validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'Username must contain only letters, numbers, and underscores.')]
    )
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator('Enter a valid email address.')]
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        }
