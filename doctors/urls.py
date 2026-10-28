from django.urls import path

from .views import DoctorDetail, DoctorList

urlpatterns = [
    path("", DoctorList.as_view()),
    path("<int:pk>/", DoctorDetail.as_view()),
]
