# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .model.ModelTLAD import TLAD as ModelTLAD

def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arpege', ticket=t, nodes=[
            Family(tag='4dvar6h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    ModelTLAD(tag='model_tlad', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

