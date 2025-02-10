# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodb import BatorODB
from .minims.AnalyseOOPS_LAM3D import AnalyseLAM3D


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar3h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='rundates', ticket=t,
                        loopconf='rundates',
                        loopsuffix='.{}',
                        nodes=[
                        Family('BA1', ticket=t, on_error='delayed_fail', nodes=[
                            BatorODB(tag='batodb', ticket=t, **kw),
                            AnalyseLAM3D(tag='AnalyseLAM3D', ticket=t, **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

