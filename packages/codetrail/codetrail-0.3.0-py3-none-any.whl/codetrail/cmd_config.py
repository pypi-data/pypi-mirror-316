"""This module holds the logic to manage repository configuration.

Usage:
    codetrail config <command>
"""

import configparser

from codetrail import commands
from codetrail import exceptions
from codetrail import models
from codetrail import utils
from codetrail.conf import CONFIG_SECTIONS
from codetrail.conf import CONFIG_USER_OPTIONS
from codetrail.conf import LOGGER


def set_config(command: commands.SetConfig) -> None:
    """Set a configuration value.

    Args:
        command: The command responsible for setting a config value.

    Raises:
        UnsupportedConfigError: In case of an unsupported configuration.
    """
    repo_path = utils.find_repository_path(command.default_path) or command.default_path
    repository = models.CodetrailRepository(repo_path)

    if command.section not in CONFIG_SECTIONS:
        msg = f"Invalid section '{command.section}'!, choose from '{CONFIG_SECTIONS}'"
        raise exceptions.UnsupportedConfigError(msg)

    if command.section in CONFIG_SECTIONS and command.option not in CONFIG_USER_OPTIONS:
        msg = f"Invalid option '{command.option}'!, choose from '{CONFIG_USER_OPTIONS}'"
        raise exceptions.UnsupportedConfigError(msg)

    repository.config.set(command.section, command.option, command.value)
    utils.write_to_config_file(repository.config_path, repository.config)
    LOGGER.info(f"Set value '{command.value}' on key '{command.key}'.")


def get_config(command: commands.GetConfig) -> None:
    """Get a configuration value.

    Args:
        command: The command responsible for getting a config value.

    Raises:
        UnsupportedConfigError: In case of an unsupported configuration.
    """
    repo_path = utils.find_repository_path(command.default_path) or command.default_path
    repository = models.CodetrailRepository(repo_path)

    try:
        value = repository.config.get(command.section, command.option)
    except configparser.NoSectionError as e:
        msg = f"Invalid section '{command.section}'!, choose from '{CONFIG_SECTIONS}'"
        raise exceptions.UnsupportedConfigError(msg) from e
    except configparser.NoOptionError as e:
        msg = f"Option '{command.option}' not found in section '{command.section}'"
        raise exceptions.UnsupportedConfigError(msg) from e
    else:
        LOGGER.info(f"{value}")
