# -*- coding: utf-8 -*-
"""Project Git utility class with submodules

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from git import GitError
from termcolor import colored

import clowder.util.formatting as fmt
from clowder.git.project_repo import ProjectRepo
from clowder.git.repo import execute_command


class ProjectRepoRecursive(ProjectRepo):
    """Class encapsulating git utilities"""

    def __init__(self, repo_path, remote, default_ref, parallel=False, print_output=True):
        ProjectRepo.__init__(self, repo_path, remote, default_ref, parallel=parallel, print_output=print_output)

    def clean(self, args=None):
        """Discard changes for repo and submodules

        :param str args: Git clean options
            - ``d`` Remove untracked directories in addition to untracked files
            - ``f`` Delete directories with .git sub directory or file
            - ``X`` Remove only files ignored by git
            - ``x`` Remove all untracked files
        :return:
        """

        ProjectRepo.clean(self, args=args)

        self._print(' - Clean submodules recursively')
        self._submodules_clean()

        self._print(' - Reset submodules recursively')
        self._submodules_reset()

        self._print(' - Update submodules recursively')
        self._submodules_update()

    def has_submodules(self):
        """Repo has submodules

        :return: True, if repo has submodules
        :rtype: bool
        """

        return len(self.repo.submodules) > 0

    def herd(self, url, depth=0, fetch=True, rebase=False):
        """Herd ref

        :param str url: URL of repo
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool fetch: Whether to fetch
        :param bool rebase: Whether to rebase instead of pull
        :return:
        """

        ProjectRepo.herd(self, url, depth=depth, fetch=fetch, rebase=rebase)
        self.submodule_update_recursive(depth)

    def herd_branch(self, url, branch, depth=0, rebase=False, fork_remote=None):
        """Herd branch

        :param str url: URL of repo
        :param str branch: Branch name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to rebase instead of pull
        :param str fork_remote: Fork remote name
        :return:
        """

        ProjectRepo.herd_branch(self, url, branch, depth=depth, rebase=rebase, fork_remote=fork_remote)
        self.submodule_update_recursive(depth)

    def herd_tag(self, url, tag, depth=0, rebase=False):
        """Herd tag

        :param str url: URL of repo
        :param str tag: Tag name
        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :param bool rebase: Whether to rebase instead of pull
        :return:
        """

        ProjectRepo.herd_tag(self, url, tag, depth=depth, rebase=rebase)
        self.submodule_update_recursive(depth)

    def is_dirty_submodule(self, path):
        """Check whether submodule repo is dirty

        :param str path: Submodule path
        :return: True, if submodule at path is dirty
        :rtype: bool
        """

        return not self.repo.is_dirty(path)

    def submodule_update_recursive(self, depth=0):
        """Update submodules recursively and initialize if not present

        :param int depth: Git clone depth. 0 indicates full clone, otherwise must be a positive integer
        :return:
        """

        print(' - Recursively update and init submodules')

        if depth == 0:
            command = ['git', 'submodule', 'update', '--init', '--recursive']
        else:
            command = ['git', 'submodule', 'update', '--init', '--recursive', '--depth', depth]

        return_code = execute_command(command, self.repo_path)
        if return_code != 0:
            message = colored(' - Failed to update submodules\n', 'red') + fmt.command_failed_error(command)
            self._print(message)
            self._exit(message)

    def sync(self, fork_remote, rebase=False):
        """Sync fork with upstream remote

        :param str fork_remote: Fork remote name
        :param bool rebase: Whether to use rebase instead of pulling latest changes
        :return:
        """

        ProjectRepo.sync(self, fork_remote, rebase=rebase)
        self.submodule_update_recursive()

    def validate_repo(self):
        """Validate repo state

        :return: True, if repo and submodules not dirty or repo doesn't exist on disk
        :rtype: bool
        """

        if not ProjectRepo.validate_repo(self):
            return False

        return not any([self.is_dirty_submodule(s.path) for s in self.repo.submodules])

    def _submodules_clean(self):
        """Clean all submodules

        Equivalent to: ``git submodule foreach --recursive git clean -ffdx``

        :return:
        """

        self._submodule_command('foreach', '--recursive', 'git', 'clean', '-ffdx',
                                error_msg=' - Failed to clean submodules')

    def _submodule_command(self, *args, **kwargs):
        """Base submodule command

        :param args: List of args to pass to ``git submodule`` command
        :return:
        """

        try:
            self.repo.git.submodule(*args)
        except (GitError, ValueError) as err:
            message = colored(str(kwargs.get('error_msg', ' - Submodule command failed')), 'red')
            self._print(message)
            self._print(fmt.error(err))
            self._exit(message)
        except (KeyboardInterrupt, SystemExit):
            self._exit()

    def _submodules_reset(self):
        """Reset all submodules

        Equivalent to: ``git submodule foreach --recursive git reset --hard``

        :return:
        """

        self._submodule_command('foreach', '--recursive', 'git', 'reset', '--hard',
                                error_msg=' - Failed to reset submodules')

    def _submodules_update(self):
        """Update all submodules

        Equivalent to: ``git submodule update --checkout --recursive --force``

        :return:
        """

        self._submodule_command('update', '--checkout', '--recursive', '--force',
                                error_msg=' - Failed to update submodules')
