from django.db import models

from doctors.models import Doctor
from patients.models import Patient


class Mapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="mappings")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="mappings")
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-assigned_at"]
        constraints = [
            models.UniqueConstraint(fields=["patient", "doctor"], name="one_doctor_per_patient")
        ]

    def __str__(self):
        return f"{self.patient} -> {self.doctor}"
