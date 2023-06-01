import xml.etree.ElementTree as ET

namespace = "http://maven.apache.org/POM/4.0.0"
ns = "{" + namespace + "}"


def add_dependencies_to_tree(tree: ET, extra_dependencies):
    """ append extra dependencies to ElementTree

    :param tree: ElementTree object
    :param extra_dependencies:
    :return:
    """

    class DependencyConfigHandler:
        def __init__(self, dependency_element, dependency_config):
            self.dependency_element = dependency_element
            self.dependency_config = dependency_config

        def config(self, element_name: str, config_name: str):
            config_value = self.dependency_config.get(config_name)
            if not config_value:
                return
            sub_element = ET.SubElement(self.dependency_element, f"{ns}{element_name}")
            sub_element.text = str(config_value)

    root = tree.getroot()

    dependencies = root.find(f"{ns}dependencies")
    if dependencies is None:
        dependencies = ET.SubElement(root, f"{ns}dependencies")

    for extra_dependency in extra_dependencies:
        dependency = ET.SubElement(dependencies, f"{ns}dependency")

        config_handler = DependencyConfigHandler(dependency, extra_dependency)
        # pom spec: https://maven.apache.org/ref/3.9.2/maven-model/maven.html#class_dependency
        config_handler.config("groupId", "group_id")
        config_handler.config("artifactId", "artifact_id")
        config_handler.config("version", "version")
        config_handler.config("type", "type")
        config_handler.config("scope", "scope")
        config_handler.config("optional", "optional")

    # https://maven.apache.org/guides/development/guide-documentation-style.html
    ET.indent(tree, space="  ", level=0)


def add_dependencies(pom_file_path, extra_dependencies):
    """ append extra dependencies into pom
    pom spec: https://maven.apache.org/ref/3.9.2/maven-model/maven.html#class_dependency

    :param pom_file_path:
    :param extra_dependencies:
    :return:
    """
    if not extra_dependencies:
        return

    tree = ET.parse(pom_file_path)

    add_dependencies_to_tree(tree, extra_dependencies)

    ET.register_namespace("", namespace)
    tree.write(pom_file_path)
