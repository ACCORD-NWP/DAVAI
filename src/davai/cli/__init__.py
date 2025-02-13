"""
Davai command-line instructions environment, around experiments and shelves.
"""
import os
import re
import importlib.resources
import configparser

# fixed parameters
DAVAI_RC_DIR = os.path.join(os.environ['HOME'], '.davairc')
DAVAI_HOST_FILE = os.path.join(DAVAI_RC_DIR, 'host')
DAVAI_XP_COUNTER = os.path.join(DAVAI_RC_DIR, '.last_xp')
CONFIG_USER_FILE = os.path.join(DAVAI_RC_DIR, 'user_config.ini')
DAVAI_XPID_SYNTAX = 'dv-{xpid_num:04}-{host}@{user}'
DAVAI_XPID_RE = re.compile(r'^dv-(?P<num>\d{4})-(?P<host>\w+)@(?P<user>\w+)$')
#: usecases implemented
usecases = ('NRV', 'ELP')
#: vortex application
vapp = 'davai'

from . import host
DAVAI_HOST = host.guess()

# CONFIG
def read_config():
    """
    Read config from base, host and user config files.
    """
    print("Read config")
    config = configparser.ConfigParser()
    with importlib.resources.open_text("davai.cli.conf", "base.ini",) as fh:
        config.read_file(fh)
    with importlib.resources.open_text("davai.cli.conf", f"{DAVAI_HOST}.ini") as fh:
        config.read_file(fh)
    CONFIG_USER_FILE = os.path.join(DAVAI_RC_DIR, 'user_config.ini')
    if os.path.exists(CONFIG_USER_FILE):
        print(f"-> Read davai.cli config from {CONFIG_USER_FILE}")
        config.read(CONFIG_USER_FILE)
    return config

config = read_config()

