import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
# без этого маркера тест НЕ сможет трогать базу данных вообще —
# pytest-django специально блокирует доступ к БД по умолчанию,
# чтобы тесты случайно не тыкались в реальные данные
class TestUserModel:
    def test_create_user_default_role(self):
        user = User.objects.create_user(username='test', password='pass12345')
        assert user.role == User.Role.CUSTOMER
        # проверяем что дефолтная роль правильно выставляется

    def test_is_seller_method(self):
        user = User.objects.create_user(
            username='seller1', password='pass12345', role=User.Role.SELLER,
        )
        assert user.is_seller() is True

    def test_customer_is_not_seller(self):
        user = User.objects.create_user(username='cust1', password='pass12345')
        assert user.is_seller() is False