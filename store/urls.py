from django.urls import path
from . import views
from .api_views import ProductListView

urlpatterns = [
    path('', views.home, name='home'),
    path('product/create/', views.create_product, name='create-product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/', ProductListView.as_view(), name='product-list'),
]