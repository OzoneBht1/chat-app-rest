from channels.consumer import database_sync_to_async
import pytest

from core_apps.chat.models import ChatMessage
from core_apps.tests.factories import UserFactory
from channels.testing import WebsocketCommunicator
from config.asgi import application
from rest_framework_simplejwt.tokens import RefreshToken


@database_sync_to_async
def create_user():
    user = UserFactory.create()
    token = RefreshToken.for_user(user)
    return user, str(token.access_token)


@database_sync_to_async
def remove_user(user):
    return user.delete()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_connection():
    user1, token1 = await create_user()
    user2, token2 = await create_user()

    communicator = WebsocketCommunicator(
        application,
        f"/ws/chat/{user2.id}/",
        headers=[(b"authorization", f"Bearer {token1}".encode())],
    )

    connected, subprotocol = await communicator.connect()
    assert connected

    message = "Hello, user2!"
    await communicator.send_json_to({"message": message})

    # Receive the message
    response = await communicator.receive_json_from()
    assert response == {
        "type": "chat.message",
        "message": message,
        "sender": user1.username,
    }

    # Check the message was saved to the database
    chat_message = await database_sync_to_async(ChatMessage.objects.get)(
        sender=user1, receiver=user2, message=message
    )
    assert chat_message is not None

    # Close the connection
    await remove_user(user1)
    await remove_user(user2)
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_invalid_user():
    user, token = await create_user()

    invalid_user_id = 9999
    communicator = WebsocketCommunicator(
        application,
        f"/ws/chat/{invalid_user_id}/",
        headers=[(b"authorization", f"Bearer {token}".encode())],
    )

    connected, subprotocol = await communicator.connect()
    assert not connected

    await communicator.disconnect()
    await remove_user(user)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_websocket_anonymous_user():
    user, _ = await create_user()

    communicator = WebsocketCommunicator(
        application,
        f"/ws/chat/{user.id}/",
    )

    connected, subprotocol = await communicator.connect()
    assert not connected

    await communicator.disconnect()
    await remove_user(user)
