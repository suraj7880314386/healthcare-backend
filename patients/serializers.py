from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id", "name", "age", "gender", "phone",
            "address", "notes", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, v):
        v = v.strip()
        if len(v) < 2:
            raise serializers.ValidationError("Name is too short")
        return v
