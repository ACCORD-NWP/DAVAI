#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Handle a Davai experiment metadata (context) for Ciboulai.
"""
import json
import os

from bronx.stdtypes import date


def _get_env_catalog_details(env):
    from gco.tools import uenv, genv
    if any([env.startswith(scheme) for scheme in ('uget:', 'uenv:')]):
        # uenv
        details = uenv.nicedump(env,
                                scheme='uget',
                                netloc='uget.multi.fr')
    else:
        # genv
        details = ['%s="%s"' % (k, v)
                   for (k, v) in genv.autofill(env).items()]
    return details


def gather_mkjob_xp_conf(xpid, conf):
    """
    Gather info from mkjob conf file + additional, and write it to file ('xpinfo.json')
    to be sent to Ciboulai to initialize XP.
    """
    env_catalog_variables = ('davaienv', 'appenv_global', 'appenv_lam', 'appenv_clim', 'appenv_fullpos_partners', 'commonenv')
    # set dynamically additional info
    if conf['ref_xpid'] == xpid:
        conf['ref_xpid'] = None
    conf.update(xpid=xpid,
                initial_time_of_launch=date.utcnow().isoformat().split('.')[0],
                user=os.environ['USER'])
    # get uenv details
    for k in env_catalog_variables:
        env = conf[k]
        details = _get_env_catalog_details(env)
        conf['{}_details'.format(k)] = '<br>'.join(details)
    # write to file
    with open('xpinfo.json', 'w') as out:
        json.dump(conf, out, indent=4, sort_keys=True)
