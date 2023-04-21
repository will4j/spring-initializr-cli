import os

from src.maven import pom_editor
from src.shell import spring_boot
from src.template import yaml_template


def generate(config_file_path, target_dir_path, is_force=False):
    def single_module_project():
        spring_boot.execute_spring_init(rendered_config, target_dir_path, is_force)

    # render template file and get config dict
    rendered_config = yaml_template.render(config_file_path)

    project_generator = MavenProjectGenerator(rendered_config, target_dir_path, is_force)
    project_generator.generate()


class ProjectGenerator:
    def __init__(self, init_param: dict, target_dir_path, is_force=False):
        self.init_param = init_param
        self.target_dir = target_dir_path
        self.is_force = is_force

    def generate(self):
        pass


class MavenProjectGenerator(ProjectGenerator):

    def generate(self):
        project_path = spring_boot.execute_spring_init(self.init_param, self.target_dir, self.is_force)
        self.handle_extra_dependencies(project_path, self.init_param.get("extra_dependencies"))

    @staticmethod
    def handle_extra_dependencies(project_path, extra_dependencies):
        if not extra_dependencies:
            return
        pom_file_path = os.path.join(project_path, "pom.xml")
        pom_editor.add_dependencies(pom_file_path, extra_dependencies)
