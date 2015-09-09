"""clowder.yaml parsing and functionality"""
import os, yaml
from termcolor import colored
from clowder.group import Group
from clowder.source import Source
from clowder.utility.clowder_utilities import (
    forall_run,
    validate_yaml,
    print_exiting
)

class ClowderController(object):
    """Class encapsulating project information from clowder.yaml for controlling clowder"""
    def __init__(self, rootDirectory):
        self.root_directory = rootDirectory
        self.default_ref = None
        self.default_remote = None
        self.default_source = None
        self.groups = []
        self.sources = []

        self._load_yaml()

    def fix_version(self, version):
        """Save current commits to a clowder.yaml in the versions directory"""
        self._validate_projects_exist()
        self._validate(self.get_all_group_names())
        versions_dir = os.path.join(self.root_directory, 'clowder', 'versions')
        version_name = version.replace('/', '-') # Replace path separateors with dashes
        version_dir = os.path.join(versions_dir, version_name)
        if not os.path.exists(version_dir):
            os.makedirs(version_dir)

        yaml_file = os.path.join(version_dir, 'clowder.yaml')
        yaml_file_output = colored(yaml_file, 'cyan')
        version_output = colored(version_name, attrs=['bold'])
        if not os.path.exists(yaml_file):
            with open(yaml_file, 'w') as file:
                print('Fixing version ' + version_output + ' at ' + yaml_file_output)
                yaml.dump(self._get_yaml(), file, default_flow_style=False)
        else:
            print('Version ' + version_output + ' already exists at ' + yaml_file_output)
            print_exiting()

    def forall_groups(self, command, group_names):
        """Runs command in all project directories of groups specified"""
        directories = []
        for group in self.groups:
            if group.name in group_names:
                for project in group.projects:
                    directories.append(project.full_path())
        forall_run(command, directories)

    def forall_projects(self, command, project_names):
        """Runs command in all project directories of projects specified"""
        directories = []
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    directories.append(project.full_path())
        forall_run(command, directories)

    def get_all_group_names(self):
        """Returns all group names for current clowder.yaml"""
        return sorted([g.name for g in self.groups])

    def get_all_project_names(self):
        """Returns all project names for current clowder.yaml"""
        return sorted([p.name for g in self.groups for p in g.projects])

    def get_fixed_version_names(self):
        """Return list of all fixed versions"""
        versions_dir = os.path.join(self.root_directory, 'clowder', 'versions')
        if os.path.exists(versions_dir):
            return os.listdir(versions_dir)
        else:
            return None

    def groom_groups(self, group_names):
        """Discard changes for projects"""
        if self._is_dirty():
            for group in self.groups:
                if group.name in group_names:
                    group.groom()
        else:
            print('No changes to discard')

    def groom_projects(self, project_names):
        """Discard changes for projects"""
        if self._is_dirty():
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.groom()
        else:
            print('No changes to discard')

    def herd_groups(self, group_names):
        """Sync projects with latest upstream changes"""
        self._validate(group_names)
        for group in self.groups:
            if group.name in group_names:
                group.herd()

    def herd_projects(self, project_names):
        """Sync projects with latest upstream changes"""
        self._validate(project_names)
        for group in self.groups:
            for project in group.projects:
                if project.name in project_names:
                    project.herd()

    def meow(self, group_names):
        """Print status for projects"""
        for group in self.groups:
            if group.name in group_names:
                group.meow()

    def meow_verbose(self, group_names):
        """Print git status for projects with changes"""
        for group in self.groups:
            if group.name in group_names:
                group.meow_verbose()

    def stash_groups(self, group_names):
        """Stash changes for projects with changes"""
        if self._is_dirty():
            for group in self.groups:
                if group.name in group_names:
                    group.stash()
        else:
            print('No changes to stash')

    def stash_projects(self, project_names):
        """Stash changes for projects with changes"""
        if self._is_dirty():
            for group in self.groups:
                for project in group.projects:
                    if project.name in project_names:
                        project.stash()
        else:
            print('No changes to stash')

    def _get_yaml(self):
        """Return python object representation for saving yaml"""
        groups_yaml = [g.get_yaml() for g in self.groups]
        sources_yaml = [s.get_yaml() for s in self.sources]
        defaults_yaml = {'ref': self.default_ref,
                         'remote': self.default_remote,
                         'source': self.default_source}
        return {'defaults': defaults_yaml,
                'sources': sources_yaml,
                'groups': groups_yaml}

    def _is_dirty(self):
        """Check if there are any dirty projects"""
        is_dirty = False
        for group in self.groups:
            if group.is_dirty():
                is_dirty = True
        return is_dirty

    def _load_yaml(self):
        """Load clowder from yaml file"""
        yaml_file = os.path.join(self.root_directory, 'clowder.yaml')
        if os.path.exists(yaml_file):
            with open(yaml_file) as file:
                parsed_yaml = yaml.safe_load(file)
                validate_yaml(parsed_yaml)

                self.default_ref = parsed_yaml['defaults']['ref']
                self.default_remote = parsed_yaml['defaults']['remote']
                self.default_source = parsed_yaml['defaults']['source']

                self.sources = [Source(s) for s in parsed_yaml['sources']]

                defaults = {'ref': self.default_ref,
                            'remote': self.default_remote,
                            'source': self.default_source}

                for group in parsed_yaml['groups']:
                    self.groups.append(Group(self.root_directory,
                                             group,
                                             defaults,
                                             self.sources))
                # self.groups.sort(key=lambda group: group.name)

    def _validate(self, group_names):
        """Validate status of all projects for specified groups"""
        valid = True
        for group in self.groups:
            if group.name in group_names:
                group.print_validation()
                if not group.is_valid():
                    valid = False
        if not valid:
            print_exiting()

    def _validate_projects_exist(self):
        """Validate existence status of all projects for specified groups"""
        projects_exist = True
        for group in self.groups:
            group.print_existence_message()
            if not group.projects_exist():
                projects_exist = False
        if not projects_exist:
            herd_output = colored('clowder herd', 'yellow')
            print('')
            print('First run ' + herd_output + ' to clone missing projects')
            print_exiting()