from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# DB locale sqlite (héritée de base.py si non override)
DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

# Emails en console en local
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# WhiteNoise inutil en dev (toggle si tu veux tester)
USE_WHITENOISE = os.getenv("USE_WHITENOISE", "false").lower() == "true"
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
