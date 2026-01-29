from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction

from .models import Interest
from .serializers import InterestSerializer
from connections.models import Connection
from django.contrib.auth import get_user_model

User = get_user_model()


class InterestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get("to_user")

        if not receiver_id:
            return Response(
                {"error": "to_user is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if sender.id == int(receiver_id):
            return Response(
                {"error": "You cannot show interest in yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent duplicate interest
        if Interest.objects.filter(sender=sender, receiver=receiver).exists():
            return Response(
                {"error": "Interest already sent"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            interest = Interest.objects.create(
                sender=sender,
                receiver=receiver
            )

            # Mutual interest → auto connection
            if Interest.objects.filter(
                sender=receiver,
                receiver=sender
            ).exists():
                Connection.objects.get_or_create(
                    sender=sender,
                    receiver=receiver,
                    defaults={"status": "accepted"}
                )

        serializer = InterestSerializer(interest)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
