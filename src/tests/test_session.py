
import obslib
import pytest
import jinja2

class TestSession:
    def test_resolve1(self):
        source_vars = {
            "a": 1,
            "b": "{{ a }}2",
            "c": "{{ b }}3"
        }

        session = obslib.Session(obslib.eval_vars(source_vars))

        value = "{{ c }}"

        assert(session.resolve(value, int) == 123)

    def test_resolve2(self):
        source_vars = {
            "a": {
                "sub": 7
            },
            "b": 2
        }

        session = obslib.Session(obslib.eval_vars(source_vars))

        value = "{{ a.sub / b }}"

        assert(session.resolve(value, float) == 3.5)

    def test_resolve3(self):
        with pytest.raises(obslib.OBSResolveException):
            source_vars = {
                "a": {
                    "sub": 7
                },
                "b": 2
            }

            session = obslib.Session(obslib.eval_vars(source_vars))
            value = session.resolve("{{ a.sub / c }}")

    def test_resolve4(self):
        source_vars = {
            "a": 1,
            "b": 2,
            "c": 5
        }

        session = obslib.Session(obslib.eval_vars(source_vars))

        value = "[ {{ a }}, {{ b }}, {{ c }} ]"

        result = session.resolve(value, list)
        assert(len(result) == 3 and isinstance(result, list))
        assert(result[0] == 1 and result[1] == 2 and result[2] == 5)

    def test_resolve5(self):
        source_vars = {
            "source": {
                "a": 1,
                "b": 2,
                "c": 5
            }
        }

        session = obslib.Session(obslib.eval_vars(source_vars))

        value = "{{ source }}"

        result = session.resolve(value, dict)
        assert(result["a"] == 1 and result["b"] == 2 and result["c"] == 5)

    def test_resolve6(self):
        source_val = None

        session = obslib.Session({})

        result = session.resolve(source_val, types=(list, type(None)))

        assert result is None

    def test_resolve7(self):
        source_val = None

        session = obslib.Session({})

        result = session.resolve(source_val, types=(list, type(None)), on_none=5)

        assert result == 5

    def test_ignore_list1(self):

        source = {
            "a": "{{ b }}",
            "b": "{{ c }}",
            "c": "{{ d }}"
        }

        session = obslib.Session(source)

        with pytest.raises(obslib.OBSResolveException):
            result = session.resolve("{{ a }}")

    def test_ignore_list2(self):

        source = {
            "a": "{{ b }}",
            "b": "{{ c }}",
            "c": "{{ d }}"
        }

        session = obslib.Session(source, ignore_list=["c"])

        result = session.resolve("{{ a }}")

        assert result == "{{ d }}"

# TODO
# Remove eval_vars from tests and rely 'resolve' to call
#   eval_vars via template_if_string

