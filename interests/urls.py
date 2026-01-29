from django.urls import path
from .views import InterestCreateView

urlpatterns = [
    path("", InterestCreateView.as_view(), name="interest"),
]
