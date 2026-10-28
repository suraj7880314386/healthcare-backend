from django.conf import settings
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models

phone_rx = RegexValidator(r"^\+?\d{10,15}$", "Enter a valid phone number (10-15 digits)")


class Patient(models.Model):
    GENDERS = [("M", "Male"), ("F", "Female"), ("O", "Other")]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patients"
    )
    name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(120)])
    gender = models.CharField(max_length=1, choices=GENDERS)
    phone = models.CharField(max_length=16, validators=[phone_rx])
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
