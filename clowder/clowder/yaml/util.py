# -*- coding: utf-8 -*-
"""clowder.yaml utilities

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError


def clowder_yaml_contains_value(parsed_yaml, value, yaml_file):
    """Check whether yaml file contains value

    :param dict parsed_yaml: Parsed YAML python object
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if value not in parsed_yaml:
        error = fmt.missing_entry_error(value, fmt.yaml_file('clowder.yaml'), yaml_file)
        raise ClowderError(error)


def dict_contains_value(dictionary, dict_name, value, yaml_file):
    """Check whether yaml file contains value

    :param dict dictionary: Parsed YAML python object
    :param str dict_name: Name of dict to print if missing
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if value not in dictionary:
        error = fmt.missing_entry_error(value, dict_name, yaml_file)
        raise ClowderError(error)


def override_import_value(dictionary, imported_dictionary, value):
    """Check whether yaml file contains required value

    :param dict dictionary: Parsed YAML python object
    :param dict imported_dictionary: Imported parsed YAML python object
    :param str value: Name of entry to check
    :return:
    """

    if value in imported_dictionary:
        dictionary[value] = imported_dictionary[value]


def validate_empty(collection, name, yaml_file):
    """Check whether collection is not empty

    :param collection: Parsed YAML python object
    :param str name: Name of collection to print if empty
    :param str yaml_file: Path to yaml file
    :return:
    """

    if collection:
        error = fmt.unknown_entry_error(name, collection, yaml_file)
        raise ClowderError(error)


def validate_not_empty(collection, name, yaml_file):
    """Check whether collection is empty

    :param collection: Parsed YAML python object
    :param str name: Name of collection to print if empty
    :param str yaml_file: Path to yaml file
    :return:
    """

    if not collection:
        error = fmt.missing_entries_error(name, yaml_file)
        raise ClowderError(error)


def validate_optional_dict(dictionary, value, func, yaml_file):
    """Check whether yaml file contains optional value

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param callabel func: Function to call to validate dictionary
    :param str yaml_file: Path to yaml file
    :return:
    """

    if value in dictionary:
        func(dictionary[value], yaml_file)
        del dictionary[value]


def validate_optional_ref(dictionary, yaml_file):
    """Check whether ref type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :return:
    """

    if 'ref' in dictionary:
        validate_type(dictionary['ref'], 'ref', str, 'str', yaml_file)
        validate_ref_type(dictionary, yaml_file)
        del dictionary['ref']


def validate_optional_bool(dictionary, value, yaml_file):
    """Check whether yaml file contains optional boolean

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    """

    _validate_optional_value(dictionary, value, bool, 'bool', yaml_file)


def validate_optional_string(dictionary, value, yaml_file):
    """Check whether yaml file contains optional string

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    """

    _validate_optional_value(dictionary, value, str, 'str', yaml_file)


def validate_required_dict(dictionary, value, func, yaml_file):
    """Check whether yaml file contains required value

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param callable func: Function to call to validate dict entries
    :param str yaml_file: Path to yaml file
    :return:

    """

    clowder_yaml_contains_value(dictionary, value, yaml_file)
    func(dictionary[value], yaml_file)
    del dictionary[value]


def validate_required_ref(dictionary, yaml_file):
    """Check for required ref value

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :return:
    """

    dict_contains_value(dictionary, 'defaults', 'ref', yaml_file)
    validate_type(dictionary['ref'], 'ref', str, 'str', yaml_file)
    validate_ref_type(dictionary, yaml_file)
    del dictionary['ref']


def validate_required_string(dictionary, dict_name, value, yaml_file):
    """Check whether yaml file contains required value

    :param dict dictionary: Parsed YAML python object
    :param str dict_name: Name of dict to print if missing
    :param str value: Name of entry to check
    :param str yaml_file: Path to yaml file
    :return:
    """

    dict_contains_value(dictionary, dict_name, value, yaml_file)
    validate_type(dictionary[value], value, str, 'str', yaml_file)
    del dictionary[value]


def validate_ref_type(dictionary, yaml_file):
    """Check whether ref type is valid

    :param dict dictionary: Parsed YAML python object
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if not _valid_ref_type(dictionary['ref']):
        error = fmt.invalid_ref_error(dictionary['ref'], yaml_file)
        raise ClowderError(error)


def validate_type_depth(value, yaml_file):
    """Validate depth value

    :param int value: Integer depth value
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    error = fmt.depth_error(value, yaml_file)
    if not isinstance(value, int):
        raise ClowderError(error)
    if int(value) < 0:
        raise ClowderError(error)


def validate_type(value, name, classinfo, type_name, yaml_file):
    """Validate value type

    :param value: Value to check
    :param str name: Name of value to print if invalid
    :param type classinfo: Type to check
    :param str type_name: Name of type to print if invalid
    :param str yaml_file: Path to yaml file
    :return:
    :raise ClowderError:
    """

    if not isinstance(value, classinfo):
        error = fmt.type_error(name, yaml_file, type_name)
        raise ClowderError(error)


def _validate_optional_value(dictionary, value, classinstance, type_name, yaml_file):
    """Check whether yaml file contains optional value

    :param dict dictionary: Parsed YAML python object
    :param str value: Name of entry to check
    :param type classinstance: Type to check
    :param str type_name: Name of type to print if invalid
    :param str yaml_file: Path to yaml file
    :return:
    """

    if value in dictionary:
        validate_type(dictionary[value], value, classinstance, type_name, yaml_file)
        del dictionary[value]


def _valid_ref_type(ref):
    """Validate that ref is formatted correctly

    :param str ref: Ref string requiring format 'refs/heads/<branch>', 'refs/tags/<tag>', or 40 character commit sha
    :return: True, if ref is properly formatted
    :rtype: bool
    """

    git_branch = "refs/heads/"
    git_tag = "refs/tags/"
    if ref.startswith(git_branch):
        return True
    elif ref.startswith(git_tag):
        return True
    elif len(ref) == 40:
        return True
    return False
