from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import NotFound

from core_apps.chat.models import ChatMessage

from .serializers import ChatMessageSerializer

User = get_user_model()

# Create your views here.


class ChatMessageHistoryListApiView(generics.ListAPIView):
    """
    API view to fetch chat message history between the current user and another user.
    The messages are ordered by creation date in descending order.
    """
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        current_user = self.request.user
        other_user_id = self.kwargs["user_id"]

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist as e:
            raise NotFound(
                f"User with requested ID {other_user_id} does not exist."
            ) from e

        return (
            ChatMessage.objects.filter(
                Q(sender=current_user, receiver=other_user)
                | Q(sender=other_user, receiver=current_user)
            )
            .select_related("sender", "receiver")
            .order_by("-created_at")
        )
