from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    # generics.CreateAPIView — готовая вьюха только под POST/создание,
    # не нужно писать вручную save()/Response(), DRF всё делает сам
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    # AllowAny — обязательно, иначе DRF по умолчанию потребует
    # авторизацию, а зарегистрироваться неавторизованный юзер
    # как раз и должен мочь

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return  self.request.user
# Create your views here.
