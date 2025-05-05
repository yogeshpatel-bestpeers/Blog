from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from Blog.models import CustomUser
from Blog.utils import generate_password_reset_link, send_custom_email
from BlogDRF.serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    UserSerializer,
)


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = CustomUser.objects.get(email=email)
            reset_link = generate_password_reset_link(user, request)
            send_custom_email(
                subject="Reset Your Password",
                message=f"Click the link to reset your password: {reset_link}",
                recipient_email=email,
            )
            return Response(
                {"message": "Password reset link sent."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data["uidb64"]
            token = serializer.validated_data["token"]
            password = serializer.validated_data["password"]

            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = CustomUser.objects.get(pk=uid)
            except Exception:
                return Response(
                    {"error": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST
                )

            token_generator = PasswordResetTokenGenerator()
            if token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response(
                    {"message": "Password has been reset successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return Response(
                {
                    "username": user.username,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response(
            {"message": "Logout Sucessfull"}, status=status.HTTP_202_ACCEPTED
        )
