# -*- coding: utf-8 -*-
"""
Loop on obstypes to test BatorODB+Screening independantly on each obstypes.
"""

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodbNew import BatorODB
from .screenings.screeningOOPS_LAM3D import ScreeningOOPS


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar3h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='obstypes', ticket=t,
                        loopconf='obstypes',
                        loopsuffix='.{}',
                        nodes=[
                            BatorODB(tag='batodb', ticket=t, **kw),
                            ScreeningOOPS(tag='screening', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

