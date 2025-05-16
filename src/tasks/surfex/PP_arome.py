# -*- coding: utf-8 -*-
"""
PP = PGD+Prep
"""
import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from ..surfex.pgd import PGD
from ..surfex.prep import Prep

def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
            Family(tag='arome', ticket=t, on_error='delayed_fail', nodes=[
                Family(tag='arome_physiography', ticket=t, nodes=[
                    PGD(tag='pgd', ticket=t, **kw),
                    Prep(tag='prep', ticket=t, **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

