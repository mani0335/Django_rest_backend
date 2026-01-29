from rest_framework import serializers
from .models import Interest


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'from_user', 'to_user', 'created_at']
        read_only_fields = ['from_user', 'created_at']
