# -*- coding: utf-8 -*-
"""Example clowder plugin command

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

from cement.ext.ext_argparse import ArgparseController, expose

from clowder.clowder_controller import CLOWDER_CONTROLLER
from clowder.clowder_repo import print_clowder_repo_status
import clowder.util.formatting as fmt


# Disable errors shown by pylint for too few public methods
# pylint: disable=R0903


class ExamplePluginController(ArgparseController):
    """Example plugin command controller class"""

    class Meta:
        """Example plugin command Meta configuration"""

        label = 'exampleplugin'
        description = 'example plugin controller description'
        stacked_on = 'base'
        stacked_type = 'embedded'

    @expose(
        help="example plugin command description",
        arguments=[
            (['--foo'], dict(action='store', default='something', help='the infamous foo option'))
        ]
    )
    def mycommand(self):
        """Example plugin command entry point"""

        self._mycommand()

    @print_clowder_repo_status
    def _mycommand(self):
        """Example plugin command private implementation"""

        print("foo: " + self.app.pargs.foo + '\n')

        print("Clowder information\n")

        defaults = CLOWDER_CONTROLLER.defaults
        print("Default ref: " + defaults.ref)
        print("Default remote name: " + defaults.remote)
        print("Default source name: " + defaults.source)
        print("Default git protocol: " + defaults.protocol)
        print("Default depth: " + str(defaults.depth))
        print("Default recursive value: " + str(defaults.recursive))
        print("Default timestamp author: " + str(defaults.timestamp_author))

        for group in CLOWDER_CONTROLLER.groups:
            print('\n' + fmt.group_name(group.name))
            print("Group name: " + group.name)
            print("Group depth: " + str(group.depth))
            print("Group recursive: " + str(group.recursive))
            print("Group timestamp author: " + str(group.timestamp_author))
            print("Group ref: " + group.ref)
            print("Group remote name: " + group.remote_name)
            for project in group.projects:
                print("\nProject name: " + project.name)
                print("Project path: " + project.path)
                print("Project ref: " + project.ref)
                print("Project remote: " + project.remote)
                print("Project depth: " + str(project.depth))
                print("Project recursive: " + str(project.recursive))
                print("Source name: " + project.source.name)
                print("Source url: " + project.source.url)
                if project.fork:
                    print("Fork name: " + project.fork.name)
                    print("Fork path: " + project.fork.path)
                    print("Fork remote name: " + project.fork.remote_name)


def load(app):
    """Example plugin command load function"""

    app.handler.register(ExamplePluginController)
