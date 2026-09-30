from django.urls import path
from .views import PredictAPIView, HistoryAPIView, DashboardAPIView, ModelPerformanceAPIView, AdminStatsAPIView

urlpatterns = [
    path("predict/", PredictAPIView.as_view(), name="api-predict"),
    path("history/", HistoryAPIView.as_view(), name="api-history"),
    path("dashboard/", DashboardAPIView.as_view(), name="api-dashboard"),
    path("model-performance/", ModelPerformanceAPIView.as_view(), name="api-model-performance"),
    path("admin-stats/", AdminStatsAPIView.as_view(), name="api-admin-stats"),
]
