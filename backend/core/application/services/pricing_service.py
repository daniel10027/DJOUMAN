def compute_booking_price(base: float, days: int = 1) -> float:
    if days < 1:
        days = 1
    return round(base * days, 2)
