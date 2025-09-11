from django.urls import reverse
from rest_framework.test import APITestCase
from infrastructure.persistence.models import User

class CommissionApiTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin", email="a@a.a", password="pwd", role="admin")

    def test_list_commissions(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("commissions-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
