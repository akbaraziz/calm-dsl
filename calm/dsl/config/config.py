import os
import errno
import configparser

from jinja2 import Environment, PackageLoader

from .config_schema import validate_config


_CONFIG = None


def get_default_user_config_file():

    user_config_file = os.path.join(os.path.expanduser("~/.calm"), "config.ini")

    # Create parent directory if not present
    if not os.path.exists(os.path.dirname(user_config_file)):
        try:
            os.makedirs(os.path.dirname(user_config_file))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    return user_config_file


def _render_config_template(
    ip,
    port,
    username,
    password,
    project_name,
    db_location,
    schema_file="config.ini.jinja2",
):

    loader = PackageLoader(__name__, "")
    env = Environment(loader=loader)
    template = env.get_template(schema_file)
    text = template.render(
        ip=ip,
        port=port,
        username=username,
        password=password,
        project_name=project_name,
        db_location=db_location,
    )
    return text.strip() + "\n"


def _get_config_file():

    cwd = os.getcwd()
    if "config.ini" in os.listdir(cwd):
        user_config_file = os.path.join(cwd, "config.ini")

    else:
        user_config_file = get_default_user_config_file()
        if not os.path.exists(user_config_file):
            raise Exception(
                "Config file {} not found. Please run: calm init dsl".format(
                    user_config_file
                )
            )

    return user_config_file


def init_config(ip, port, username, password, project_name, db_location):

    # Default user config file
    user_config_file = get_default_user_config_file()

    # Render config template
    text = _render_config_template(
        ip, port, username, password, project_name, db_location
    )

    # Write config
    with open(user_config_file, "w") as fd:
        fd.write(text)


def get_config():

    global _CONFIG

    if not _CONFIG:
        # Create config object
        user_config_file = _get_config_file()
        config = configparser.ConfigParser()
        config.optionxform = str  # Maintaining case sensitivity for field names
        config.read(user_config_file)

        # Validate config
        if not validate_config(config):
            raise Exception("Invalid config file: {}".format(user_config_file))

        _CONFIG = config

    return _CONFIG


def print_config():

    config_file = _get_config_file()
    print(config_file)
    with open(config_file) as fd:
        print(fd.read())
