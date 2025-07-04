# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family

from .raw2odb.batodb import BatorODB
from .screenings.screeningCNT0 import Screening as ScreeningCNT0
from .minims.minimCNT0 import Minim as MinimCNT0


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='4dvar6h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    BatorODB(tag='batodb', ticket=t, **kw),
                    ScreeningCNT0(tag='screening', ticket=t, **kw),
                    MinimCNT0(tag='minim', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

