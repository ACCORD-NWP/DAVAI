# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family

from .raw2odb.batodb import BatorODB
from .screenings.screeningOOPS import Screening as ScreeningOOPS
from .minims.minimOOPS import Minim as MinimOOPS
from ..objects.obsop.Hscreened import Hscreened


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='3dvar6h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    BatorODB(tag='batodb', ticket=t, **kw),
                    ScreeningOOPS(tag='screening', ticket=t, **kw),
                    Hscreened(tag='test_adjoint', ticket=t, on_error='delayed_fail', **kw),
                    MinimOOPS(tag='minim', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

