import json
import os
import re
import subprocess
import sys

from ok import config_logger, Logger
from ok.update.GitUpdater import replace_ok_script_ver
from ok.update.python_env import delete_files, \
    create_venv, find_line_in_requirements

logger = Logger.get_logger(__name__)


def replace_string_in_file(file_path, old_pattern, new_string):
    """
    Replace occurrences of old_pattern with new_string in the specified file using regex.

    :param file_path: Path to the file
    :param old_pattern: Regex pattern to be replaced
    :param new_string: Replacement string
    """

    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the old pattern with the new string using regex
    new_content = re.sub(old_pattern, new_string, content)

    # Write the new content back to the file
    with open(file_path, 'w') as file:
        file.write(new_content)

    logger.info(f"Replaced pattern '{old_pattern}' with '{new_string}' in {file_path}")


def create_app_env(code_dir, build_dir, dependencies):
    full_version = find_line_in_requirements(os.path.join(code_dir, 'requirements.txt'), 'ok-script')
    if not full_version:
        logger.error('Could not find ok-script version in requirements.txt')
        return
    logger.info(f'ok-script full_version: {full_version}')
    env_path = create_venv('app_env', os.path.join(build_dir))
    try:
        env_python_exe = os.path.join(env_path, 'Scripts', 'python.exe')
        for dependency in dependencies:
            dependency = replace_ok_script_ver(dependency, full_version)
            subprocess.run([env_python_exe, "-m", "pip", "install"] + dependency.split())
        delete_files(root_dir=env_path)
        return True
    except Exception as e:
        logger.error("An error occurred while creating the virtual environment.", e)


def create_launcher_env(code_dir='.', build_dir='.'):
    launcher_json_file = os.path.join(code_dir, 'launcher.json')
    with open(launcher_json_file, 'r') as file:
        launcher_json = json.load(file)
    full_version = find_line_in_requirements(os.path.join(code_dir, 'requirements.txt'), 'ok-script')
    if not full_version:
        logger.error('Could not find ok-script version in requirements.txt')
        return
    logger.info(f'ok-script full_version: {full_version}')
    lenv_path = create_venv('launcher_env', os.path.join(build_dir))
    try:
        lenv_python_exe = os.path.join(lenv_path, 'Scripts', 'python.exe')
        params = [lenv_python_exe, "-m", "pip", "install", "PySide6-Fluent-Widgets==1.7.1", '--no-deps',
                  '--no-cache-dir']
        result = subprocess.run(params, check=True, capture_output=True, text=True)
        logger.info("install PySide6-Fluent-Widgets success")
        logger.info(result.stdout)

        params = [lenv_python_exe, "-m", "pip", "install",
                  full_version,
                  '--no-cache-dir']
        result = subprocess.run(params, check=True, capture_output=True, text=True)
        logger.info("install ok-script success")
        logger.info(result.stdout)
        delete_files(root_dir=lenv_path)
        return True
    except Exception as e:
        logger.error("An error occurred while creating the virtual environment.", e)


# python -m ok.gui.launcher.init_lenv
if __name__ == '__main__':
    config_logger(name='launcher')
    full_version = find_line_in_requirements('requirements.txt', 'ok-script')
    if not full_version:
        logger.error('Could not find ok-script version in requirements.txt')
        sys.exit(1)
    lenv_path = create_venv('launcher_env')
    replace_string_in_file('launcher.json', r'ok-script(?:==[\d.]+)?', full_version)
    try:
        lenv_python_exe = os.path.join(lenv_path, 'Scripts', 'python.exe')
        params = [lenv_python_exe, "-m", "pip", "install", "PySide6-Fluent-Widgets>=1.5.5", '--no-deps',
                  '--no-cache-dir']
        result = subprocess.run(params, check=True, capture_output=True, text=True)
        logger.info("install PySide6-Fluent-Widgets success")
        logger.info(result.stdout)

        params = [lenv_python_exe, "-m", "pip", "install",
                  full_version,
                  '--no-cache-dir']
        result = subprocess.run(params, check=True, capture_output=True, text=True)
        logger.info("install ok-script success")
        logger.info(result.stdout)
        delete_files()
    except subprocess.CalledProcessError as e:
        logger.error("An error occurred while creating the virtual environment.")
        logger.error(e.stderr)
