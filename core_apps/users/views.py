from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

User = get_user_model()
# Create your views here.


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
