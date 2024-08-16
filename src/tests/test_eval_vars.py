
import obslib
import pytest
import jinja2

class TestEvalVars:
    def test_eval_vars(self):
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

