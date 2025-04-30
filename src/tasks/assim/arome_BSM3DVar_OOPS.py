# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodbLAM import BatorODB
from .screenings.screeningOOPS_LAM3D import ScreeningOOPS
from .minims.minimOOPS_LAM3D import MinimNoVARBC as MinimOOPSNoVARBC


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
                            ScreeningOOPS(tag='screeningoops', ticket=t, **kw),
                            MinimOOPSNoVARBC(tag='minimoops_novarbc', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

