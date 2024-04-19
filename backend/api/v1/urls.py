from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
    path('schema/', SpectacularAPIView.as_view(), name='schema')
]