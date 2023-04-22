import os

from src.maven import pom_editor
from src.shell import spring_boot
from src.template import yaml_template


def generate(config_file_path, target_dir_path, is_force=False):
    # render template file and get config dict
    rendered_config = yaml_template.render(config_file_path)

    project_generator = ProjectGenerator.factory(rendered_config, target_dir_path, is_force)
    project_generator.generate()


class ProjectGenerator:

    @staticmethod
    def factory(init_param: dict, target_dir_path, is_force=False):
        project_type = init_param.get("type")
        if project_type in {"maven-project"}:
            return MavenProjectGenerator(init_param, target_dir_path, is_force)
        elif project_type in {"gradle-project"}:
            return GradleProjectGenerator(init_param, target_dir_path, is_force)
        raise ValueError("Invalid project type")

    def __init__(self, init_param: dict, target_dir_path, is_force=False):
        self.init_param = init_param
        self.target_dir = target_dir_path
        self.is_force = is_force

    def handle_extra_dependencies(self, project_path, extra_dependencies):
        raise NotImplementedError("Please implement dependency append logic.")

    def generate(self):
        project_path = spring_boot.execute_spring_init(self.init_param, self.target_dir, self.is_force)
        self.handle_extra_dependencies(project_path, self.init_param.get("extra_dependencies"))


class MavenProjectGenerator(ProjectGenerator):

    def handle_extra_dependencies(self, project_path, extra_dependencies):
        if not extra_dependencies:
            return
        pom_file_path = os.path.join(project_path, "pom.xml")
        pom_editor.add_dependencies(pom_file_path, extra_dependencies)


class GradleProjectGenerator(ProjectGenerator):
    def handle_extra_dependencies(self, project_path, extra_dependencies):
        pass
