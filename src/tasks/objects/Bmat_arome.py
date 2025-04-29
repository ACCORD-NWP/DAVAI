# -*- coding: utf-8 -*-

import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .bmat.BuildEnsembleLAM import BuildEnsemble
from .bmat.EnVarAdjointLAM import EnVarAdjoint

def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='arome', ticket=t, nodes=[
            Family(tag='3dvar3h', ticket=t, nodes=[
                Family(tag='default_compilation_flavour', ticket=t, nodes=[
                    BuildEnsemble(tag='BuildEnsemble', ticket=t, **kw),
                    EnVarAdjoint(tag='EnVarAdjoint', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

