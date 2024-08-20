
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
        with pytest.raises(jinja2.exceptions.UndefinedError):
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

