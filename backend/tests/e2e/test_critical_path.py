from django.urls import reverse
from rest_framework.test import APITestCase
from infrastructure.persistence.models import User, ServiceCategory, Service, Booking, Payment
from datetime import datetime, timedelta, timezone

class CriticalPathTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", email="alice@test.com", password="pass123")
        self.client.force_authenticate(user=self.user)
        self.cat = ServiceCategory.objects.create(name="Nettoyage", slug="nettoyage")
        self.service = Service.objects.create(category=self.cat, owner=self.user, title="Ménage", base_price=1000)

    def test_flow(self):
        # Créer booking
        url = reverse("bookings-list")
        start = datetime.now(timezone.utc)
        end = start + timedelta(days=1, hours=2)
        res = self.client.post(url, {
            "service": self.service.id,
            "equipment": None,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        }, format="json")
        self.assertEqual(res.status_code, 201)
        booking_id = res.data["id"]

        # Confirmer booking
        url = reverse("bookings-confirm", args=[booking_id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 200)

        # Payment intent
        url = reverse("payments-create-intent")
        res = self.client.post(url, {
            "booking_id": booking_id,
            "method": "wave",
            "amount": "3000.00",
            "currency": "XOF",
            "idempotency_key": "idem-1",
        }, format="json")
        self.assertEqual(res.status_code, 201)
        payment_id = res.data["id"]
        provider_ref = res.data["provider_ref"]

        # Webhook success (Wave)
        url = reverse("payment-webhooks-wave")
        res = self.client.post(url, {"provider_ref": provider_ref, "status": "succeeded"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Payment.objects.filter(id=payment_id, status="succeeded").exists())

        # Générer contrat
        url = reverse("contracts-generate")
        res = self.client.post(url, {"booking_id": booking_id, "context": {"client": "alice"}}, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertIn("file_url", res.data)