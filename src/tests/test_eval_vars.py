
import obslib
import pytest
import jinja2

class TestEvalVars:
    def test_indirection1(self):
        var_list = {
            "a": "1",
            "b": "{{ a }}",
            "c": "{{ b }}{{ d }}",
            "d": 6
        }

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)

        result = obslib.eval_vars(var_list, environ)

        assert(result["a"] == "1")
        assert(result["b"] == "1")
        assert(result["c"] == "16")
        assert(result["d"] == 6)

    def test_indirection2(self):
        var_list = {
            "a": {
                "sub": "{{ b.sub }}"
            },
            "b": {
                "sub": "9"
            },
            "z": "{{ a.sub }}"
        }

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)

        result = obslib.eval_vars(var_list, environ)

        assert(result["z"] == "9")
        assert(result["b"]["sub"] == "9")
        assert(result["a"]["sub"] == "9")

    def test_unresolvable1(self):
        var_list = {
            "a": "{{ b }}",
            "b": "{{ a }}"
        }

        with pytest.raises(obslib.OBSResolveException):
            environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)

            result = obslib.eval_vars(var_list, environ)

    def test_unresolvable2(self):
        var_list = {
            "z": "z",
            "a": "{{ z }}{{ b }}",
            "b": "{{ z }}{{ a }}"
        }

        with pytest.raises(obslib.OBSResolveException):
            environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)

            result = obslib.eval_vars(var_list, environ)

    def test_unresolvable3(self):
        var_list = {
            "a": {
                "sub": "{{ b.sub }}"
            },
            "b": {
                "sub": "{{ a.sub }}"
            }
        }

        with pytest.raises(obslib.OBSResolveException):
            environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)

            result = obslib.eval_vars(var_list, environ)

