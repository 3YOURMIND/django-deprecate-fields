SECRET_KEY = "django-deprecate-fields-test-secret-key"

INSTALLED_APPS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
