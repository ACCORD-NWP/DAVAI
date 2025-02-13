#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Utilities.
"""

import os
import io
import datetime
import sys

from . import config


def expandpath(path):
    """Expand user and env var in a path)."""
    return os.path.expanduser(os.path.expandvars(path))

def set_default_mtooldir():
    """Set env var MTOOLDIR from config if not already in environment."""
    if not os.environ.get('MTOOLDIR', None):
        MTOOLDIR = expandpath(config['paths'].get('default_mtooldir'))
        if MTOOLDIR:
            os.environ['MTOOLDIR'] = MTOOLDIR

def vconf2usecase(vconf):
    """Convert vconf to usecase."""
    return vconf.upper()

def usecase2vconf(usecase):
    """Convert usecase to vconf."""
    return usecase.lower()

def initialized():
    """
    Make sure Davai env is initialized for user.
    """
    # import inside function because of circular dependency
    # Setup directories
    for d in ('experiments', 'logs', 'default_mtooldir'):
        p = expandpath(config.get('paths', d))
        if os.path.exists(p):
            if not os.path.isdir(p):
                raise ValueError("config[paths][{}] is not a directory : '{}'".format(d, p))
        else:
            if '$' in p:
                raise ValueError("config[paths][{}] is not expandable : '{}'".format(d, p))
            os.makedirs(p)
    if not os.path.exists(DAVAI_RC_DIR):
        os.makedirs(DAVAI_RC_DIR)

def show_config():
    """Show current config."""
    config.write(sys.stdout)

