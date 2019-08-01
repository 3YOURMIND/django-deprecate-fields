import sys
import django

from django.db.models import BooleanField, NullBooleanField


# https://docs.djangoproject.com/en/2.1/ref/models/fields/#booleanfield
USE_NULLBOOLEANFIELD = django.VERSION < (2, 1, 0)


class AccessDeprecatedField(Exception):
    """Raise exception when deprecated field is accessed"""


def raise_exception(self):
    """replacement for a deprecated field"""
    raise AccessDeprecatedField("Deprecated field shouldn't be used anymore!")


def deprecate_field(original_field, return_instead=None, forbid_access=True):
    """
    Can be used in models to delete a Field in a Backwards compatible manner.
    The process for deleting old model Fields is:
    1. Mark a field as deprecated by wrapping the field with this function
    2. Wait until (1) is deployed to every relevant server/branch
    3. Delete the field from the model.

    For (1) and (3) you need to run ./manage.py makemigrations:
    :param original_field: The field to deprecate
    :param return_instead: A value or function that
    :param forbid_access: raise an exception when field is accessed
    the field will pretend to have
    """
    field_to_return = original_field
    if not set(sys.argv) & {"makemigrations", "migrate"}:
        if return_instead is None and forbid_access:
            field_to_return = property(raise_exception)
        elif callable(return_instead):
            field_to_return = return_instead()
        else:
            field_to_return = return_instead
    else:
        if type(field_to_return) == BooleanField and USE_NULLBOOLEANFIELD:
            # A BooleanField does not allow null=True, so we need to cast
            # this to a NullBooleanField for Django < 2.1
            field_to_return = NullBooleanField(
                help_text=field_to_return.help_text,
                default=field_to_return.default
            )
        else:
            field_to_return.null = True
    return field_to_return
