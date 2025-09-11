from django.test import TestCase
from core.application.services.pricing_service import compute_booking_price

class PricingServiceTest(TestCase):
    def test_compute_booking_price_minimum_one_day(self):
        self.assertEqual(compute_booking_price(100, 0), 100.0)
        self.assertEqual(compute_booking_price(100, 1), 100.0)
        self.assertEqual(compute_booking_price(100, 2), 200.0)
