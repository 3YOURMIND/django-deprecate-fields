import pytest

from django_deprecate_fields.deprecate_field import DeprecatedField
from tests.models import DeprecationModel


@pytest.mark.filterwarnings('ignore::DeprecationWarning')
class TestCore:
    def test_descriptor_access(self):
        """
        Test that accessing a descriptor through Model class works.

        When accessing a descriptor through a Model instance (i.e. a concrete
        record), the result should be whatever logic the descriptor is set up
        to execute.

        When accessing a descriptor through a Model class, the result should be
        the descriptor itself as there is no object on which to act.
        """
        assert DeprecationModel().foo is None
        assert isinstance(DeprecationModel.foo, DeprecatedField)

    def test_static_return_instead(self):
        """
        Test that a deprecated field with a static return_instead value works.
        """
        assert DeprecationModel().bar == "bar"

    def test_function_return_instead(self):
        """
        Test that a deprecated field with a function-based return_instead works.
        """
        assert DeprecationModel().baz == "baz"

    def test_method_return_instead(self):
        """
        Test that a deprecated field with a method-based return_instead works.
        """
        dm = DeprecationModel(eggs="eggs")
        assert dm.ham == "eggs"
        assert dm.ham == dm.eggs
