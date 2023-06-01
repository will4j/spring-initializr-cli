import os
import xml.etree.ElementTree as ET

from src.maven import pom_editor
from src.maven.pom_editor import ns

pwd = os.path.dirname(__file__)


def test_add_dependencies_to_tree():
    template_pom = os.path.join(pwd, "template-pom.xml")

    tree = ET.parse(template_pom)

    extra_dependencies = [
        {
            "group_id": "net.will4j",
            "artifact_id": "jea01"
        },
        {
            "group_id": "net.will4j",
            "artifact_id": "jea02",
            "version": "0.2"
        },
        {
            "group_id": "net.will4j",
            "artifact_id": "jea03",
            "version": "0.3",
            "type": "jar",
            "scope": "compile",
            "optional": "true"
        }
    ]
    pom_editor.add_dependencies_to_tree(tree, extra_dependencies)

    root = tree.getroot()

    dependencies = root.find(f"{ns}dependencies").findall(f"{ns}dependency")
    assert len(dependencies) == 4

    jea01 = [d for d in dependencies if d.findtext(f"{ns}artifactId") == "jea01"]
    assert jea01[0].findtext(f"{ns}groupId") == "net.will4j"
    assert jea01[0].findtext(f"{ns}version") is None

    jea02 = [d for d in dependencies if d.findtext(f"{ns}artifactId") == "jea02"]
    assert jea02[0].findtext(f"{ns}groupId") == "net.will4j"
    assert jea02[0].findtext(f"{ns}version") == "0.2"
    assert jea02[0].findtext(f"{ns}type") is None

    jea03 = [d for d in dependencies if d.findtext(f"{ns}artifactId") == "jea03"]
    assert jea03[0].findtext(f"{ns}groupId") == "net.will4j"
    assert jea03[0].findtext(f"{ns}version") == "0.3"
    assert jea03[0].findtext(f"{ns}type") == "jar"
    assert jea03[0].findtext(f"{ns}scope") == "compile"
    assert jea03[0].findtext(f"{ns}optional") == "true"
