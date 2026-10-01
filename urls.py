from django.urls import path
from .views import home, detect_view, result_view, about_view, contact_view

urlpatterns = [
    path("", home, name="home"),
    path("detect/", detect_view, name="detect"),
    path("result/<int:prediction_id>/", result_view, name="result"),
    path("about/", about_view, name="about"),
    path("contact/", contact_view, name="contact"),
]
