"""
URL configuration for moto_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/catalog/', include('catalog.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # это "сырая" схема в формате OpenAPI (YAML/JSON) — машиночитаемая,
    # сама по себе для человека не особо удобна

    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # это уже удобный визуальный интерфейс — Swagger UI,
    # где можно посмотреть все эндпоинты и даже потестить их прямо
    # в браузере (нажал "Try it out" → отправил запрос → увидел ответ)

    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # альтернативный вид документации, ReDoc — просто другой стиль
    # отображения той же схемы, некоторым больше нравится читать
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
