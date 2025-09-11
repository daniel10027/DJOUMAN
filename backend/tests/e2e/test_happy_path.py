from django.urls import reverse
from rest_framework.test import APITestCase
from infrastructure.persistence.models import User

class HappyPathTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", email="alice@test.com", password="pass123")

    def test_flow_booking(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("categories-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
