# -*- coding: utf-8 -*-
"""Clowder test swift command line controller

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

import os

from cement.ext.ext_argparse import ArgparseController, expose

from clowder_test.execute import (
    execute_command,
    clowder_test_exit
)


class SwiftController(ArgparseController):
    """Clowder test command swift controller"""

    path = os.path.join(os.getcwd(), 'test', 'scripts', 'swift')

    class Meta:
        """Clowder test swift Meta configuration"""

        label = 'swift'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = 'Run swift tests'

    @expose(
        help='Run all swift tests'
    )
    def all(self):
        """clowder swift tests"""

        path = os.path.join(os.getcwd(), 'test', 'scripts')
        return_code = self._execute_command('./test_example_swift.sh', path)
        clowder_test_exit(return_code)

    @expose(
        help='Run swift config versions tests'
    )
    def config_versions(self):
        """clowder swift config versions tests"""

        return_code = self._execute_command('./config_versions.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run swift configure remotes tests'
    )
    def configure_remotes(self):
        """clowder swift configure remotes tests"""

        return_code = self._execute_command('./configure_remotes.sh', self.path)
        clowder_test_exit(return_code)

    @expose(
        help='Run swift reset tests'
    )
    def reset(self):
        """clowder swift reset tests"""

        return_code = self._execute_command('./reset.sh', self.path)
        clowder_test_exit(return_code)

    def _execute_command(self, command, path):
        """Private execute command"""

        access = 'write' if self.app.pargs.write else 'read'
        test_env = {'ACCESS_LEVEL': access}
        if self.app.pargs.parallel:
            test_env["PARALLEL"] = '--parallel'
        return execute_command(command, path, env=test_env)