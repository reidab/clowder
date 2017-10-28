"""Representation of clowder.yaml project"""

from __future__ import print_function

import inspect
import os
import sys

from termcolor import colored

import clowder.util.formatting as fmt
from clowder.error.clowder_error import ClowderError
from clowder.git.project_repo import ProjectRepo
from clowder.git.project_repo_recursive import ProjectRepoRecursive
from clowder.model.fork import Fork
from clowder.util.connectivity import is_offline
from clowder.util.decorators import project_repo_exists
from clowder.util.execute import execute_forall_command


class Project(object):
    """clowder.yaml project class"""

    def __init__(self, root_directory, project, group, defaults, sources):
        self.name = project['name']
        self.path = project['path']

        self._root_directory = root_directory
        self._ref = project.get('ref', group.get('ref', defaults['ref']))
        self._remote = project.get('remote', group.get('remote', defaults['remote']))
        self._depth = project.get('depth', group.get('depth', defaults['depth']))
        self._recursive = project.get('recursive', group.get('recursive', defaults.get('recursive', False)))
        self._timestamp_author = project.get('timestamp_author', group.get('timestamp_author',
                                                                           defaults.get('timestamp_author', None)))
        self._print_output = True

        self._source = None
        source_name = project.get('source', group.get('source', defaults['source']))
        for source in sources:
            if source.name == source_name:
                self._source = source

        self._url = self._source.get_url_prefix() + self.name + ".git"

        self.fork = None
        if 'fork' in project:
            fork = project['fork']
            if fork['remote'] == self._remote:
                error = fmt.remote_name_error(fork['name'], self.name, self._remote)
                print(fmt.invalid_yaml_error())
                print(error + '\n')
                sys.exit(1)
            self.fork = Fork(fork, self._root_directory, self.path, self._source)

    @project_repo_exists
    def branch(self, local=False, remote=False):
        """Print branches for project"""

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if not is_offline():
            if remote:
                if self.fork is None:
                    repo.fetch(self._remote, depth=self._depth)
                else:
                    repo.fetch(self.fork.remote_name)
                    repo.fetch(self._remote)

        repo.print_branches(local=local, remote=remote)

    @project_repo_exists
    def clean(self, args='', recursive=False):
        """Discard changes for project"""

        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive and recursive)
        repo.clean(args=args)

    @project_repo_exists
    def clean_all(self):
        """Discard all changes for project"""

        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive)
        repo.clean(args='fdx')

    @project_repo_exists
    def diff(self):
        """Show git diff for project"""

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        repo.status_verbose()

    def exists(self):
        """Check if project exists on disk"""

        path = os.path.join(self.full_path())
        return os.path.isdir(path)

    def existing_branch(self, branch, is_remote):
        """Check if branch exists"""

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if not is_remote:
            return repo.existing_local_branch(branch)

        rem = self._remote if self.fork is None else self.fork.remote_name
        return repo.existing_remote_branch(branch, rem)

    @project_repo_exists
    def fetch_all(self):
        """Fetch upstream changes if project exists on disk"""

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if self.fork is None:
            repo.fetch(self._remote, depth=self._depth)
            return

        repo.fetch(self.fork.remote_name)
        repo.fetch(self._remote)

    def formatted_project_path(self):
        """Return formatted project path"""

        repo_path = os.path.join(self._root_directory, self.path)
        return ProjectRepo.format_project_string(repo_path, self.path)

    def full_path(self):
        """Return full path to project"""

        return os.path.join(self._root_directory, self.path)

    def get_current_timestamp(self):
        """Clone project or update latest from upstream"""

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        return repo.get_current_timestamp()

    def get_yaml(self, resolved=False):
        """Return python object representation for saving yaml"""

        if resolved:
            ref = self._ref
        else:
            repo = ProjectRepo(self.full_path(), self._remote, self._ref)
            ref = repo.sha()

        project = {'name': self.name,
                   'path': self.path,
                   'depth': self._depth,
                   'recursive': self._recursive,
                   'ref': ref,
                   'remote': self._remote,
                   'source': self._source.name}

        if self.fork:
            fork_yaml = self.fork.get_yaml()
            project['fork'] = fork_yaml

        if self._timestamp_author:
            project['timestamp_author'] = self._timestamp_author

        return project

    def herd(self, branch=None, tag=None, depth=None, rebase=False, parallel=False):
        """Clone project or update latest from upstream"""

        self._print_output = not parallel

        herd_depth = self._depth if depth is None else depth
        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive,
                          parallel=parallel, print_output=self._print_output)

        if branch:
            fork_remote = None if self.fork is None else self.fork.remote_name
            self._run_herd_command('herd_branch', repo, self._url, branch,
                                   depth=herd_depth, rebase=rebase, fork_remote=fork_remote)
            return

        if tag:
            self._run_herd_command('herd_tag', repo, self._url, tag, depth=herd_depth, rebase=rebase)
            return

        self._run_herd_command('herd', repo, self._url, depth=herd_depth, rebase=rebase)

    def is_dirty(self):
        """Check if project is dirty"""

        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive)
        return not repo.validate_repo()

    def is_valid(self):
        """Validate status of project"""

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        return repo.validate_repo()

    def print_exists(self):
        """Print existence validation message for project"""

        if not self.exists():
            print(self.status())
            ProjectRepo.exists(self.full_path())

    def print_validation(self):
        """Print validation message for project"""

        if not self.is_valid():
            print(self.status())
            ProjectRepo.validation(self.full_path())

    @project_repo_exists
    def prune(self, branch, force=False, local=False, remote=False):
        """Prune branch"""

        if local and remote:
            self._prune_local(branch, force)
            self._prune_remote(branch)
        elif local:
            self._prune_local(branch, force)
        elif remote:
            self._prune_remote(branch)

    def reset(self, timestamp=None, parallel=False):
        """Reset project branches to upstream or checkout tag/sha as detached HEAD"""

        self._print_output = not parallel

        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive,
                          parallel=parallel, print_output=self._print_output)
        self._reset(repo, timestamp=timestamp)

    def run(self, command, ignore_errors, parallel=False):
        """Run command or script in project directory"""

        if not parallel:
            if not self.exists():
                print(colored(" - Project is missing\n", 'red'))
                return

        self._print_output = not parallel
        self._print(fmt.command(command))

        forall_env = {'CLOWDER_PATH': self._root_directory,
                      'PROJECT_PATH': self.full_path(),
                      'PROJECT_NAME': self.name,
                      'PROJECT_REMOTE': self._remote,
                      'PROJECT_REF': self._ref}

        if self.fork:
            forall_env['FORK_REMOTE'] = self.fork.remote_name

        return_code = execute_forall_command(command.split(), self.full_path(), forall_env, self._print_output)
        if not ignore_errors:
            err = fmt.command_failed_error(command)
            if return_code != 0:
                self._print(err)
                self._exit(err, return_code=return_code, parallel=parallel)

    @project_repo_exists
    def start(self, branch, tracking):
        """Start a new feature branch"""

        remote = self._remote if self.fork is None else self.fork.remote_name
        depth = self._depth if self.fork is None else 0

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        repo.start(remote, branch, depth, tracking)

    def status(self, padding=None):
        """Return formatted status for project"""

        if not ProjectRepo.existing_git_repository(self.full_path()):
            return colored(self.name, 'green')

        project_output = ProjectRepo.format_project_string(self.full_path(), self.path)
        current_ref_output = ProjectRepo.format_project_ref_string(self.full_path())

        if padding:
            project_output = project_output.ljust(padding)

        return project_output + ' ' + current_ref_output

    @project_repo_exists
    def stash(self):
        """Stash changes for project if dirty"""

        if self.is_dirty():
            repo = ProjectRepo(self.full_path(), self._remote, self._ref)
            repo.stash()

    def sync(self, rebase=False, parallel=False):
        """Sync fork project with upstream"""

        self._print_output = not parallel

        repo = self._repo(self.full_path(), self._remote, self._ref, self._recursive,
                          parallel=parallel, print_output=self._print_output)
        self._run_herd_command('herd', repo, self._url, rebase=rebase)
        self._print(self.fork.status())
        repo.sync(self.fork.remote_name, rebase=rebase)

    @staticmethod
    def _exit(message, parallel=False, return_code=1):
        """Exit based on serial or parallel job"""

        if parallel:
            raise ClowderError(message)
        sys.exit(return_code)

    def _print(self, val):
        """Print output if self._print_output is True"""

        if self._print_output:
            print(val)

    def _prune_local(self, branch, force):
        """Prune local branch"""

        repo = ProjectRepo(self.full_path(), self._remote, self._ref)
        if repo.existing_local_branch(branch):
            repo.prune_branch_local(branch, force)

    def _prune_remote(self, branch):
        """Prune remote branch"""

        remote = self._remote if self.fork is None else self.fork.remote_name
        repo = ProjectRepo(self.full_path(), remote, self._ref)
        if repo.existing_remote_branch(branch, remote):
            repo.prune_branch_remote(branch, remote)

    @staticmethod
    def _repo(path, remote, ref, recursive, **kwargs):
        """Clone project or update latest from upstream"""

        if recursive:
            return ProjectRepoRecursive(path, remote, ref, **kwargs)
        return ProjectRepo(path, remote, ref, **kwargs)

    def _reset(self, repo, timestamp=None):
        """Clone project or update latest from upstream"""

        if self.fork is None:
            if timestamp:
                repo.reset_timestamp(timestamp, self._timestamp_author, self._ref)
                return

            repo.reset(depth=self._depth)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)

        self._print(fmt.fork_string(self.name))
        if timestamp:
            repo.reset_timestamp(timestamp, self._timestamp_author, self._ref)
            return

        repo.reset()

    def _run_herd_command(self, command, repo, *args, **kwargs):
        """Run herd command"""

        if self.fork is None:
            getattr(repo, command)(*args, **kwargs)
            return

        self._print(self.fork.status())
        repo.configure_remotes(self._remote, self._url, self.fork.remote_name, self.fork.url)

        self._print(fmt.fork_string(self.name))
        kwargs['depth'] = 0
        getattr(repo, command)(*args, **kwargs)

        self._print(fmt.fork_string(self.fork.name))

        frame = inspect.currentframe()
        vals = inspect.getargvalues(frame)
        branch_arg = [a for a in vals.args if vals.locals[a] if vals.locals[a] == 'branch']
        branch = branch_arg[0] if branch_arg else None
        repo.herd_remote(self.fork.url, self.fork.remote_name, branch=branch)
