from django.urls import path
from core.views import health_check, DeepSeekAnalysisView  # Importación ABSOLUTA

urlpatterns = [
    path('api/health/', health_check, name='health-check'),
    path('api/deepseek/', DeepSeekAnalysisView.as_view(), name='deepseek-analysis'),
]