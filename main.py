import argparse
import os.path
import subprocess

import yaml
from jinja2 import Environment, FileSystemLoader


def load_template(template_path):
    """load yaml config file to dict

    :param template_path:
    :return:
    """
    with open(template_path, 'r') as f:
        # 加载YAML格式的配置文件
        config = yaml.safe_load(f)

        # 创建Jinja2环境
        env = Environment(loader=FileSystemLoader('.'))

        # 渲染模板
        template = env.from_string(yaml.dump(config))
        return yaml.safe_load(template.render())


def execute_spring_init(init_param: dict, target_dir, force=False):
    shell_cmd = ["spring", "init"]
    options = ["type", "language", "boot-version", "group-id", "artifact-id", "name", "description", "package-name",
               "packaging", "java-version", "version"]
    dependencies = init_param.get("dependencies", [])
    for option in options:
        if option in init_param:
            shell_cmd += [f"--{option}", init_param[option]]
    if dependencies:
        shell_cmd += ["--dependencies", ",".join(dependencies)]
    if force:
        shell_cmd.append("--force")
    shell_cmd.append(os.path.join(target_dir, init_param["name"]))

    # 执行Spring初始化命令
    print(f'run command: {shell_cmd}')
    process = subprocess.Popen(shell_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f'Spring initialization failed with error: {stderr.decode("utf-8")}')
        exit(process.returncode)


if __name__ == '__main__':
    # 定义输入参数
    parser = argparse.ArgumentParser(description='Generate Spring project skeleton with cli.')
    parser.add_argument('target_dir', type=str, help='the path of project directory')
    parser.add_argument('--config-file', type=str, required=True, help='the path of config file')
    parser.add_argument('--force', '-f', action='store_true', help='force replace target directory if exists')
    args = parser.parse_args()

    # 处理输入参数
    config_file_path = args.config_file
    target_dir_path = args.target_dir
    is_force = args.force

    # 解析配置文件并渲染Jinja2模板
    rendered_config = load_template(config_file_path)

    # 进行相应的处理
    execute_spring_init(rendered_config, target_dir_path, is_force)
