import xml.etree.ElementTree as ET
from xml.dom import minidom


def add_dependencies(pom_file_path, extra_dependencies):
    """ append extra dependencies into pom

    :param pom_file_path:
    :param extra_dependencies:
    :return:
    """
    if not extra_dependencies:
        return

    ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
    tree = ET.parse(pom_file_path)
    root = tree.getroot()

    dependencies = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")
    if dependencies is None:
        dependencies = ET.SubElement(root, "dependencies")

    for extra_dependency in extra_dependencies:
        dependency = ET.SubElement(dependencies, "dependency")

        group_id_node = ET.SubElement(dependency, "groupId")
        group_id_node.text = extra_dependency["group_id"]

        artifact_id_node = ET.SubElement(dependency, "artifactId")
        artifact_id_node.text = extra_dependency["artifact_id"]

        version = extra_dependency.get("version")
        if version:
            version_node = ET.SubElement(dependency, "version")
            version_node.text = version

    # https://maven.apache.org/guides/development/guide-documentation-style.html
    ET.indent(tree, space="  ", level=0)
    tree.write(pom_file_path)
