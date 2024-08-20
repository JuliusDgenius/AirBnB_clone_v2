#!/usr/bin/python3
"""Distribute an archive to your web server"""
from fabric.contrib import files
from fabric.api import env, put, run, local
import time
import os

env.hosts = ['34.204.60.189', '54.145.155.95']


def do_pack():
    """Script to generate a .tgz archive from the contents of the
    web_static
    """

    time_format = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{:s}.tgz web_static/".
              format(time_format))
        return ("versions/web_static_{:}.tgz".format(time_format))
    except RuntimeError:
        return None

def do_deploy(archive_path):
    """deploy function
    """
    if not os.path.exists(archive_path):
        return False

    data_path = '/data/web_static/releases/'
    temp = archive_path.split(".")[0]
    file_name = temp.split("/")[1]
    dest = data_path + file_name
    try:
        put(archive_path, '/tmp')
        run('sudo mkdir -p {}'.format(dest))
        run('sudo tar -xzf /tmp/{}.tgz -C {}'.format(file_name, dest))
        run('sudo rm -f /tmp/{}.tgz'.format(file_name))
        run('sudo mv -rf {}/web_static/* {}/'.format(dest, dest))
        run('sudo rm -rf {}/web_static/'.format(dest))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(dest))
        return True
    except RuntimeError:
        return False

def deploy():
    """Create archive files and upload them to remote server
    """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
