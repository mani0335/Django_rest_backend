from django.urls import path
from .views import (
    SendConnectionRequest,
    accept_connection,
    remove_connection
)

urlpatterns = [
    path("send/", SendConnectionRequest.as_view()),
    path("accept/", accept_connection),
    path("remove/<int:id>/", remove_connection),
]
