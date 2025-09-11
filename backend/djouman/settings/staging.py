from .base import *

DEBUG = False

# Staging proche de la prod, mais sans forcer SSL si besoin
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "false").lower() == "true"

# WhiteNoise activable par env
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
