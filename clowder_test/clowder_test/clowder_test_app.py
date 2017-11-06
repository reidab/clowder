# -*- coding: utf-8 -*-
"""Clowder test command line app

.. codeauthor:: Joe Decapo <joe@polka.cat>

"""

from __future__ import print_function

import os
import sys

import colorama
from cement.core.foundation import CementApp

from clowder_test.cli.base_controller import BaseController
from clowder_test.cli.cats_controller import CatsController
from clowder_test.cli.cocos2d_controller import Cocos2dController
from clowder_test.cli.llvm_controller import LLVMController
from clowder_test.cli.swift_controller import SwiftController
from clowder_test.execute import execute_command


class ClowderApp(CementApp):
    """Clowder command CLI app"""

    class Meta:
        """Clowder command CLI Meta configuration"""

        label = 'clowder'
        extensions = ['argcomplete']
        base_controller = 'base'
        handlers = [
            BaseController,
            CatsController,
            Cocos2dController,
            LLVMController,
            SwiftController
        ]


def main():
    """Clowder command CLI main function"""

    print()

    scripts_dir = os.path.join(os.getcwd(), 'test', 'scripts')
    return_code = execute_command('./setup_local_test_directory.sh', scripts_dir)
    if return_code != 0:
        print(' - Failed to setup local test directory')
        sys.exit(return_code)

    with ClowderApp() as app:
        app.run()


if __name__ == '__main__':
    colorama.init()
    main()