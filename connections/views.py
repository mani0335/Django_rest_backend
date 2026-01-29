from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Connection

User = get_user_model()


class SendConnectionRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get("receiver_id")

        if not receiver_id:
            return Response(
                {"error": "receiver_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if int(receiver_id) == request.user.id:
            return Response(
                {"error": "You cannot connect with yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Receiver not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if Connection.objects.filter(
            sender=request.user,
            receiver=receiver
        ).exists():
            return Response(
                {"error": "Request already sent"},
                status=status.HTTP_400_BAD_REQUEST
            )

        Connection.objects.create(
            sender=request.user,
            receiver=receiver,
            status="pending"
        )

        return Response(
            {"message": "Connection request sent"},
            status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_connection(request):
    connection_id = request.data.get("connection_id")

    if not connection_id:
        return Response(
            {"error": "connection_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        connection = Connection.objects.get(id=connection_id)
    except Connection.DoesNotExist:
        return Response(
            {"error": "Connection not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if connection.receiver != request.user:
        return Response(
            {"error": "You are not allowed to accept this request"},
            status=status.HTTP_403_FORBIDDEN
        )

    connection.status = "accepted"
    connection.save()

    return Response(
        {"message": "Connection accepted"},
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_connections(request):
    user = request.user

    connections = Connection.objects.filter(
        status="accepted",
        sender=user
    ) | Connection.objects.filter(
        status="accepted",
        receiver=user
    )

    data = []
    for conn in connections:
        other_user = conn.receiver if conn.sender == user else conn.sender
        data.append({
            "connection_id": conn.id,
            "user_id": other_user.id,
            "username": other_user.username
        })

    return Response(data)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_connection(request, id):
    try:
        connection = Connection.objects.get(id=id)
        connection.delete()
        return Response({"message": "Connection removed successfully"})
    except Connection.DoesNotExist:
        return Response({"error": "Connection not found"}, status=404)