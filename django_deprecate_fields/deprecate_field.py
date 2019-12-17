import sys
import warnings

from django.db.models import BooleanField, NullBooleanField


class DeprecatedField(object):
    """
    Descriptor class for deprecated fields. Do not use directly, use the
    deprecate_field function instead.
    """

    def __init__(self, val):
        self.val = val

    def _get_name(self, obj):
        """
        Try to find this field's name in the model class
        """
        for k, v in type(obj).__dict__.items():
            if v is self:
                return k
        return '<unknown>'

    def __get__(self, obj, type=None):
        warnings.warn('accessing deprecated field %s.%s' % (
                obj.__class__.__name__, self._get_name(obj)
            ), DeprecationWarning, stacklevel=2)
        if not callable(self.val):
            return self.val
        return self.val()

    def __set__(self, obj, val):
        warnings.warn('writing to deprecated field %s.%s' % (
                obj.__class__.__name__, self._get_name(obj)
            ), DeprecationWarning, stacklevel=2)
        self.val = val


def deprecate_field(field_instance, return_instead=None):
    """
    Can be used in models to delete a Field in a Backwards compatible manner.
    The process for deleting old model Fields is:
    1. Mark a field as deprecated by wrapping the field with this function
    2. Wait until (1) is deployed to every relevant server/branch
    3. Delete the field from the model.

    For (1) and (3) you need to run ./manage.py makemigrations:
    :param field_instance: The field to deprecate
    :param return_instead: A value or function that
    the field will pretend to have
    """
    if not set(sys.argv) & {"makemigrations", "migrate", "showmigrations"}:
        return DeprecatedField(return_instead)

    if not type(field_instance) == BooleanField:
        field_instance.null = True
        return field_instance

    # A BooleanField does not allow null=True, so we need to cast
    # this to a NullBooleanField
    return NullBooleanField(
        help_text=field_instance.help_text,
        default=field_instance.default
    )
