import argparse

from src import project_generator

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

    # generate spring skeleton project
    project_generator.generate(config_file_path, target_dir_path, is_force)
