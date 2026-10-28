from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ser = LoginSerializer(data=request.data, context={"request": request})
        ser.is_valid(raise_exception=True)
        u = ser.validated_data["user"]

        tok = RefreshToken.for_user(u)
        return Response(
            {
                "user": {"id": u.id, "name": u.name, "email": u.email},
                "access": str(tok.access_token),
                "refresh": str(tok),
            },
            status=status.HTTP_200_OK,
        )