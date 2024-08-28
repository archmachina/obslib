
import obslib
import pytest

class TestExtractProperty:
    def test_extract_property1(self):
        source = {
            "prop1": 1
        }

        value = obslib.extract_property(source, "prop1")

        assert(value == 1)
        assert(len(source.keys()) == 0)

    def test_extract_property2(self):
        source = {
            "prop1": 1
        }

        value = obslib.extract_property(source, "prop1")

        assert(value == 1)
        assert(len(source.keys()) == 0)

    def test_required_value(self):
        source = {
            "prop1": 1
        }

        with pytest.raises(KeyError):
            value = obslib.extract_property(source, "prop2")

    def test_optional_value(self):
        source = {
            "prop1": 1
        }

        value = obslib.extract_property(source, "prop2", optional=True)

        assert(value is None)

