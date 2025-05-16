# -*- coding: utf-8 -*-
"""
LBC = Lateral Boundary Conditions
Creation of LBCs from a coupling model to a LAM
"""

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .arpege_lbc import ArpegeLBCbyFullpos
from .ifs_lbc import IFS_LBCbyFullpos


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
                Family(tag='ifs', ticket=t, on_error='delayed_fail', nodes=[
                    IFS_LBCbyFullpos(tag='from_ifs', ticket=t, **kw),
                    ], **kw),
                Family(tag='arpege', ticket=t, on_error='delayed_fail', nodes=[
                    ArpegeLBCbyFullpos(tag='from_arpege', ticket=t, **kw),
                    ], **kw),
            #Family(tag='arome', ticket=t, nodes=[
            #    LBCbyFullpos(tag='from_arome', ticket=t, **kw),
            #    ], **kw),a
            ], **kw),
        ],
    )

