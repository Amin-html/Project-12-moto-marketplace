from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
# get_user_model() вместо прямого импорта User —
# так serializer не завязан на конкретный класс, а всегда берёт
# то, что указано в AUTH_USER_MODEL. Хорошая практика.

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    # write_only=True — пароль принимаем на вход, но никогда не отдаём
    # обратно в JSON-ответе (иначе он утечёт в response)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone']

    def create(self, validated_data):
        # ВАЖНО: именно так, а не User.objects.create(**validated_data) —
        # это была одна из твоих старых ошибок (пароль без хеша).
        # create_user() сам вызывает set_password() внутри.
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    """Для отображения текущего юзера (/me/), без пароля вообще."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone']