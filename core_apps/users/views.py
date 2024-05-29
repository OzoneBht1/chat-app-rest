from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, PublicUserInfoSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Register a new User.
    """

    queryset = User.objects.all()
    permission_classes = []
    authentication_classes = []
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    """
    Blacklist the refresh token when the user logs out.
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh Token is required."}, status=400)
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserListApiView(generics.ListAPIView):
    """
    An API to get a list of user's publicly available information
    to select them for starting a chat conversation.
    """

    serializer_class = PublicUserInfoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.get_regular_users()
