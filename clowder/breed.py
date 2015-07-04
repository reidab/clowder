import sys
import os
import shutil
import subprocess

import clowder.log
import clowder.utilities

class Breed(object):

    def __init__(self, url, clowderDirectory):
        command = 'repo init -u ' + url
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
        command = 'repo sync'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
        command = 'repo forall -c git checkout master'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
        os.mkdir(clowderDirectory)
        os.chdir(clowderDirectory)
        command = 'git clone ' + url + ' clowder'
        print("Running '" + command + "'")
        clowder.utilities.ex(command)
