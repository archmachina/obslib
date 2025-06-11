
import obslib
import pytest

class TestParseBool:
    def test_parse_valid1(self):
        assert(obslib.parse_bool("True") == True)

    def test_parse_valid2(self):
        assert(obslib.parse_bool("true") == True)

    def test_parse_valid3(self):
        assert(obslib.parse_bool("1") == True)

    def test_parse_valid4(self):
        assert(obslib.parse_bool(1) == True)

    def test_parse_valid5(self):
        assert(obslib.parse_bool(True) == True)

    def test_parse_valid6(self):
        assert(obslib.parse_bool("False") == False)

    def test_parse_valid7(self):
        assert(obslib.parse_bool("false") == False)

    def test_parse_valid8(self):
        assert(obslib.parse_bool("0") == False)

    def test_parse_valid9(self):
        assert(obslib.parse_bool(0) == False)

    def test_parse_valid10(self):
        assert(obslib.parse_bool(False) == False)

    def test_parse_invalid1(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.parse_bool(2)

    def test_parse_invalid2(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.parse_bool(-1)

    def test_parse_invalid3(self):
        with pytest.raises(obslib.OBSConversionException):
            obslib.parse_bool("truex")


