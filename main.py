import argparse
import os.path
import subprocess

import yaml
from jinja2 import Environment, FileSystemLoader
from maven import pom_editor


def render_template(template_path):
    """render yaml config template to dict

    :param template_path:
    :return:
    """
    with open(template_path, 'r') as f:
        # load yaml config file
        config = yaml.safe_load(f)

        # create jinja2 environment
        env = Environment(loader=FileSystemLoader('.'))

        # render jinja2 template
        template = env.from_string(yaml.dump(config))
        return yaml.safe_load(template.render())


def execute_spring_init(init_param: dict, target_dir, force=False):
    def option_cmd(option_name: str):
        option_key = option_name.replace('-', '_')
        if option_key in option_name:
            return [f"--{option_name}", init_param[option_key]]
        return []

    shell_cmd = ["spring", "init"]
    options = ["type", "language", "boot-version", "group-id", "artifact-id", "name", "description", "package-name",
               "packaging", "java-version", "version"]
    dependencies = init_param.get("dependencies", [])
    for option in options:
        shell_cmd += option_cmd(option)
    if dependencies:
        shell_cmd += ["--dependencies", ",".join(dependencies)]
    if force:
        shell_cmd.append("--force")

    project_dir = os.path.join(target_dir, init_param["name"])
    shell_cmd.append(project_dir)

    # execute spring init command in subprocess
    print(f'run command: {shell_cmd}')
    process = subprocess.Popen(shell_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f'Spring initialization failed with error: {stderr.decode("utf-8")}')
        exit(process.returncode)

    handle_extra_dependencies(project_dir, init_param.get("extra_dependencies"))


def handle_extra_dependencies(project_path, extra_dependencies):
    pom_file_path = os.path.join(project_path, "pom.xml")
    pom_editor.add_dependencies(pom_file_path, extra_dependencies)


if __name__ == '__main__':
    # define command line arguments
    parser = argparse.ArgumentParser(description='Generate Spring project skeleton with cli.')
    parser.add_argument('target_dir', type=str, help='the path of project directory')
    parser.add_argument('--config-file', type=str, required=True, help='the path of config file')
    parser.add_argument('--force', '-f', action='store_true', help='force replace target directory if exists')
    args = parser.parse_args()

    # get arguments
    config_file_path = args.config_file
    target_dir_path = args.target_dir
    is_force = args.force

    # render template file and get config dict
    rendered_config = render_template(config_file_path)
    print(rendered_config)

    # do spring init
    execute_spring_init(rendered_config, target_dir_path, is_force)
