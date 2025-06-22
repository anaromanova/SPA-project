from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from spa_project.users.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = []  # доступно всем

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]