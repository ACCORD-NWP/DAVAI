# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodb import BatorODB
from .screenings.screeningCNT0_LAM3D import Screening as ScreeningCNT0
from .minims.minimCNT0_LAM3D import Minim as MinimCNT0


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar3h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='rundates', ticket=t,
                        loopconf='rundates',
                        loopsuffix='.{}',
                        nodes=[
                            BatorODB(tag='batodb', ticket=t, **kw),
                            ScreeningCNT0(tag='screeningCNT0', ticket=t, **kw),
                            MinimCNT0(tag='minimCNT0', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

