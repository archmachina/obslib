
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

