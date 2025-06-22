from django.urls import path
from . import views
from .api_views import ProductListView

from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LogoutView
from .views import custom_logout_view


urlpatterns = [
    path('', views.home, name='home'),
    path('product/create/', views.create_product, name='create-product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:pk>/', views.update_cart_quantity, name='update-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:pk>/', views.order_confirmation, name='order-confirmation'),
    path('my-orders/', views.my_orders, name='my-orders'),

    #auth
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
# sher123
# Sher@716