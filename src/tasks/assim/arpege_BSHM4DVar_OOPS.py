# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family

from .raw2odb.batodb import BatorODB
from .screenings.screeningOOPS import Screening as ScreeningOOPS
from .minims.minimOOPS import Minim as MinimOOPS
from .minims.Analyse4dvar import Analyse4dvar
from .opobs.Htlad import Htlad

def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='4dvar6h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    #BatorODB(tag='batodb', ticket=t, **kw),
                    #ScreeningOOPS(tag='screeningoops', ticket=t, **kw),
                    Htlad(tag='test_adjoint', ticket=t, on_error='delayed_fail', **kw),
                    #MinimOOPS(tag='minimoops', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

