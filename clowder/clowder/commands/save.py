# -*- coding: utf-8 -*-
"""Clowder command controller class

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os
import sys

import clowder.util.formatting as fmt
from clowder.commands.util import (
    validate_groups,
    validate_projects_exist
)
from clowder.yaml.saving import save_yaml


def save(clowder, version):
    """Save current commits to a clowder.yaml in the versions directory

    :param ClowderController clowder: ClowderController instance
    :param str version: Name of saved version
    """

    validate_projects_exist(clowder)
    validate_groups(clowder.groups)
    versions_dir = os.path.join(clowder.root_directory, '.clowder', 'versions')
    version_name = version.replace('/', '-')  # Replace path separators with dashes
    version_dir = os.path.join(versions_dir, version_name)
    if not os.path.exists(version_dir):
        try:
            os.makedirs(version_dir)
        except OSError as err:
            if err.errno != os.errno.EEXIST:
                raise

    yaml_file = os.path.join(version_dir, 'clowder.yaml')
    if os.path.exists(yaml_file):
        print(fmt.save_version_exists_error(version_name, yaml_file) + '\n')
        sys.exit(1)

    print(fmt.save_version(version_name, yaml_file))
    save_yaml(clowder.get_yaml(), yaml_file)
