from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.authentication import JWTAuthentication


@database_sync_to_async
def get_user(token_key: str):
    try:
        jwt_object = JWTAuthentication()
        print(jwt_object)
        validated_token = jwt_object.get_validated_token(token_key)
        print(jwt_object)
        user = jwt_object.get_user(validated_token)
        return user
    except Exception:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Take the token from headers, and add user or anonymous user to
    the scope depending upon the validity of the token.
    """

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            try:
                _, token_key = headers[b"authorization"].decode().split()
            except ValueError:
                token_key = None
            scope["user"] = (
                AnonymousUser() if token_key is None else await get_user(token_key)
            )
            return await super().__call__(scope, receive, send)

        scope["user"] = AnonymousUser()
        return await super().__call__(scope, receive, send)
