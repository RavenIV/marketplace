from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .views import CategoryListView, ProductViewSet, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'products', ProductViewSet, basename='product')
router_v1.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.jwt')),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('products/<str:product_slug>/shopping/',
    #      ShoppingCartView.as_view(), name='shopping')
]
