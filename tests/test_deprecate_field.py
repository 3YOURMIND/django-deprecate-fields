from __future__ import annotations

import unittest
import warnings
from unittest.mock import patch

from django.test import override_settings

from django_deprecate_fields import DeprecatedField, FieldDeprecatedError, deprecate_field


class _MockField:
    null = False


class TestDeprecatedFieldDescriptor(unittest.TestCase):

    @staticmethod
    def _make_class(return_instead=None, raise_on_access=False):
        return type(
            "MyModel",
            (),
            {"my_field": DeprecatedField(return_instead, raise_on_access=raise_on_access)},
        )

    def test_read_emits_deprecation_warning(self):
        obj = self._make_class()()
        with self.assertWarns(DeprecationWarning):
            _ = obj.my_field

    def test_read_logs_warning(self):
        obj = self._make_class()()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with self.assertLogs("django_deprecate_fields.deprecate_field", level="WARNING") as cm:
                _ = obj.my_field
        self.assertTrue(any("my_field" in msg for msg in cm.output))

    def test_read_class_level_returns_descriptor(self):
        MyModel = self._make_class()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = MyModel.my_field
        self.assertIsInstance(result, DeprecatedField)
        self.assertFalse(any(issubclass(w.category, DeprecationWarning) for w in caught))

    def test_read_default_return_is_none(self):
        obj = self._make_class()()
        with self.assertWarns(DeprecationWarning):
            result = obj.my_field
        self.assertIsNone(result)

    def test_read_returns_return_instead_value(self):
        obj = self._make_class(return_instead="legacy_value")()
        with self.assertWarns(DeprecationWarning):
            result = obj.my_field
        self.assertEqual(result, "legacy_value")

    def test_read_calls_return_instead_callable(self):
        call_count = []

        def factory():
            call_count.append(1)
            return "from_callable"

        obj = self._make_class(return_instead=factory)()
        with self.assertWarns(DeprecationWarning):
            result = obj.my_field
        self.assertEqual(result, "from_callable")
        self.assertEqual(len(call_count), 1)

    def test_read_raises_on_access(self):
        obj = self._make_class(raise_on_access=True)()
        with self.assertRaises(FieldDeprecatedError):
            _ = obj.my_field

    def test_write_emits_deprecation_warning(self):
        obj = self._make_class()()
        with self.assertWarns(DeprecationWarning):
            obj.my_field = "new_value"

    def test_write_logs_warning(self):
        obj = self._make_class()()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with self.assertLogs("django_deprecate_fields.deprecate_field", level="WARNING") as cm:
                obj.my_field = "new_value"
        self.assertTrue(any("my_field" in msg for msg in cm.output))

    def test_write_raises_on_access(self):
        obj = self._make_class(raise_on_access=True)()
        with self.assertRaises(FieldDeprecatedError):
            obj.my_field = "new_value"

    def test_read_warning_message_format(self):
        obj = self._make_class()()
        with self.assertWarnsRegex(
            DeprecationWarning, r"accessing deprecated field MyModel\.my_field"
        ):
            _ = obj.my_field

    def test_write_warning_message_format(self):
        obj = self._make_class()()
        with self.assertWarnsRegex(
            DeprecationWarning, r"writing to deprecated field MyModel\.my_field"
        ):
            obj.my_field = "x"

    def test_field_name_unknown_when_descriptor_not_on_class(self):
        descriptor = DeprecatedField(None)
        obj = type("MyModel", (), {})()
        with self.assertWarnsRegex(DeprecationWarning, r"<unknown>"):
            descriptor.__get__(obj, type(obj))


class TestDeprecateFieldFunction(unittest.TestCase):

    def test_normal_mode_returns_descriptor(self):
        with patch("sys.argv", ["manage.py"]):
            result = deprecate_field(_MockField())
        self.assertIsInstance(result, DeprecatedField)

    def test_makemigrations_returns_field(self):
        field = _MockField()
        with patch("sys.argv", ["manage.py", "makemigrations"]):
            result = deprecate_field(field)
        self.assertIs(result, field)

    def test_migrate_returns_field(self):
        field = _MockField()
        with patch("sys.argv", ["manage.py", "migrate"]):
            result = deprecate_field(field)
        self.assertIs(result, field)

    def test_showmigrations_returns_field(self):
        field = _MockField()
        with patch("sys.argv", ["manage.py", "showmigrations"]):
            result = deprecate_field(field)
        self.assertIs(result, field)

    def test_migration_command_sets_null_true(self):
        field = _MockField()
        with patch("sys.argv", ["manage.py", "makemigrations"]):
            result = deprecate_field(field)
        self.assertTrue(result.null)

    def test_return_instead_passed_to_descriptor(self):
        with patch("sys.argv", ["manage.py"]):
            result = deprecate_field(_MockField(), return_instead="sentinel")
        self.assertIsInstance(result, DeprecatedField)
        self.assertEqual(result.val, "sentinel")

    def test_raise_on_access_passed_to_descriptor(self):
        with patch("sys.argv", ["manage.py"]):
            result = deprecate_field(_MockField(), raise_on_access=True)
        self.assertIsInstance(result, DeprecatedField)
        self.assertTrue(result.raise_on_access)

    @override_settings(DEPRECATE_FIELD_CUSTOM_MIGRATION_COMMAND={"pgmakemigrations"})
    def test_custom_command_returns_field(self):
        field = _MockField()
        with patch("sys.argv", ["manage.py", "pgmakemigrations"]):
            result = deprecate_field(field)
        self.assertIs(result, field)

    @override_settings(DEPRECATE_FIELD_CUSTOM_MIGRATION_COMMAND={"pgmakemigrations"})
    def test_custom_command_nonmatching_returns_descriptor(self):
        with patch("sys.argv", ["manage.py", "runserver"]):
            result = deprecate_field(_MockField())
        self.assertIsInstance(result, DeprecatedField)
