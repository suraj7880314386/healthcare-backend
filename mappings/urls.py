from django.urls import path

from .views import MappingDetail, MappingList

urlpatterns = [
    path("", MappingList.as_view()),
    path("<int:pk>/", MappingDetail.as_view()),
]
