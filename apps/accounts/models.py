from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    AGENT = 'AGENT'
    BUYER = 'BUYER'

    ROLE_CHOICES = [
        (AGENT, 'Agent'),
        (BUYER, 'Buyer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}" # type: ignore

    @property
    def is_agent(self):
        return self.role == self.AGENT

    @property
    def is_buyer(self):
        return self.role == self.BUYER
