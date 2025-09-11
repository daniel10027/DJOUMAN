from django.urls import reverse
from rest_framework.test import APITestCase

class AuthApiTest(APITestCase):
    def test_register_and_login(self):
        url = reverse("auth-register")
        data = {"username": "bob", "email": "bob@test.com", "password": "secret123"}
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

        url = reverse("auth-login")
        res = self.client.post(url, {"identifier": "bob", "password": "secret123"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
