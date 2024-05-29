from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Common(models.Model):
    """
    Abstract model to be inherited as a base which
    provides datetimestamps for the models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ChatMessage(Common):
    """
    A model to track chat messages.
    """

    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    message = models.TextField()

    class Meta:
        ordering = ("-created_at",)
