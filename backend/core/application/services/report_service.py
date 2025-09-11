from django.db.models import Sum, Count
from infrastructure.persistence.models import Booking, Payment

def kpis():
    bookings = Booking.objects.all()
    payments = Payment.objects.all()
    return {
        "bookings_count": bookings.count(),
        "bookings_amount": float(bookings.aggregate(s=Sum("price"))["s"] or 0),
        "payments_succeeded": payments.filter(status="succeeded").count(),
        "commission_amount": float(bookings.aggregate(s=Sum("commission_amount"))["s"] or 0),
    }
