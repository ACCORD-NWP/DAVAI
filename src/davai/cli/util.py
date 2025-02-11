#!/usr/bin/env python3
# -*- coding:Utf-8 -*-
"""
Utilities.
"""

import os
import io
import datetime

from . import config


def expandpath(path):
    """Expand user and env var in a path)."""
    return os.path.expanduser(os.path.expandvars(path))

def default_mtooldir():
    """Return default MTOOLDIR from config."""
    MTOOLDIR = expandpath(config['paths'].get('default_mtooldir'))
    return MTOOLDIR

def set_default_mtooldir():
    """Set env var MTOOLDIR from config if not already in environment."""
    if not os.environ.get('MTOOLDIR', None):
        MTOOLDIR = default_mtooldir()
        if MTOOLDIR:
            os.environ['MTOOLDIR'] = MTOOLDIR

def export_token_in_profile(token):
    """Export Ciboulai token in davai profile."""
    from . import DAVAI_PROFILE
    with io.open(DAVAI_PROFILE, 'a') as p:
        p.write("export CIBOULAI_TOKEN={}  # update: {}\n".format(token, str(datetime.date.today())))

def vconf2usecase(vconf):
    """Convert vconf to usecase."""
    return vconf.upper()

def usecase2vconf(usecase):
    """Convert usecase to vconf."""
    return usecase.lower()

