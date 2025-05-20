
import obslib
import pytest
import jinja2

class TestTemplateIfString:
    def test_resolve_refs1(self):
        source = {
            "a": "{{ b }}",
            "b": "{{ c }}",
            "c": "final"
        }

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        result = obslib.template_if_string("{{ a }}", environ, source)

        assert result == "{{ b }}"

    def test_resolve_refs2(self):
        source = {
            "a": "{{ b }}",
            "b": "{{ c }}",
            "c": "final"
        }

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        result = obslib.template_if_string("{{ a }}", environ, source, resolve_refs=True)

        assert result == "final"

    def test_resolve_refs3(self):
        # template_if_string should ignore the 'x' variable as it
        # isn't referenced from the template string (directly or
        # indirectly)
        source = {
            "a": "{{ b }}",
            "b": "{{ c }}",
            "c": "final",
            "x": "{{ not_exist }}"
        }

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        result = obslib.template_if_string("{{ a }}", environ, source, resolve_refs=True)

        assert result == "final"

    def test_resolve_refs4(self):
        # template_if_string should fail as 'not_exist' doesn't
        # exist in the source vars
        source = {
            "a": "{{ b }}",
            "b": "{{ c }}",
            "c": "{{ x }}",
            "x": "{{ not_exist }}"
        }

        environ = jinja2.Environment(undefined=jinja2.StrictUndefined, keep_trailing_newline=True)
        with pytest.raises(obslib.OBSResolveException):
            result = obslib.template_if_string("{{ a }}", environ, source, resolve_refs=True)

