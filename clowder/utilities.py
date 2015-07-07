# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import os
import shutil
import sys

def ex(command):
    print("Running '" + command + "'")
    r = Popen(command, stderr=PIPE, shell=True)
    stderr = r.communicate()
    if r.poll() != 0:
        print('The command "{0}" failed: {1}'.format(command, stderr))
        print('Aborting.\n')
        sys.exit()

def unknownArg(command, arg):
    print('Unknown argument for "{0}": "{1}"\n'.format(command, arg))
    print(r'\t ❓  Dunno what that means...  ¯\_(ツ)_/¯\n')
    print('Aborting.\n')
    sys.exit()

def removeAllFilesInDirectory(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def rchop(thestring, ending):
    if thestring.endswith(ending):
        return thestring[:-len(ending)]
    return thestring
