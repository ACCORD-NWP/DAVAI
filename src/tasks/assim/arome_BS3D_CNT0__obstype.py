# -*- coding: utf-8 -*-
"""
Loop on obstypes to test BatorODB+Screening independantly on each obstypes.
"""

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodb import BatorODB
from .screenings.screeningCNT0_LAM3D import Screening as ScreeningCNT0


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar3hcnt0', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='obstypes', ticket=t,
                        loopconf='obstypes',
                        loopsuffix='.{}',
                        nodes=[
                            BatorODB(tag='batodb', ticket=t, **kw),
                            ScreeningCNT0(tag='screening', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

