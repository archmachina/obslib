
import obslib
import pytest

class TestObsCoerceInt:
    def test_valid1(self):
        assert(obslib.coerce_value("5", int) == 5)

    def test_valid2(self):
        assert(obslib.coerce_value(5, int) == 5)

    def test_valid3(self):
        assert(obslib.coerce_value("-1", int) == -1)

    def test_valid4(self):
        assert(obslib.coerce_value("-1", int) == -1)

    def test_invalid1(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value("x", int)

    def test_invalid2(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value("A", int)


class TestObsCoerceBool:
    def test_true1(self):
        assert(obslib.coerce_value("true", bool) == True)

    def test_true2(self):
        assert(obslib.coerce_value("True", bool) == True)

    def test_true3(self):
        assert(obslib.coerce_value("1", bool) == True)

    def test_true4(self):
        assert(obslib.coerce_value(1, bool) == True)

    def test_false1(self):
        assert(obslib.coerce_value("false", bool) == False)

    def test_false2(self):
        assert(obslib.coerce_value("False", bool) == False)

    def test_false3(self):
        assert(obslib.coerce_value("0", bool) == False)

    def test_false3(self):
        assert(obslib.coerce_value(0, bool) == False)

    def test_invalid1(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(2, bool)

    def test_invalid2(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(-1, bool)

    def test_invalid3(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value("2", bool)

    def test_invalid4(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value("-1", bool)

class LoaderTest:
    def __init__(self, val):
        self.val = val

class TestObsCoerceLoader:
    def test_invalid_loader(self):
        with pytest.raises(obslib.OBSValidationException):
            obslib.coerce_value(5, int, loader="test")

    def test_custom_failed(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value("test", LoaderTest)

    def test_custom_loader(self):
        text = "test123"
        res = obslib.coerce_value(text, LoaderTest, loader=lambda x: (True, LoaderTest(x)))
        assert(res.val == text)

class TestObsCoerceYaml:
    def test_yaml_dict(self):
        result = obslib.coerce_value("{ 'a': 1, 'b': 2 }", dict)
        assert(isinstance(result, dict))
        assert(result["a"] == 1 and result["b"] == 2)
        assert(len(result.keys()) == 2)

    def test_yaml_list(self):
        result = obslib.coerce_value("[1, 2, 3]", list)
        assert(isinstance(result, list))
        assert(result[0] == 1 and result[1] == 2 and result[2] == 3)
        assert(len(result) == 3)

    def test_yaml_dict_invalid(self):
        with pytest.raises(obslib.OBSConversionException):
            result = obslib.coerce_value("{ 'a': 1, 'b': 2", dict)

    def test_yaml_list_invalid(self):
        with pytest.raises(obslib.OBSConversionException):
            result = obslib.coerce_value("[1, 2, 3", list)

    def test_yaml_multiple_types1(self):
        result = obslib.coerce_value("[1, 2, 3]", (dict, list))
        assert(isinstance(result, list))
        assert(result[0] == 1 and result[1] == 2 and result[2] == 3)
        assert(len(result) == 3)

    def test_yaml_multiple_types2(self):
        result = obslib.coerce_value("{ 'a': 1, 'b': 2 }", (list, dict))
        assert(isinstance(result, dict))
        assert(result["a"] == 1 and result["b"] == 2)
        assert(len(result.keys()) == 2)

    def test_yaml_complex_type(self):
        result = obslib.coerce_value("{ 'a': 1, 'b': [1, 2, 3], 'c': { 'a': 1, 'b': 'test' } }", dict)
        assert(isinstance(result, dict))
        assert(len(result.keys()) == 3)

        # Check 'a'
        assert(result["a"] == 1)

        # Check 'b'
        assert(isinstance(result["b"], list))
        assert(result["b"][0] == 1 and result["b"][1] == 2 and result["b"][2] == 3 and len(result["b"]) == 3)

        # Check 'c'
        assert(isinstance(result["c"], dict))
        assert(len(result["c"].keys()) == 2)
        assert(result["c"]["a"] == 1 and result["c"]["b"] == "test")

    def test_yaml_none_type1(self):
        with pytest.raises(obslib.OBSConversionException):
            result = obslib.coerce_value(None, list)

    def test_yaml_none_type2(self):
        with pytest.raises(obslib.OBSConversionException):
            result = obslib.coerce_value(None, dict)

