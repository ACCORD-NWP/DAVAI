# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

from footprints import FPDict, FPList
import vortex
from vortex import toolbox
from vortex.layout.nodes import Task, Driver

import davai  # for algos and specific resources


def setup(t, **kw):
    return Driver(
        tag     = 'setup',
        ticket  = t,
        nodes   = [
            CiboulaiXpSetup(tag='ciboulai_xpsetup', ticket=t, **kw),
        ],
        options=kw
    )


class CiboulaiXpSetup(Task):

    def process(self):
        t = self.ticket
        sh = self.sh

        # convert conf to be passed to algo through footprints
        conf = FPDict(self.conf)
        for k, v in conf.items():
            if isinstance(v, list):
                conf[k] = FPList(v)

        if 'compute' in self.steps or 'early-fetch' in self.steps:  # it should run on transfert nodes
            sh.title('Toolbox algo tb01 = tbalgo')
            tb01 = tbalgo = toolbox.algo(
                engine         = 'algo',
                kind           = 'ciboulai_xpsetup_mkjob',
                xpid           = self.conf.xpid,
                conf           = conf,
            )
            print(t.prompt, 'tb01 =', tb01)
            print()
            tbalgo.run(None)

        if 'late-backup' in self.steps:
            sh.title('Toolbox output tb02')
            tb02 = toolbox.output(
                role           = 'XPinfo',
                block          = 'summaries_stack',
                experiment     = self.conf.xpid,
                format         = 'json',
                hook_send      = (davai.vtx.hooks.summaries.send_to_DAVAI_server,
                                  self.conf.expertise_fatal_exceptions),
                kind           = 'xpinfo',
                local          = 'xpinfo.[format]',
                nativefmt      = '[format]',
            )
            print(t.prompt, 'tb02 =', tb02)
            print()
