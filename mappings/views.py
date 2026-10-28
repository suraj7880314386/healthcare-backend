from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from doctors.serializers import DoctorSerializer
from patients.models import Patient

from .models import Mapping
from .serializers import MappingSerializer


class MappingList(generics.ListCreateAPIView):
    serializer_class = MappingSerializer

    def get_queryset(self):
        return Mapping.objects.filter(patient__owner=self.request.user).select_related(
            "patient", "doctor"
        )


class MappingDetail(APIView):

    def get(self, request, pk):
        pt = get_object_or_404(Patient, pk=pk, owner=request.user)
        qs = Mapping.objects.filter(patient=pt).select_related("doctor")
        docs = [
            {
                "mapping_id": m.id,
                "assigned_at": m.assigned_at,
                "doctor": DoctorSerializer(m.doctor).data,
            }
            for m in qs
        ]
        return Response({"patient": pt.id, "patient_name": pt.name, "doctors": docs})

    def delete(self, request, pk):
        m = get_object_or_404(Mapping, pk=pk, patient__owner=request.user)
        m.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
