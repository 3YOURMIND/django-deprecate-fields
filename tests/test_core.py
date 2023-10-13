import pytest

from django_deprecate_fields.deprecate_field import DeprecatedField
from tests.models import DeprecationModel


class TestCore:
    @pytest.mark.filterwarnings('ignore::DeprecationWarning')
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
