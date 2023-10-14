from django_deprecate_fields import deprecate_field
from django.db import models


class DeprecationModel(models.Model):
    foo = deprecate_field(models.IntegerField())
