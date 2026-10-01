from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import NewsPrediction
from ml.predict import PredictionService

def home(request):
    return render(request, "home.html")

@login_required
def detect_view(request):
    return render(request, "detector/detect.html")

@login_required
def result_view(request, prediction_id=None):
    if prediction_id:
        result = get_object_or_404(NewsPrediction, id=prediction_id, user=request.user)
        return render(request, "detector/result.html", {"result": result})
    return redirect("detect")

def about_view(request):
    return render(request, "about.html")

def contact_view(request):
    return render(request, "contact.html")
