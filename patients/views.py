from rest_framework import generics

from .models import Patient
from .serializers import PatientSerializer


class PatientList(generics.ListCreateAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        # only the patients added by the logged in user
        return Patient.objects.filter(owner=self.request.user)

    def perform_create(self, ser):
        ser.save(owner=self.request.user)


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(owner=self.request.user)
