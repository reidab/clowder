# -*- coding: utf-8 -*-
"""Clowder test command line base controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import (
    execute_command,
    clowder_test_exit
)


VERSION = '0.1.0'


class BaseController(ArgparseController):
    """Clowder app base controller"""

    path = os.path.join(os.getcwd(), 'test', 'scripts')

    class Meta:
        """Clowder app base Meta configuration"""

        label = 'base'
        description = 'Clowder test runner'
        arguments = [
            (['--parallel', '-p'], dict(action='store_true', help='run tests with parallel commands')),
            (['--write', '-w'], dict(action='store_true', help='run tests requiring test repo write access')),
            (['-v', '--version'], dict(action='version', version=VERSION))
        ]

    @expose(
        help='Run all tests'
    )
    def all(self):
        """clowder test all command"""

        scripts = ['./test_example_cats.sh', './test_example_cocos2d.sh',
                   './test_example_llvm.sh', './test_example_swift.sh']
        for script in scripts:
            return_code = self._execute_command(script, self.path)
            clowder_test_exit(return_code)

        self.offline()
        self.parallel()
        self.unittests()

    @expose(
        help='Run offline tests'
    )
    def offline(self):
        """clowder offline tests"""

        path = os.path.join(self.path, 'cats')
        return_code = self._execute_command('./offline.sh', path)
        clowder_test_exit(return_code)

    @expose(
        help='Run parallel tests',
        arguments=[
            (['--write', '-w'], dict(action='store_true', help='run tests requiring test repo write access'))
        ]
    )
    def parallel(self):
        """clowder parallel tests"""

        access = 'write' if self.app.pargs.write else 'read'
        test_env = {'ACCESS_LEVEL': access, "PARALLEL": '--parallel'}

        return_code = self._execute_command('./test_parallel.sh', self.path, test_env=test_env)
        clowder_test_exit(return_code)

    @expose(
        help='Run unit tests',
        arguments=[
            (['version'], dict(choices=['python2', 'python3'], metavar='PYTHON_VERSION',
                               help='Python vesion to run unit tests for'))
        ]
    )
    def unittests(self):
        """clowder unit tests"""

        if self.app.pargs.version == 'python2':
            test_env = {"PYTHON_VERSION": 'python'}
        else:
            test_env = {"PYTHON_VERSION": 'python3'}

        return_code = self._execute_command('./unittests.sh', self.path, test_env=test_env)
        clowder_test_exit(return_code)

    @expose(
        help='Run tests requiring remote write permissions',
        arguments=[
            (['--parallel', '-p'], dict(action='store_true', help='run tests with parallel commands'))
        ]
    )
    def write(self):
        """clowder write tests"""

        test_env = {'ACCESS_LEVEL': 'write'}
        if self.app.pargs.parallel:
            test_env["PARALLEL"] = '--parallel'

        example_dir = os.path.join(self.path, 'cats')
        cats_scripts = ['./write_herd.sh', './write_prune.sh', './write_repo.sh', './write_start.sh']
        for script in cats_scripts:
            return_code = self._execute_command(script, example_dir, test_env=test_env)
            clowder_test_exit(return_code)

        example_dir = os.path.join(self.path, 'cocos2d')
        return_code = self._execute_command('./write_protocol.sh', example_dir, test_env=test_env)
        clowder_test_exit(return_code)

        example_dir = os.path.join(self.path, 'llvm')
        llvm_scripts = ['./write_forks.sh', './write_sync.sh']
        for script in llvm_scripts:
            return_code = self._execute_command(script, example_dir, test_env=test_env)
            clowder_test_exit(return_code)

        example_dir = os.path.join(self.path, 'swift')
        return_code = self._execute_command('./write_configure_remotes.sh', example_dir, test_env=test_env)
        clowder_test_exit(return_code)

    def _execute_command(self, command, path, test_env=None):
        """Private execute command"""

        if test_env is None:
            access = 'write' if self.app.pargs.write else 'read'
            test_env = {'ACCESS_LEVEL': access}
            if self.app.pargs.parallel:
                test_env["PARALLEL"] = '--parallel'

        return execute_command(command, path, env=test_env)