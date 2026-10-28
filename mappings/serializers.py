from rest_framework import serializers

from .models import Mapping


class MappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.name", read_only=True)

    class Meta:
        model = Mapping
        fields = ["id", "patient", "doctor", "patient_name", "doctor_name", "assigned_at"]
        read_only_fields = ["id", "assigned_at"]

    def validate_patient(self, p):
        
        if p.owner_id != self.context["request"].user.id:
            raise serializers.ValidationError("Patient not found")
        return p

    def validate(self, d):
        if Mapping.objects.filter(patient=d["patient"], doctor=d["doctor"]).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient")
        return d
