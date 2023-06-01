import os

from src.template import yaml_template

pwd = os.path.dirname(__file__)

def test_render():
    rendered = yaml_template.render(os.path.join(pwd, "test-render.yaml"))
    assert rendered is not None
    assert rendered["version"] == "1.0"
    assert rendered["test_value"] == "test value"
    assert rendered["render_value"] == "test value"
    assert rendered["group_id"] == "net.will4j"
    assert rendered["artifact_id"] == "jea"
    assert rendered["dependencies"] == ["lombok", "web"]

    extra_dependencies = rendered["extra_dependencies"]
    assert extra_dependencies[0]["group_id"] == "net.will4j"
    assert extra_dependencies[0]["artifact_id"] == "jea-api"
    assert extra_dependencies[1]["artifact_id"] == "jea-biz"
    assert extra_dependencies[1]["version"] == "1.0"
