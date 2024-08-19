
import obslib
import pytest
import jinja2

class TestSession:
    def test_first(self):
        source_vars = {
            "a": 1,
            "b": "{{ a }}2",
            "c": "{{ b }}3"
        }


        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        source_vars = obslib.eval_vars(source_vars, environ)
        session = obslib.Session(environ, source_vars)

        value = "{{ c }}"

        assert(session.resolve(value, int) == 123)

