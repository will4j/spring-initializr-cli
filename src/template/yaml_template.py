from jinja2 import Environment, FileSystemLoader

import yaml


def render(template_path):
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
        return yaml.safe_load(template.render(config))
