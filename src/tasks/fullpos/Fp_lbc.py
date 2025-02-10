# -*- coding: utf-8 -*-
"""
Fi = Forecast (inline fullpos)
"""
from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .arpege_lbc import ArpegeLBCbyFullpos
from .ifs_lbc import IFS_LBCbyFullpos


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
                Family(tag='ifs', ticket=t, on_error='delayed_fail', nodes=[
                    IFS_LBCbyFullpos(tag='fp_lbc-ifs', ticket=t, **kw),
                    ], **kw),
                Family(tag='arpege', ticket=t, on_error='delayed_fail', nodes=[
                    ArpegeLBCbyFullpos(tag='fp_lbc-arpege', ticket=t, **kw),
                    ], **kw),
            #Family(tag='arome', ticket=t, nodes=[
            #    LBCbyFullpos(tag='fp_lbc.from-arome', ticket=t, **kw),
            #    ], **kw),a
            ], **kw),
        ],
    )

