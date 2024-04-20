from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryReadViewSet,
    ProductReadViewSet,
    ShoppingView,
    ShoppingCartView,
    SubcategoryReadViewset,
    UserViewSet,
)

router_v1 = DefaultRouter()
router_v1.register(r'categories',
                   CategoryReadViewSet,
                   basename='category')
router_v1.register(r'subcategories',
                   SubcategoryReadViewset,
                   basename='subcategory')
router_v1.register(r'products',
                   ProductReadViewSet,
                   basename='product')
router_v1.register(r'users',
                   UserViewSet,
                   basename='user')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.jwt')),
    path('schema/docs/',
         SpectacularSwaggerView.as_view(url_name='schema')),
    path('schema/',
         SpectacularAPIView.as_view(),
         name='schema'),
    path('products/<str:product_slug>/shopping/',
         ShoppingView.as_view(),
         name='shopping'),
    path('shopping-cart/',
         ShoppingCartView.as_view(),
         name='cart')
]
