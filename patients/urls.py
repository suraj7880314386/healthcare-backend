from django.urls import path

from .views import PatientDetail, PatientList

urlpatterns = [
    path("", PatientList.as_view()),
    path("<int:pk>/", PatientDetail.as_view()),
]
