from django.urls import path
from .views import OrderListView, OrderDetailView, CheckoutView, UpdateOrderStatusView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='order-status-update'),
]