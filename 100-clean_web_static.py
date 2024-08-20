#!/usr/bin/python3
"""Delete outdated archives
"""
from frabric.api import *
import os

env.hosts = ['34.204.60.189', '54.145.155.95']


def do_clean(number=0):
    """clear old archives from database
    number (int): Number of archives to keep
    """
    number = 1 if int(number) == 0 else int(number)

    # Arrange archive from oldest to newest
    archives = sorted(os.listdir("versions"))

    # pop the newest archives
    [archives.pop() for i in range(number)]

    # delete remaining old archive files
    with lcd("versions"):
        [local('sudo rm ./{}'.format(arch)) for arch in archives]

    with cd('/data/web_static/releases'):
        # ensures files are listed from oldest to newest on the server
        archives = run('ls -tr').split()

        # select only folders starting with web_ into the new archive list
        archives = [arch for arch in archives if 'web_static_' in arch]
        [archives.pop() for i in range(number)]

        # seperate files to keep and delete unwanted ones
        [run('sudo rm -rf ./{}'.format(arch)) for arch in archives]
