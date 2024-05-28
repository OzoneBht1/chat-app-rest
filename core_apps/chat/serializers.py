from rest_framework import serializers

from core_apps.users.serializers import PublicUserInfoSerializer

from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer class for Chat Message. The sender and receiver
    fields are serialized with only publicly accessible information
    of the user.
    """

    sender = PublicUserInfoSerializer()
    receiver = PublicUserInfoSerializer()

    class Meta:
        model = ChatMessage
        fields = "__all__"
