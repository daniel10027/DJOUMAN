from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class BurstAnonThrottle(AnonRateThrottle):
    rate = "20/min"

class BurstUserThrottle(UserRateThrottle):
    rate = "60/min"
