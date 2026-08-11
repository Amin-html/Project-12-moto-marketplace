from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from .models import SellerProfile

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

class VerifySellerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, seller_id):
        if request.user.role != 'admin':
            return Response({'error': 'Only admin can verify sellers'}, status=403)

        try:
            profile = SellerProfile.objects.get(user_id=seller_id)
        except SellerProfile.DoesNotExist:
            return Response({'error': 'Seller profile not found'}, status=404)

        profile.is_verified = True
        profile.save()

        return Response({'status': 'verified', 'shop_name': profile.shop_name})
# Create your views here.
