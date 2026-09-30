from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PredictionCreateSerializer, NewsPredictionSerializer, ModelPerformanceSerializer
from detector.models import NewsPrediction, ModelPerformance
from ml.predict import PredictionService

class PredictAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PredictionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = PredictionService().predict(serializer.validated_data["news_text"])
        except FileNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        record = NewsPrediction.objects.create(
            user=request.user,
            news_text=serializer.validated_data["news_text"],
            news_url=serializer.validated_data.get("news_url") or None,
            **result,
        )
        return Response(NewsPredictionSerializer(record).data, status=status.HTTP_201_CREATED)

class HistoryAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = NewsPrediction.objects.filter(user=request.user)[:100]
        return Response(NewsPredictionSerializer(qs, many=True).data)

class DashboardAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = NewsPrediction.objects.filter(user=request.user)
        return Response({
            "total_predictions": qs.count(),
            "real_count": qs.filter(prediction="REAL").count(),
            "fake_count": qs.filter(prediction="FAKE").count(),
            "recent_predictions": NewsPredictionSerializer(qs[:10], many=True).data,
        })

class ModelPerformanceAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ModelPerformanceSerializer(ModelPerformance.objects.all()[:20], many=True).data)

class AdminStatsAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_staff or getattr(getattr(request.user, "profile", None), "role", "") == "admin"):
            return Response({"detail": "Admin access required."}, status=403)
        qs = NewsPrediction.objects.all()
        return Response({
            "total_users": User.objects.count(),
            "total_predictions": qs.count(),
            "real_count": qs.filter(prediction="REAL").count(),
            "fake_count": qs.filter(prediction="FAKE").count(),
            "recent_predictions": NewsPredictionSerializer(qs[:10], many=True).data,
            "model_performance": ModelPerformanceSerializer(ModelPerformance.objects.all()[:10], many=True).data,
        })
