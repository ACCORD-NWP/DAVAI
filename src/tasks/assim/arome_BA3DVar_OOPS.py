# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .raw2odb.batodbNew import BatorODB
from .minims.OOPSAnalysis_LAM3DVar import OOPSAnalysisLAM3DVar as Analysis


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar3h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    LoopFamily(tag='rundates', ticket=t,
                        loopconf='rundates',
                        loopsuffix='.{}',
                        nodes=[
                            Family(tag='BA', ticket=t, on_error='delayed_fail', nodes=[
                                BatorODB(tag='batodb', ticket=t, **kw),
                                Analysis(tag='analysis', ticket=t, **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

