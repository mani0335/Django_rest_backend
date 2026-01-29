from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["name", "category", "age", "bio"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        # If viewing own profile → full data
        if instance.user == request.user:
            return data

        # If not connected → hide sensitive fields
        if not self.context.get("is_connected", False):
            data.pop("age", None)
            data.pop("bio", None)

        return data
