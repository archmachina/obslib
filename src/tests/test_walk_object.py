
import obslib
import pytest

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

