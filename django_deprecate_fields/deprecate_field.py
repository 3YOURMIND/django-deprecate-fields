import logging
import sys
import warnings

logger = logging.getLogger(__name__)


class FieldDeprecatedError(Exception):
    pass


class DeprecatedField(object):
    """
    Descriptor class for deprecated fields. Do not use directly, use the
    deprecate_field function instead.
    """

    def __init__(self, val, raise_on_access=False):
        self.val = val
        self.raise_on_access = raise_on_access

    def _get_name(self, obj):
        """
        Try to find this field's name in the model class
        """
        for k, v in type(obj).__dict__.items():
            if v is self:
                return k
        return "<unknown>"

    def __get__(self, obj, type=None):
        msg = "accessing deprecated field %s.%s" % (
            obj.__class__.__name__,
            self._get_name(obj),
        )
        if self.raise_on_access:
            raise FieldDeprecatedError(msg)

        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        logger.warning(msg)
        if not callable(self.val):
            return self.val
        return self.val()

    def __set__(self, obj, val):
        msg = "writing to deprecated field %s.%s" % (
            obj.__class__.__name__,
            self._get_name(obj),
        )
        if self.raise_on_access:
            raise FieldDeprecatedError(msg)

        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        logger.warning(msg)
        self.val = val


def deprecate_field(field_instance, return_instead=None, raise_on_access=False, commands_requiring_concrete_class=None):
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
    :param raise_on_access: If true, raise FieldDeprecated instead of logging a warning
    :param commands_requiring_concrete_class: A set of commands that need the actual field
    """
    base_django_migration_commands = {"makemigrations", "migrate", "showmigrations"}
    exhaustive_commands = base_django_migration_commands | (
            commands_requiring_concrete_class or set()
    )
    if not set(sys.argv) & exhaustive_commands:
        return DeprecatedField(return_instead, raise_on_access=raise_on_access)

    field_instance.null = True
    return field_instance
