# -*- coding: utf-8 -*-
"""
Loop on obstypes to test BatorODB+Screening independantly on each obstypes.
"""

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodb import BatorODB
from .screenings.screening_LAM3D import Screening


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar3h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='obstypes', ticket=t,
                        loopconf='obstypes',
                        loopsuffix='.{}',
                        nodes=[
                        Family('BSM', ticket=t, on_error='delayed_fail', nodes=[
                            BatorODB(tag='batodb', ticket=t, **kw),
                            Screening(tag='screening', ticket=t, **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

