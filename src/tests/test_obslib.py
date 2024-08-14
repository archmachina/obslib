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
        text = "test123"
        res = obslib.coerce_value(LoaderTest, text, loader=lambda x: (True, LoaderTest(x)))
        assert(res.val == text)

class TestObsCoerceYaml:
    def test_yaml_dict(self):
        result = obslib.coerce_value(dict, "{ 'a': 1, 'b': 2 }")
        assert(isinstance(result, dict))
        assert(result["a"] == 1 and result["b"] == 2)
        assert(len(result.keys()) == 2)

    def test_yaml_list(self):
        result = obslib.coerce_value(list, "[1, 2, 3]")
        assert(isinstance(result, list))
        assert(result[0] == 1 and result[1] == 2 and result[2] == 3)
        assert(len(result) == 3)

    def test_yaml_dict_invalid(self):
        with pytest.raises(obslib.OBSConversionException):
            result = obslib.coerce_value(dict, "{ 'a': 1, 'b': 2")

    def test_yaml_list_invalid(self):
        with pytest.raises(obslib.OBSConversionException):
            result = obslib.coerce_value(list, "[1, 2, 3")

    def test_yaml_multiple_types1(self):
        result = obslib.coerce_value((dict, list), "[1, 2, 3]")
        assert(isinstance(result, list))
        assert(result[0] == 1 and result[1] == 2 and result[2] == 3)
        assert(len(result) == 3)

    def test_yaml_multiple_types2(self):
        result = obslib.coerce_value((list, dict), "{ 'a': 1, 'b': 2 }")
        assert(isinstance(result, dict))
        assert(result["a"] == 1 and result["b"] == 2)
        assert(len(result.keys()) == 2)

    def test_yaml_complex_type(self):
        result = obslib.coerce_value(dict, "{ 'a': 1, 'b': [1, 2, 3], 'c': { 'a': 1, 'b': 'test' } }")
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

class TestWalkObject:
    def test_primitive(self):
        assert(obslib.walk_object("test", callback=lambda x: x) == "test")

    def test_primitive_update(self):
        assert(obslib.walk_object("test", callback=lambda x: x + "other", update=True) == "testother")

    def test_primitive_noupdate(self):
        assert(obslib.walk_object("test", callback=lambda x: x + "other", update=False) == "test")

    def test_primitive_callback(self):
        ret = { "item": "" }

        def save_obj(x, ret=ret):
            ret["item"] = x

        obslib.walk_object("test", callback=save_obj)
        assert(ret["item"] == "test")

    def test_complex_count_int(self):
        item = {
            "a": 1,
            "b": [ 5, 6, 7 ],
            "c": {
                "d": 4,
                "e": [ 1, 2 ]
            }
        }

        state = {
            "sum": 0,
            "count": 0
        }

        def sum_add(x, state=state):
            if (isinstance(x, int)):
                state["sum"] = state["sum"] + x
                state["count"] = state["count"] + 1

        obslib.walk_object(item, callback=sum_add)

        assert(state["sum"] == 26)
        assert(state["count"] == 7)

    def test_complex_update(self):
        item = {
            "a": 1,
            "b": 2,
            "c": "test",
            "d": [ 4, 5, "other" ]
        }

        def update(x):
            if isinstance(x, str):
                return x + x

            if isinstance(x, int):
                return x * x

            return x

        item = obslib.walk_object(item, callback=update, update=True)

        assert(item["a"] == 1 and item["b"] == 4 and item["c"] == "testtest")
        assert(item["d"][0] == 16 and item["d"][1] == 25 and item["d"][2] == "otherother")

    def test_complex_update_depth1(self):
        item = {
            "a": 1,
            "b": 2,
            "c": "test",
            "d": [ 4, 5, "other" ]
        }

        def update(x):
            if isinstance(x, str):
                return x + x

            if isinstance(x, int):
                return x * x

            return x

        newitem = obslib.walk_object(item, callback=update, update=True, depth=0)

        assert(id(item) == id(newitem))

        assert(item["a"] == 1 and item["b"] == 4 and item["c"] == "testtest")
        assert(item["d"][0] == 4 and item["d"][1] == 5 and item["d"][2] == "other")

    def test_complex_update_depth2(self):
        item = {
            "a": 2,
            "b": {
                "c": 3,
                "d": {
                    "e": 4
                }
            }
        }

        def update(x):
            if isinstance(x, int):
                return x * x

            return x

        newitem = obslib.walk_object(item, callback=update, update=True, depth=1)

        assert(id(item) == id(newitem))

        assert(item["a"] == 4)
        assert(item["b"]["c"] == 9)
        assert(item["b"]["d"]["e"] == 4)

    def test_complex_noupdate_depth1(self):
        item = {
            "a": 2,
            "b": {
                "c": 3,
                "d": {
                    "e": 4
                }
            }
        }

        def update(x):
            if isinstance(x, int):
                return x * x

            return x

        newitem = obslib.walk_object(item, callback=update, update=False, depth=1)

        assert(id(item) == id(newitem))

        assert(item["a"] == 2)
        assert(item["b"]["c"] == 3)
        assert(item["b"]["d"]["e"] == 4)

