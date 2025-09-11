from django.urls import reverse
from rest_framework.test import APITestCase
from infrastructure.persistence.models import User, ServiceCategory, Service, Profile, UserRole

class MatchingApiTest(APITestCase):
    def setUp(self):
        self.u = User.objects.create_user(username="bob", email="b@b.b", password="pwd", role=UserRole.FREELANCE)
        Profile.objects.create(user=self.u, geo_lat=5.34, geo_lng=-4.02)
        self.cat = ServiceCategory.objects.create(name="Plomberie", slug="plomberie")
        Service.objects.create(category=self.cat, owner=self.u, title="Plombier")

    def test_search(self):
        url = reverse("matching-search")
        res = self.client.get(url, {"category_id": self.cat.id, "lat": 5.34, "lng": -4.02})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(res.data) >= 1)
