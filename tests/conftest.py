import django
import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


def pytest_configure(config):
    settings.configure(
        INSTALLED_APPS=["tests"],
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3"}},
    )
    django.setup()
