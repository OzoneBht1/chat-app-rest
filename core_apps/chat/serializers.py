from rest_framework import serializers

from core_apps.users.serializers import PublicUserInfoSerializer

from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = PublicUserInfoSerializer()
    receiver = PublicUserInfoSerializer()

    class Meta:
        model = ChatMessage
        fields = "__all__"
