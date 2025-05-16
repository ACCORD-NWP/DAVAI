# -*- coding: utf-8 -*-
"""
Physiography:
PGD + clim 923(N923=1)
on a range of LAM geometries
"""
import vortex
from vortex import toolbox
from vortex.layout.nodes import Driver, Family, LoopFamily

from .make_lam_domain import MakeLamDomain
from ..surfex.pgd import PGD
from .c923 import C923
from .finalize_pgd import FinalizePGD

def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
            Family(tag='arome', ticket=t, on_error='delayed_fail', nodes=[
                Family(tag='arome_physiography', ticket=t, nodes=[
                    LoopFamily(tag='lam_geometries', ticket=t,
                        loopconf='geometrys',
                        loopsuffix='-{0.tag}',
                        nodes=[
                        Family(tag='geo', ticket=t, on_error='delayed_fail', nodes=[
                            MakeLamDomain(tag='make_domain', ticket=t, **kw),
                            PGD(tag='pgd', ticket=t, **kw),
                            C923(tag='c923n1', ticket=t, **kw),
                            FinalizePGD(tag='finalize_pgd', ticket=t, **kw),
                            ], **kw),
                        ], **kw),
                    ], **kw),
                ], **kw),
            ], **kw),
        ],
    )

