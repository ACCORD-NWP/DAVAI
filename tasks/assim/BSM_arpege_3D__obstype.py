# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex.layout.nodes import Driver, Family, LoopFamily

from .batodb import BatorODB
from .screening import Screening
from .minim import Minim


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='3dvar', ticket=t, nodes=[
                LoopFamily(tag='obstype', ticket=t,
                    loopconf='obstypes',
                    loopsuffix='.{}',
                    nodes=[
                    Family('BSM', ticket=t, on_error='delayed_fail', nodes=[
                        BatorODB(tag='batodb', ticket=t, **kw),
                        Screening(tag='screening', ticket=t, **kw),
                        Minim(tag='minim', ticket=t, **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

