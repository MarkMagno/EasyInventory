from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
from django.core.validators import EmailValidator, RegexValidator, MinValueValidator
from django.utils import timezone

class Equipment(models.Model):
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)]  # Ensure positive prices
    )
    asset_number = models.CharField(
        max_length=20, 
        unique=True,
        validators=[RegexValidator(r'^[a-zA-Z0-9-]+$', 'Asset number must contain only letters, numbers, and hyphens.')]
    )
    model_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^[a-zA-Z0-9-]+$', 'Model number must contain only letters, numbers, and hyphens.')]
    )
    due_date = models.DateField(null=True, blank=True)
    checked_out_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='checked_out_equipment'
    )

    def save(self, *args, **kwargs):
        self.asset_number = escape(self.asset_number)
        self.model_number = escape(self.model_number)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.model_number} ({self.asset_number})"


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_enabled = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.role = escape(self.role)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class CheckoutRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='checkout_requests'
    )
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name='checkout_requests'
    )
    use_case = models.TextField(
        validators=[RegexValidator(r'^[\s\S]{10,500}$', 'Use case must be between 10 and 500 characters.')]
    )
    date_needed_until = models.DateField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    request_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.use_case = escape(self.use_case)
        super().save(*args, **kwargs)

    def approve(self):
        self.status = 'approved'
        self.equipment.due_date = self.date_needed_until
        self.equipment.checked_out_to = self.user
        self.equipment.save()
        self.save()

    def deny(self):
        self.status = 'denied'
        self.save()

    def __str__(self):
        return f"Request by {self.user.username} for {self.equipment.asset_number}"
