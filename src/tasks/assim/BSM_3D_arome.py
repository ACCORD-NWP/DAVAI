# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodb import BatorODB
from .screenings.screening_LAM3D import Screening
from .minims.minimCNT0_LAM3D import Minim as MinimCNT0
from .minims.minimOOPS_LAM3D import Minim as MinimOOPS


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar3h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='rundates', ticket=t,
                        loopconf='rundates',
                        loopsuffix='.{}',
                        nodes=[
                        Family('BSM', ticket=t, on_error='delayed_fail', nodes=[
                            BatorODB(tag='batodb', ticket=t, **kw),
                            Family('multitasks', ticket=t, on_error='delayed_fail', nodes=[
                                Screening(tag='screening', ticket=t, **kw),
                                # delayed_fail to let the minimOOPS run before raising error
                                MinimCNT0(tag='minimCNT0', ticket=t, on_error='delayed_fail', **kw),
                                #MinimOOPS(tag='minimOOPS', ticket=t, **kw),
                                ], **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

