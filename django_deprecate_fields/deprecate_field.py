import logging
import sys
import warnings

from django.utils.encoding import force_str

logger = logging.getLogger(__file__)


class DeprecatedField(object):
    """
    Descriptor class for deprecated fields. Do not use directly, use the
    deprecate_field function instead.
    """

    def __init__(self, val=None, use_current=False, field_name=None):
        self.use_current = use_current
        self.field_name = field_name
        self.val = val

    def __get__(self, instance, type=None):
        msg = "accessing deprecated field %s.%s" % (
            instance.__class__.__name__,
            self.field_name,
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        logger.warning(msg)

        val = self.val

        if self.use_current and val is None:
            val = getattr(instance, self.field_name, None)

        if not callable(val):
            return val

        return val()

    def __set__(self, obj, val):
        msg = "writing to deprecated field %s.%s" % (
            obj.__class__.__name__,
            self._get_name(obj),
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        logger.warning(msg)
        self.val = val


def deprecate_field(field_instance, return_instead=None, use_current=False):
    """
    Can be used in models to delete a Field in a Backwards compatible manner.
    The process for deleting old model Fields is:
    1. Mark a field as deprecated by wrapping the field with this function
    2. Wait until (1) is deployed to every relevant server/branch
    3. Delete the field from the model.

    For (1) and (3) you need to run ./manage.py makemigrations:
    :param field_instance: The field to deprecate
    :param return_instead: A value or function that
    the field will pretend to have.
    :param use_current: A boolean to indicate whether to read the previous 
    value of the field if return_instead=None.
    """
    if not set(sys.argv) & {"makemigrations", "migrate", "showmigrations"}:
        if return_instead is None and use_current:
            field_name = force_str(field_instance.name)
            return DeprecatedField(use_current=use_current, field_name=field_name)
        return DeprecatedField(return_instead)

    field_instance.null = True
    return field_instance
