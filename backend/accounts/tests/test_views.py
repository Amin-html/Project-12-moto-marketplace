import pytest
from rest_framework.test import APIClient

@pytest.fixture
# fixture — переиспользуемый "заготовленный" объект для тестов,
# чтобы не писать APIClient() в каждом тесте вручную
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestRegisterView:
    def test_register_success(self, api_client):
        response = api_client.post('/api/auth/register/', {
            'username': 'newuser',
            'password': 'strongpass123',
            'email': 'new@test.com',
        })
        assert response.status_code == 201
        assert 'password' not in response.data
        # проверяем и то, что write_only реально работает —
        # пароль не должен утечь в ответе

    def test_register_password_is_hashed(self, api_client):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        api_client.post('/api/auth/register/', {
            'username': 'hashtest',
            'password': 'strongpass123',
        })
        user = User.objects.get(username='hashtest')
        assert user.password != 'strongpass123'
        # если бы кто-то по ошибке использовал create() вместо
        # create_user() — пароль хранился бы как есть, plain text,
        # этот тест бы это поймал


@pytest.mark.django_db
class TestLoginView:
    def test_login_returns_tokens(self, api_client):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.create_user(username='loginuser', password='strongpass123')

        response = api_client.post('/api/auth/login/', {
            'username': 'loginuser',
            'password': 'strongpass123',
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data