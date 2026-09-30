from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class APITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="StrongPassword123!")

    def test_predict_requires_auth(self):
        response = self.client.post(reverse("api-predict"), data={"news_text":"This is a sufficiently long news text for testing."}, content_type="application/json")
        self.assertEqual(response.status_code, 403)
