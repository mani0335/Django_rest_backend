from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('auth/login', TokenObtainPairView.as_view()),
    path('profile/', include('profiles.urls')),
    path('interest/', include('interests.urls')),

    path("connections/", include("connections.urls")),
]
