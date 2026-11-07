from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .utils import SetCookiesUtil
from .models import User

# Create your views here.

class RegisterView(APIView, SetCookiesUtil):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = Response(
            {
                "message": "User registered successfully.",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )
        return response

class LoginView(TokenObtainPairView, SetCookiesUtil):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        response = Response({"user": serializer.validated_data['user'], "access": str(access)}, status=status.HTTP_200_OK)
        self.set_refresh_cookie(response, str(refresh))

        return response

class RefreshView(TokenRefreshView, SetCookiesUtil):
    permission_classes = [AllowAny]
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token provided."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
            response = Response({"access": str(access)}, status=status.HTTP_200_OK)
            return response
        except Exception:
            return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView, SetCookiesUtil):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        self.clear_refresh_cookie(response)
        return response

class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)