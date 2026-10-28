from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id", "name", "specialization", "email", "phone",
            "experience", "created_by", "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate_email(self, v):
        return v.lower()

    def validate_experience(self, v):
        if v > 70:
            raise serializers.ValidationError("Experience looks too high")
        return v
