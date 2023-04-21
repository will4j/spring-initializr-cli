import os

from src.template import yaml_template

pwd = os.path.dirname(__file__)

def test_render():
    rendered = yaml_template.render(os.path.join(pwd, "test_render.yaml"))
    assert rendered is not None
    assert rendered["version"] == "1.0"
    assert rendered["test_value"] == "test value"
    assert rendered["render_value"] == "test value"
