from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Profile
from .serializers import ProfileSerializer
from connections.models import Connection
from django.db.models import Q


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        viewer = request.user

        # View own profile
        if viewer.id == user_id:
            profile = Profile.objects.get(user=viewer)
            serializer = ProfileSerializer(
                profile,
                context={
                    "request": request,
                    "is_connected": True
                }
            )
            return Response(serializer.data)

        # Check accepted connection
        is_connected = Connection.objects.filter(
            Q(sender=viewer, receiver_id=user_id) |
            Q(sender_id=user_id, receiver=viewer),
            status="accepted"
        ).exists()

        if not is_connected:
            return Response(
                {"error": "You are not connected to this user"},
                status=status.HTTP_403_FORBIDDEN
            )

        # View connected user's profile
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(
            profile,
            context={
                "request": request,
                "is_connected": True
            }
        )
        return Response(serializer.data)
