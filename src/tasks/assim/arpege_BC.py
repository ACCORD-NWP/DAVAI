# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodb import BatorODB
from .surface.canari import Canari


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
            Family(tag='arpege', ticket=t, nodes=[
                Family(tag='surf_assim_6h', ticket=t, nodes=[
                    BatorODB(tag='batodb', ticket=t, **kw),
                    Canari(tag='canari', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

