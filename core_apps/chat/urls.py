from django.urls import path
from .views import ChatMessageHistoryListApiView


urlpatterns = [
    path(
        "history/<int:user_id>/",
        ChatMessageHistoryListApiView.as_view(),
        name="chat_message_history",
    )
]
