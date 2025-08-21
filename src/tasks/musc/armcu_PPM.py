# -*- coding: utf-8 -*-

from vortex.layout.nodes import Family, Driver, LoopFamily

from .pgd import MUSC_PGD as PGD
from .prep import MUSCPrep as Prep
from .musc import MUSCForecast


def setup(t, **kw):
    return Driver(tag='drv', ticket=t, options=kw, nodes=[
        Family(tag='default_compilation_flavour', ticket=t, nodes=[
            Family(tag='case_armcu', ticket=t, nodes=[
                PGD(tag='pgd', ticket=t, **kw),
                Prep(tag='prep', ticket=t, **kw),
                ], **kw),
            ], **kw),
        LoopFamily(tag='gmkpack', ticket=t, loopconf='compilation_flavours', loopsuffix='.{}', nodes=[
            Family(tag='case_armcu', ticket=t, nodes=[
                # tag must start with model_*
                MUSCForecast(tag='arome_nominal', ticket=t, on_error='delayed_fail', **kw),
                MUSCForecast(tag='arpege_nominal', ticket=t, on_error='delayed_fail', **kw),
                ], **kw),
            ], **kw),
        ]
    )
