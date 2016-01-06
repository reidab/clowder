"""Clowder utilities"""
import errno, os, sys
from termcolor import colored
from clowder.utility.git_utilities import (
    git_current_branch,
    git_current_sha,
    git_is_detached,
    git_is_dirty
)

def force_symlink(file1, file2):
    """Force symlink creation"""
    try:
        os.symlink(file1, file2)
    except OSError as error:
        if error.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)

def format_project_string(repo_path, name):
    """Return formatted project name"""
    if git_is_dirty(repo_path):
        color = 'red'
        symbol = '*'
    else:
        color = 'green'
        symbol = ''
    return colored(name + symbol, color)

def format_ref_string(repo_path):
    """Return formatted repo ref name"""
    if git_is_detached(repo_path):
        current_ref = git_current_sha(repo_path)
        return colored('(HEAD @ ' + current_ref + ')', 'magenta')
    else:
        current_branch = git_current_branch(repo_path)
        return colored('(' + current_branch + ')', 'magenta')

def print_exists(repo_path):
    """Print existence validation messages"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        print(' - Project is missing')

def print_validation(repo_path):
    """Print validation messages"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return
    if git_is_dirty(repo_path):
        print(' - Dirty repo. Please stash, commit, or discard your changes')

def validate_repo_state(repo_path):
    """Validate repo state"""
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return True
    return not git_is_dirty(repo_path)

# Disable errors shown by pylint for no specified exception types
# pylint: disable=W0702
# Disable errors shown by pylint for statements which appear to have no effect
# pylint: disable=W0104
def validate_yaml(parsed_yaml):
    """Validate clowder loaded from yaml file"""
    try:
        error = colored('Missing \'defaults\'', 'red')
        defaults = parsed_yaml['defaults']
        error = colored('Missing \'ref\' in \'defaults\'\n', 'red')
        defaults['ref']
        del defaults['ref']
        error = colored('Missing \'remote\' in \'defaults\'\n', 'red')
        defaults['remote']
        del defaults['remote']
        error = colored('Missing \'source\' in \'defaults\'\n', 'red')
        defaults['source']
        del defaults['source']
        if 'depth' in defaults:
            del defaults['depth']
        if len(defaults) > 0:
            dict_entries = ''.join('{}: {}\n'.format(key, val)
                                   for key, val in sorted(defaults.items()))
            error = colored('Uknown entry in \'defaults\'\n\n' +
                            dict_entries, 'red')
            raise Exception('Unknown default value')

        error = colored('Missing \'sources\'\n', 'red')
        for source in parsed_yaml['sources']:
            error = colored('Missing \'name\' in \'sources\'\n', 'red')
            source['name']
            error = colored('Missing \'url\' in \'sources\'\n', 'red')
            source['url']

        error = colored('Missing \'groups\'\n', 'red')
        for group in parsed_yaml['groups']:
            error = colored('Missing \'name\' in \'group\'\n', 'red')
            group['name']
            error = colored('Missing \'projects\' in \'group\'\n', 'red')
            for project in group['projects']:
                error = colored('Missing \'name\' in \'project\'\n', 'red')
                project['name']
                del project['name']
                error = colored('Missing \'path\' in \'project\'\n', 'red')
                project['path']
                del project['path']
                if 'remote' in project:
                    del project['remote']
                if 'ref' in project:
                    del project['ref']
                if 'source' in project:
                    del project['source']
                if 'depth' in project:
                    del project['depth']
                if 'forks' in project:
                    for fork in project['forks']:
                        error = colored('Missing \'name\' in \'fork\'\n', 'red')
                        fork['name']
                        del fork['name']
                        error = colored('Missing \'remote\' in \'fork\'\n', 'red')
                        fork['remote']
                        del fork['remote']
                        if len(fork) > 0:
                            dict_entries = ''.join('{}: {}\n'.format(key, val)
                                                   for key, val in sorted(fork.items()))
                            error = colored('Uknown entry in \'fork\'\n\n' +
                                            dict_entries, 'red')
                            raise Exception('Unknown fork value')
                    del project['forks']
                if len(project) > 0:
                    dict_entries = ''.join('{}: {}\n'.format(key, val)
                                           for key, val in sorted(project.items()))
                    error = colored('Uknown entry in \'project\'\n\n' +
                                    dict_entries, 'red')
                    raise Exception('Unknown project value')
    except:
        print('')
        clowder_output = colored('clowder.yaml', 'cyan')
        print(clowder_output + ' appears to be invalid')
        print('')
        print(error)
        sys.exit(1)
