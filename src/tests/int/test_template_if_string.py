
import obslib
import pytest
import jinja2

class TestTemplateIfString:
    def test_template_type1(self):
        source = 7

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        result = obslib.template_if_string(source, environ, {})

        assert isinstance(result, int)
        assert result == 7

    def test_template_type2(self):
        source = True

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        result = obslib.template_if_string(source, environ, {})

        assert isinstance(result, bool)
        assert result == True

    def test_template_type3(self):
        source = "{{ a }}"
        source_vars = {
            "a": 7
        }

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        result = obslib.template_if_string(source, environ, source_vars)

        assert isinstance(result, int)
        assert result == 7

    def test_template_type3(self):
        source = None

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        result = obslib.template_if_string(source, environ, {})

        assert result is None

    def test_template_type3(self):
        # template_if_string should only template an object if it is a string,
        # ignoring complex objects

        source = {
            "a": "{{ b }}"
        }
        source_vars = {
            "b": "6"
        }

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        result = obslib.template_if_string(source, environ, source_vars)

        assert isinstance(result, dict)
        assert "a" in result
        assert result["a"] == "{{ b }}"

