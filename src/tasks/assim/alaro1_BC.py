# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, unicode_literals, division

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodb import BatorODB
from .surface.canari_alaro import CanariAlaro


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
            Family(tag='alaro1', ticket=t, nodes=[
                Family(tag='surf_assim_3h', ticket=t, nodes=[
                    BatorODB(tag='batodb', ticket=t, **kw),
                    CanariAlaro(tag='canari', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

