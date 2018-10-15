import sys

from django.db.models import BooleanField, NullBooleanField


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
    if not set(sys.argv) & {"makemigrations", "migrate"}:
        if not callable(return_instead):
            return return_instead
        return return_instead()
    
    if not type(field_instance) == BooleanField:
        field_instance.null = True
        return field_instance
    
    # A BooleanField does not allow null=True, so we need to cast
    # this to a NullBooleanField
    return NullBooleanField(
        help_text=field_instance.help_text,
        default=field_instance.default
    )
