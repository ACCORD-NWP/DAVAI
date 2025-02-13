"""
Davai environment around experiments and shelves.
"""
import os
import re
import socket

from . import DAVAI_HOST_FILE

hosts_re_patterns = dict(belenos_re_pattern = "^belenoslogin\d\.belenoshpc\.meteo\.fr$",
                         taranis_re_pattern = "^taranislogin\d\.taranishpc\.meteo\.fr$",
                         atos_bologna_re_pattern = "^a[abcd]\d-\d+(.bullx)?$",
                         )


def guess():
    """
    Guess host from (by order of resolution):
      - presence in DAVAI_HOST_FILE
      - resolution from socket.gethostname() through RE patterns of base and user config
    """
    if os.path.exists(DAVAI_HOST_FILE):
        with open(DAVAI_HOST_FILE, 'r') as f:
            host = f.read().strip()
    else:
        socket_hostname = socket.gethostname()
        for h, pattern in hosts_re_patterns.items():
            if re.match(pattern, socket_hostname):
                host = h[:-len('_re_pattern')]  # h is '{host}_re_pattern'
                break
            else:
                host = None
    if not host:
        raise ValueError(" ".join([f"Couldn't guess host in '{DAVAI_HOST_FILE}', " +
                                   f"nor guess from hostname ({socket_hostname}) and"
                                   "keys '*host*_re_pattern' in section 'hosts' of config files."]))
    else:
        print(f"-> Running Davai on host '{host}'.")
    return host

