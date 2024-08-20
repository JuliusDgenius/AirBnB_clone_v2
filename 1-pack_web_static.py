#!/usr/bin/python3
"""Createa fabric file
"""
from fabric.api import local
import time


def do_pack():
    """A script that generates a .tgz archive from the content
    of the web_static
    """
    time_format = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_staic_{:s}.tgz web_static/".
              format(time_format))
        return ("versions/web_static_{:s}.tgz".format(time_format))
    except RuntimeError:
        return None
