import obslib
import pytest

class TestObsCoerceInt:
    def test_valid1(self):
        assert(obslib.coerce_value(int, "5") == 5)

    def test_valid2(self):
        assert(obslib.coerce_value(int, 5) == 5)

    def test_valid3(self):
        assert(obslib.coerce_value(int, "-1") == -1)

    def test_valid4(self):
        assert(obslib.coerce_value(int, "-1") == -1)

    def test_invalid1(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(int, "x")

    def test_invalid2(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(int, "A")


class TestObsCoerceBool:
    def test_true1(self):
        assert(obslib.coerce_value(bool, "true") == True)

    def test_true2(self):
        assert(obslib.coerce_value(bool, "True") == True)

    def test_true3(self):
        assert(obslib.coerce_value(bool, "1") == True)

    def test_true4(self):
        assert(obslib.coerce_value(bool, 1) == True)

    def test_false1(self):
        assert(obslib.coerce_value(bool, "false") == False)

    def test_false2(self):
        assert(obslib.coerce_value(bool, "False") == False)

    def test_false3(self):
        assert(obslib.coerce_value(bool, "0") == False)

    def test_false3(self):
        assert(obslib.coerce_value(bool, 0) == False)

    def test_invalid1(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(bool, 2)

    def test_invalid2(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(bool, -1)

    def test_invalid3(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(bool, "2")

    def test_invalid4(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(bool, "-1")

class LoaderTest:
    def __init__(self, val):
        self.val = val

class TestObsCoerceLoader:
    def test_invalid_loader(self):
        with pytest.raises(obslib.OBSValidationException):
            obslib.coerce_value(int, 5, loader="test")

    def test_custom_failed(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.coerce_value(LoaderTest, "test")

    def test_custom_loader(self):
        res = obslib.coerce_value(LoaderTest, "test123", loader=lambda x: (True, LoaderTest(x)))
        assert(res.val == "test123")

