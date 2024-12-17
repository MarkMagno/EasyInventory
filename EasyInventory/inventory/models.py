from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Equipment(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    asset_number = models.CharField(max_length=20, unique=True)
    model_number = models.CharField(max_length=20)
    due_date = models.DateField(null=True, blank=True)
    checked_out_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='checked_out_equipment')

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

    def __str__(self):
        return self.user.username

class CheckoutRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkout_requests')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='checkout_requests')
    use_case = models.TextField()
    date_needed_until = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(default=timezone.now)

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
