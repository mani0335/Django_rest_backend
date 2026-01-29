from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Interest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_interests")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_interests")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")
