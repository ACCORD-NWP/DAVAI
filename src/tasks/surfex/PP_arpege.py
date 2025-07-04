# -*- coding: utf-8 -*-
"""
PP_geo = PGD+Prep
"""
import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from tasks.surfex.pgd import PGD
from tasks.surfex.prep import Prep


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
            Family(tag='arpege', ticket=t, on_error='delayed_fail', nodes=[
                Family(tag='arpege_physiography', ticket=t, nodes=[
                    LoopFamily(tag='gauss_grids', ticket=t,
                        loopconf='geometrys',
                        loopsuffix='-{0.tag}',
                        nodes=[
                        Family(tag='PP', ticket=t, on_error='delayed_fail', nodes=[
                            PGD(tag='pgd', ticket=t, **kw),
                            Prep(tag='prep', ticket=t, **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

