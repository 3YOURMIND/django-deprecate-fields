from django_deprecate_fields import deprecate_field
from django.db import models


def calc_baz(_):
    return "baz"


class DeprecationModel(models.Model):
    def _deprecate_ham(self):
        return self.eggs

    foo = deprecate_field(models.IntegerField())
    bar = deprecate_field(models.CharField(max_length=30), return_instead="bar")
    baz = deprecate_field(models.CharField(max_length=30), return_instead=calc_baz)
    eggs = models.CharField(max_length=30, blank=True)
    ham = deprecate_field(models.CharField(max_length=30), return_instead=_deprecate_ham)
