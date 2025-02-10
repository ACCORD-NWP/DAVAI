#!/usr/bin/env python
# -*- coding:Utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import io

import vortex
from vortex.layout.jobs import JobAssistantPlugin
from davai.util import set_env4git
from bronx.fancies import loggers
logger = loggers.getLogger(__name__)


class DavaiJobAssistantPlugin(JobAssistantPlugin):
    """JobAssistant plugin for Davai."""
    _footprint = dict(
        info = 'Davai JobAssistant Plugin',
        attr = dict(
            kind = dict(
                values = ['davai', ]
            ),
        ),
    )

    def plugable_env_setup(self, t, **kw):  # @UnusedVariable
        t.env.MPIAUTOCONFIG = self.masterja.conf.mpiautoconfig
        t.env.DAVAI_SERVER = self.masterja.conf.davai_server
        t.env.LD_LIBRARY_PATH = '/opt/softs/intel/oneapi/2023.2/mpi/2021.10.0/libfabric/lib'
        t.env.I_MPI_ROOT = '/opt/softs/intel/oneapi/2023.2/mpi/2021.10.0'
        if 'eccodes_samples_path' in self.masterja.conf:
            t.env.ECCODES_SAMPLES_PATH = self.masterja.conf.eccodes_samples_path
        if 'eccodes_definition_path' in self.masterja.conf:
            t.env.ECCODES_DEFINITION_PATH = self.masterja.conf.eccodes_definition_path
        # set token from file if not in env
        ciboulai_token = None
        if 'CIBOULAI_TOKEN' not in t.env:
            if 'ciboulai_token_file' in self.masterja.conf:
                logger.info("Ciboulai token not in env; read in file, as set in config")
                try:
                    with io.open(self.masterja.conf.ciboulai_token_file, 'r') as tf:
                        ciboulai_token = tf.readline().strip()
                except FileNotFoundError:
                    pass
            if ciboulai_token is None:
                logger.warning("Ciboulai token not found in env var CIBOULAI_TOKEN " +
                               "nor in file provided in config's 'ciboulai_token_file' attribute: " +
                               "sending results to Ciboulai may fail.")
            else:
                t.env.CIBOULAI_TOKEN = ciboulai_token
        if 'bufr_tables' in self.masterja.conf:
            t.env.BUFR_TABLES = self.masterja.conf.bufr_tables

    def plugable_extra_session_setup(self, t, **kw):  # @UnusedVariable
        """genv cycles need to be "registered" using '*_cycle' config variables"""
        self.masterja.conf['davai_cycle'] = self.masterja.conf['davaienv']
        for appenv in [k for k in self.masterja.conf if k.startswith("appenv_")]:
            self.masterja.conf['{}_cycle'.format(appenv[7:])] = self.masterja.conf[appenv]

    def plugable_toolbox_setup(self, t, **kw):  # @UnusedVariable
        """
        Davai toolbox setup:
            * Set 'vortex_set_aside' toolbox variable in order to export input resources to bucket
            * Set jobname for Algos
        """
        if self.masterja.conf.shelves2bucket:
            vortex_set_aside = dict(defaults=dict(namespace='vortex.archive.fr',
                                                  storage='shelves.bucket.localhost'),
                                    includes=[self.masterja.conf.input_shelf,])
            self.masterja.conf.vortex_set_aside = vortex_set_aside
            vortex.toolbox.defaults(vortex_set_aside=vortex_set_aside)
        # jobname for Algos, to broadcast this information to ciboulai
        vortex.toolbox.defaults(mkjob_jobname=self.masterja.conf.jobname)
        # mpiname, to activate DDT
        if 'mpiname' in self.masterja.conf:
            vortex.toolbox.defaults(mpiname=self.masterja.conf.mpiname)

    def plugable_system_setup(self, t, **kw):
        if self.masterja.conf.promote_coredump:
            # Unlimited size for core-dump files
            t.sh.setulimit('core')
            # Intel wants this variable to be in lowercase... ifort is such a nice compiler :-(
            t.env.setvar('decfort_dump_flag', 'TRUE', enforce_uppercase=False)


class DavaiDevJobAssistantPlugin(DavaiJobAssistantPlugin):
    """JobAssistant plugin for Davai development."""
    _footprint = dict(
        info = 'Davai dev JobAssistant Plugin',
        attr = dict(
            kind = dict(
                values = ['davaidev', ]
            ),
        ),
    )

    def plugable_toolbox_setup(self, t, **kw):
        super(DavaiDevJobAssistantPlugin, self).plugable_toolbox_setup(t, **kw)
        vortex.toolbox.active_promise = False  # deactivate the cleaning of promises in cache


class GitJobAssistantPlugin(JobAssistantPlugin):
    """JobAssistant plugin for Git."""
    _footprint = dict(
        info = 'Git JobAssistant Plugin',
        attr = dict(
            kind = dict(
                values = ['git', ]
            ),
        ),
    )

    def plugable_env_setup(self, t, **kw):  # @UnusedVariable
        set_env4git()
