# -*- coding: utf-8 -*-
"""clowder.yaml forks validation

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.yaml.util import (
    validate_required_value,
    validate_type
)


def validate_yaml_fork(fork, yaml_file):
    """Validate fork in clowder loaded from yaml file

    :param dict fork: Parsed YAML python object for fork
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    validate_type(fork, 'fork', dict, 'dict', yaml_file)

    if not fork:
        error = fmt.missing_entries_error('fork', yaml_file)
        raise ClowderError(error)

    validate_required_value(fork, 'fork', 'name', str, 'str', yaml_file)
    validate_required_value(fork, 'fork', 'remote', str, 'str', yaml_file)

    if fork:
        error = fmt.unknown_entry_error('fork', fork, yaml_file)
        raise ClowderError(error)
