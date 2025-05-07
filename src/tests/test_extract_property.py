
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

    def test_optional_value1(self):
        source = {
            "prop1": 1
        }

        value = obslib.extract_property(source, "prop2", optional=True)

        assert value is None

    def test_optional_value2(self):
        source = {
            "prop1": 1
        }

        with pytest.raises(KeyError):
            value = obslib.extract_property(source, "prop2", optional=False)

            assert value is None

    def test_replace_none1(self):
        source = {
            "prop1": None
        }

        value = obslib.extract_property(source, "prop1", default=5, replace_none=False)

        assert value is None

    def test_replace_none2(self):
        source = {
            "prop1": None
        }

        value = obslib.extract_property(source, "prop1", default=5, replace_none=True)

        assert value == 5

    def test_extract_remove1(self):
        source = {
            "test1": 1,
            "test2": 2,
            "test3": 3
        }

        test1 = obslib.extract_property(source, "test1")
        test2 = obslib.extract_property(source, "test2")

        assert isinstance(test1, int) and test1 == 1
        assert isinstance(test2, int) and test2 == 2

        assert len(source.keys()) == 1 and "test3" in source
        assert source["test3"] == 3

    def test_extract_remove2(self):
        source = {
            "test1": 1,
            "test2": 2,
            "test3": 3
        }

        test1 = obslib.extract_property(source, "test1", remove=False)
        test2 = obslib.extract_property(source, "test2", remove=False)

        assert isinstance(test1, int) and test1 == 1
        assert isinstance(test2, int) and test2 == 2

        assert len(source.keys()) == 3

        assert "test1" in source and isinstance(source["test1"], int)
        assert "test2" in source and isinstance(source["test2"], int)
        assert "test3" in source and isinstance(source["test3"], int)

        assert source["test1"] == 1
        assert source["test2"] == 2
        assert source["test3"] == 3

