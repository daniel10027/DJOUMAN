from .base import *

DEBUG = False

# Sécurité
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "true").lower() == "true"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Optionnel: si tu es derrière un proxy/ELB
if os.getenv("SECURE_PROXY_SSL_HEADER", "true").lower() == "true":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF Trusted Origins (ex: https://api.domain.com,https://admin.domain.com)
_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
if _csrf:
    CSRF_TRUSTED_ORIGINS = [s.strip() for s in _csrf.split(",") if s.strip()]

# WhiteNoise recommandée en production (active via env)
USE_WHITENOISE = os.getenv("USE_WHITENOISE", "true").lower() == "true"
if USE_WHITENOISE and "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
        "default": {
            "BACKEND": os.getenv("DEFAULT_FILE_STORAGE", "django.core.files.storage.FileSystemStorage"),
        },
    }
