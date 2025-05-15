# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family

from .raw2odb.batodb import BatorODB
from .minims.OOPSAnalysis_4DVar import Analysis4dvar


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='4dvar6h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    BatorODB(tag='batodb', ticket=t, **kw),
                    Analysis4dvar(tag='analysis', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

