"""
Davai environment around experiments and shelves.
"""
import importlib.resources
import sys
import os
import re
import configparser
import socket
import io
import subprocess

__version__ = "1.2.4"

# fixed parameters
DAVAI_RC_DIR = os.path.join(os.environ['HOME'], '.davairc')
DAVAI_XP_COUNTER = os.path.join(DAVAI_RC_DIR, '.last_xp')
DAVAI_XPID_SYNTAX = 'dv-{xpid_num:04}-{host}@{user}'
DAVAI_XPID_RE = re.compile(r'^dv-(?P<num>\d{4})-(?P<host>\w+)@(?P<user>\w+)$')
#DAVAI_XPID_RE = re.compile('^' + DAVAI_XPID_SYNTAX.replace('{xpid_num:04}', '\d+').
#                                                   replace('-{host}', '(-\w+)?').
#                                                   replace('{user}', '\w+') + '$')
CONFIG_USER_FILE = os.path.join(DAVAI_RC_DIR, 'user_config.ini')

#: usecases implemented
usecases = ('NRV', 'ELP')
#: vortex application
vapp = 'davai'


def guess_host():
    """
    Guess host from (by order of resolution):
      - presence as 'host' in section [hosts] of base and user config
      - resolution from socket.gethostname() through RE patterns of base and user config
    """
    host = config.get('hosts', 'host', fallback=None)
    if not host:
        socket_hostname = socket.gethostname()
        for h, pattern in config['hosts'].items():
            if re.match(pattern, socket_hostname):
                host = h[:-len('_re_pattern')]  # h is '{host}_re_pattern'
                break
    if not host:
        raise ValueError(("Couldn't find 'host' in [hosts] section of config files ('{}', base config), " +
                          "nor guess from hostname ({}) and keys '*host*_re_pattern' " +
                          "in section 'hosts' of same config files.").format(
            CONFIG_USER_FILE, socket_hostname))
    return host


# CONFIG
config = configparser.ConfigParser()
with importlib.resources.open_text("davai.conf", "base.ini",) as fh:
    config.read_file(fh)
# read user config a first time to help guessing host
if os.path.exists(CONFIG_USER_FILE):
    config.read(CONFIG_USER_FILE)
# then complete config with host config file
with importlib.resources.open_text("davai.conf", f"{guess_host()}.ini") as fh:
    config.read_file(fh)
# and read again user config so that it overwrites host config
if os.path.exists(CONFIG_USER_FILE):
    config.read(CONFIG_USER_FILE)

def show_config():
    """Show current config."""
    print("Configuration, from:")
    for c in ("BASE_CONFIG", "HOST_CONFIG", CONFIG_USER_FILE):
        print(" - {}".format(c))
    print("-" * 80)
    config.write(sys.stdout)

def preset_user_config_file(prompt=None):
    """Copy a (empty/commented) template of user config file."""
    if not os.path.exists(CONFIG_USER_FILE):
        if not os.path.exists(os.path.basename(CONFIG_USER_FILE)):
            os.makedirs(os.path.basename(CONFIG_USER_FILE))
        with importlib.resources.open_text(
            "davai.conf", "user_config_template.ini",
        ) as i:
            t = i.readlines()
        with io.open(CONFIG_USER_FILE, 'w') as o:
            for l in t:
                o.write('#' + l)
        prompt = True
    if prompt:
        print("See user config file to be tuned in : '{}'".format(CONFIG_USER_FILE))


# INITIALIZATION
def initialized():
    """
    Make sure Davai env is initialized for user.
    """
    # import inside function because of circular dependency
    from .util import expandpath
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
    # User config
    preset_user_config_file()

DAVAI_HOST = guess_host()
