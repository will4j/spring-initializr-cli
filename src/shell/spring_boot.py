import os
import subprocess


def execute_spring_init(init_param: dict, target_dir, force=False):
    def option_cmd(option_name: str):
        option_key = option_name.replace('-', '_')
        if option_key in init_param:
            return [f"--{option_name}", init_param[option_key]]
        return []

    shell_cmd = ["spring", "init"]

    options = ["type", "language", "boot-version", "group-id", "artifact-id", "name", "description", "package-name",
               "packaging", "java-version", "version"]
    for option in options:
        shell_cmd += option_cmd(option)

    dependencies = init_param.get("dependencies", [])
    if dependencies:
        shell_cmd += ["--dependencies", ",".join(dependencies)]

    if force:
        shell_cmd.append("--force")

    project_path = os.path.join(target_dir, init_param["name"])
    shell_cmd.append(project_path)

    # execute spring init command in subprocess
    print(f'run command: {shell_cmd}')
    process = subprocess.Popen(shell_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f'Spring initialization failed with error: {stderr.decode("utf-8")}')
        exit(process.returncode)

    return project_path
