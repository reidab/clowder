"""Clowder yaml printing"""
import os
import sys
from pygments import highlight
from pygments.lexers.data import YamlLexer
from pygments.formatters import get_formatter_by_name
from clowder.utility.clowder_utilities import parse_yaml
from clowder.utility.print_utilities import print_open_file_error

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702

def print_yaml(root_directory):
    """Print current clowder yaml"""
    yaml_file = os.path.join(root_directory, 'clowder.yaml')
    parsed_yaml = parse_yaml(yaml_file)
    yaml_files = []
    while True:
        yaml_files.append(yaml_file)
        if 'import' not in parsed_yaml:
            break
        imported_yaml = parsed_yaml['import']
        if imported_yaml == 'default':
            yaml_file = os.path.join(root_directory,
                                     '.clowder',
                                     'clowder.yaml')
        else:
            yaml_file = os.path.join(root_directory,
                                     '.clowder',
                                     'versions',
                                     imported_yaml,
                                     'clowder.yaml')
        parsed_yaml = parse_yaml(yaml_file)
    for parsed_yaml in reversed(yaml_files):
        if os.path.isfile(yaml_file):
            try:
                with open(yaml_file) as file:
                    contents = file.read()
                    terminal_formatter = get_formatter_by_name('terminal16m')
                    outfile = os.path.join(root_directory, 'formatted_clowder.yaml')
                    try:
                        with open(outfile, 'w') as out_file:
                            print(" - Save yaml to file")
                            print(highlight(contents, YamlLexer(), terminal_formatter, outfile=out_file))
                    except:
                        # print_save_file_error(yaml_file)
                        sys.exit(1)
            except Exception as err:
                print_open_file_error(yaml_file)
                sys.exit(1)
