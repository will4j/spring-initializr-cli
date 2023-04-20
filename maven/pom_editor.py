import xml.etree.ElementTree as ET


def add_dependencies(pom_file_path, extra_dependencies):
    """ append extra dependencies into pom

    :param pom_file_path:
    :param extra_dependencies:
    :return:
    """
    if not extra_dependencies:
        return

    tree = ET.parse(pom_file_path)
    root = tree.getroot()

    dependencies = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")
    if dependencies is None:
        dependencies = ET.SubElement(root, "dependencies")

    dependency = ET.SubElement(dependencies, "dependency")

    print(extra_dependencies)
    for extra_dependency in extra_dependencies:
        group_id_node = ET.SubElement(dependency, "groupId")
        group_id_node.text = extra_dependency["group_id"]

        artifact_id_node = ET.SubElement(dependency, "artifactId")
        artifact_id_node.text = extra_dependency["artifact_id"]

        version = extra_dependency.get("version")
        if version:
            version_node = ET.SubElement(dependency, "version")
            version_node.text = version

    tree.write(pom_file_path)
